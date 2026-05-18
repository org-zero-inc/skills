---
name: picture-downloader
description: |
  从 Unsplash 和 Pexels 搜索并下载高质量免费图片。支持关键词搜索、指定下载数量、选择平台来源和图片尺寸，无需 API Key。
  当用户提到"下载图片"、"搜索图片"、"下载照片"、"download pictures"、"search photos"、
  "download images"、"找图片"、"下图片"、"图片素材"、"免费图片"、"高清图片"、
  "从unsplash下载"、"从pexels下载"、"下载壁纸"、"下载背景图"、"找几张XX的图"、
  "帮我找图片"、"需要几张图片"等任何涉及从免费图库搜索和下载图片的场景时触发此技能。
  即使用户只是模糊地说"帮我找几张猫的图片"或"我需要一些风景照"，也应触发。
  支持 Unsplash 和 Pexels 两大平台，无需 API Key，默认下载原始尺寸图片。
---

# Picture Downloader - 免费图库图片下载器

从 Unsplash 和 Pexels 搜索并下载高质量免费图片，无需 API Key。

## 依赖

脚本依赖 `curl_cffi` 库（用于绕过反爬虫机制），需确保已安装：

```bash
pip install curl_cffi
```

## 使用方式

```bash
python <skill-path>/scripts/download_pictures.py <关键词> [-n 数量] [-s 来源] [-o 输出目录] [--size 尺寸]
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `keyword` | 是 | 搜索关键词，英文效果最佳 |
| `-n, --count` | 否 | 下载数量，默认 5，最大 50 |
| `-s, --source` | 否 | `unsplash`、`pexels`、`both`（默认 `both`） |
| `-o, --output` | 否 | 保存目录，默认 `./downloaded_images/<关键词>/` |
| `--size` | 否 | Unsplash 图片尺寸（默认 `raw` 原始尺寸） |
| `--delay` | 否 | 下载间隔秒数（默认 0.5） |

### Unsplash 尺寸选项

| 尺寸 | 说明 |
|------|------|
| `raw` | 原始尺寸（默认，最高质量，文件较大） |
| `full` | 2400px 宽，适合桌面壁纸 |
| `regular` | 1080px 宽，适合一般用途 |
| `small` | 400px 宽，适合缩略图 |
| `thumb` | 200px 宽，适合预览 |

注意：`--size` 参数仅影响 Unsplash 图片。Pexels 始终下载原始尺寸。

## 使用示例

下载 5 张猫的图片（默认两个平台各取一半）：
```bash
python scripts/download_pictures.py cat -n 5
```

仅从 Unsplash 下载 10 张原始尺寸风景图：
```bash
python scripts/download_pictures.py "mountain landscape" -n 10 -s unsplash --size raw
```

从 Pexels 下载 3 张日落图到指定目录：
```bash
python scripts/download_pictures.py sunset -n 3 -s pexels -o ./my_photos
```

## 工作流程

1. **解析用户需求**：从用户描述中提取关键词、下载数量、平台偏好、输出目录
2. **构建命令**：根据参数组装 Python 命令并执行
3. **汇报结果**：向用户展示下载结果（成功/失败数量、保存位置、图片归属页链接）

## 注意事项

- 英文关键词搜索效果远优于中文
- 无需 API Key，脚本通过 `curl_cffi` 模拟浏览器访问绕过反爬
- 下载的图片遵循各平台免费许可协议（Unsplash License / Pexels License）
- 每张图片的元数据保存在 `_download_metadata.json` 中
- `raw` 尺寸可能很大（10-20MB），网络较慢时建议使用 `full` 或 `regular`
- 下载间隔默认 0.5 秒，避免被限流
