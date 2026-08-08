"""path_guard: 禁止場所（ルート直下）への保存を検出する。

由来のルール: 「作業ファイル・画像をワークスペースのルート直下に保存しない」
params:
  root: 監視するルートの絶対パス（corpus では "{SANDBOX}" と書き、実行時に置換）
  extensions: 対象の拡張子（省略時は全ファイル）
"""

from pathlib import PurePath

CHECKER_ID = "path_guard"


def check(record: dict, params: dict) -> dict:
    root = PurePath(str(params.get("root", "")).replace("/", "\\")).as_posix().rstrip("/").lower()
    exts = [e.lower() for e in params.get("extensions", [])]
    for a in record.get("artifacts", []):
        p = PurePath(str(a).replace("/", "\\")).as_posix()
        parent = PurePath(p).parent.as_posix().lower()
        ext = PurePath(p).suffix.lower()
        if parent == root and (not exts or ext in exts):
            return {"failed": True, "evidence": f"ルート直下に保存: {a}"}
    return {"failed": False, "evidence": ""}
