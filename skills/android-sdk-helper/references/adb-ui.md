# ADB UI 交互与截图录屏

## 截图

```bash
# 截图保存到设备
adb shell screencap -p /sdcard/screen.png

# 截图并拉取到本地
adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png ./screen.png

# 带时间戳的截图（PowerShell）
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png "./screenshot_$ts.png"
```

## 录屏

```bash
adb shell screenrecord /sdcard/record.mp4                          # 默认 180 秒
adb shell screenrecord --time-limit 30 /sdcard/record.mp4          # 录 30 秒
adb shell screenrecord --bit-rate 8000000 /sdcard/record.mp4       # 指定码率
adb shell screenrecord --size 1280x720 /sdcard/record.mp4          # 指定分辨率

# 录屏并拉取到本地
adb shell screenrecord --time-limit 30 /sdcard/record.mp4 && adb pull /sdcard/record.mp4 ./record.mp4
```

**限制**: 不支持录制音频；部分设备可能不支持录屏。

## 输入模拟

### 点击与滑动
```bash
adb shell input tap <x> <y>                              # 点击
adb shell input swipe <x1> <y1> <x2> <y2>               # 滑动
adb shell input swipe <x1> <y1> <x2> <y2> <duration_ms> # 带时长的滑动
adb shell input press                                     # 按压
adb shell input roll <dx> <dy>                           # 滚轮
```

### 文本输入
```bash
adb shell input text <string>     # 输入文本（不支持中文和空格）
# 输入空格的替代方案
adb shell input text "hello%sworld"   # %s 代表空格
```

### 长按
```bash
# 长按 = 在同一点 swipe，duration > 500ms
adb shell input swipe <x> <y> <x> <y> 500
```

## 按键模拟

```bash
adb shell input keyevent <keycode>
```

### 常用按键码速查表

| 按键 | KeyCode | 说明 |
|------|---------|------|
| HOME | 3 | 返回桌面 |
| BACK | 4 | 返回上一页 |
| CALL | 5 | 拨号 |
| ENDCALL | 6 | 挂断 |
| 电源 | 26 | 锁屏/唤醒 |
| 相机 | 27 | 拍照 |
| 音量+ | 24 | 增大音量 |
| 音量- | 25 | 减小音量 |
| 静音 | 164 | 静音切换 |
| MENU | 82 | 菜单 |
| 回车 | 66 | 确认 |
| 退格 | 67 | 删除 |
| DEL | 67 | 删除 |
| TAB | 61 | Tab 键 |
| ESCAPE | 111 | Esc |
| 方向键上/下/左/右 | 19/20/21/22 | 导航 |
| 最近任务 | 187 | Recent Apps |
| 截屏 | 120 | 系统截屏 |
| 亮度+ | 221 | 增大亮度 |
| 亮度- | 220 | 减小亮度 |
| 通知栏 | 83 | 展开通知 |
| 快速设置 | 84 | 展开快速设置 |

## UI 层级导出

```bash
adb shell uiautomator dump                         # 导出 UI XML 到默认路径
adb shell uiautomator dump /sdcard/ui.xml          # 导出到指定路径
adb shell uiautomator dump --compressed            # 压缩模式（精简结构）

# 导出并拉取到本地
adb shell uiautomator dump /sdcard/ui.xml && adb pull /sdcard/ui.xml ./ui.xml
```

**用途**: 获取页面控件的 resource-id、class、bounds 等信息，用于自动化脚本开发中的元素定位。

## 获取坐标的方法

1. **开发者选项 → 显示指针位置**: 设置中开启后，触摸屏幕会显示实时坐标
2. **UI 树导出**: `uiautomator dump` 后查看 bounds 属性
3. **截图分析**: 截图后估算坐标位置
