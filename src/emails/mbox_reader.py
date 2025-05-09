from __future__ import annotations

import email
from email.message import Message
from email.policy import default
from typing import Generator


# https://stackoverflow.com/a/59682472/6890681
class MboxReader:
    def __init__(self, mbox_path: str) -> None:
        self.handle = open(mbox_path, "rb")
        assert self.handle.readline().startswith(b"From ")

    def __enter__(self) -> MboxReader:
        return self

    def __exit__(self, _exc_type, _exc_value, _exc_traceback) -> None:  # noqa: ANN001
        self.handle.close()

    def __iter__(self) -> Generator[Message]:
        lines: list[bytes] = []
        while True:
            line = self.handle.readline()
            if line == b"" or line.startswith(b"From "):
                yield email.message_from_bytes(b"".join(lines), policy=default)  # type: ignore[arg-type]
                if line == b"":
                    break
                lines = []
                continue
            if line.startswith(b">") and line.lstrip(b">").startswith(b"From "):
                line = line[1:]
            lines.append(line)
