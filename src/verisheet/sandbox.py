"""Restricted execution boundary owned by Person 4.

The OS/container boundary is the security control. AST checks are defense-in-depth only and
must never be represented as sufficient isolation by themselves.
"""

from pathlib import Path


class RestrictedSandbox:
    """Execute generated analysis scripts in a non-privileged isolated process/container.

    Requirements: no network, no secrets, read-only workbook mount, writable temporary artifact
    mount, explicit import allowlist, CPU/memory/time caps, process cleanup and bounded stdout.
    """

    def __init__(self, timeout_seconds: int = 20, memory_mb: int = 1024):
        """Set resource limits and sandbox configuration; do not start with elevated privileges."""
        self.timeout_seconds = timeout_seconds
        self.memory_mb = memory_mb
        # ####CODE HERE
        raise NotImplementedError("Person 4: initialise sandbox backend")

    def validate_script_ast(self, script_text: str) -> None:
        """Perform defense-in-depth AST checks against forbidden imports/calls/reflection.

        Reject open(), subprocess, socket, shell execution, arbitrary imports, reflection and
        dynamic code execution unless a reviewed tool explicitly requires them. This is not
        a substitute for running inside an OS/container security boundary.
        """
        # ####CODE HERE
        raise NotImplementedError("Person 4: implement AST policy check")

    def run_script(self, script_path: str | Path, input_dir: str | Path, output_dir: str | Path) -> dict:
        """Run script in isolation and return exit code, bounded stdout/stderr and duration."""
        # ####CODE HERE
        raise NotImplementedError("Person 4: implement isolated process execution")
