import json
import tempfile
import unittest
from pathlib import Path

from scripts.reference_sync import (
    HttpResult,
    REQUIRED_REFERENCE_HEADINGS,
    ReferenceSyncError,
    apply_sync,
    finalize_reference,
    inspect_upstream,
    parse_llms_sources,
    verify_reference,
)


LLMS_URL = "https://docs.example.test/product/docs/llms.txt"
ONE_MD = "https://docs.example.test/product/docs/one.md"
TWO_MD = "https://docs.example.test/product/docs/two.md"
ONE_URL = "https://docs.example.test/product/docs/one"
TWO_URL = "https://docs.example.test/product/docs/two"


class FakeUpstream:
    def __init__(self, links, documents):
        self.links = list(links)
        self.documents = dict(documents)
        self.calls = []

    def __call__(self, url, headers, timeout):
        self.calls.append((url, dict(headers), timeout))
        if url == LLMS_URL:
            body = "\n".join(
                f"- [Page {index}]({link})"
                for index, link in enumerate(self.links, 1)
            ).encode("utf-8")
            return HttpResult(
                status=200,
                body=body,
                headers={"content-type": "text/plain; charset=utf-8"},
                final_url=LLMS_URL,
            )

        document = self.documents[url]
        etag = document["etag"]
        if headers.get("If-None-Match") == etag:
            return HttpResult(
                status=304,
                body=b"",
                headers={"etag": etag},
                final_url=url,
            )
        return HttpResult(
            status=200,
            body=document["body"],
            headers={
                "content-type": "text/markdown; charset=utf-8",
                "etag": etag,
            },
            final_url=url,
        )


def document(body, etag):
    return {"body": body, "etag": etag}


def reference_content():
    source_target = "../_source/docs-example-test/one.md"
    return f"""# Test reference

{REQUIRED_REFERENCE_HEADINGS[0]}

{REQUIRED_REFERENCE_HEADINGS[1]}

{REQUIRED_REFERENCE_HEADINGS[2]}

{REQUIRED_REFERENCE_HEADINGS[3]}

{REQUIRED_REFERENCE_HEADINGS[4]}

### 5.1 Test coverage

**Source:** [one.md]({source_target})

### Source Coverage

| Active exact source | Status | Compiled coverage or exclusion reason |
|---|---|---|
| [one.md]({source_target}) | Included | §5.1 Test coverage |

{REQUIRED_REFERENCE_HEADINGS[5]}
"""


class ReferenceSyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        self.manifest_path = self.project_root / "docs" / "reference-manifest.json"
        self.source_dir = self.project_root / "docs" / "_source"

    def tearDown(self):
        self.temporary_directory.cleanup()

    def sync(self, upstream):
        manifest, report, downloads = inspect_upstream(
            llms_url=LLMS_URL,
            manifest_path=self.manifest_path,
            source_dir=self.source_dir,
            project_root=self.project_root,
            opener=upstream,
        )
        apply_sync(manifest, self.manifest_path, downloads)
        return manifest, report, downloads

    def test_parse_llms_sources_keeps_unique_same_site_markdown_links(self):
        content = """
- [One](https://docs.example.test/product/docs/one.md)
- [Duplicate](https://docs.example.test/product/docs/one.md#section)
- [Relative](two.md)
- [External](https://other.example.test/product/docs/three.md)
- [Not Markdown](https://docs.example.test/product/docs/llms.txt)
"""

        self.assertEqual(
            parse_llms_sources(content, LLMS_URL),
            [(ONE_URL, ONE_MD), (TWO_URL, TWO_MD)],
        )

    def test_sync_stores_exact_markdown_and_a_noop_sync_changes_nothing(self):
        upstream = FakeUpstream(
            [ONE_MD, TWO_MD],
            {
                ONE_MD: document(b"# One\n\nExact source.\n", '"one-v1"'),
                TWO_MD: document(b"# Two\r\n\r\nExact bytes.\r\n", '"two-v1"'),
            },
        )

        manifest, report, downloads = self.sync(upstream)

        self.assertEqual(report.added, [ONE_URL, TWO_URL])
        self.assertEqual(len(downloads), 2)
        one_path = self.project_root / manifest["sources"][ONE_URL]["filepath"]
        two_path = self.project_root / manifest["sources"][TWO_URL]["filepath"]
        self.assertEqual(one_path.read_bytes(), b"# One\n\nExact source.\n")
        self.assertEqual(two_path.read_bytes(), b"# Two\r\n\r\nExact bytes.\r\n")
        manifest_bytes = self.manifest_path.read_bytes()

        proposed, second_report, second_downloads = inspect_upstream(
            llms_url=LLMS_URL,
            manifest_path=self.manifest_path,
            source_dir=self.source_dir,
            project_root=self.project_root,
            opener=upstream,
        )
        apply_sync(proposed, self.manifest_path, second_downloads)

        self.assertFalse(second_report.has_changes)
        self.assertEqual(second_report.unchanged, [ONE_URL, TWO_URL])
        self.assertEqual(second_downloads, {})
        self.assertEqual(self.manifest_path.read_bytes(), manifest_bytes)

    def test_changed_removed_and_reactivated_sources_are_reported_safely(self):
        upstream = FakeUpstream(
            [ONE_MD, TWO_MD],
            {
                ONE_MD: document(b"# One v1\n", '"one-v1"'),
                TWO_MD: document(b"# Two v1\n", '"two-v1"'),
            },
        )
        manifest, _, _ = self.sync(upstream)
        two_path = self.project_root / manifest["sources"][TWO_URL]["filepath"]

        upstream.links = [ONE_MD]
        upstream.documents[ONE_MD] = document(b"# One v2\n", '"one-v2"')
        manifest, report, _ = self.sync(upstream)

        self.assertEqual(report.changed, [ONE_URL])
        self.assertEqual(report.removed, [TWO_URL])
        self.assertFalse(manifest["sources"][TWO_URL]["active"])
        self.assertEqual(two_path.read_bytes(), b"# Two v1\n")

        upstream.links = [ONE_MD, TWO_MD]
        manifest, report, downloads = self.sync(upstream)

        self.assertEqual(report.reactivated, [TWO_URL])
        self.assertTrue(manifest["sources"][TWO_URL]["active"])
        self.assertNotIn(two_path, downloads)

    def test_sync_repairs_a_tampered_local_snapshot(self):
        upstream = FakeUpstream(
            [ONE_MD],
            {ONE_MD: document(b"# One\n", '"one-v1"')},
        )
        manifest, _, _ = self.sync(upstream)
        one_path = self.project_root / manifest["sources"][ONE_URL]["filepath"]
        one_path.write_bytes(b"tampered\n")

        _, report, downloads = self.sync(upstream)

        self.assertEqual(report.repaired, [ONE_URL])
        self.assertIn(one_path.resolve(), downloads)
        self.assertEqual(one_path.read_bytes(), b"# One\n")

    def test_finalize_is_compiler_agnostic_and_detects_stale_output(self):
        upstream = FakeUpstream(
            [ONE_MD],
            {ONE_MD: document(b"# One\n", '"one-v1"')},
        )
        self.sync(upstream)
        reference_path = self.project_root / "docs" / "_compiled" / "reference.md"
        contract_path = self.project_root / "REFERENCE_COMPILATION.md"
        metadata_path = self.project_root / "docs" / "_compiled" / "reference.meta.json"
        reference_path.parent.mkdir(parents=True)
        reference_path.write_text(reference_content(), encoding="utf-8")
        contract_path.write_text("Publish only grounded facts.\n", encoding="utf-8")

        metadata = finalize_reference(
            manifest_path=self.manifest_path,
            reference_path=reference_path,
            contract_path=contract_path,
            metadata_path=metadata_path,
            project_root=self.project_root,
        )

        self.assertEqual(metadata["source_count"], 1)
        self.assertEqual(
            metadata["publication_contract"],
            "REFERENCE_COMPILATION.md",
        )
        self.assertNotIn("compilation_prompt", metadata)
        self.assertEqual(
            verify_reference(
                manifest_path=self.manifest_path,
                reference_path=reference_path,
                contract_path=contract_path,
                metadata_path=metadata_path,
                project_root=self.project_root,
            ),
            [],
        )

        reference_path.write_text(reference_content() + "\nChanged.\n", encoding="utf-8")
        errors = verify_reference(
            manifest_path=self.manifest_path,
            reference_path=reference_path,
            contract_path=contract_path,
            metadata_path=metadata_path,
            project_root=self.project_root,
        )

        self.assertIn("Compiled reference changed after it was finalized", errors)

    def test_finalize_rejects_incomplete_source_coverage(self):
        upstream = FakeUpstream(
            [ONE_MD],
            {ONE_MD: document(b"# One\n", '"one-v1"')},
        )
        self.sync(upstream)
        reference_path = self.project_root / "docs" / "_compiled" / "reference.md"
        contract_path = self.project_root / "REFERENCE_COMPILATION.md"
        metadata_path = self.project_root / "docs" / "_compiled" / "reference.meta.json"
        reference_path.parent.mkdir(parents=True)
        incomplete = reference_content().replace(
            "| [one.md](../_source/docs-example-test/one.md) | Included | §5.1 Test coverage |\n",
            "",
        )
        reference_path.write_text(incomplete, encoding="utf-8")
        contract_path.write_text("Publish only grounded facts.\n", encoding="utf-8")

        with self.assertRaisesRegex(
            ReferenceSyncError,
            "Active source is missing from Source Coverage",
        ):
            finalize_reference(
                manifest_path=self.manifest_path,
                reference_path=reference_path,
                contract_path=contract_path,
                metadata_path=metadata_path,
                project_root=self.project_root,
            )

    def test_manifest_is_deterministic_json(self):
        upstream = FakeUpstream(
            [ONE_MD],
            {ONE_MD: document(b"# One\n", '"one-v1"')},
        )
        self.sync(upstream)

        parsed = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(parsed["schema_version"], 1)
        self.assertNotIn("last_fetched", self.manifest_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
