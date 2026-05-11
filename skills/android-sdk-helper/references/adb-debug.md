# ADB 日志与调试

## Logcat

### 基本用法
```bash
adb logcat                              # 实时日志流
adb logcat -d                           # 输出后退出（dump 模式，看历史日志）
adb logcat -c                           # 清空日志缓冲区
adb logcat -g                           # 查看缓冲区大小
adb logcat -G <size>                    # 设置缓冲区大小（如 16M）
```

### 过滤
```bash
adb logcat -b crash                     # 崩溃缓冲区（专注崩溃）
adb logcat -b main                      # 主缓冲区
adb logcat -b system                    # 系统缓冲区
adb logcat -b events                    # 事件缓冲区
adb logcat -b radio                     # 无线电缓冲区

adb logcat *:E                          # Error 及以上
adb logcat *:W                          # Warning 及以上
adb logcat *:I                          # Info 及以上
adb logcat <tag>:<level> *:S            # 只看特定 Tag（S = Silent 其他）

adb logcat --pid=<pid>                  # 按 PID 过滤
adb logcat --pid=$(adb shell pidof <pkg>) -v threadtime  # 按包名过滤
```

### 格式化
```bash
adb logcat -v time                      # 显示时间戳
adb logcat -v threadtime                # 时间戳 + 线程信息（最常用）
adb logcat -v long                      # 长格式
adb logcat -v brief                     # 简短格式（默认）
```

### 保存与轮转
```bash
adb logcat -f /sdcard/logcat.txt                    # 写入设备文件
adb logcat -v threadtime -f /sdcard/logcat.txt      # 写入设备文件（带时间）
adb logcat -r 1024 -n 5 -f /sdcard/logcat.txt       # 轮转：每 1MB 一个文件，保留 5 个
```

### 日志保存到本地电脑
```bash
# PowerShell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
adb logcat -d -v threadtime > "logcat_$timestamp.txt"
```

## Dumpsys

### 常用 dumpsys
```bash
adb shell dumpsys activity <package>     # Activity 信息
adb shell dumpsys activity top           # 当前顶部 Activity
adb shell dumpsys activity activities    # 完整 Activity 任务栈
adb shell dumpsys meminfo <package>      # 应用内存详情
adb shell dumpsys cpuinfo                # CPU 使用率
adb shell dumpsys battery                # 电池信息
adb shell dumpsys notification           # 通知信息
adb shell dumpsys window                 # 窗口信息
adb shell dumpsys package <package>      # 包信息（权限/组件等）
adb shell dumpsys connectivity           # 网络连接详情
adb shell dumpsys dbinfo                 # 数据库使用信息
adb shell dumpsys procstats              # 进程历史统计
```

### 图形性能
```bash
adb shell dumpsys gfxinfo <package>                # 图形渲染 / FPS / Jank 统计
adb shell dumpsys gfxinfo <package> framestats     # 详细帧时间
# 重置帧数据
adb shell dumpsys gfxinfo <package> reset
```

## 性能分析

### 冷启动耗时
```bash
adb shell am start -S -W <pkg>/<activity>
# 输出 WaitTime / TotalTime 等指标
```

### 内存监控
```bash
# 单次查看
adb shell dumpsys meminfo <package>

# 持续监控（PowerShell 循环 60 秒）
1..60 | ForEach-Object { adb shell dumpsys meminfo <package> | Select-String "TOTAL"; Start-Sleep 1 }
```

### CPU 监控
```bash
adb shell top -m 10                     # Top 10 CPU 进程
adb shell top -p <pid>                  # 监控指定进程
adb shell top -b -n 1                   # Batch 模式（适合脚本）
```

### 进程管理
```bash
adb shell ps                            # 列出进程
adb shell ps -A                         # Android 10+ 语法
adb shell ps | grep <package>           # 过滤特定进程
adb shell pidof <package>               # 快速获取 PID
adb shell kill <pid>                    # 杀进程（确认后执行）
adb shell kill -9 <pid>                 # 强制杀进程（确认后执行）
adb shell cat /proc/<pid>/oom_adj       # OOM 优先级
```

## Bug 报告

```bash
adb bugreport                           # 生成完整 Bugreport（输出到 stdout）
adb bugreport bugreport.zip             # 保存到本地文件
# Bugreport 包含: logcat + dumpsys + 其他系统状态
```

### 最小化 Bug 报告（快速获取关键信息）
```bash
# 清空日志 → 复现问题 → 抓日志
adb logcat -c
# ... 操作复现问题 ...
adb logcat -d -v threadtime -b crash > crash.txt
adb logcat -d -v threadtime > logcat.txt
adb shell dumpsys activity top > activity_top.txt
```
