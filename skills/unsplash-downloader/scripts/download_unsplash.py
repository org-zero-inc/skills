#!/usr/bin/env python3
"""从 Unsplash 搜索并下载高质量免费图片（无需 API Key，使用 curl_cffi 绕过反爬）。"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse

try:
    from curl_cffi import requests as cffi_requests
except ImportError:
    print("缺少依赖 curl_cffi，请先安装: pip install curl_cffi", file=sys.stderr)
    sys.exit(1)

SIZE_PRESETS = {
    "raw": {"w": None, "q": 100, "fit": "max"},
    "full": {"w": 2400, "q": 95, "fit": "max"},
    "regular": {"w": 1080, "q": 85, "fit": "max"},
    "small": {"w": 400, "q": 80, "fit": "max"},
    "thumb": {"w": 200, "q": 80, "fit": "max"},
}


def sanitize_filename(name, max_length=50):
    name = re.sub(r'[^\w\s-]', '', name).strip()
    name = re.sub(r'[\s]+', '_', name)
    return name[:max_length] if len(name) > max_length else name


def detect_content_type(data):
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return ".png"
    if data[:3] == b'\xff\xd8\xff':
        return ".jpg"
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return ".webp"
    if data[:4] == b'GIF8':
        return ".gif"
    return ".jpg"


def build_unsplash_url(base_url, size="raw"):
    preset = SIZE_PRESETS.get(size, SIZE_PRESETS["raw"])
    params = []
    if preset["w"]:
        params.append(f"w={preset['w']}")
    params.append(f"q={preset['q']}")
    if preset.get("fit"):
        params.append(f"fit={preset['fit']}")
    params.append("auto=format")
    return base_url + "?" + "&".join(params)


def fetch_page(url):
    r = cffi_requests.get(url, impersonate='chrome', timeout=30)
    r.raise_for_status()
    return r.text


def search_unsplash(keyword, count, size="raw"):
    search_url = f"https://unsplash.com/s/photos/{urllib.parse.quote(keyword)}"
    try:
        html = fetch_page(search_url)
    except Exception as e:
        print(f"  Unsplash 搜索失败: {e}", file=sys.stderr)
        return []

    photo_bases = re.findall(
        r'https://images\.unsplash\.com/(photo-\d+-[a-f0-9]+|premium_photo-\d+-[a-f0-9]+)',
        html,
    )
    photo_bases = list(dict.fromkeys(photo_bases))

    photo_links = re.findall(r'href="/photos/([a-zA-Z0-9_-]+)"', html)
    photo_links = list(dict.fromkeys(photo_links))

    photos = []
    for i, base_id in enumerate(photo_bases[:count]):
        base_url = f"https://images.unsplash.com/{base_id}"
        download_url = build_unsplash_url(base_url, size)
        slug = photo_links[i] if i < len(photo_links) else base_id
        photos.append({
            "id": base_id,
            "url": download_url,
            "description": keyword,
            "photographer": "unknown",
            "width": 0,
            "height": 0,
            "source": "unsplash",
            "page_url": f"https://unsplash.com/photos/{slug}",
        })

    return photos


def download_photo(photo, output_dir, index):
    if not photo.get("url"):
        return None

    filename = f"{index + 1:03d}_{sanitize_filename(photo['description'], 30)}_{photo['source']}_{photo['id']}"
    filepath_base = os.path.join(output_dir, filename)

    urls_to_try = [photo["url"]]
    if photo.get("fallback_url") and photo["fallback_url"] != photo["url"]:
        urls_to_try.append(photo["fallback_url"])

    for attempt, url in enumerate(urls_to_try):
        try:
            r = cffi_requests.get(url, impersonate='chrome', timeout=60)
            if r.status_code != 200 or len(r.content) < 500:
                if attempt < len(urls_to_try) - 1:
                    continue
                raise Exception(f"HTTP {r.status_code}")
            data = r.content
            ext = detect_content_type(data)
            filepath = filepath_base + ext
            counter = 1
            while os.path.exists(filepath):
                filepath = f"{filepath_base}_{counter}{ext}"
                counter += 1
            with open(filepath, "wb") as f:
                f.write(data)
            size_kb = len(data) / 1024
            print(f"  -> #{index + 1}: {os.path.basename(filepath)} ({size_kb:.0f} KB) [unsplash]")
            return filepath
        except Exception as e:
            if attempt < len(urls_to_try) - 1:
                continue
            print(f"  !! #{index + 1}: 失败 - {e} [unsplash]", file=sys.stderr)
            return None


def main():
    parser = argparse.ArgumentParser(description="从 Unsplash 搜索并下载高质量免费图片")
    parser.add_argument("keyword", help="搜索关键词")
    parser.add_argument("-n", "--count", type=int, default=5, help="下载数量（默认 5，最大 50）")
    parser.add_argument("-o", "--output", default="", help="保存目录（默认 ./downloaded_images_unsplash/<keyword>）")
    parser.add_argument("--size", choices=["raw", "full", "regular", "small", "thumb"], default="raw", help="图片尺寸（默认 raw）")
    parser.add_argument("--delay", type=float, default=0.5, help="下载间隔秒数（默认 0.5）")
    args = parser.parse_args()

    keyword = args.keyword
    count = min(max(args.count, 1), 50)
    output_dir = args.output or os.path.join(".", "downloaded_images_unsplash", sanitize_filename(keyword))

    os.makedirs(output_dir, exist_ok=True)

    print(f"[search] 关键词: {keyword} | 数量: {count} | 尺寸: {args.size}")
    print(f"[output] {os.path.abspath(output_dir)}")
    print()

    print(f"[unsplash] 搜索 {count} 张...")
    all_photos = search_unsplash(keyword, count, size=args.size)
    print(f"[unsplash] 找到 {len(all_photos)} 张")

    if not all_photos:
        print("[error] 未找到任何图片，请尝试其他关键词。")
        sys.exit(1)

    print(f"\n[download] 开始下载 {len(all_photos)} 张图片...")

    results = {"success": [], "failed": [], "total": len(all_photos)}
    for i, photo in enumerate(all_photos):
        result = download_photo(photo, output_dir, i)
        if result:
            results["success"].append({
                "file": result,
                "source": "unsplash",
                "photographer": photo["photographer"],
                "page_url": photo["page_url"],
            })
        else:
            results["failed"].append(photo)
        if i < len(all_photos) - 1:
            time.sleep(args.delay)

    print(f"\n[done] {len(results['success'])} 成功 / {len(results['failed'])} 失败 / 共 {results['total']} 张")
    if results["success"]:
        print(f"[output] {os.path.abspath(output_dir)}")
        print()
        for item in results["success"]:
            print(f"  - {os.path.basename(item['file'])} (unsplash) {item['page_url']}")

    meta_path = os.path.join(output_dir, "_download_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
