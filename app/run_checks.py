#!/usr/bin/env python
"""ローカル品質ゲート（単一タスクスクリプト）。

「テスト green ＋ 中核層カバレッジ下限（80%）」を機械的に強制する。
手動実行だけに頼らず、pre-commit / pre-push からも同じチェックを呼べるようにする。

使い方（app/ ディレクトリで）:
    uv run python run_checks.py
"""

from __future__ import annotations

import subprocess

#: 実行するチェック（コマンドと説明）。uv run 経由で解決する前提。
CHECKS: list[tuple[str, list[str]]] = [
    ("black --check", ["black", "--check", "."]),
    ("ruff", ["ruff", "check", "."]),
    (
        "pytest + coverage (core/io >= 80%)",
        [
            "pytest",
            "tests/",
            "--cov=screenshot_editor.core",
            "--cov=screenshot_editor.io",
            "--cov-report=term-missing",
            "--cov-fail-under=80",
        ],
    ),
]


def main() -> int:
    failures: list[str] = []
    for label, cmd in CHECKS:
        print(f"==> {label}: {' '.join(cmd)}")
        # cmd は本ファイル冒頭で定義した固定の静的コマンドのみ（外部入力なし）。
        result = subprocess.run(cmd, check=False)  # noqa: S603
        if result.returncode != 0:
            failures.append(label)
    if failures:
        print("\n失敗したチェック: " + ", ".join(failures))
        return 1
    print("\nすべてのチェックに合格しました。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
