# ADB 设备管理

## 设备连接

```bash
adb devices                    # 列出连接的设备（基本信息）
adb devices -l                 # 列出设备及详细信息（型号/产品/传输）
adb -s <serial> <command>      # 指定目标设备执行命令
adb connect <ip>:<port>        # 无线连接设备
adb disconnect [<ip>:<port>]   # 断开无线连接
adb kill-server                # 终止 adb 服务端（设备识别异常时修复用）
adb start-server               # 启动 adb 服务端
adb reconnect                  # 断开并重新连接 USB 设备
adb usb                        # 切换回 USB 模式
adb tcpip <port>               # 切换到 TCP/IP 模式（无线调试前置）
```

### WiFi 调试完整流程
```bash
# 1. USB 连接设备后执行
adb tcpip 5555
# 2. 拔掉 USB，连接同一网络
adb connect <设备IP>:5555
# 3. 验证
adb devices
```

## 设备信息查询

### 基本信息
```bash
adb shell getprop ro.build.version.release    # Android 版本号
adb shell getprop ro.build.version.sdk        # SDK API Level
adb shell getprop ro.product.model            # 设备型号
adb shell getprop ro.product.brand            # 设备品牌
adb shell getprop ro.build.display.id         # 系统版本标识
adb shell getprop ro.hardware                 # 硬件信息
adb shell getprop                             # 列出所有系统属性
```

### 屏幕信息
```bash
adb shell wm size              # 屏幕分辨率
adb shell wm density           # 屏幕密度 (DPI)
adb shell dumpsys display      # 显示详情
adb shell dumpsys window displays  # 窗口显示详情
```

### 硬件信息
```bash
adb shell cat /proc/cpuinfo    # CPU 信息
adb shell cat /proc/meminfo    # 内存信息
adb shell df -h                # 磁盘空间
adb shell dumpsys battery      # 电池状态
```

## 设备重启与模式切换

```bash
adb reboot                    # 普通重启（确认后执行）
adb reboot recovery           # 重启到 Recovery 模式（危险）
adb reboot bootloader         # 重启到 Bootloader/Fastboot（危险）
adb root                      # 以 root 权限重启 adb 守护进程（危险，需 debug 版本）
adb unroot                    # 恢复非 root 权限
adb remount                   # 重新挂载 /system 为可读写（需 root，危险）
```

## 屏幕与显示设置

```bash
adb shell wm dismiss-keyguard              # 解锁屏幕（无密码时）
adb shell svc power stayon true            # 保持屏幕常亮（usb连接时）
adb shell svc power stayon usb             # 仅 USB 连接时常亮
adb shell settings put system screen_off_timeout 600000  # 屏幕超时 10 分钟
adb shell settings put system screen_brightness 200     # 设置亮度 0-255
```
