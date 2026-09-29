import unittest
from unittest.mock import patch

from scripts import build_catalog


class CatalogParsingTests(unittest.TestCase):
    def test_duplicate_group_assignments_are_rejected(self):
        groups = {
            "first": ["same-skill", "only-first"],
            "second": ["same-skill", "only-second"],
        }
        with patch.object(build_catalog, "GROUPS", groups):
            self.assertEqual(
                build_catalog.group_metadata_problems(),
                ["same-skill is assigned to multiple groups: first, second"],
            )

    def test_group_titles_must_match_group_keys(self):
        groups = {"first": ["one"], "second": ["two"]}
        titles = {"first": "First", "orphan": "Orphan"}
        with patch.multiple(build_catalog, GROUPS=groups, GROUP_TITLES=titles):
            self.assertEqual(
                build_catalog.group_metadata_problems(),
                [
                    "groups without titles: second",
                    "titles without groups: orphan",
                ],
            )


if __name__ == "__main__":
    unittest.main()
