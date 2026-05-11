---
name: android-sdk-helper
description: Android SDK 命令行工具速查与执行助手。覆盖 adb、aapt、apksigner、apkanalyzer、sdkmanager、bundletool、monkey、uiautomator 等全部命令行工具。当用户提到"adb"、"截图"、"包名"、"安装APK"、"抓日志"、"logcat"、"设代理"、"查内存"、"当前页面"、"崩溃日志"、"签名检查"、"APK信息"、"monkey测试"、"录屏"、"模拟点击"、"清除数据"、"覆盖安装"、"冷启动"、"帧率"、"端口转发"、"WiFi调试"、"关闭动画"、"pull文件"、"push文件"、"卸载应用"、"授权"、"Android命令"、"安卓命令"等任何涉及 Android 设备操作、APK 分析、SDK 工具使用的场景时触发此技能。即使用户只是模糊地说"帮我看下设备信息"、"这个APK的信息"、"应用装不上"等，也应触发。
---

# Android SDK Helper

Android SDK 命令行工具的场景化速查与执行助手。用户说需求，你给命令或直接执行。

## SDK 路径解析

> 前置条件：Android SDK 已安装，且设置了 `ANDROID_HOME` 或 `ANDROID_SDK_ROOT` 环境变量。

使用 aapt、apksigner、zipalign、d8、apkanalyzer、sdkmanager 等 SDK 工具前，**必须**先解析路径：

```bash
# 跨平台解析，输出 JSON（需 uv）
$sdk = uv run <skill-dir>/scripts/resolve_sdk.py | ConvertFrom-Json
```

解析后可用变量（以实际输出为准，未安装的工具不会出现在 JSON 中）：

| 变量 | 说明 |
|------|------|
| `$sdk.aapt` / `$sdk.aapt2` | build-tools 下的 AAPT |
| `$sdk.apksigner` | build-tools 下的签名工具 |
| `$sdk.zipalign` / `$sdk.d8` | build-tools 下的其他工具 |
| `$sdk.apkanalyzer` | cmdline-tools 下的 APK 分析工具 |
| `$sdk.sdkmanager` | cmdline-tools 下的 SDK 管理工具 |
| `$sdk.adb` | platform-tools 下的 adb |

**关键规则**：
- 环境变量未设置时脚本会报错退出，此时**停止执行**并提醒用户设置
- **不要**自行猜测 SDK 路径，必须通过此脚本获取
- adb 通常已在 PATH 中独立可用，脚本中的 `$sdk.adb` 仅做备用

## 执行策略

根据命令的风险等级选择执行方式：

| 等级 | 说明 | 执行方式 | 示例 |
|------|------|---------|------|
| 只读 | 查看/查询类，不改变设备状态 | **直接执行** | 截图、查包名、看日志、查设备信息 |
| 修改 | 改变设备/应用状态，但可逆 | **确认后执行** | 安装/卸载、清数据、设代理、关闭动画 |
| 危险 | 不可逆或影响系统 | **必须确认，展示命令让用户手动执行** | 恢复出厂、root、格式化 |

## 场景速查表

以下是按场景的最常用命令。详细参数和更多命令见 `references/` 目录。

### 设备管理

| 用户意图 | 命令 | 参考 |
|---------|------|------|
| 查看连接的设备 | `adb devices -l` | adb-device.md |
| 查看设备型号 | `adb shell getprop ro.product.model` | adb-device.md |
| 查看Android版本 | `adb shell getprop ro.build.version.release` | adb-device.md |
| 查看屏幕分辨率 | `adb shell wm size` | adb-device.md |
| 查看屏幕密度 | `adb shell wm density` | adb-device.md |
| WiFi调试 | `adb tcpip 5555` → `adb connect <ip>:5555` | adb-device.md |
| 重启设备 | 确认后: `adb reboot` | adb-device.md |

### 应用管理

| 用户意图 | 命令 | 参考 |
|---------|------|------|
| 查看所有包名 | `adb shell pm list packages` | adb-app.md |
| 按关键词查包名 | `adb shell pm list packages <keyword>` | adb-app.md |
| 只看第三方应用 | `adb shell pm list packages -3` | adb-app.md |
| 安装APK | 确认后: `adb install -r -t -g <apk>` | adb-app.md |
| 卸载应用 | 确认后: `adb uninstall <package>` | adb-app.md |
| 清除应用数据 | 确认后: `adb shell pm clear <package>` | adb-app.md |
| 授予权限 | 确认后: `adb shell pm grant <pkg> <perm>` | adb-app.md |
| 查看APK路径 | `adb shell pm path <package>` | adb-app.md |
| 强制停止应用 | 确认后: `adb shell am force-stop <package>` | adb-app.md |
| 启动Activity | `adb shell am start -n <pkg>/<activity>` | adb-app.md |
| 查看当前Activity | `adb shell dumpsys activity top \| head -20` | adb-app.md |

### 截图与录屏

| 用户意图 | 命令 | 参考 |
|---------|------|------|
| 截图到本地 | `adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png ./screen.png` | adb-ui.md |
| 录屏 | `adb shell screenrecord --time-limit 30 /sdcard/record.mp4 && adb pull /sdcard/record.mp4 ./record.mp4` | adb-ui.md |
| 模拟点击 | `adb shell input tap <x> <y>` | adb-ui.md |
| 模拟滑动 | `adb shell input swipe <x1> <y1> <x2> <y2> [duration]` | adb-ui.md |
| 输入文本 | `adb shell input text <string>` | adb-ui.md |
| 按键 | `adb shell input keyevent <keycode>` | adb-ui.md |
| 导出UI树 | `adb shell uiautomator dump /sdcard/ui.xml && adb pull /sdcard/ui.xml` | adb-ui.md |

**常用按键码**: HOME=3, BACK=4, 电源=26, MENU=82, 最近任务=187, 音量+=24, 音量-=25, 回车=66, 退格=67

### 日志与调试

| 用户意图 | 命令 | 参考 |
|---------|------|------|
| 实时日志 | `adb logcat -v threadtime` | adb-debug.md |
| 崩溃日志 | `adb logcat -b crash -v threadtime` | adb-debug.md |
| 按包名过滤 | `adb logcat --pid=$(adb shell pidof <pkg>) -v threadtime` | adb-debug.md |
| 按级别过滤 | `adb logcat *:E -v threadtime` | adb-debug.md |
| 清空日志 | `adb logcat -c` | adb-debug.md |
| 保存日志到文件 | `adb logcat -v threadtime -f /sdcard/logcat.txt` | adb-debug.md |
| Bug报告 | `adb bugreport bugreport.zip` | adb-debug.md |
| 查看内存 | `adb shell dumpsys meminfo <package>` | adb-debug.md |
| 查看CPU | `adb shell dumpsys cpuinfo` | adb-debug.md |
| 帧率/FPS | `adb shell dumpsys gfxinfo <package>` | adb-debug.md |
| 冷启动耗时 | `adb shell am start -S -W <pkg>/<activity>` | adb-debug.md |

### 网络与代理

| 用户意图 | 命令 | 参考 |
|---------|------|------|
| 设置代理 | 确认后: `adb shell settings put global http_proxy <ip>:<port>` | adb-network.md |
| 查看代理 | `adb shell settings get global http_proxy` | adb-network.md |
| 清除代理 | 确认后: `adb shell settings put global http_proxy :0` | adb-network.md |
| 关闭WiFi | 确认后: `adb shell svc wifi disable` | adb-network.md |
| 开启WiFi | 确认后: `adb shell svc wifi enable` | adb-network.md |
| 端口转发 | `adb forward tcp:<local> tcp:<device>` | adb-network.md |
| 反向端口转发 | `adb reverse tcp:<device> tcp:<local>` | adb-network.md |

### 文件操作

| 用户意图 | 命令 | 参考 |
|---------|------|------|
| 推送文件 | 确认后: `adb push <local> <remote>` | adb-file.md |
| 拉取文件 | `adb pull <remote> [<local>]` | adb-file.md |
| 查看应用私有数据 | `adb shell run-as <pkg> ls` | adb-file.md |
| 读取SharedPreferences | `adb shell run-as <pkg> cat shared_prefs/<file>.xml` | adb-file.md |

### APK 分析工具

> 使用前必须先执行「SDK 路径解析」(`$sdk = uv run ... | ConvertFrom-Json`)，下述命令中的工具需替换为 `$sdk.aapt`、`$sdk.apksigner` 等

| 用户意图 | 命令 | 参考 |
|---------|------|------|
| 查看APK基本信息 | `& $sdk.aapt dump badging <apk>` | apk-tools.md |
| 查看APK权限 | `& $sdk.aapt dump permissions <apk>` | apk-tools.md |
| 查看Manifest | `& $sdk.aapt dump xmltree <apk> AndroidManifest.xml` | apk-tools.md |
| 检查签名 | `& $sdk.apksigner verify -v --print-certs <apk>` | apk-tools.md |
| 签名APK | 危险: 用户提供 keystore 信息 | apk-tools.md |
| 对比两个APK | `& $sdk.apkanalyzer apk compare --different-only <apk1> <apk2>` | apk-tools.md |
| 查看方法数 | `& $sdk.apkanalyzer dex method-count <apk>` | apk-tools.md |
| AAB转APKS | `bundletool build-apks --bundle=<aab> --output=<apks>` | apk-tools.md |

### 测试与环境

| 用户意图 | 命令 | 参考 |
|---------|------|------|
| Monkey测试 | 确认后: `adb shell monkey -p <pkg> -v 1000` | sdk-other.md |
| 列出已安装SDK | `& $sdk.sdkmanager --list_installed` | sdk-other.md |
| 关闭动画(自动化) | 确认后: 3条 settings put 命令 | sdk-other.md |
| 保持屏幕常亮 | 确认后: `adb shell svc power stayon true` | sdk-other.md |
| 不保留活动 | 确认后: `adb shell settings put global always_finish_activities 1` | sdk-other.md |
| Perfetto性能分析 | `adb shell perfetto -t 10s -o /data/misc/perfetto-traces/trace sched freq idle am wm` | sdk-other.md |

## 常用组合工作流

这些是 QA 日常高频的一键式操作：

### 清理重装
```bash
adb uninstall <package>
adb install -r -t -g <apk>
adb shell am start -n <pkg>/<activity>
```

### 截图保存到本地
```bash
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png "./screenshot_$timestamp.png"
```

### 抓崩溃日志
```bash
adb logcat -c
adb logcat -b crash -v threadtime
```

### 设代理+后清理
```bash
# 设置
adb shell settings put global http_proxy <ip>:<port>
# ... 测试 ...
# 清除
adb shell settings put global http_proxy :0
```

### 自动化环境配置
```bash
adb shell settings put global window_animation_scale 0
adb shell settings put global transition_animation_scale 0
adb shell settings put global animator_duration_scale 0
adb shell svc power stayon true
```

### 提取已安装APK
```bash
$apkPath = (adb shell pm path <package> | Select-String "package:") -replace "package:", ""
adb pull $apkPath ./extracted.apk
```

## 详细参考

当上述速查表无法满足需求时，按需读取 references 目录获取完整命令列表和参数说明：

| 文件 | 内容 |
|------|------|
| `references/adb-device.md` | 设备连接、信息查询、重启模式 |
| `references/adb-app.md` | 安装/卸载、包管理、权限、Activity 操作 |
| `references/adb-debug.md` | logcat、dumpsys、bugreport、性能分析 |
| `references/adb-ui.md` | 截图、录屏、输入模拟、UI 树、按键码完整表 |
| `references/adb-network.md` | 代理、WiFi/数据、端口转发、飞行模式 |
| `references/adb-file.md` | push/pull、run-as、文件管理 |
| `references/apk-tools.md` | aapt、aapt2、apksigner、apkanalyzer、bundletool、zipalign、keytool |
| `references/sdk-other.md` | sdkmanager、monkey、uiautomator、perfetto、d8、环境配置 |

读取规则：只在需要时读取对应的 reference 文件，不要一次性全部加载。

## 多设备处理

当 `adb devices` 返回多台设备时，所有命令需要加 `-s <serial>` 前缀指定目标设备。执行命令前先检查设备数量，多设备时提醒用户选择。
