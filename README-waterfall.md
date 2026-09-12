# AI-DLC 使い方ガイド — ウォーターフォール編

> **対象読者**: AI-DLC を初めて使う方。要件定義から設計・実装・運用まで、  
> 順番に進めていくウォーターフォール型の開発に適した使い方をまとめています。

---

## AI-DLC とは

AI-DLC (AI-Driven Development Life Cycle) は、AI コーディングアシスタントを  
**構造化された開発ワークフロー**に変えるフレームワークです。

- アイデア出しから設計・実装・テスト・運用まで、決まった順番で進みます
- 各フェーズの終わりに **承認ゲート** があり、あなたが「次へ進む」と承認するまで先に進みません
- 何を決定したか、なぜそうしたかが自動的に記録されます

---

## ウォーターフォールに向いているスコープ

| スコープ名 | 特徴 | 向いているケース |
|---|---|---|
| `enterprise` | 全33ステージ実行・厳格な変更管理・完全な監査証跡 | 規制・コンプライアンスが必要な大規模開発 |
| `classic` | アイデア出しフェーズをスキップして設計から開始 | 要件が固まっている中規模プロジェクト |

ウォーターフォールでは **要件 → 設計 → 実装 → テスト → 運用** の順番を守ることが重要なので、  
すべてのステージを実行する `enterprise` または `classic` が適しています。

---

## 5つのフェーズ

```
[初期化] → [アイデア出し] → [立ち上げ] → [構築] → [運用]
              (Ideation)    (Inception)  (Construction) (Operation)
```

| フェーズ | 主な作業 |
|---|---|
| **初期化** | プロジェクト記録の作成、ワークフロー開始 |
| **アイデア出し** | 市場調査、スコープ定義、チーム編成、要求の承認 |
| **立ち上げ** | 要件分析、ドメイン設計、契約設計、機能設計、NFR設計、デリバリー計画 |
| **構築** | コード生成、ビルド・テスト、CI/CDパイプライン |
| **運用** | デプロイ、監視設定、インシデント対応、フィードバック最適化 |

---

## 始め方（ステップバイステップ）

### ステップ 1: Kiro IDE を開く

このプロジェクトフォルダを Kiro IDE で開きます。  
AI-DLC は自動的に有効になっています（設定済み）。

### ステップ 2: モデルを確認する

Kiro IDE のチャットモデルを **Claude Opus 4.8** に設定します。  
AI-DLC は高度な推論モデルで最もよく動作します。

### ステップ 3: セットアップを確認する

チャットに以下のコマンドを入力して、問題がないか確認します:

```
/aidlc --doctor
```

「PASS」または「ok」が並んでいれば準備完了です。

### ステップ 4: ワークフローを開始する

チャットに作りたいものを説明します。`enterprise` スコープを明示的に指定します:

```
/aidlc --scope enterprise 在庫管理システムのREST APIを作成したい
```

または規制が不要な場合は `classic` スコープ:

```
/aidlc --scope classic ユーザー認証システムを作成したい
```

### ステップ 5: 承認ゲートで確認・次へ進む

各フェーズが終わると、AI-DLC は**承認ゲート**で止まります。  
AIが作成した成果物（要件書、設計書など）を確認して:

- **承認する場合**: `y` または `1` と入力して次へ進む
- **修正を求める場合**: 修正内容をテキストで伝える
- **やり直す場合**: `n` と入力してフィードバックを伝える

### ステップ 6: 完了後に成果物を確認する

ワークフローが完了すると、すべての成果物が以下の場所に保存されます:

```
aidlc/spaces/default/intents/<プロジェクト名-ID>/
```

---

## ウォーターフォールの典型的な流れ（enterprise スコープ）

```
/aidlc --scope enterprise <プロジェクト説明>
         ↓
  [初期化] ワークフロー記録を作成
         ↓
  [アイデア出し]
    1. 市場調査 (Market Research)
    2. スコープ定義 (Scope Definition)
    3. フィージビリティ (Feasibility)
    4. チーム編成 (Team Formation)
    5. 大まかなモックアップ (Rough Mockups)
    6. 精緻化モックアップ (Refined Mockups)
    7. 承認・引き継ぎ (Approval Handoff)       ← 承認ゲート
         ↓
  [立ち上げ]
    8. リバースエンジニアリング (既存コードがあれば)
    9. 要件分析 (Requirements Analysis)
   10. ドメイン設計 (Domain Design)
   11. 契約設計 (Contract Design)
   12. 機能設計 (Functional Design)
   13. NFR要件 (NFR Requirements)
   14. NFR設計 (NFR Design)
   15. ユーザーストーリー (User Stories)
   16. ユニット生成 (Units Generation)
   17. プラクティス発見 (Practices Discovery)
   18. デリバリー計画 (Delivery Planning)       ← 承認ゲート
         ↓
  [構築]
   19. インフラ設計 (Infrastructure Design)
   20. コード生成 (Code Generation)
   21. ビルド・テスト (Build and Test)
   22. CIパイプライン (CI Pipeline)             ← 承認ゲート
         ↓
  [運用]
   23. 環境プロビジョニング (Environment Provisioning)
   24. デプロイパイプライン (Deployment Pipeline)
   25. デプロイ実行 (Deployment Execution)
   26. 監視設定 (Observability Setup)
   27. インシデント対応 (Incident Response)
   28. パフォーマンス検証 (Performance Validation)
   29. フィードバック最適化 (Feedback Optimization) ← 承認ゲート
         ↓
      完了！
```

---

## 便利なコマンド

| コマンド | 説明 |
|---|---|
| `/aidlc --doctor` | セットアップの確認 |
| `/aidlc --status` | 現在の進捗を確認 |
| `/aidlc --scope enterprise <説明>` | enterprise スコープで開始 |
| `/aidlc --scope classic <説明>` | classic スコープで開始 |
| `/aidlc --stage <ステージ名>` | 特定のステージにジャンプ |
| `/aidlc --version` | バージョン確認 |
| `aidlc-replay` | これまでの作業履歴を表示 |
| `aidlc-outcomes-pack` | 成果物まとめ (OUTCOMES.md) を生成 |

---

## よくある質問

**Q. 途中で止まってしまったら？**  
A. `/aidlc --status` で現在地を確認し、そのまま作業を再開できます。  
Kiro IDE を再度開けば、前回の続きから再開します。

**Q. 承認ゲートで何を確認すればいい？**  
A. AIが作成した成果物（要件書・設計書など）を人間の目でレビューします。  
「この設計で実装を進めて問題ないか？」を確認するのが主な目的です。

**Q. enterprise と classic はどう違う？**  
A. `enterprise` はアイデア出しフェーズも含む全33ステージを実行し、  
変更が生じると必ず再承認が必要です。`classic` はアイデア出しをスキップして  
設計から始まり、変更管理は緩やかです。

**Q. 成果物はどこに保存される？**  
A. `aidlc/spaces/default/intents/<プロジェクト名-ID>/` 以下に保存されます。  
Git でコミットすれば、チーム全員と共有できます。

---

## トラブルシューティング

| 症状 | 対処法 |
|---|---|
| `aidlc` コマンドが見つからない | PowerShell を再起動するか `$env:Path = 'C:\Users\User\AppData\Local\aidlc\bin;' + $env:Path` を実行 |
| `/aidlc --doctor` でエラーが出る | エラー内容を確認し、表示された手順に従って修正 |
| ワークフローが進まない | `/aidlc --status` で現在地を確認し、チャットで続きを指示 |

---

*AI-DLC 2.8.2 / Kiro IDE harness*
