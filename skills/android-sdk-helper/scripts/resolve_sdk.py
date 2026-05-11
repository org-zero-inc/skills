"""Android SDK 路径解析 - 跨平台

前置条件: Android SDK 已安装，且设置了 ANDROID_HOME 或 ANDROID_SDK_ROOT 环境变量。

用法:
  uv run resolve_sdk.py
"""

import json
import os
import sys
from pathlib import Path


def find_latest(base: Path) -> Path | None:
    dirs = sorted((d for d in base.iterdir() if d.is_dir()), reverse=True)
    return dirs[0] if dirs else None


def resolve(tools_dir: Path, name: str) -> str | None:
    suffixes = [".exe", ".bat", ".cmd"] if sys.platform == "win32" else [""]
    for s in suffixes:
        p = tools_dir / (name + s)
        if p.exists():
            return str(p)
    return None


def main():
    sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
    if not sdk_root:
        print(
            json.dumps(
                {"error": "未设置 ANDROID_HOME 或 ANDROID_SDK_ROOT 环境变量"},
                ensure_ascii=False,
            )
        )
        sys.exit(1)

    sdk = Path(sdk_root)
    if not sdk.exists():
        print(json.dumps({"error": f"SDK 路径不存在: {sdk_root}"}, ensure_ascii=False))
        sys.exit(1)

    result = {"sdk_root": str(sdk)}

    bt_base = sdk / "build-tools"
    if bt_base.exists():
        bt = find_latest(bt_base)
        if bt:
            result["build_tools_dir"] = str(bt)
            for t in ["aapt", "aapt2", "apksigner", "zipalign", "d8"]:
                r = resolve(bt, t)
                if r:
                    result[t] = r

    ct_base = sdk / "cmdline-tools"
    if ct_base.exists():
        ct = find_latest(ct_base)
        if ct:
            result["cmdline_tools_dir"] = str(ct)
            for t in ["apkanalyzer", "sdkmanager", "avdmanager"]:
                r = resolve(ct / "bin", t)
                if r:
                    result[t] = r

    pt = sdk / "platform-tools"
    if pt.exists():
        result["platform_tools_dir"] = str(pt)
        r = resolve(pt, "adb")
        if r:
            result["adb"] = r

    emu = sdk / "emulator"
    if emu.exists():
        r = resolve(emu, "emulator")
        if r:
            result["emulator"] = r

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
