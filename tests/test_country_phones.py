"""Real-source numbering metadata contracts; these never call a phone/provider."""

import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("country_phones", ROOT / "bin/build-country-phones.py")
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class CountryPhoneReferenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "resources/data/country-phone-reference.v1.json").read_text())
        cls.catalog = json.loads((ROOT / "resources/data/country-catalog.v1.json").read_text())
        cls.metadata, cls.manifest = BUILDER.verified_sources(ROOT / "resources/data/phone-metadata")

    def test_snapshot_is_pinned_official_and_licensed(self):
        self.assertEqual("Apache-2.0", self.manifest["license"])
        self.assertEqual("v9.0.42", self.manifest["release"])
        self.assertEqual("8d8d75272c351b60b87163db5328e439c53a6b56", self.manifest["commit"])
        self.assertEqual(
            "b6491939ddaeb9d585a34fe0f0ebd096e83c5ac9a1c5d6dddf38ba4b162b28ca",
            hashlib.sha256(self.metadata).hexdigest(),
        )
        for source in self.manifest["files"]:
            self.assertIn(
                "raw.githubusercontent.com/google/libphonenumber/" + self.manifest["commit"] + "/", source["url"]
            )
        self.assertIn("Apache License", (ROOT / "resources/data/phone-metadata/LICENSE").read_text())

    def test_every_selector_is_present_but_unknown_is_not_a_guessed_country_prefix(self):
        self.assertEqual(set(self.catalog["selectors"]), set(self.data["selectors"]))
        self.assertEqual(257, len(self.data["selectors"]))
        direct, unknown = 0, []
        for selector, reference in self.data["selectors"].items():
            with self.subTest(selector=selector):
                self.assertEqual(
                    self.catalog["selectors"][selector]["country_code"], reference["canonical_country_code"]
                )
                self.assertFalse(reference["canonical_numbering_fallback_applied"])
                if reference["status"] == "direct_upstream_region":
                    direct += 1
                    self.assertEqual(selector, reference["metadata_region"])
                    self.assertEqual(
                        self.data["regions"][selector]["country_calling_code"], reference["country_calling_code"]
                    )
                else:
                    unknown.append(selector)
                    self.assertEqual("no_direct_region_metadata", reference["status"])
                    self.assertIsNone(reference["metadata_region"])
                    self.assertIsNone(reference["country_calling_code"])
        self.assertEqual(245, direct)
        self.assertEqual(["AQ", "BV", "CP", "CQ", "DG", "EA", "GS", "HM", "IC", "PN", "TF", "UM"], unknown)
        self.assertEqual(unknown, self.data["coverage"]["selectors_without_direct_metadata"])

    def test_exceptional_and_island_regions_use_actual_upstream_records(self):
        for region, calling_code in {"AC": "247", "TA": "290", "SH": "290", "XK": "383", "AX": "358"}.items():
            with self.subTest(region=region):
                self.assertEqual(calling_code, self.data["regions"][region]["country_calling_code"])
                self.assertEqual("direct_upstream_region", self.data["selectors"][region]["status"])
        self.assertEqual("SH", self.data["selectors"]["AC"]["canonical_country_code"])
        self.assertEqual("XK", self.data["selectors"]["XK"]["canonical_country_code"])
        self.assertNotIn("iso_alpha3", self.data["regions"]["XK"])
        self.assertNotIn("iso_numeric", self.data["regions"]["XK"])
        for selector, related in {"CQ": "GG", "EA": "ES", "IC": "ES", "CP": "FR", "DG": "IO"}.items():
            self.assertEqual(related, self.data["selectors"][selector]["canonical_region_reference"])
            self.assertIsNone(self.data["selectors"][selector]["country_calling_code"])

    def test_shared_codes_preserve_regions_and_do_not_identify_business_location(self):
        groups = self.data["calling_code_groups"]
        self.assertEqual("US", groups["1"]["main_region"])
        self.assertGreater(len(groups["1"]["regions"]), 20)
        self.assertEqual(["GB", "GG", "IM", "JE"], groups["44"]["regions"])
        self.assertEqual(["SH", "TA"], groups["290"]["regions"])
        for code, group in groups.items():
            self.assertIn(group["main_region"], group["regions"])
            self.assertEqual(len(group["regions"]), len(set(group["regions"])))
            for region in group["regions"]:
                self.assertEqual(code, self.data["regions"][region]["country_calling_code"])
        self.assertTrue(
            self.data["usage"]["business_contacts_may_have_a_different_numbering_region_from_their_address"]
        )

    def test_non_geographic_services_are_separate_from_listing_countries(self):
        self.assertEqual(
            ["800", "808", "870", "878", "881", "882", "883", "888", "979"],
            list(self.data["non_geographic_calling_codes"]),
        )
        self.assertNotIn("001", self.data["selectors"])
        self.assertNotIn("001", self.data["regions"])
        self.assertTrue(set(self.data["non_geographic_calling_codes"]).isdisjoint(self.data["calling_code_groups"]))
        for code, plan in self.data["non_geographic_calling_codes"].items():
            self.assertEqual("001", plan["region_code"])
            self.assertEqual(code, plan["country_calling_code"])

    def test_every_upstream_example_matches_its_plan_and_possible_length(self):
        examples = 0
        plans = list(self.data["regions"].values()) + list(self.data["non_geographic_calling_codes"].values())
        for plan in plans:
            for kind, descriptor in plan["number_types"].items():
                example = descriptor["example_national_number"]
                if example is None:
                    continue
                examples += 1
                with self.subTest(region=plan["region_code"], calling_code=plan["country_calling_code"], kind=kind):
                    self.assertIsInstance(example, str)
                    self.assertRegex(example, r"^[0-9]+$")
                    self.assertIsNotNone(re.fullmatch(plan["general_national_number_pattern"], example))
                    self.assertIsNotNone(
                        re.fullmatch(
                            descriptor["national_number_pattern"] or plan["general_national_number_pattern"], example
                        )
                    )
                    if descriptor["possible_national_lengths"]:
                        self.assertIn(len(example), descriptor["possible_national_lengths"])
        self.assertGreater(examples, 1000)

    def test_national_leading_zero_is_not_lost_to_integer_conversion_or_prefix_stripping(self):
        italy = self.data["regions"]["IT"]
        self.assertEqual("0212345678", italy["number_types"]["fixedLine"]["example_national_number"])
        self.assertIsNone(italy["national_prefix"])
        self.assertEqual("39", italy["country_calling_code"])
        self.assertIn("$1", self.data["regions"]["GG"]["national_prefix_transform_rule"])

    def test_retired_aliases_do_not_silently_become_current_plans(self):
        for code in ["AN", "CS", "BU", "UK", "SU", "YU"]:
            self.assertNotIn(code, self.data["regions"])
            self.assertNotIn(code, self.data["selectors"])
        self.assertEqual("choose", self.data["aliases"]["AN"]["action"])
        self.assertEqual(["CW", "SX", "BQ"], self.data["aliases"]["AN"]["replacement_selectors"])
        self.assertIsNone(self.data["aliases"]["CS"]["canonical_country_code"])
        self.assertEqual("normalise", self.data["aliases"]["UK"]["action"])
        self.assertEqual("GB", self.data["aliases"]["UK"]["canonical_country_code"])

    def test_builder_is_reproducible_from_offline_snapshot(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "phones.json"
            process = subprocess.run(
                [sys.executable, str(ROOT / "bin/build-country-phones.py"), "--output", str(output)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(
                (ROOT / "resources/data/country-phone-reference.v1.json").read_bytes(), output.read_bytes()
            )
            self.assertEqual(245, json.loads(process.stdout)["geographic_regions"])

    def test_corrupt_or_unlicensed_snapshot_cannot_be_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            location = Path(temp)
            manifest = copy.deepcopy(self.manifest)
            for entry in manifest["files"]:
                (location / entry["path"]).write_bytes(
                    (ROOT / "resources/data/phone-metadata" / entry["path"]).read_bytes()
                )
            (location / "manifest.json").write_text(json.dumps(manifest))
            (location / "PhoneNumberMetadata.xml").write_bytes(self.metadata + b"\n")
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                BUILDER.verified_sources(location)
        wrong_license = {**self.manifest, "license": "unknown"}
        with self.assertRaisesRegex(ValueError, "license"):
            BUILDER.build(self.metadata, self.catalog, wrong_license, "a" * 64)

    def test_duplicate_source_region_and_unknown_length_grammar_fail_closed(self):
        import xml.etree.ElementTree as ET

        xml = ET.fromstring(self.metadata)
        territory = xml.find("territories")
        territory.append(copy.deepcopy(territory[0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            BUILDER.build(ET.tostring(xml), self.catalog, self.manifest, "a" * 64)
        for invalid in ["[9-6]", "[1-99999]", "0", "-1", "8;9", ""]:
            with self.subTest(value=invalid), self.assertRaises(ValueError):
                BUILDER.lengths(invalid)
        self.assertEqual([4, 5, 6, 9], BUILDER.lengths("[4-6],9"))

    def test_source_manifest_cannot_omit_hash_validation_or_redirect_to_another_file(self):
        with tempfile.TemporaryDirectory() as temp:
            location = Path(temp)
            for entry in self.manifest["files"]:
                (location / entry["path"]).write_bytes(
                    (ROOT / "resources/data/phone-metadata" / entry["path"]).read_bytes()
                )
            mutations = [
                {"files": []},
                {"files": [self.manifest["files"][0]] * 2},
                {"commit": "master"},
                {"license": "unknown"},
                {
                    "files": [
                        {**self.manifest["files"][0], "url": "https://example.test/metadata"},
                        self.manifest["files"][1],
                    ]
                },
                {"files": [{**self.manifest["files"][0], "path": "../outside.xml"}, self.manifest["files"][1]]},
            ]
            for mutation in mutations:
                with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                    (location / "manifest.json").write_text(json.dumps({**self.manifest, **mutation}))
                    BUILDER.verified_sources(location)

    def test_snapshot_symlink_is_not_followed_or_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            location = Path(temp)
            outside = location / "unrelated.xml"
            outside.write_bytes(self.metadata)
            (location / "PhoneNumberMetadata.xml").symlink_to(outside)
            (location / "LICENSE").write_bytes((ROOT / "resources/data/phone-metadata/LICENSE").read_bytes())
            (location / "manifest.json").write_text(json.dumps(self.manifest))
            with self.assertRaisesRegex(ValueError, "real direct"):
                BUILDER.verified_sources(location)
            self.assertEqual(self.metadata, outside.read_bytes())

    def test_selector_mapping_requires_a_known_canonical_country(self):
        catalog = copy.deepcopy(self.catalog)
        catalog["selectors"]["CQ"]["country_code"] = "ZZ"
        with self.assertRaisesRegex(ValueError, "unknown canonical"):
            BUILDER.build(self.metadata, catalog, self.manifest, "a" * 64)


if __name__ == "__main__":
    unittest.main()
