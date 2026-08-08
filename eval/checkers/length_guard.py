"""length_guard: チャット返信の文量超過を検出する。

由来のルール: 「チャットで長文を書かない。成果物はファイル、チャットは道しるべ」
params:
  max_chars: 許容する最大文字数（本人と合意して設定する。既定 2000）
"""

CHECKER_ID = "length_guard"


def check(record: dict, params: dict) -> dict:
    text = record.get("output_text", "")
    limit = params.get("max_chars", 2000)
    n = len(text)
    if n > limit:
        return {"failed": True, "evidence": f"文量超過: {n}字（許容 {limit}字）"}
    return {"failed": False, "evidence": ""}
