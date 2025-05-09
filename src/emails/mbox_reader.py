from __future__ import annotations

import email
import itertools
from email.message import Message
from email.policy import default
from pathlib import Path
from typing import Generator


# https://stackoverflow.com/a/59682472/6890681
class MboxReader:
    def __init__(self, mbox_path: Path) -> None:
        self.handle = mbox_path.open("rb")
        assert self.handle.readline().startswith(b"From ")

    def __enter__(self) -> MboxReader:
        return self

    def __exit__(self, _exc_type, _exc_value, _exc_traceback) -> None:  # noqa: ANN001
        self.handle.close()

    def __iter__(self) -> Generator[tuple[Message, int]]:
        lines: list[bytes] = []
        for line in itertools.chain(iter(self.handle.readline, b""), (b"From ",)):
            if line.startswith(b"From "):
                message_bytes = b"".join(lines)
                message_size = len(message_bytes)
                message = email.message_from_bytes(message_bytes, policy=default)  # type: ignore[arg-type]
                yield message, message_size
                lines.clear()
            if line.startswith(b">") and line.lstrip(b">").startswith(b"From "):
                line = line[1:]
            lines.append(line)
