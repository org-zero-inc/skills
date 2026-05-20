# Skill: pexels-downloader

# Pexels Downloader - Pexels 免费图库图片下载器

从 Pexels 搜索并下载高质量免费图片，无需 API Key。

## 依赖

脚本依赖 `curl_cffi` 库（用于绕过反爬虫机制），需确保已安装：

```bash
pip install curl_cffi
```

## 使用方式

```bash
python <skill-path>/scripts/download_pexels.py <关键词> [-n 数量] [-o 输出目录] [--delay 间隔]
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `keyword` | 是 | 搜索关键词，英文效果最佳 |
| `-n, --count` | 否 | 下载数量，默认 5，最大 50 |
| `-o, --output` | 否 | 保存目录，默认 `./downloaded_images_pexels/<关键词>/` |
| `--delay` | 否 | 下载间隔秒数（默认 0.5） |

注意：Pexels 始终下载原始尺寸图片，不支持尺寸选项。

## 使用示例

下载 5 张猫的图片：
```bash
python scripts/download_pexels.py cat -n 5
```

下载 10 张风景图：
```bash
python scripts/download_pexels.py "mountain landscape" -n 10
```

下载 3 张日落图到指定目录：
```bash
python scripts/download_pexels.py sunset -n 3 -o ./my_photos
```

## 工作流程

1. **解析用户需求**：从用户描述中提取关键词、下载数量、输出目录
2. **构建命令**：根据参数组装 Python 命令并执行
3. **汇报结果**：向用户展示下载结果（成功/失败数量、保存位置、图片归属页链接）

## 注意事项

- 英文关键词搜索效果远优于中文
- 无需 API Key，脚本通过 `curl_cffi` 模拟浏览器访问绕过反爬
- 下载的图片遵循 Pexels License 免费许可协议
- 每张图片的元数据保存在 `_download_metadata.json` 中
- 下载间隔默认 0.5 秒，避免被限流
