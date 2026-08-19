import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class AgentInstructionTests(unittest.TestCase):
    def test_claude_imports_canonical_instructions(self):
        self.assertEqual(
            (PROJECT_ROOT / "CLAUDE.md").read_text(encoding="utf-8"),
            "@AGENTS.md\n",
        )

    def test_antigravity_imports_canonical_instructions(self):
        self.assertEqual(
            (PROJECT_ROOT / ".agents/rules/project.md").read_text(
                encoding="utf-8"
            ),
            "@../../AGENTS.md\n",
        )

    def test_copilot_instructions_match_canonical_instructions(self):
        self.assertEqual(
            (PROJECT_ROOT / ".github/copilot-instructions.md").read_text(
                encoding="utf-8"
            ),
            (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        )

    def test_sync_check_passes(self):
        result = subprocess.run(
            [
                sys.executable,
                str(PROJECT_ROOT / "scripts/sync_agent_instructions.py"),
                "--check",
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
