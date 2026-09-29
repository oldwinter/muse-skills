import unittest
from unittest.mock import patch

from scripts import build_catalog


class CatalogParsingTests(unittest.TestCase):
    def test_include_in_prompt_requires_the_real_metadata_key(self):
        true_cases = (
            'metadata: { "includeInPrompt": true }',
            "metadata:" + chr(10) + "  includeInPrompt: true",
        )
        false_cases = (
            "# includeInPrompt: true",
            "notincludeInPrompt: true",
            'description: "includeInPrompt: true"',
            'metadata: { "includeInPrompt": false }',
        )
        for block in true_cases:
            with self.subTest(block=block):
                self.assertTrue(build_catalog.include_in_prompt(block))
        for block in false_cases:
            with self.subTest(block=block):
                self.assertFalse(build_catalog.include_in_prompt(block))

    def test_frontmatter_accepts_bom_and_cross_platform_line_endings(self):
        for separator in (chr(10), chr(13) + chr(10)):
            for bom in ("", chr(0xFEFF)):
                with self.subTest(separator=repr(separator), bom=bool(bom)):
                    text = bom + separator.join(
                        ["---", "name: demo", "description: Demo", "---", "# Body"]
                    )
                    parsed = build_catalog.parse_frontmatter(text)
                    self.assertEqual(parsed["name"], "demo")
                    self.assertEqual(parsed["description"], "Demo")
        self.assertEqual(
            build_catalog.parse_frontmatter("---" + chr(10) + "name: demo"),
            {},
        )

    def test_block_scalars_preserve_paragraph_breaks(self):
        folded = chr(10).join(
            ["description: >", "  First paragraph.", "", "  Second paragraph."]
        )
        multiple = chr(10).join(
            ["description: >", "  First paragraph.", "", "", "  Second paragraph."]
        )
        literal = chr(10).join(
            ["description: |", "  First paragraph.", "", "  Second paragraph."]
        )
        self.assertEqual(
            build_catalog.frontmatter_value(folded, "description"),
            "First paragraph." + chr(10) + "Second paragraph.",
        )
        self.assertEqual(
            build_catalog.frontmatter_value(multiple, "description"),
            "First paragraph." + chr(10) * 2 + "Second paragraph.",
        )
        self.assertEqual(
            build_catalog.frontmatter_value(literal, "description"),
            "First paragraph." + chr(10) * 2 + "Second paragraph.",
        )

    def test_availability_parser_stays_inside_entries_section(self):
        text = chr(10).join(
            [
                "version: 1",
                "before:",
                "  ignored_before:",
                "    status: disabled",
                "entries:",
                "  alpha:",
                "    status: available",
                "after:",
                "  ignored_after:",
                "    status: disabled",
            ]
        )
        self.assertEqual(
            build_catalog.parse_skills_yaml(text),
            {"alpha": {"status": "available"}},
        )

    def test_scope_parser_ignores_indented_comments_and_blank_lines(self):
        text = chr(10).join(
            [
                "",
                "  # indented comment words",
                "prod real-skill another-skill",
                "  ",
            ]
        )
        self.assertEqual(
            build_catalog.scope_names(text),
            {"real-skill", "another-skill"},
        )

    def test_duplicate_group_assignments_are_rejected(self):
        groups = {
            "first": ["same-skill", "only-first"],
            "second": ["same-skill", "only-second"],
        }
        titles = {"first": "First", "second": "Second"}
        with patch.multiple(build_catalog, GROUPS=groups, GROUP_TITLES=titles):
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
