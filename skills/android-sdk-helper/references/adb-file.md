# ADB 文件操作

## Push / Pull

```bash
# 推送文件到设备（确认后执行）
adb push <local_file> <remote_path>
adb push <local_dir> <remote_dir>         # 推送整个目录

# 从设备拉取文件
adb pull <remote_path>                     # 拉取到当前目录
adb pull <remote_path> <local_path>        # 拉取到指定路径
adb pull <remote_dir> <local_dir>          # 拉取整个目录
adb pull -a <remote_path> <local_path>     # 保留时间戳
```

### 常见拉取场景
```bash
# 拉取截图
adb pull /sdcard/screen.png ./

# 拉取录屏
adb pull /sdcard/record.mp4 ./

# 拉取已安装的 APK
$path = (adb shell pm path <package> | Select-String "package:" | Select-Object -First 1) -replace "package:", ""
adb pull $path ./extracted.apk

# 拉取 Bugreport
adb pull /data/local/tmp/bugreport.zip ./
```

## 设备端文件管理

```bash
adb shell ls <path>                  # 列出目录
adb shell ls -la <path>              # 详细列表（权限/大小）
adb shell cat <path>                 # 查看文件内容
adb shell rm <path>                  # 删除文件
adb shell rm -r <path>               # 递归删除目录
adb shell mkdir <path>               # 创建目录
adb shell cp <src> <dst>             # 复制文件
adb shell mv <src> <dst>             # 移动/重命名
adb shell chmod <mode> <path>        # 修改权限
adb shell find <path> -name "<pattern>"  # 查找文件
```

## 访问应用私有数据 (run-as)

> 仅 debuggable 应用可用

```bash
# 以应用身份执行命令
adb shell run-as <package> <command>

# 查看应用私有目录
adb shell run-as <package> ls
adb shell run-as <package> ls -la

# 查看 SharedPreferences
adb shell run-as <package> ls shared_prefs/
adb shell run-as <package> cat shared_prefs/<file>.xml

# 查看/导出数据库
adb shell run-as <package> ls databases/
adb shell run-as <package> cat databases/<db>

# 拉取应用私有文件到本地
adb shell run-as <package> cat <private_file> > local_file

# 修改 SharedPreferences（确认后执行）
adb shell run-as <package> sh -c "echo '<xml/>' > shared_prefs/<file>.xml"
```

## 常用路径

| 路径 | 说明 |
|------|------|
| `/sdcard/` | 外部存储根目录 |
| `/sdcard/Download/` | 下载目录 |
| `/sdcard/DCIM/` | 相册 |
| `/sdcard/Android/data/<pkg>/` | 应用外部数据 |
| `/data/data/<pkg>/` | 应用内部数据（需 root 或 run-as） |
| `/data/app/` | 已安装 APK 位置 |
| `/data/local/tmp/` | 临时目录（可读写） |
| `/system/app/` | 系统预装应用 |
| `/system/priv-app/` | 特权系统应用 |
