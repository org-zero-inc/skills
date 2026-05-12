---
name: curl-converter
description: 将 cURL 命令转换为各种编程语言的 HTTP 请求代码。使用 npm 包 curlconverter 进行转换，支持 Python、JavaScript、Go、Java、PHP、Rust 等 40+ 种语言/库组合。当用户提到"转换curl"、"curl转代码"、"curl to python"、"curl转python"、"curl转js"、"curl转java"、"curl转go"、"curl转请求代码"等任何涉及将 cURL 命令转换为编程语言代码的场景时触发此技能。即使用户只是粘贴了一段 curl 命令并问"帮我转成XX语言"或"这个curl用XX怎么写"，也应触发。
---

# curlconverter - cURL 命令转代码

将用户提供的 cURL 命令转换为指定编程语言的 HTTP 请求代码，基于 npm 包 `curlconverter` 实现。

## 工作流程

### 1. 识别输入

从用户消息中提取 cURL 命令。cURL 命令通常以 `curl` 开头，可能跨多行。常见格式：

```
curl 'https://example.com/api' \
  -H 'Content-Type: application/json' \
  -d '{"key":"value"}'
```

### 2. 确定目标语言

根据用户指定的目标语言进行转换。如果用户未指定，默认使用 **Python (requests)**。

将用户提到的语言/库映射到 curlconverter 支持的 `--language` 参数值：

| 用户可能说的 | --language 值 |
|---|---|
| Python, python, requests | `python` |
| JavaScript, JS, fetch, 浏览器 | `javascript` |
| Node.js, node, node-fetch | `node` |
| axios, node-axios | `node-axios` |
| Go, Golang | `go` |
| Java | `java` |
| Java OkHttp | `java-okhttp` |
| Java HttpURLConnection | `java-httpurlconnection` |
| PHP | `php` |
| PHP Guzzle | `php-guzzle` |
| Rust | `rust` |
| C# | `csharp` |
| Ruby | `ruby` |
| Kotlin | `kotlin` |
| Swift | `swift` |
| Dart | `dart` |
| C | `c` |
| MATLAB | `matlab` |
| R | `r` |
| PowerShell | `powershell` |
| Ansible | `ansible` |
| Clojure | `clojure` |
| Elixir | `elixir` |
| Julia | `julia` |
| Lua | `lua` |
| Perl | `perl` |
| OCaml | `ocaml` |
| Objective-C | `objc` |
| wget | `wget` |
| HTTPie | `httpie` |
| HAR | `har` |
| JSON | `json` |

完整语言列表可通过 `npx curlconverter --help` 查看。如果用户提到的语言不在映射表中，尝试模糊匹配；如果无法匹配，列出可用语言让用户选择。

### 3. 执行转换

使用以下命令格式执行转换：

```powershell
$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8
echo '<curl命令>' | npx curlconverter --language <语言> -
```

**注意事项：**
- cURL 命令中的引号需要正确转义
- 末尾的 `-` 表示从标准输入读取
- 如果命令较复杂（含多层引号、特殊字符），将 cURL 命令写入临时文件再传入：
  ```powershell
  $tmpFile = New-TemporaryFile
  Set-Content -Path $tmpFile -Value '<curl命令>' -Encoding UTF8
  npx curlconverter --language <语言> - < $tmpFile
  Remove-Item $tmpFile
  ```

### 4. 输出结果

- **默认行为**：直接在聊天中展示转换后的代码，使用对应语言的代码块格式（如 ```python、```javascript）
- **保存文件**：如果用户要求保存为文件，根据语言选择合适的扩展名（.py、.js、.go 等）保存到当前工作目录

文件扩展名映射：

| 语言 | 扩展名 |
|---|---|
| python | .py |
| javascript | .js |
| node / node-axios / node-got / node-ky / node-request / node-superagent | .js |
| go | .go |
| java / java-okhttp / java-httpurlconnection / java-jsoup | .java |
| php / php-guzzle / php-requests | .php |
| rust | .rs |
| csharp | .cs |
| ruby | .rb |
| kotlin | .kt |
| swift | .swift |
| dart | .dart |
| c | .c |
| r | .R |
| lua | .lua |
| julia | .jl |
| perl | .pl |
| clojure | .clj |
| elixir | .ex |
| ocaml | .ml |
| 其他 | .txt |

### 5. 批量转换

如果用户要求将同一个 cURL 命令转换为多种语言，并行执行多个转换命令，然后将所有结果一起展示。

## 示例交互

**示例 1：基础转换**
> 用户：把这个 curl 转成 python：curl https://api.example.com/users -H 'Authorization: Bearer token123'

执行：`echo "curl https://api.example.com/users -H 'Authorization: Bearer token123'" | npx curlconverter --language python -`

输出转换后的 Python 代码。

**示例 2：指定语言**
> 用户：curl 'https://httpbin.org/post' -d '{"name":"test"}' 转成 go

执行：`echo "curl 'https://httpbin.org/post' -d '{""name"":""test""}' " | npx curlconverter --language go -`

**示例 3：保存文件**
> 用户：把这个 curl 转成 JavaScript 并保存为 fetch.js

转换后保存到 `fetch.js` 文件。

## 错误处理

- 如果 cURL 命令格式不正确，提示用户检查命令格式
- 如果 curlconverter 报错，显示错误信息并建议用户检查 cURL 命令语法
- 如果 npx 不在 PATH 中，提示用户需要安装 Node.js
