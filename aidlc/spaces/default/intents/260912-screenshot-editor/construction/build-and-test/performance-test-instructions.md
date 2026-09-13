# Performance Test Instructions — screenshot-editor（mvp）

performance-requirements.md（PERF-1〜4）に対する検証方針。要件どおり、mvp・個人利用のため
**厳密なベンチマーク/SLA は Out of Scope**（「正式な性能試験は行わない」「体感的に実用的」を基準）。
ここでは設計アプローチの充足を確認する軽量な手順を定める。

## 検証方針

性能目標は「体感的に即時/実用的」であり、自動化された数値ベンチマークは設けない。
代わりに、応答性を担保する**設計アプローチが実装に反映されていること**を確認する。

| ID | 目標（目安） | 検証方法（mvp） |
|----|------|----------|
| PERF-1 | プレビュー反映 ≤300ms 目安 | 設計確認: プレビューは表示解像度に合わせた縮小版（最大 900px）に適用（`ui/main_window.py` の `_PREVIEW_MAX` と `_update_preview`）。原寸適用は保存時のみ。手動起動で体感確認（任意）。 |
| PERF-2 | 開く ≤1s 目安 | 設計確認: Pillow で開き縮小プレビューを 1 度生成。手動体感確認（任意）。 |
| PERF-3 | 保存 ≤1s 目安 | 設計確認: 原寸へ 1 パス適用し非破壊アトミック保存（`io/image_io.py`）。 |
| PERF-4 | バッチは枚数に比例・UI 非ブロック | 設計確認: バッチは QThread ワーカーで実行し進捗をシグナル通知（`ui/batch_dialog.py`）。UI スレッドをブロックしない。 |

## 手動体感確認（任意）

実機の Windows で GUI を起動し、一般的な PNG/JPEG（フルHD〜4K）で下記を体感確認する:

```
uv run python -m screenshot_editor
```

- スライダー操作でプレビューがほぼ即時に更新されるか（PERF-1）
- 画像を開く/保存が待たされないか（PERF-2/3）
- バッチ実行中に UI が固まらず進捗が出るか（PERF-4）

## Out of Scope

- 厳密なベンチマーク基準・SLA・負荷試験・回帰検出の自動化（mvp・個人利用のため）。
- 高解像度（4K 超）・大量枚数の最適化（主対象外。ただしクラッシュはしない = NFR1）。

## 所有ステージ / 検証の限界

Operation フェーズ（performance-validation 等）は本スコープではスキップされているため、
自動化された性能検証を所有する後続ステージは存在しない。PERF-1〜4 は要件どおり形式的な
自動計測の対象外であり、設計アプローチの静的確認と任意の手動体感確認で扱う。

## Sources

- performance-requirements.md（PERF-1〜4、Out of Scope）
- performance-design.md（縮小プレビュー・ワーカースレッド・1 パス保存）

## Assumptions & Open Questions

- 数値目標は目安。実測に基づく最適化はコード生成後に必要に応じて行う（要件どおり）。
