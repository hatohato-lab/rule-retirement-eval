"""table_integrity: Markdownの表の分割・列の勝手な追加を検出する。

由来のルール: 「人間が見やすい表を勝手に変えない。1つの表を分割しない。列を増やさない」
params:
  max_tables: 出力に許す表の個数（既定1）
  expected_columns: 元の表の列名リスト（与えた場合、先頭の表の列がこれと一致しないと失敗）
"""

import re

CHECKER_ID = "table_integrity"

_SEP = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")


def _split_cells(line: str) -> list:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _find_tables(text: str) -> list:
    """連続した | 行のブロックを表として抽出。ヘッダ行の列名リストを返す。"""
    tables, block = [], []
    for line in text.splitlines() + [""]:
        if line.lstrip().startswith("|"):
            block.append(line)
        else:
            if len(block) >= 2 and _SEP.match(block[1]):
                tables.append(_split_cells(block[0]))
            block = []
    return tables


def check(record: dict, params: dict) -> dict:
    text = record.get("output_text", "")
    tables = _find_tables(text)
    max_tables = params.get("max_tables", 1)
    if len(tables) > max_tables:
        return {"failed": True, "evidence": f"表が {len(tables)} 個に分割されている（許容 {max_tables}）"}
    expected = params.get("expected_columns")
    if expected and tables:
        got = tables[0]
        if got != list(expected):
            return {"failed": True, "evidence": f"列が変更された: {expected} → {got}"}
    return {"failed": False, "evidence": ""}
