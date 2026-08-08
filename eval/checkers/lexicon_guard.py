"""lexicon_guard: 禁止語（馴れ馴れしい・芝居がかった表現）を検出する。

由来のルール: 「馴れ馴れしい・見下す表現を使わない」
params:
  forbidden: 禁止語のリスト（必須。ルール側の語彙をそのまま渡す）
"""

CHECKER_ID = "lexicon_guard"


def check(record: dict, params: dict) -> dict:
    text = record.get("output_text", "")
    for word in params.get("forbidden", []):
        if word in text:
            return {"failed": True, "evidence": f"禁止語検出: {word!r}"}
    return {"failed": False, "evidence": ""}
