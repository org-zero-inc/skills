# ADB 应用管理

## 包管理 (pm)

### 列出包
```bash
adb shell pm list packages              # 所有已安装包
adb shell pm list packages -3           # 仅第三方应用
adb shell pm list packages -s           # 仅系统应用
adb shell pm list packages -f           # 包名 + APK 路径
adb shell pm list packages -d           # 已禁用的包
adb shell pm list packages -e           # 已启用的包
adb shell pm list packages <keyword>    # 按关键词过滤
```

### 包信息
```bash
adb shell pm path <package>             # 获取 APK 路径
adb shell pm dump <package>             # 完整包信息（权限/版本/数据路径）
adb shell pidof <package>               # 获取应用 PID
adb shell pm list permissions -g        # 列出所有权限组及权限
```

### 包操作（确认后执行）
```bash
adb shell pm clear <package>            # 清除应用数据和缓存
adb shell pm grant <pkg> <permission>   # 授予权限
adb shell pm revoke <pkg> <permission>  # 撤销权限
adb shell pm disable-user <package>     # 禁用应用
adb shell pm enable <package>           # 启用应用
```

### 常用权限授权示例
```bash
# 存储权限
adb shell pm grant <pkg> android.permission.READ_EXTERNAL_STORAGE
adb shell pm grant <pkg> android.permission.WRITE_EXTERNAL_STORAGE
# 位置权限
adb shell pm grant <pkg> android.permission.ACCESS_FINE_LOCATION
adb shell pm grant <pkg> android.permission.ACCESS_COARSE_LOCATION
# 相机和麦克风
adb shell pm grant <pkg> android.permission.CAMERA
adb shell pm grant <pkg> android.permission.RECORD_AUDIO
# 电话状态
adb shell pm grant <pkg> android.permission.READ_PHONE_STATE
```

## 安装与卸载（确认后执行）

### 安装
```bash
adb install <apk>                       # 基本安装
adb install -r <apk>                    # 覆盖安装（保留数据）
adb install -r -t <apk>                 # 覆盖 + 允许测试包
adb install -r -d <apk>                 # 覆盖 + 允许降级
adb install -r -g <apk>                 # 覆盖 + 自动授权
adb install -r -t -g <apk>              # 覆盖 + 测试包 + 自动授权（自动化最常用）
adb install-multiple <apk1> <apk2>      # 安装 Split APK
```

### 卸载
```bash
adb uninstall <package>                 # 完全卸载
adb shell pm uninstall -k <package>     # 卸载但保留数据
adb shell pm uninstall --user 0 <pkg>   # 为当前用户卸载（不删文件，可卸系统预装）
adb shell cmd package install-existing <pkg>  # 恢复被卸载的应用
```

## Activity/Intent 操作 (am)

### 启动 Activity
```bash
adb shell am start -n <pkg>/<activity>                        # 基本启动
adb shell am start -a android.intent.action.VIEW -d <url>     # Deep Link
adb shell am start -n <pkg>/<act> --es <key> <value>         # 传 String 参数
adb shell am start -n <pkg>/<act> --ez <key> <bool>          # 传 Boolean 参数
adb shell am start -n <pkg>/<act> --ei <key> <int>           # 传 Int 参数
adb shell am start -n <pkg>/<act> --eu <key> <uri>           # 传 URI 参数
adb shell am start -W <pkg>/<activity>                        # 启动并输出耗时
adb shell am start -S <pkg>/<activity>                        # 先强制停止再启动（冷启动）
```

### 其他 AM 操作
```bash
adb shell am force-stop <package>           # 强制停止应用（确认后执行）
adb shell am kill <package>                 # 请求停止后台进程（非强制）
adb shell am broadcast -a <action>          # 发送广播
adb shell am instrument -w <pkg>/<runner>   # 运行 Instrumentation 测试
```

### 查看当前 Activity
```bash
adb shell dumpsys activity top | head -20                              # 当前顶部 Activity
adb shell "dumpsys activity activities | grep mResumedActivity"         # 当前 Resume 的 Activity
adb shell "dumpsys window | grep -i mCurrentFocus"                     # 当前焦点窗口
```
