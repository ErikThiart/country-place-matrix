"""Pinned real postal references: preserve scope, exceptions and source ambiguity."""

import copy
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("country_addresses", ROOT / "bin/build-country-addresses.py")
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class CountryAddressReferenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "resources/data/country-addresses.v1.json").read_text())
        cls.catalog = json.loads((ROOT / "resources/data/country-catalog.v1.json").read_text())
        cls.manifest = json.loads((BUILDER.SOURCES / "manifest.v1.json").read_text())

    def test_sources_and_distributable_outputs_have_verified_hashes_and_licenses(self):
        sources = {source["key"]: source for source in self.data["sources"]}
        self.assertEqual("v2.3.2", sources["commerceguys_addressing"]["release"])
        self.assertEqual("MIT", sources["commerceguys_addressing"]["license"])
        self.assertEqual(BUILDER.COMMIT, sources["commerceguys_addressing"]["revision"])
        for item in self.data["sources"] + self.manifest["outputs"] + self.manifest["licenses"]:
            with self.subTest(file=item["file"]):
                self.assertEqual(
                    item["sha256"],
                    hashlib.sha256((ROOT / item["file"]).read_bytes()).hexdigest(),
                )
        self.assertIn(
            "Permission is hereby granted",
            (BUILDER.SOURCES / "commerceguys-LICENSE").read_text(),
        )
        self.assertIn(
            "Apache License",
            (BUILDER.SOURCES / "google-libaddressinput-LICENSE").read_text(),
        )

    def test_complete_identity_inventory_does_not_guess_retired_or_test_countries(self):
        self.assertEqual(set(self.catalog["countries"]), set(self.data["countries"]))
        self.assertEqual(set(self.catalog["selectors"]), set(self.data["selectors"]))
        self.assertEqual(250, len(self.data["countries"]))
        self.assertEqual(257, len(self.data["selectors"]))
        for selector, item in self.data["selectors"].items():
            self.assertEqual(
                self.catalog["selectors"][selector]["country_code"],
                item["country_code"],
            )
            self.assertFalse(item["public_activation_approved"])
            self.assertTrue(item["reference_only"])
        for code in ["AN", "CS", "XA", "XB", "UK", "BU"]:
            self.assertNotIn(code, self.data["selectors"])
        self.assertEqual("Saudi Arabia", self.catalog["countries"]["SA"]["name"])
        self.assertEqual("Namibia", self.catalog["countries"]["NA"]["name"])

    def test_dedicated_parent_and_generic_are_distinct_not_worldwide_acceptance(self):
        coverage = self.data["coverage"]
        self.assertEqual(206, coverage["upstream_dedicated_formats"])
        self.assertEqual(204, coverage["canonical_dedicated_formats"])
        self.assertEqual(46, len(coverage["generic_selectors"]))
        self.assertFalse(coverage["national_or_provider_acceptance_claimed"])
        for code in coverage["generic_selectors"]:
            item = self.data["selectors"][code]
            self.assertEqual("generic", item["format_status"])
            self.assertEqual("unknown", item["postal_code_status"])
            self.assertIsNone(item["postal_code_pattern"])
        for code, parent in {
            "CP": "FR",
            "CQ": "GG",
            "DG": "IO",
            "EA": "ES",
            "IC": "ES",
        }.items():
            item = self.data["selectors"][code]
            self.assertEqual("parent", item["format_status"])
            self.assertEqual(parent, item["format_country_code"])
            self.assertTrue(item["parent_format_requires_territory_review"])
            self.assertEqual(
                item["postal_code_pattern"],
                item["address_reference"]["postal_code_pattern"],
            )

    def test_islands_preserve_actual_own_postcodes_instead_of_canonical_parent(self):
        for code, postcode in {"AC": "ASCN 1ZZ", "TA": "TDCU 1ZZ"}.items():
            item = self.data["selectors"][code]
            self.assertEqual("SH", item["country_code"])
            self.assertEqual(code, item["format_country_code"])
            self.assertEqual("dedicated", item["format_status"])
            result = BUILDER.php(
                BUILDER.PHP_PATTERNS,
                {
                    code: {
                        "pattern": item["postal_code_pattern"],
                        "examples": [postcode],
                    }
                },
            )
            self.assertTrue(result[code]["examples"][postcode])
            self.assertNotEqual(
                self.data["countries"]["SH"]["postal_code_pattern"],
                item["postal_code_pattern"],
            )

    def test_every_available_postal_pattern_compiles_with_actual_application_engine(
        self,
    ):
        checks = BUILDER.php(
            BUILDER.PHP_PATTERNS,
            {
                code: {
                    "pattern": item["postal_code_pattern"],
                    "examples": item["postal_code_examples"],
                }
                for code, item in self.data["selectors"].items()
            },
        )
        self.assertEqual(168, self.data["coverage"]["countries_with_source_examples"])
        self.assertEqual(166, self.data["coverage"]["countries_with_validated_source_examples"])
        for code, item in self.data["selectors"].items():
            with self.subTest(country=code):
                result = checks[code]
                self.assertIsNot(result["pattern_compiles"], False)
                self.assertEqual(
                    item["postal_code_examples_valid"],
                    [value for value, valid in result["examples"].items() if valid is True],
                )
                self.assertEqual(
                    item["source_example_conflicts"],
                    [value for value, valid in result["examples"].items() if valid is False],
                )

    def test_source_errors_are_retained_but_never_promoted_as_valid_examples(self):
        self.assertEqual(
            {"BY", "EC", "EE", "GB", "KR", "PE", "SO"},
            set(self.data["coverage"]["source_example_conflicts"]),
        )
        self.assertIn("RH6 OHP", self.data["countries"]["GB"]["source_example_conflicts"])
        self.assertEqual([], self.data["countries"]["KR"]["postal_code_examples_valid"])
        for item in self.data["countries"].values():
            self.assertTrue(set(item["source_example_conflicts"]).isdisjoint(item["postal_code_examples_valid"]))
            self.assertTrue(set(item["source_example_conflicts"]).issubset(item["postal_code_examples"]))

    def test_official_example_overlay_has_dated_attribution_and_does_not_rewrite_raw_sources(
        self,
    ):
        evidence = json.loads(BUILDER.checked(BUILDER.SOURCES / "postal-evidence.v1.json", BUILDER.POSTAL_EVIDENCE_SHA))
        self.assertEqual(
            ["BY", "EC", "EE", "GB", "KR", "PE"],
            self.data["coverage"]["countries_with_official_examples"],
        )
        self.assertEqual(
            ["06043", "30114"],
            [entry["value"] for entry in self.data["countries"]["KR"]["official_postal_code_examples"]],
        )
        self.assertIn("10621", self.data["countries"]["EE"]["postal_code_examples_display"])
        self.assertIn("220050", self.data["countries"]["BY"]["postal_code_examples_display"])
        self.assertEqual([], self.data["countries"]["KR"]["postal_code_examples_valid"])
        self.assertEqual(["110-110", "699-800"], self.data["countries"]["KR"]["postal_code_examples"])
        for source in evidence["sources"].values():
            self.assertTrue(source["url"].startswith("https://"))
            self.assertEqual("2026-10-27", source["retrieved_at"])
            self.assertEqual(64, len(source["source_body_sha256"]))
            self.assertEqual(
                hashlib.sha256(source["minimal_factual_excerpt"].encode()).hexdigest(),
                source["excerpt_sha256"],
            )
            self.assertFalse(source["current_national_acceptance_established"])
        for item in self.data["countries"].values():
            self.assertTrue(set(item["source_example_conflicts"]).isdisjoint(item["postal_code_examples_display"]))
            self.assertTrue(set(item["postal_code_examples_valid"]).issubset(item["postal_code_examples_display"]))
            for example in item["official_postal_code_examples"]:
                self.assertEqual("official_postal_reference_examples", example["source_key"])
                self.assertIn(example["evidence_key"], evidence["sources"])
                self.assertIn(example["value"], item["postal_code_examples_display"])

    def test_historical_somalia_spacing_conflict_is_not_claimed_as_current_hint(self):
        item = self.data["countries"]["SO"]
        self.assertEqual([], item["postal_code_examples_display"])
        self.assertEqual([], item["official_postal_code_examples"])
        evidence = json.loads((BUILDER.SOURCES / "postal-evidence.v1.json").read_text())
        self.assertEqual("2004-09", evidence["sources"]["SO"]["source_document_date"])
        self.assertEqual(["JH  09010"], evidence["countries"]["SO"]["unresolved_pattern_examples"])
        checks = BUILDER.php(
            BUILDER.PHP_PATTERNS,
            {
                "SO": {
                    "pattern": item["postal_code_pattern"],
                    "examples": ["JH 09010", "JH  09010"],
                }
            },
        )
        self.assertEqual({"JH 09010": True, "JH  09010": False}, checks["SO"]["examples"])
        self.assertFalse(item["public_activation_approved"])

    def test_official_example_addition_rejects_missing_provenance_and_pattern_conflicts(
        self,
    ):
        evidence = json.loads((BUILDER.SOURCES / "postal-evidence.v1.json").read_text())
        conflicting = copy.deepcopy(evidence)
        conflicting["countries"]["KR"]["examples"][0]["value"] = "110-110"
        with self.assertRaisesRegex(ValueError, "unchanged postal pattern"):
            BUILDER.add_official_examples(copy.deepcopy(self.data["selectors"]), conflicting)
        missing = copy.deepcopy(evidence)
        missing["countries"]["KR"]["examples"][0]["evidence_key"] = "unattributed"
        with self.assertRaisesRegex(ValueError, "provenance"):
            BUILDER.add_official_examples(copy.deepcopy(self.data["selectors"]), missing)

    def test_every_available_subdivision_pattern_compiles_without_becoming_a_country_rule(
        self,
    ):
        patterns = {
            row["source_id"]: {"pattern": row["postal_code_pattern"], "examples": []}
            for row in self.data["subdivisions"]
            if row["postal_code_pattern"]
        }
        self.assertEqual(36, len(patterns))
        checks = BUILDER.php(BUILDER.PHP_PATTERNS, patterns)
        for identity, result in checks.items():
            with self.subTest(postal_subdivision=identity):
                self.assertTrue(result["pattern_compiles"])

    def test_leading_zero_country_differences_and_unicode_are_not_silently_coerced(
        self,
    ):
        fixtures = {
            "US": {"02108": True, "SW1A 1AA": False, "02108x": False},
            "GB": {"SW1A 1AA": True, "02108": False, "RH6 OHP": False},
            "JP": {"100-0001": True, "1000001": True, "SW1A 1AA": False},
        }
        result = BUILDER.php(
            BUILDER.PHP_PATTERNS,
            {
                code: {
                    "pattern": self.data["countries"][code]["postal_code_pattern"],
                    "examples": list(examples),
                }
                for code, examples in fixtures.items()
            },
        )
        for code, expected in fixtures.items():
            self.assertEqual(expected, result[code]["examples"])
        japan = [row for row in self.data["subdivisions"] if row["source_path"] == ["JP", "01"]]
        self.assertEqual(1, len(japan))
        self.assertEqual("北海道", japan[0]["local_name"])
        self.assertEqual("01", japan[0]["code"])

    def test_postcode_absence_is_source_scoped_and_generic_is_unknown(self):
        for item in self.data["countries"].values():
            self.assertEqual("source_format_not_national_absence", item["postal_code_status_scope"])
            if item["postal_code_status"] == "not_used":
                self.assertTrue(item["source_has_explicit_format"])
                self.assertNotIn("postalCode", item["source_used_fields"])
            if item["postal_code_status"] == "pattern":
                self.assertTrue(item["postal_code_pattern"])
        self.assertEqual("not_used", self.data["countries"]["HK"]["postal_code_status"])
        self.assertEqual("unknown", self.data["countries"]["AQ"]["postal_code_status"])

    def test_twelve_reviewed_postcode_omissions_allow_capture_without_invented_rules(
        self,
    ):
        expected = {
            "CD",
            "DJ",
            "GH",
            "GY",
            "LC",
            "MS",
            "NU",
            "PS",
            "TL",
            "TT",
            "UG",
            "WS",
        }
        self.assertEqual(expected, set(self.data["coverage"]["postal_capture_overlays"]))
        for code in expected:
            item = self.data["countries"][code]
            with self.subTest(country=code):
                self.assertIn("postalCode", item["used_fields"])
                self.assertNotIn("postalCode", item["source_used_fields"])
                self.assertNotIn("postalCode", item["directory_required_fields"])
                self.assertIsNone(item["postal_code_pattern"])
                self.assertEqual("unknown", item["postal_code_status"])
                overlay = item["overlays"][0]
                self.assertFalse(overlay["strict_pattern_approved"])
                self.assertFalse(overlay["required"])
                self.assertFalse(overlay["format_order_approved"])
                self.assertTrue(overlay["source_url"].startswith("https://www.upu.int/"))

    def test_shipping_recipient_requirements_never_become_directory_requirements(self):
        for item in self.data["countries"].values():
            self.assertIn("givenName", item["source_shipping_required_fields"])
            self.assertTrue(BUILDER.PERSONAL_FIELDS.isdisjoint(item["directory_required_fields"]))
            self.assertEqual(item["required_fields"], item["source_shipping_required_fields"])

    def test_postal_hierarchies_have_stable_namespaced_ids_and_all_parents(self):
        rows = self.data["subdivisions"]
        self.assertEqual(12075, len(rows))
        self.assertEqual(63, len(self.data["coverage"]["subdivision_roots"]))
        paths = {tuple(row["source_path"]) for row in rows}
        self.assertEqual(len(rows), len(paths))
        self.assertEqual(len(rows), len({row["source_id"] for row in rows}))
        for row in rows:
            self.assertEqual("commerceguys_postal", row["source_namespace"])
            self.assertFalse(row["geographic_membership_approved"])
            self.assertEqual(row["country_code"], row["source_path"][0])
            if len(row["source_path"]) > 2:
                self.assertIn(tuple(row["source_path"][:-1]), paths)

    def test_overlapping_postal_codes_do_not_reassign_country_geography(self):
        rows = {tuple(row["source_path"]): row for row in self.data["subdivisions"]}
        self.assertEqual("Missouri", rows[("US", "MO")]["name"])
        self.assertFalse(rows[("US", "MO")]["routing_only"])
        self.assertFalse(rows[("US", "CA")]["routing_only"])
        for path in [
            ("US", "PR"),
            ("US", "AA"),
            ("CN", "MO"),
            ("CN", "HK"),
            ("CN", "TW"),
        ]:
            self.assertTrue(rows[path]["routing_only"])
            self.assertFalse(rows[path]["geographic_membership_approved"])

    def test_runtime_metadata_matches_full_bundle_and_has_verifiable_provenance(self):
        path = ROOT / "resources/data/country-address-metadata.v1.json"
        metadata = json.loads(path.read_text())
        self.assertNotIn("subdivisions", metadata)
        self.assertLess(path.stat().st_size, 2 * 1024 * 1024)
        for field in [
            "version",
            "sources",
            "countries",
            "selectors",
            "field_roles",
            "coverage",
        ]:
            self.assertEqual(self.data[field], metadata[field])
        self.assertEqual(
            hashlib.sha256((ROOT / metadata["full_bundle_file"]).read_bytes()).hexdigest(),
            metadata["full_bundle_sha256"],
        )

    def test_tampered_source_and_unsafe_archives_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "source"
            path.write_bytes(b"altered")
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                BUILDER.checked(path, BUILDER.ARCHIVE_SHA)
            for name, kind in [
                ("../escape", tarfile.REGTYPE),
                ("addressing-" + BUILDER.COMMIT + "/link", tarfile.SYMTYPE),
            ]:
                archive = Path(temp) / "bad.tar.gz"
                with tarfile.open(archive, "w:gz") as stream:
                    entry = tarfile.TarInfo(name)
                    entry.type = kind
                    entry.linkname = "/etc/passwd"
                    stream.addfile(entry, io.BytesIO(b""))
                with self.assertRaisesRegex(ValueError, "Unsafe"):
                    BUILDER.extract(archive, Path(temp))

    def test_every_generated_artifact_rebuilds_offline_byte_for_byte(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "bin/build-country-addresses.py"), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
