# APK 分析工具

> 所有工具使用前必须先执行 SKILL.md 中的「SDK 路径解析」流程（`$sdk = uv run ... | ConvertFrom-Json`）。下文命令中的工具名均应替换为 `$sdk.aapt`、`$sdk.apksigner`、`$sdk.apkanalyzer` 等。

## AAPT / AAPT2

> 位于 `<sdk>/build-tools/<version>/` 目录下，已解析为 `$sdk.aapt` / `$sdk.aapt2`

### AAPT dump 命令
```bash
aapt dump badging <apk>                   # APK 概要（包名/版本/图标/权限）
aapt dump permissions <apk>               # 权限列表
aapt dump resources <apk>                 # 资源表
aapt dump configurations <apk>            # 支持的配置（语言/密度等）
aapt dump xmltree <apk> AndroidManifest.xml  # Manifest XML 树
aapt dump xmlstrings <apk> <path>         # XML 中的字符串
aapt dump strings <apk>                   # 所有字符串资源
aapt dump values <apk> [<config>]         # values 资源
```

### AAPT list
```bash
aapt list <apk>                           # 列出 APK 内所有文件
aapt list -v <apk>                        # 详细列表（含压缩方法/大小）
```

### AAPT2
```bash
aapt2 dump badging <apk>                  # 同 aapt，AAPT2 版本
aapt2 dump permissions <apk>
aapt2 dump resources <apk>
aapt2 dump configurations <apk>
aapt2 dump xmltree --file AndroidManifest.xml <apk>
aapt2 dump strings <apk>
aapt2 version                             # 版本号
```

## Apksigner

> 位于 `<sdk>/build-tools/<version>/` 目录下，已解析为 `$sdk.apksigner` 变量

### 验证签名
```bash
apksigner verify <apk>                            # 验证签名是否有效
apksigner verify -v <apk>                         # 详细验证（含签名方案版本 v1/v2/v3/v4）
apksigner verify --print-certs <apk>              # 输出证书信息
apksigner verify -v --print-certs <apk>           # 完整验证 + 证书（最全面）
```

### 签名 APK（危险操作，需确认）
```bash
apksigner sign --ks <keystore> --ks-key-alias <alias> --out <output.apk> <input.apk>
apksigner sign --ks <keystore> --ks-pass pass:<pwd> --key-pass pass:<pwd> --out <out> <in>
apksigner sign --ks <keystore> --v1-signing-enabled true --v2-signing-enabled true --out <out> <in>
```

## Keytool

> JDK 自带工具

```bash
keytool -genkey -v -keystore <name>.jks -keyalg RSA -keysize 2048 -validity 10000 -alias <alias>  # 生成密钥
keytool -list -v -keystore <keystore>         # 查看 keystore 内容
keytool -printcert -jarfile <apk>             # 查看 APK 签名证书
keytool -exportcert -alias <alias> -keystore <keystore> -file <cert.crt>  # 导出证书
```

## Apkanalyzer

> 位于 `<sdk>/cmdline-tools/latest/bin/` 目录下，已解析为 `$sdk.apkanalyzer` 变量

### APK 信息
```bash
apkanalyzer apk summary <apk>                # 概要（包名/版本/大小）
apkanalyzer apk file-size <apk>              # APK 文件大小
apkanalyzer apk download-size <apk>          # 下载大小（压缩后）
apkanalyzer apk features <apk>               # 使用的 Feature
```

### APK 对比
```bash
apkanalyzer apk compare <apk1> <apk2>                    # 对比差异
apkanalyzer apk compare --different-only <apk1> <apk2>   # 仅显示差异
apkanalyzer apk compare --files-only <apk1> <apk2>       # 仅文件差异
```

### DEX 分析
```bash
apkanalyzer dex list <apk>                   # 列出 DEX 文件
apkanalyzer dex references <apk>             # 类引用
apkanalyzer dex packages <apk>               # 包/类列表
apkanalyzer dex packages --proguard-mapping <mapping> <apk>  # 反混淆
apkanalyzer dex methods <apk>                # 所有方法
apkanalyzer dex method-count <apk>           # 方法总数
apkanalyzer dex method-count-by-package <apk>  # 按包统计方法数
```

### Manifest
```bash
apkanalyzer manifest print <apk>             # 打印 Manifest
apkanalyzer manifest application-id <apk>    # Application ID
apkanalyzer manifest version-name <apk>      # 版本名
apkanalyzer manifest version-code <apk>      # 版本号
apkanalyzer manifest min-sdk <apk>           # 最低 SDK
apkanalyzer manifest target-sdk <apk>        # 目标 SDK
apkanalyzer manifest permissions <apk>       # 权限列表
apkanalyzer manifest debuggable <apk>        # 是否可调试
```

### 资源与文件
```bash
apkanalyzer files list <apk>                 # 文件列表
apkanalyzer files cat --file <path> <apk>    # 查看文件内容
apkanalyzer resources packages <apk>         # 资源包
apkanalyzer resources configs --type <type> <apk>  # 资源配置
apkanalyzer resources value --type <type> --name <name> --config <config> <apk>  # 资源值
apkanalyzer resources xml --file <path> <apk>     # XML 资源
```

## Bundletool

### AAB → APKS
```bash
bundletool build-apks --bundle=<aab> --output=<apks>
bundletool build-apks --bundle=<aab> --output=<apks> --ks=<ks> --ks-key-alias=<alias>
```

### 安装与提取
```bash
bundletool install-apks --apks=<apks>                           # 安装 APKS
bundletool get-device-spec --output=device.json                 # 获取设备规格
bundletool extract-apks --apks=<apks> --output-dir=<dir> --device-spec=device.json  # 提取 APK
```

### 查看 AAB
```bash
bundletool dump manifest --bundle=<aab>     # 查看 AAB 的 Manifest
bundletool verify --bundle=<aab>            # 验证 AAB
```

## Zipalign

> 位于 `<sdk>/build-tools/<version>/` 目录下，已解析为 `$sdk.zipalign` 变量

```bash
zipalign -f 4 <input.apk> <output.apk>     # 4 字节对齐（签名前执行）
zipalign -c -v 4 <apk>                     # 验证是否已对齐
```

**注意**: zipalign 必须在 apksigner 签名**之前**执行。v1 签名(jarsigner)则需要在签名**之后**执行。

## D8

> 位于 `<sdk>/build-tools/<version>/` 目录下，已解析为 `$sdk.d8` 变量

```bash
d8 --release --output <dir> <class_files>   # Release 模式编译 DEX
d8 --debug --output <dir> <class_files>     # Debug 模式
d8 --min-api <level> --output <dir> <files> # 指定最低 API
```
