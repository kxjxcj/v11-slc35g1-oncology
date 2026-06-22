#!/usr/bin/env python3
"""
D10.1 数据下载脚本
- 多线程并行下载 5 个 scRNA-seq 数据集
- 断点续传 + 进度显示
- 自动重试
"""
import os
import sys
import time
import json
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

OUT_DIR = Path("/Users/chen/.mavis/agents/mavis/workspace/genomics_exploration/17_v8_feature_driven/50_paper_v11_D10_scGen/D10.1_data/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = OUT_DIR.parent / "download_log.json"

# 数据集 URL 配置
# 注: figshare 链接需要完整 User-Agent, 大文件下载 ~ 2-3 MB/s
DATASETS = [
    # 1. Dixit 2016 (GSE90063) - ~2.5GB raw, 已有 figshare h5ad
    {
        "name": "dixit_2016_raw",
        "url": "https://ndownloader.figshare.com/files/34011689",
        "size_estimate_gb": 2.5,
        "source": "figshare (theislab sc-pert)",
        "expected_h5ad_type": "raw counts"
    },
    {
        "name": "dixit_2016_processed",
        "url": "https://ndownloader.figshare.com/files/34014608",
        "size_estimate_gb": 0.5,
        "source": "figshare (theislab sc-pert)",
        "expected_h5ad_type": "processed (normalized)"
    },
    # 2. Norman 2019 (GSE133344) - bonus dataset, also useful
    {
        "name": "norman_2019_raw",
        "url": "https://ndownloader.figshare.com/files/34002548",
        "size_estimate_gb": 0.8,
        "source": "figshare (theislab sc-pert)",
        "expected_h5ad_type": "raw counts"
    },
    {
        "name": "norman_2019_processed",
        "url": "https://ndownloader.figshare.com/files/34027562",
        "size_estimate_gb": 0.3,
        "source": "figshare (theislab sc-pert)",
        "expected_h5ad_type": "processed (normalized)"
    },
]

# Replogle 2022 / Adamson 2016 / Schraivogel 2020 / Belk 2022 - need separate approach
# Will be added after primary downloads succeed

class DownloadTracker:
    def __init__(self):
        self.lock = threading.Lock()
        self.status = {}

    def update(self, name, **kwargs):
        with self.lock:
            if name not in self.status:
                self.status[name] = {"name": name}
            self.status[name].update(kwargs)

    def save(self):
        with open(LOG_FILE, "w") as f:
            json.dump(self.status, f, indent=2)

tracker = DownloadTracker()

def download_with_resume(url, dest_path, name, max_retries=5):
    """下载文件，支持断点续传 + 重试"""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        "Accept": "*/*",
    }

    for attempt in range(1, max_retries + 1):
        try:
            # 获取已下载大小
            existing = 0
            if dest_path.exists():
                existing = dest_path.stat().st_size

            req = urllib.request.Request(url, headers=headers)
            if existing > 0:
                req.add_header("Range", f"bytes={existing}-")

            tracker.update(name, attempt=attempt, status="connecting", existing_mb=existing/1e6)
            with urllib.request.urlopen(req, timeout=60) as resp:
                code = resp.getcode()
                if code not in (200, 206):
                    raise RuntimeError(f"HTTP {code}")

                # 解析 Content-Length / Content-Range
                cl = resp.headers.get("Content-Length")
                cr = resp.headers.get("Content-Range")
                if cr:
                    # bytes START-END/TOTAL
                    total = int(cr.split("/")[-1])
                elif cl:
                    total = int(cl) + existing
                else:
                    total = None

                mode = "ab" if existing > 0 and code == 206 else "wb"

                tracker.update(name, status="downloading", total_mb=total/1e6 if total else None)
                start_time = time.time()
                last_log = start_time

                with open(dest_path, mode) as f:
                    downloaded = existing
                    chunk_size = 1024 * 1024  # 1MB
                    while True:
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        now = time.time()
                        if now - last_log > 30:  # 每 30s 更新
                            elapsed = now - start_time
                            speed = (downloaded - existing) / elapsed / 1e6  # MB/s
                            pct = (downloaded / total * 100) if total else None
                            tracker.update(
                                name, downloaded_mb=downloaded/1e6,
                                speed_mbps=round(speed, 2),
                                pct=round(pct, 1) if pct else None,
                                elapsed_s=round(elapsed)
                            )
                            tracker.save()
                            last_log = now

            # 完成
            final_size = dest_path.stat().st_size
            tracker.update(
                name, status="done", downloaded_mb=final_size/1e6,
                total_mb=final_size/1e6
            )
            tracker.save()
            print(f"  [OK] {name}: {final_size/1e9:.2f} GB downloaded")
            return True

        except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as e:
            print(f"  [RETRY {attempt}/{max_retries}] {name}: {type(e).__name__}: {e}")
            tracker.update(name, status=f"error: {type(e).__name__}", error=str(e)[:200])
            tracker.save()
            if attempt < max_retries:
                wait = 2 ** attempt
                time.sleep(wait)
            else:
                print(f"  [FAIL] {name}: giving up after {max_retries} attempts")
                return False
        except Exception as e:
            print(f"  [FATAL] {name}: {type(e).__name__}: {e}")
            tracker.update(name, status=f"fatal: {type(e).__name__}", error=str(e)[:200])
            tracker.save()
            return False

    return False


def main():
    print("=" * 60)
    print("D10.1 数据下载 - Phase 1 (Dixit + Norman)")
    print("=" * 60)

    # 先串行下载小数据集 (Dixit processed, Norman), 大数据集并行
    # 但同时只跑 2 个并发（避免网络拥堵）
    print(f"\n下载目标目录: {OUT_DIR}")
    print(f"数据集数量: {len(DATASETS)}")
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 用 ThreadPoolExecutor 跑 2 并发
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {}
        for ds in DATASETS:
            dest = OUT_DIR / f"{ds['name']}.h5ad"
            print(f"提交任务: {ds['name']} -> {dest}")
            print(f"  估计大小: {ds['size_estimate_gb']} GB")
            print(f"  来源: {ds['source']}")
            fut = executor.submit(
                download_with_resume, ds["url"], dest, ds["name"]
            )
            futures[fut] = ds["name"]

        completed = 0
        for fut in as_completed(futures):
            name = futures[fut]
            ok = fut.result()
            completed += 1
            print(f"  [{completed}/{len(DATASETS)}] {name}: {'✓' if ok else '✗'}")

    print("\n" + "=" * 60)
    print("Phase 1 完成 (Dixit + Norman)")
    print(f"  状态已保存: {LOG_FILE}")
    print("=" * 60)

    # 打印最终状态
    for ds in DATASETS:
        info = tracker.status.get(ds["name"], {})
        size_mb = info.get("downloaded_mb", 0)
        print(f"  {ds['name']}: {size_mb/1000:.2f} GB - {info.get('status', 'unknown')}")


if __name__ == "__main__":
    main()
