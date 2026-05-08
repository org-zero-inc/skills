---
name: windows-system-update
description: |
  执行 Windows 系统全面更新，包括：1）检查并安装 Windows 系统更新；2）使用 winget 更新已安装应用；3）使用 scoop 更新已安装应用。
  更新完成后自动清理下载缓存（优先使用各工具自带的清理命令）。
  当用户提到"系统更新"、"更新Windows"、"winget更新"、"scoop更新"、"更新所有软件"、"更新应用"、"系统维护"、"检查更新"、"升级系统"等关键词时触发此技能。
  即使没有明确说"系统更新"，只要上下文涉及在 Windows 上批量更新系统或应用，都应触发此技能。
---

# Windows 系统更新技能

本技能用于在 Windows 11 系统上执行全面的系统更新操作，涵盖操作系统更新、winget 应用更新、scoop 应用更新，并在完成后清理下载缓存。

## 执行流程

按以下顺序逐步执行。每一步完成后报告结果，再进入下一步。所有命令必须使用 **PowerShell 7+** 语法。

### 第一步：检查并安装 Windows 系统更新

使用 PowerShell 的 `PSWindowsUpdate` 模块检查和安装 Windows 更新。

```powershell
# 安装 PSWindowsUpdate 模块（如尚未安装）
if (-not (Get-Module -ListAvailable -Name PSWindowsUpdate)) {
    Install-Module -Name PSWindowsUpdate -Force -Scope CurrentUser
}

# 导入模块
Import-Module PSWindowsUpdate

# 检查可用更新
Get-WindowsUpdate -AcceptSource -AutoSelect -Verbose

# 安装所有可用更新（自动接受并自动重启）
Install-WindowsUpdate -AcceptAll -AutoReboot -Verbose

# 安装微软更新
Install-WindowsUpdate -AcceptAll -AutoReboot -Verbose -MicrosoftUpdate
```

**注意事项：**
- 如果系统需要重启才能完成更新，`-AutoReboot` 会自动重启。若用户不希望自动重启，移除 `-AutoReboot` 参数，改为 `-IgnoreReboot`。
- 如果用户当前不方便重启，询问用户是否稍后重启。
- 某些更新可能需要多次安装-重启循环，提示用户在重启后再次运行本技能。

### 第二步：使用 winget 更新已安装应用

```powershell
# 查看可更新的应用列表
winget upgrade --all --verbose
```

**注意事项：**
- `--all` 会更新所有可更新的应用。如果用户只想查看，先用 `winget upgrade` 列表，确认后再执行 `winget upgrade --all`。
- 某些应用可能要求管理员权限，此时需要在管理员终端中运行。
- 如果个别应用更新失败，不影响其他应用继续更新，记录失败的应用名称供用户参考。

### 第三步：使用 scoop 更新已安装应用

```powershell
# 先更新 scoop 自身和 bucket 信息
scoop update

# 更新所有已安装的应用
scoop update --all
```

**注意事项：**
- 如果 scoop 未安装，跳过此步骤并告知用户。
- 某些应用可能需要 7zip 或其他依赖来解压，确保 scoop 的依赖项是最新的。

### 第四步：清理下载缓存

更新完成后，必须按以下优先级清理各工具产生的下载文件：

#### 4.1 清理 Windows 更新缓存

```powershell
# 使用 Windows 自带的磁盘清理工具（优先）
cleanmgr /d C /autoclean
```

如果 `cleanmgr` 不可用或用户希望更彻底清理：

```powershell
# 停止 Windows Update 服务后手动清理
Stop-Service -Name wuauserv -Force
Remove-Item -Path "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue
Start-Service -Name wuauserv
```

#### 4.2 清理 winget 缓存

```powershell
# winget 没有专用清理命令，手动清理下载目录
Remove-Item -Path "$env:LOCALAPPDATA\Packages\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe\LocalCache\DiagOutputDir\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:TEMP\winget\*" -Recurse -Force -ErrorAction SilentlyContinue
```

#### 4.3 清理 scoop 缓存

```powershell
# 使用 scoop 自带清理命令（优先）
scoop cache rm --all

# 清理旧版本应用
sweep cleanup --all 2>$null; scoop cleanup --all

# 如果 scoop cleanup 命令不在，使用以下替代
# scoop cleanup -k --all 2>$null
```

#### 4.4 清理系统临时文件（通用）

```powershell
# 清理用户临时目录
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue

# 清理 Windows 临时目录（需管理员权限）
Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
```

## 输出报告

所有步骤完成后，生成一份简要报告，包含：

```
=== Windows 系统更新报告 ===
日期: <执行日期>

1. Windows 系统更新
   状态: <成功/失败/无需更新>
   已安装更新数: <N>
   备注: <是否需要重启等>

2. winget 应用更新
   状态: <成功/失败>
   已更新应用数: <N>
   失败应用: <列表，无则填"无">

3. scoop 应用更新
   状态: <成功/失败/未安装>
   已更新应用数: <N>

4. 缓存清理
   Windows 更新缓存: <已清理>
   winget 缓存: <已清理>
   scoop 缓存: <已清理>
   临时文件: <已清理>
```

## 常见问题处理

| 问题 | 解决方案 |
|------|----------|
| PSWindowsUpdate 安装失败 | 尝试以管理员身份运行 PowerShell，或使用 `Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted` |
| winget 命令未找到 | 执行 `winget` 确认是否安装；如未安装，从 Microsoft Store 安装"应用安装程序" |
| scoop 命令未找到 | 跳过 scoop 步骤，提示用户可运行 `irm get.scoop.sh \| iex` 安装 |
| 权限不足 | 提示用户以管理员身份运行终端后重试 |
| 网络超时 | 建议检查网络连接，或尝试更换网络后重新执行 |
