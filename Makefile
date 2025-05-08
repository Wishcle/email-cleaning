
.PHONY: all
all: sync

.PHONY: sync
sync:
	uv sync

.PHONY: test
test: lint check

.PHONY: lint
lint:
	uv run ruff check

.PHONY: fix
fix:
	uv run ruff check --fix

.PHONY: check
check:
	uv run mypy
