# ADB 网络与代理

## HTTP 代理

```bash
# 设置代理（确认后执行）
adb shell settings put global http_proxy <ip>:<port>

# 查看当前代理
adb shell settings get global http_proxy

# 清除代理（确认后执行）
adb shell settings put global http_proxy :0
```

### 配合 Charles/Proxyman 抓包流程
```bash
# 1. 设置代理
adb shell settings put global http_proxy 192.168.1.100:8888
# 2. 在 Charles 中安装证书（HTTPS 抓包）
# 3. 进行测试...
# 4. 测试完成后清除代理
adb shell settings put global http_proxy :0
```

## WiFi 与移动数据

```bash
# WiFi（确认后执行）
adb shell svc wifi enable             # 开启 WiFi
adb shell svc wifi disable            # 关闭 WiFi

# 移动数据（确认后执行）
adb shell svc data enable             # 开启移动数据
adb shell svc data disable            # 关闭移动数据

# 飞行模式（确认后执行）
adb shell cmd connectivity airplane-mode enable    # 开启
adb shell cmd connectivity airplane-mode disable   # 关闭
```

## 网络信息查询

```bash
adb shell ifconfig                   # IP 配置
adb shell ip addr show               # IP 地址详情
adb shell netcfg                     # IP 配置（旧语法）
adb shell dumpsys connectivity       # 网络连接详情
adb shell ping -c 4 <host>           # Ping 测试
adb shell nslookup <domain>          # DNS 解析
```

## 端口转发

```bash
# 本地端口 → 设备端口（电脑访问设备上的服务）
adb forward tcp:<local_port> tcp:<device_port>

# 设备端口 → 本地端口（设备访问电脑上的服务）
adb reverse tcp:<device_port> tcp:<local_port>

# 查看已设置的转发
adb forward --list
adb reverse --list

# 移除转发
adb forward --remove tcp:<local_port>
adb reverse --remove tcp:<device_port>

# 移除所有
adb forward --remove-all
adb reverse --remove-all
```

### 常见场景
```bash
# React Native / Flutter 调试：设备访问电脑 DevServer
adb reverse tcp:8081 tcp:8081

# 映射设备的 WebView 调试端口
adb forward tcp:9222 localabstract:webview_devtools_remote_<pid>

# 访问设备上的 HTTP 服务
adb forward tcp:3000 tcp:3000
```
