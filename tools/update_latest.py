#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从八个应用各自仓库的 GitHub Releases 拉取最新正式版，写入 data/latest.json。

- 只用 /releases/latest（GitHub 本身会排除草稿和预发布）。
- 只收录安装包：<Repo>-<版本>.dmg 或 <Repo>-<版本>.zip；源码包（-source）和 .sha256 不作为下载主文件。
- 某应用没有合格安装包时 available=false，页面显示「暂不可下载」。
- 用法：GITHUB_TOKEN=... python3 tools/update_latest.py
"""
import json, os, re, sys, urllib.request, urllib.error, plistlib, datetime

sys.path.insert(0, os.path.dirname(__file__))
from content import APPS, OWNER

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "latest.json")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def get(url, raw=False):
    req = urllib.request.Request(url, headers={
        "User-Agent": "gao-apps-updater",
        "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json",
    })
    if TOKEN and "api.github.com" in url:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return data if raw else json.loads(data)


def find_build(app, tag, version, body):
    repo = app["repo"]
    # 1) Info.plist（搞研究 / 搞节奏 / 搞积蓄 / 搞词元）
    if app.get("version_source") == "Info.plist":
        try:
            pl = plistlib.loads(get(f"https://api.github.com/repos/{OWNER}/{repo}/contents/Info.plist?ref={tag}", raw=True))
            if str(pl.get("CFBundleShortVersionString")) == version and pl.get("CFBundleVersion"):
                return str(pl["CFBundleVersion"])
        except Exception as e:
            print(f"  ! {repo} Info.plist: {e}", file=sys.stderr)
    # 2) Release 说明里的「build 13」「构建 14」「build119」
    m = re.search(r"(?:build|构建)\s*(\d+)", body or "", re.I)
    if m:
        return m.group(1)
    # 3) README：「版本 1.16，构建 116」「1.11 / build 12」
    try:
        readme = get(f"https://api.github.com/repos/{OWNER}/{repo}/readme?ref={tag}", raw=True).decode("utf-8", "ignore")
        v = re.escape(version)
        m = re.search(rf"{v}\s*[，,/（(]\s*(?:build|构建)\s*(\d+)", readme, re.I)
        if m:
            return m.group(1)
    except Exception as e:
        print(f"  ! {repo} README: {e}", file=sys.stderr)
    return None


def pick_installer(app, assets):
    pat = re.compile(rf"^{re.escape(app['repo'])}-(\d+(?:\.\d+)*)\.(dmg|zip)$", re.I)
    cands = [a for a in assets if pat.match(a["name"]) and a.get("state", "uploaded") == "uploaded"]
    cands.sort(key=lambda a: (0 if a["name"].lower().endswith(".dmg") else 1))
    return cands[0] if cands else None


def entry(app):
    repo = app["repo"]
    base = {
        "slug": app["slug"], "name": app["name"], "repo": f"{OWNER}/{repo}",
        "releases_url": f"https://github.com/{OWNER}/{repo}/releases",
        "available": False,
    }
    try:
        rel = get(f"https://api.github.com/repos/{OWNER}/{repo}/releases/latest")
    except urllib.error.HTTPError as e:
        print(f"  ! {repo}: no latest release ({e.code})", file=sys.stderr)
        return base
    if rel.get("draft") or rel.get("prerelease"):
        return base
    asset = pick_installer(app, rel.get("assets", []))
    if not asset:
        return base
    version = re.match(rf"^{re.escape(repo)}-(\d+(?:\.\d+)*)\.", asset["name"], re.I).group(1)
    sha_asset = next((a for a in rel["assets"] if a["name"] == asset["name"] + ".sha256"), None)
    sha256 = None
    if asset.get("digest", "").startswith("sha256:"):
        sha256 = asset["digest"].split(":", 1)[1]
    base.update({
        "available": True,
        "tag": rel["tag_name"],
        "release_name": rel.get("name"),
        "release_url": rel["html_url"],
        "version": version,
        "build": find_build(app, rel["tag_name"], version, rel.get("body", "")),
        "file": asset["name"],
        "format": asset["name"].rsplit(".", 1)[1].lower(),
        "url": asset["browser_download_url"],
        "size": asset["size"],
        "sha256": sha256,
        "sha256_url": sha_asset["browser_download_url"] if sha_asset else None,
        "published_at": rel["published_at"],
    })
    return base


def main():
    old = None
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            old = json.load(f)
    apps = []
    for app in APPS:
        e = entry(app)
        print(f"{app['name']}: {e.get('file', '暂不可下载')} build={e.get('build')}")
        apps.append(e)
    if old and old.get("apps") == apps:
        print("no change")
        return
    data = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "note": "由 tools/update_latest.py 自动生成；每个应用指向其自身仓库最新正式 Release 的安装包。",
        "apps": apps,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("updated", OUT)


if __name__ == "__main__":
    main()
