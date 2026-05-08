---
name: flutter-apk-signing
description: |
  为Flutter Android项目配置APK release签名。当用户需要打包APK release版本、配置签名密钥、生成keystore文件、或在编译release包时遇到签名相关错误时使用此skill。
---

# Flutter APK 签名配置

本skill帮助你在Flutter项目中配置Android release签名的完整流程。

## 工作流程

### 1. 检测项目结构

首先确认项目是Flutter项目并包含Android平台：

```
确认 android/app/build.gradle 存在
确认项目根目录有 pubspec.yaml
```

### 2. 生成 Keystore 文件

使用 `keytool` 命令生成keystore。keystore文件建议放在 `android/app/` 目录下。

**默认命令模板：**
```bash
keytool -genkey -v -keystore android/app/release.jks -alias <密钥别名> -keyalg RSA -keysize 2048 -validity 10000 -storepass <keystore密码> -keypass <密钥密码> -dname "CN=<名称>, O=<组织>, C=<国家代码>"
```

**参数说明：**
- `-keystore`: keystore文件路径，建议使用 `release.jks` 或 `<项目名>.jks`
- `-alias`: 密钥别名
- `-keyalg`: 加密算法，使用 `RSA`
- `-keysize`: 密钥长度，使用 `2048`
- `-validity`: 有效期(天)，推荐 `10000`（约27年）
- `-storepass`: keystore密码
- `-keypass`: 密钥密码
- `-dname`: 证书信息（CN=名称, O=组织, C=国家代码）

**所有需要用户输入的参数，必须通过 `question` 工具逐一询问用户后填入，不要使用任何默认值或示例值。需询问的参数包括：**
1. keystore密码
2. 密钥密码
3. 密钥别名
4. 证书名称（CN）
5. 证书组织（O）
6. 国家代码（C）

### 3. 配置 build.gradle

编辑 `android/app/build.gradle`，在 `android` 块中添加签名配置：

```groovy
android {
    // ... 其他配置 ...

    signingConfigs {
        release {
            keyAlias '<密钥别名>'
            keyPassword '<密钥密码>'
            storeFile file('release.jks')
            storePassword '<keystore密码>'
        }
    }
    
    buildTypes {
        release {
            signingConfig signingConfigs.release
            // ... 其他配置 ...
        }
    }
}
```

### 4. 配置密钥信息（可选但推荐）

为了安全起见，建议将敏感信息放在 `local.properties` 或环境变量中，而不是直接写在 build.gradle 中。

**方式一：使用 local.properties**

在项目根目录的 `local.properties` 中添加：
```properties
KEYSTORE_PASSWORD=<keystore密码>
KEY_PASSWORD=<密钥密码>
KEY_ALIAS=<密钥别名>
```

然后修改 `build.gradle`：
```groovy
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('local.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    signingConfigs {
        release {
            keyAlias keystoreProperties['KEY_ALIAS']
            keyPassword keystoreProperties['KEY_PASSWORD']
            storeFile file('release.jks')
            storePassword keystoreProperties['KEYSTORE_PASSWORD']
        }
    }
    // ...
}
```

**方式二：使用环境变量**

在 `build.gradle` 中使用：
```groovy
signingConfigs {
    release {
        keyAlias System.getenv('KEY_ALIAS') ?: ''
        keyPassword System.getenv('KEY_PASSWORD') ?: ''
        storeFile file('release.jks')
        storePassword System.getenv('KEYSTORE_PASSWORD') ?: ''
    }
}
```

### 5. 验证配置

配置完成后，提示用户可以运行以下命令测试：

```bash
flutter build apk --release
```

## 完整示例

假设用户项目名为 `my_app`，需要配置签名：

1. **通过 `question` 工具询问用户**：keystore密码、密钥密码、密钥别名、证书名称（CN）、证书组织（O）、国家代码（C）

2. **生成keystore**（在项目根目录下执行，使用用户提供的参数）：
```bash
keytool -genkey -v -keystore android/app/my_app.jks -alias <用户提供的密钥别名> -keyalg RSA -keysize 2048 -validity 10000 -storepass <用户提供的keystore密码> -keypass <用户提供的密钥密码> -dname "CN=<用户提供的名称>, O=<用户提供的组织>, C=<用户提供的国家代码>"
```

3. **配置 android/app/build.gradle**：
按照上述模板添加 `signingConfigs` 和 `buildTypes` 配置。

4. **提示用户**：
- 将 `*.jks` 文件加入 `.gitignore`
- 妥善保管密码和keystore文件备份

## 注意事项

1. **密码安全**：使用强密码，不要使用简单密码如 `123456`
2. **备份**：keystore文件丢失无法找回，务必备份
3. **.gitignore**：将 `.jks` 文件加入版本控制忽略列表
4. **多环境**：如有不同环境（dev/staging/prod），可以为每个环境创建不同的keystore