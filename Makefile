
.PHONY: all
all: sync

.PHONY: sync
sync:
	uv sync

.PHONY: check
check:
	uv run ruff check

.PHONY: fix
fix:
	uv run ruff check --fix
