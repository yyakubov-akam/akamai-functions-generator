import unittest

from scripts.check_public_boundary import find_private_paths, tracked_paths


class PublicBoundaryTests(unittest.TestCase):
    def test_finds_local_workflow_and_generated_function_paths(self):
        self.assertEqual(
            find_private_paths(
                [
                    "README.md",
                    "ingest_v2.py",
                    "docs/techdocs-akamai-com/faq.md",
                    "docs/_working/functions-reference-pass-1.md",
                    "functions/example/src/index.js",
                    "scripts/reference_sync.py",
                    "CODEGEN_REFERENCE_PROMPT.md",
                    "REPOSITORY_WORKFLOWS.md",
                ]
            ),
            [
                "CODEGEN_REFERENCE_PROMPT.md",
                "REPOSITORY_WORKFLOWS.md",
                "docs/_working/functions-reference-pass-1.md",
                "docs/techdocs-akamai-com/faq.md",
                "functions/example/src/index.js",
                "ingest_v2.py",
            ],
        )

    def test_similar_public_paths_are_allowed(self):
        self.assertEqual(
            find_private_paths(
                [
                    "docs/_source/techdocs-akamai-com/faq.md",
                    "scripts/reference_sync.py",
                    "tests/test_reference_sync.py",
                ]
            ),
            [],
        )

    def test_current_repository_respects_public_boundary(self):
        self.assertEqual(find_private_paths(tracked_paths()), [])


if __name__ == "__main__":
    unittest.main()
