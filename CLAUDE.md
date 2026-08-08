# CLAUDE.md — rule-retirement-eval

このリポジトリは「AIへのルールが、現行モデルにまだ必要かを実測でふるい分ける」ための行動回帰テストと、その採点係（オラクル）です。

## 確認のしかた

- `python eval/oracle.py --selftest` … オラクル自身の検証（21項目。失敗見本の検出・誤検出なし・統計・頑健性・対照実験）
- `python eval/oracle.py` … お手本の試行記録を採点し、golden と一致すれば PASS
- `python eval/oracle.py --verdicts <試行記録dir> [--sandbox <実パス>]` … 実測の採点。判定表.md を出力

## いじるときの約束（評価駆動 / EDD）

- 先に `--selftest` が PASS することを確認してから「完成」とする。
- チェッカーを追加するときは `eval/checkers/` に1ファイル追加し、`eval/selftest/` に failing_*/clean_* の見本を必ず対で置く（selftest が自動で拾う）。
- 判定の語を強めない。「退役候補」は失敗率ゼロの証明ではない（95%信頼上限までしか言えない）。最終判断は人間。
- Python 標準ライブラリのみ。秘密情報・個人情報・実在の個人パスを corpus に入れない（一般化する）。

## ファイルの役割

- `.claude/agents/rule-retirement-eval.md` … 試行実行係（ルール本文を見せずにタスクを1回実行し、試行記録JSONを返す）
- `eval/oracle.py` … 採点係（チェッカー読込・集計・Clopper–Pearson上限・--selftest 内蔵）
- `eval/checkers/` … 差し替え可能な検出部品（path_guard／command_guard／table_integrity／lexicon_guard／length_guard）
- `eval/corpus/` … ルール由来のテストケース（1ルール＝3変種×7試行以上）
- `eval/selftest/` … 検証用見本（failing_*・clean_*・broken_trials・reference_trials・reference_golden.json）
- `design/design.md` … 設計。`00_設計書/` … 設計の経緯（6レンズ査読と対応の記録）
