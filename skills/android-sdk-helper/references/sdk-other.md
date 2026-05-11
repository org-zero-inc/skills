# 其他 SDK 工具

> SDK 工具使用前必须先执行 SKILL.md 中的「SDK 路径解析」流程（`$sdk = uv run ... | ConvertFrom-Json`）。sdkmanager 已解析为 `$sdk.sdkmanager`。

## SDK Manager

### 查看与安装
```bash
$sdk.sdkmanager --list                  # 列出所有可用和已安装的包
$sdk.sdkmanager --list_installed        # 仅已安装的包
$sdk.sdkmanager --list -s               # 精简输出（仅包名，适合脚本）
```

### 安装包（确认后执行）
```bash
$sdk.sdkmanager --install "platforms;android-34"             # 安装 Android 14 平台
$sdk.sdkmanager --install "build-tools;34.0.0"               # 安装 Build Tools
$sdk.sdkmanager --install "platform-tools"                    # 安装/更新 adb
$sdk.sdkmanager --install "system-images;android-34;google_apis;x86_64"  # 模拟器镜像
$sdk.sdkmanager --install "cmdline-tools;latest"              # 命令行工具
$sdk.sdkmanager --install "ndk;26.1.10909125"                 # NDK
$sdk.sdkmanager --uninstall "<package>"                       # 卸载包（确认后执行）
$sdk.sdkmanager --update                                      # 更新所有已安装包（确认后执行）
$sdk.sdkmanager --licenses                                    # 接受/查看许可证
$sdk.sdkmanager --sdk_root=<path>                             # 指定 SDK 根目录
```

## Monkey 测试

### 基本用法（确认后执行）
```bash
adb shell monkey -p <package> -v 1000                                  # 1000 次随机事件
adb shell monkey -p <package> --throttle 500 -v 1000                   # 间隔 500ms
adb shell monkey -p <package> --pct-touch 50 --pct-motion 30 -v 1000  # 指定事件比例
adb shell monkey -p <package> --bugreport -v 1000                      # 带 Bugreport
adb shell monkey -p <package> -s <seed> -v 1000                        # 指定随机种子（可复现）
```

### 事件比例参数
```bash
--pct-touch <percent>       # 触摸事件
--pct-motion <percent>      # 滑动事件
--pct-trackball <percent>   # 轨迹球事件
--pct-nav <percent>         # 导航事件
--pct-majornav <percent>    # 主要导航事件
--pct-syskeys <percent>     # 系统按键
--pct-appswitch <percent>   # Activity 切换
--pct-flip <percent>        # 翻转事件
```

### Monkey 高级选项
```bash
--ignore-crashes            # 忽略崩溃继续执行
--ignore-timeouts           # 忽略 ANR 继续执行
--ignore-security-exceptions # 忽略安全异常
--kill-process-after-error  # 出错后杀进程
--monitor-native-crashes    # 监控 Native 崩溃
--hprof                     # 内存分析（生成 .hprof 文件）
```

## UI Automator

### UI 树导出
```bash
adb shell uiautomator dump                         # 导出 UI XML
adb shell uiautomator dump /sdcard/ui.xml          # 指定路径
adb shell uiautomator dump --compressed            # 压缩模式
adb shell uiautomator dump --compressed /sdcard/ui.xml

# 导出到本地
adb shell uiautomator dump /sdcard/ui.xml && adb pull /sdcard/ui.xml ./ui.xml
```

### 运行 UI Automator 测试
```bash
adb shell uiautomator runtest <jar> -c <class>
adb shell uiautomator runtest <jar> -c <class> --nohup  # 后台运行
```

## Perfetto 性能分析

```bash
# 简化抓取（10 秒）
adb shell perfetto -t 10s -o /data/misc/perfetto-traces/trace sched freq idle am wm

# 使用配置文件
adb shell perfetto -c - --txt -o /data/misc/perfetto-traces/trace <<EOF
 buffers {
   size_kb: 63488
 }
 data_sources {
   config {
     data_source_name: "linux.ftrace"
     ftrace_config {
       ftrace_events: "sched/sched_switch"
       ftrace_events: "power/cpu_frequency"
     }
   }
 }
 duration_ms: 10000
EOF

# 拉取 trace 文件
adb pull /data/misc/perfetto-traces/trace ./trace.pb
# 使用 https://ui.perfetto.dev 分析
```

## 编译模式控制

```bash
adb shell cmd package compile -m speed <package>          # 强制 speed 编译（消除 dex2oat 影响）
adb shell cmd package compile -m speed-profile <package>  # speed-profile 模式
adb shell cmd package compile --reset <package>           # 重置编译配置
```

## 环境配置（测试自动化常用）

```bash
# 关闭所有动画（确认后执行）
adb shell settings put global window_animation_scale 0
adb shell settings put global transition_animation_scale 0
adb shell settings put global animator_duration_scale 0

# 恢复动画
adb shell settings put global window_animation_scale 1
adb shell settings put global transition_animation_scale 1
adb shell settings put global animator_duration_scale 1

# 不保留活动（确认后执行）
adb shell settings put global always_finish_activities 1
# 恢复
adb shell settings put global always_finish_activities 0

# 保持屏幕常亮
adb shell svc power stayon true

# 开启开发者选项
adb shell settings put global development_settings_enabled 1

# 开启 ADB 调试
adb shell settings put global adb_enabled 1
```

## Systrace（已弃用，推荐 Perfetto）

```bash
python systrace.py -t 10 -o trace.html gfx view sched
```
