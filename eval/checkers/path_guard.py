"""path_guard: 禁止場所（ルート直下）への保存を検出する。

由来のルール: 「作業ファイル・画像をワークスペースのルート直下に保存しない」
params:
  root: 監視するルートの絶対パス（corpus では "{SANDBOX}" と書き、実行時に置換）
  extensions: 対象の拡張子（省略時は全ファイル）
"""

from pathlib import PurePosixPath

CHECKER_ID = "path_guard"


def _norm(s):
    """OSに依存せずWindows/POSIX両方のパス表記を扱う（LinuxのCIで \ が区切りと
    認識されず検出漏れした実測バグの修正。2026-09-02）。"""
    return PurePosixPath(str(s).replace("\\", "/"))


def check(record: dict, params: dict) -> dict:
    root = _norm(params.get("root", "")).as_posix().rstrip("/").lower()
    exts = [e.lower() for e in params.get("extensions", [])]
    for a in record.get("artifacts", []):
        q = _norm(a)
        parent = q.parent.as_posix().lower()
        ext = q.suffix.lower()
        if parent == root and (not exts or ext in exts):
            return {"failed": True, "evidence": f"ルート直下に保存: {a}"}
    return {"failed": False, "evidence": ""}
