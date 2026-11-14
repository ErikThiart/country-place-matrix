"""Evidence matrix tests use retained real worldwide source inventories."""

import copy
import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("country_readiness", ROOT / "bin/build-country-readiness.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class CountryReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs, cls.hashes = builder.read_inputs()
        cls.rows = {row["selector"]: row for row in builder.build_rows(cls.inputs)}

    def test_full_inventory_retired_pseudo_exclusion_and_explicit_xk(self):
        self.assertEqual(257, len(self.rows))
        self.assertEqual(250, len({row["canonical"] for row in self.rows.values()}))
        self.assertEqual("exceptional", self.rows["XK"]["identity_status"])
        for excluded in ["AN", "CS", "SU", "YU", "XA", "XB", "001", "UK"]:
            self.assertNotIn(excluded, self.rows)
        self.assertEqual("GB", self.inputs["catalog"]["aliases"]["UK"]["country_code"])
        self.assertTrue(all(not row["public_activation_approved"] for row in self.rows.values()))

    def test_special_contexts_keep_distinct_country_address_phone_timezone_evidence(self):
        mappings = {"AC": "SH", "TA": "SH", "CP": "FR", "CQ": "GG", "DG": "IO", "EA": "ES", "IC": "ES"}
        for selector, canonical in mappings.items():
            with self.subTest(selector=selector):
                row = self.rows[selector]
                self.assertEqual(canonical, row["canonical"])
                self.assertEqual((0, 0), (row["zone_tab"], row["zone1970"]))
        self.assertEqual("dedicated", self.rows["AC"]["format"])
        self.assertEqual("AC", self.rows["AC"]["format_country"])
        self.assertEqual("247", self.rows["AC"]["calling_code"])
        self.assertEqual("290", self.rows["TA"]["calling_code"])
        for selector in ["CP", "CQ", "DG"]:
            self.assertEqual("reference_root_only", self.rows[selector]["membership"])
            self.assertTrue(self.rows[selector]["membership_gap"])
            self.assertIsNone(self.rows[selector]["calling_code"])
            self.assertEqual("parent", self.rows[selector]["format"])
        ea = self.rows["EA"]
        self.assertTrue(ea["requires_place_choice"])
        self.assertEqual([2519582, 6362988], ea["membership_roots"])
        self.assertEqual("administrative_roots", ea["membership"])
        self.assertIsNone(ea["phone_region"])

    def test_saudi_arabia_and_namibia_are_not_region_abbreviations_or_defaults(self):
        self.assertEqual(
            ("Saudi Arabia", "SA", "966"),
            (self.rows["SA"]["canonical_name"], self.rows["SA"]["canonical"], self.rows["SA"]["calling_code"]),
        )
        self.assertEqual(
            ("Namibia", "NA", "264"),
            (self.rows["NA"]["canonical_name"], self.rows["NA"]["canonical"], self.rows["NA"]["calling_code"]),
        )
        self.assertGreater(self.rows["SA"]["geo_localities"], 5000)
        self.assertGreater(self.rows["NA"]["geo_localities"], 2000)
        self.assertEqual(0, self.rows["NA"]["valid_source_examples"])
        self.assertEqual("pattern-ok", self.rows["NA"]["pattern"])

    def test_real_counts_reconcile_without_double_counting_parent_contexts(self):
        canonical_rows = [row for row in self.rows.values() if row["selector"] == row["canonical"]]
        geo = self.inputs["geonames"]
        self.assertEqual(geo["counts"]["A"], sum(row["geo_administrative"] for row in canonical_rows))
        self.assertEqual(geo["counts"]["P"], sum(row["geo_localities"] for row in canonical_rows))
        self.assertEqual(
            len(self.inputs["full_address"]["subdivisions"]), sum(row["postal_subdivisions"] for row in canonical_rows)
        )
        self.assertEqual(245, sum(row["phone_region"] is not None for row in self.rows.values()))
        self.assertEqual(46, sum(row["format"] == "generic" for row in self.rows.values()))
        self.assertEqual(206, sum(row["format"] == "dedicated" for row in self.rows.values()))
        self.assertEqual(5, sum(row["format"] == "parent" for row in self.rows.values()))

    def test_postal_patterns_conflicts_official_evidence_and_unknowns_stay_distinct(self):
        korea = self.rows["KR"]
        self.assertEqual(
            ("pattern-ok", 0, 2, 2),
            (korea["pattern"], korea["valid_source_examples"], korea["official_examples"], korea["source_conflicts"]),
        )
        somalia = self.rows["SO"]
        self.assertEqual(
            (0, 0, 2), (somalia["valid_source_examples"], somalia["official_examples"], somalia["source_conflicts"])
        )
        self.assertEqual("unknown", self.rows["CD"]["pattern"])
        self.assertTrue(self.rows["CD"]["optional_capture_overlay"])
        self.assertEqual("source-unused", self.rows["AE"]["pattern"])
        self.assertEqual("generic", self.rows["AQ"]["format"])
        self.assertEqual("unknown", self.rows["AQ"]["pattern"])
        self.assertEqual(12, sum(row["optional_capture_overlay"] for row in self.rows.values()))

    def test_mismatched_inventory_or_country_mapping_is_rejected(self):
        inputs = copy.deepcopy(self.inputs)
        inputs["geonames"]["selectors"]["EA"]["country_code"] = "ZA"
        with self.assertRaisesRegex(ValueError, "GeoNames canonical mismatch"):
            builder.build_rows(inputs)
        inputs = copy.deepcopy(self.inputs)
        del inputs["phone"]["selectors"]["AC"]
        with self.assertRaisesRegex(ValueError, "Selector source inventory mismatch"):
            builder.build_rows(inputs)
        inputs = copy.deepcopy(self.inputs)
        inputs["phone"]["selectors"]["CP"]["canonical_numbering_fallback_applied"] = True
        with self.assertRaisesRegex(ValueError, "Parent phone fallback"):
            builder.build_rows(inputs)

    def test_report_is_current_deterministic_and_all_relative_links_exist(self):
        report = builder.render(self.inputs, self.hashes)
        self.assertEqual(report, builder.render(self.inputs, self.hashes))
        self.assertEqual((ROOT / "docs/country-data-matrix.md").read_text(), report)
        self.assertEqual(
            257,
            sum(
                line.startswith("| ") and " / " in line and line.split(" / ")[0][2:] in self.rows
                for line in report.splitlines()
            ),
        )
        for link in re.findall(r"\]\(([^)]+)\)", report):
            if not link.startswith(("https:", "http:")):
                self.assertTrue((ROOT / "docs" / link).is_file(), link)
        for fingerprint in self.hashes.values():
            self.assertIn(fingerprint, report)
        self.assertEqual("a&#124;b c", builder.cell("a|b\nc"))


if __name__ == "__main__":
    unittest.main()
