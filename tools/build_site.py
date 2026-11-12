#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""根据 tools/content.py（文案）和 data/latest.json（版本与安装包）生成静态页面。

用法：python3 tools/build_site.py
GitHub Action 在 latest.json 更新后会重新运行本脚本，使无 JavaScript 时的下载链接也保持最新。
"""
import json, os, sys, datetime, html

sys.path.insert(0, os.path.dirname(__file__))
from content import APPS, OWNER

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LATEST = json.load(open(os.path.join(ROOT, "data", "latest.json"), encoding="utf-8"))
BY = {a["slug"]: a for a in LATEST["apps"]}
SITE = "https://ucaseryff.github.io/gao-apps/"
CN = ["零", "一", "二", "三", "四", "五", "六", "七", "八"]
e = html.escape

ICON = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M10 3v10m0 0l-4-4m4 4l4-4M4 16h12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def day(iso):
    t = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    return t.strftime("%Y-%m-%d")


def mb(n):
    return f"{n / 1e6:.1f} MB"


def vlabel(d):
    return f"V{d['version']}" + (f" · build {d['build']}" if d.get("build") else "")


def dl_slot(d):
    if not d or not d.get("available"):
        return ('<span class="dl-btn is-off" aria-disabled="true">暂不可下载</span>'
                f'<span class="dl-meta"><span>暂无正式安装包</span><a href="{e(d["releases_url"])}">查看发布页</a></span>')
    links = f'<a href="{e(d["release_url"])}">发布说明</a>'
    if d.get("sha256_url"):
        links += f' · <a href="{e(d["sha256_url"])}">SHA-256 校验文件</a>'
    links += f' · <a href="{e(d["releases_url"])}">所有版本</a>'
    build = f' · build {e(d["build"])}' if d.get("build") else ""
    return (f'<a class="dl-btn" href="{e(d["url"])}" download>{ICON}<span>下载 <span class="v">V{e(d["version"])}</span></span></a>'
            f'<span class="dl-meta"><b>{e(d["file"])}</b><span>{mb(d["size"])} · {day(d["published_at"])} 发布{build}</span><span>{links}</span></span>')


def head(title, desc, root, theme_color, page_url):
    return f'''<!doctype html>
<html lang="zh-CN" data-root="{root}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="{theme_color}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{page_url}">
<link rel="canonical" href="{page_url}">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/site.css">
</head>'''


def nav(root, active=None):
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{root}{a["slug"]}/"{cur if a["slug"] == active else ""}>{a["name"]}</a>' for a in APPS)
    return f'''<header class="nav"><div class="wrap">
<a class="brand" href="{root}"><span class="brand-mark">搞</span><span class="brand-text">搞系列</span></a>
<nav class="nav-apps" aria-label="八个应用">{links}</nav>
</div></header>'''


def foot(root):
    return f'''<footer class="foot"><div class="wrap">
<div>搞系列 · 作者 非凡（Feifan Yu） · <a href="https://github.com/{OWNER}">github.com/{OWNER}</a></div>
<nav><a href="{root}">总览</a><a href="https://github.com/{OWNER}/gao-apps">本站源码</a><span>安装包均托管在各应用仓库的 GitHub Releases</span></nav>
</div></footer>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
'''


# ---------- 各应用首屏舞台 ----------
def stage(app):
    s, w = app["slug"], app["stage_words"]
    if s == "yanjiu":
        tags = "".join(f"<span>{x}</span>" for x in w)
        bars = "".join(f'<span style="height:{h}%"></span>' for h in (46, 78, 60, 100, 70, 88, 52))
        return f'<div class="paper"><b>研究档案</b><i></i><i></i><i></i><i></i><i></i><div class="tags">{tags}</div></div><div class="city">{bars}</div>'
    if s == "jiezou":
        tabs = "".join(f"<span>{x}</span>" for x in w)
        return f'<div class="ring r2"></div><div class="ring r1"></div><div class="sun"></div><div class="clock"><b>25:00</b><small>专注中</small></div><div class="tabs">{tabs}</div>'
    if s == "jixu":
        tabs = "".join(f"<span>{x}</span>" for x in w)
        rows = '<div class="row"><i></i><em></em></div>' * 4
        return f'<div class="ledger"><header>{tabs}</header>{rows}<div class="goal">攒钱目标<div></div></div></div><div class="coins"><span></span><span></span><span></span></div>'
    if s == "ciyuan":
        seg = "".join(f"<span>{x}</span>" for x in w)
        bars = "".join(f'<span style="height:{h}%;animation-delay:{i*60}ms"></span>' for i, h in enumerate((34, 52, 41, 70, 58, 86, 64, 92, 48, 75)))
        return f'<div class="seg">{seg}</div><div class="chart">{bars}</div><div class="stream">input · output · cache read · cache write · input · output</div>'
    if s == "jiling":
        meters = "".join(f'<div class="meter">{x}<div style="--w:{p}%"></div></div>' for x, p in zip(w, (62, 48, 22, 35, 54)))
        spark = ('<svg viewBox="0 0 300 70" preserveAspectRatio="none" aria-hidden="true"><polyline fill="none" stroke="#6ef08a" stroke-width="2" '
                 'points="0,52 20,48 40,50 60,30 80,38 100,22 120,34 140,28 160,44 180,18 200,26 220,40 240,24 260,30 280,14 300,22"/></svg>')
        return f'<div class="edge"></div><div class="panel">{spark}{meters}</div>'
    if s == "menhu":
        tiles = "".join(f'<div class="tile"><i></i>{x}</div>' for x in w[:7])
        tiles += '<div class="tile folder"><i><b></b><b></b><b></b><b></b></i>文件夹</div>'
        return f'<div class="rail"></div><div class="grid">{tiles}</div><div class="dots"><b></b><b></b><b></b></div>'
    if s == "wenjian":
        src = ('<span class="k">\\documentclass</span>{article}\n<span class="k">\\begin</span>{document}\n'
               '<span class="k">\\section</span>{引言}\n本文讨论……\n<span class="c">% SyncTeX 双向定位</span>\n'
               '<span class="k">\\begin</span>{equation}\n  <span class="a">E = mc^2</span>\n<span class="k">\\end</span>{equation}\n'
               '<span class="k">\\end</span>{document}')
        return (f'<pre>{src}</pre><div class="page"><h4>论文标题</h4><small>作者</small><b>1 引言</b><i></i><i class="hl"></i><i></i>'
                f'<p class="eq">E = mc²</p><i></i><i style="width:70%"></i></div><span class="sync">⇄ SyncTeX</span>')
    if s == "caozuo":
        keys = "".join(f"<span>{x}</span>" for x in w)
        return f'<div class="screen"><span></span><span></span><span></span></div><div class="palette">搜索操作<kbd>⌥⌘O</kbd></div><div class="keys">{keys}</div>'
    return ""


def mini(app):
    s = app["slug"]
    if s == "yanjiu":
        return '<div class="mini">' + "".join(f'<span style="height:{h}%"></span>' for h in (40, 70, 52, 92, 60)) + "</div>"
    if s == "ciyuan":
        return '<div class="mini">' + "".join(f'<span style="height:{h}%"></span>' for h in (30, 52, 40, 76, 60, 90)) + "</div>"
    if s == "jixu":
        return '<div class="mini">' + "".join(f'<span style="height:{h}%"></span>' for h in (36, 62, 90)) + "</div>"
    if s == "menhu":
        return '<div class="mini">' + "<span></span>" * 8 + "</div>"
    return ""


COLORS = {"yanjiu": "#f5f0e6", "jiezou": "#fff7ee", "jixu": "#f1f0e9", "ciyuan": "#ebe8e3", "jiling": "#0c0d0f",
          "menhu": "#f3f2fd", "wenjian": "#f8f6f0", "caozuo": "#eff4f4"}


def app_page(i, app):
    d = BY.get(app["slug"])
    root = "../"
    url = SITE + app["slug"] + "/"
    title = f"{app['name']} · {app['tagline'].rstrip('。')} | 搞系列"
    feats = "".join(f"<li><h3>{e(t)}</h3><p>{e(p)}</p></li>" for t, p in app["features"])
    notes = "".join(f"<li>{e(n)}</li>" for n in app["notes"])
    stale = not d or not d.get("available") or d.get("version") != app["notes_version"]
    stale_msg = (f'最新版本已更新为 V{e(d["version"])}，更新内容请看 <a href="{e(d["release_url"])}">发布说明</a>。'
                 if d and d.get("available") else "")
    sha_text = f'{d["file"]}\nSHA-256 {d["sha256"]}' if d and d.get("sha256") else ""
    prev_a, next_a = APPS[i - 1], APPS[(i + 1) % len(APPS)]
    fmt = "DMG" if app["kind"] == "dmg" else "ZIP"
    return head(title, app["lede"], root, COLORS[app["slug"]], url) + f'''
<body class="app theme-{app["slug"]}">
{nav(root, app["slug"])}
<main>
<section class="hero"><div class="wrap">
  <div class="hero-text">
    <p class="eyebrow"><span class="idx">{i + 1:02d}</span><span class="bar"></span>搞系列之{CN[i + 1]} · {e(app["role"])}</p>
    <h1 class="title"><img class="icon" src="{root}assets/icons/{app["slug"]}.png" alt="" width="76" height="76">{e(app["name"])}</h1>
    <span class="title-en">{e(app["en"])}</span>
    <p class="tagline">{e(app["tagline"])}</p>
    <p class="lede">{e(app["lede"])}</p>
    <div class="dl" data-app="{app["slug"]}" data-repo="{app["repo"]}" data-dl="{app["slug"]}">
      <div class="dl dl-slot">{dl_slot(d)}</div>
      <p class="dl-req"><span>macOS 14 或更高</span><span>Apple Silicon</span><span>暂无 Intel 版</span><span>{fmt} 安装包</span></p>
    </div>
  </div>
  <div class="stage s-{app["slug"]}" aria-hidden="true">{stage(app)}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head"><h2>能做什么</h2><p>摘自 <a href="https://github.com/{OWNER}/{app["repo"]}#readme">{app["repo"]} README</a></p></div>
  <ul class="features n{len(app["features"])}">{feats}</ul>
</div></section>

<section class="section"><div class="wrap" data-notes-for="{app["slug"]}" data-notes-version="{app["notes_version"]}">
  <div class="sec-head"><h2>V{app["notes_version"]} 更新</h2><p>摘自正式发布说明</p></div>
  <ul class="notes notes-fresh"{" hidden" if stale else ""}>{notes}</ul>
  <p class="notes-stale"{"" if stale else " hidden"}>{stale_msg}</p>
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head"><h2>安装与校验</h2><p>如实说明，不做夸大</p></div>
  <div class="facts">
    <div class="fact"><h3>系统要求</h3><ul><li>macOS 14 或更高版本</li><li>Apple Silicon（M 系列芯片）</li><li>暂未提供 Intel 版本</li></ul></div>
    <div class="fact"><h3>安装</h3><p>{e(app["install"])}</p><p class="muted">如果 macOS 拦截打开，先确认下载来源，再到「系统设置 → 隐私与安全性」允许打开。</p></div>
    <div class="fact"><h3>签名与数据</h3><p>{e(app["signing"])}未上架 App Store。</p><p class="muted">安装包不含任何个人数据。本地数据目录：<code>{e(app["data"])}</code></p><span class="sha" data-sha="{app["slug"]}">{e(sha_text)}</span></div>
  </div>
</div></section>

<div class="wrap"><nav class="pager" aria-label="其他应用">
  <a href="{root}{prev_a["slug"]}/"><small>← 上一个</small><b>{prev_a["name"]}</b></a>
  <a class="next" href="{root}{next_a["slug"]}/"><small>下一个 →</small><b>{next_a["name"]}</b></a>
</nav></div>
</main>
{foot(root)}'''


def index_page():
    root = "./"
    cards = ""
    for i, app in enumerate(APPS):
        d = BY.get(app["slug"])
        ver = f'<span class="ver" data-ver="{app["slug"]}">{e(vlabel(d))}</span>' if d and d.get("available") \
            else f'<span class="ver off" data-ver="{app["slug"]}">暂不可下载</span>'
        cards += f'''<a class="card theme-{app["slug"]}" href="{app["slug"]}/" data-app="{app["slug"]}" data-repo="{app["repo"]}">
  <div class="card-top s-mini-{app["slug"]}"><span class="card-num">{i + 1:02d}</span>{mini(app)}</div><img class="card-icon" src="assets/icons/{app["slug"]}.png" alt="" width="72" height="72" loading="lazy">
  <div class="card-body"><h2>{app["name"]}<small>{e(app["role"])}</small></h2><p>{e(app["tagline"])}</p>
  <div class="card-foot">{ver}<span class="go">了解 →</span></div></div>
</a>'''
    desc = "搞系列：搞研究、搞节奏、搞积蓄、搞词元、搞机灵、搞门户、搞文件、搞操作，八个原生 macOS 应用的介绍与下载。"
    return head("搞系列 · 八个原生 macOS 应用", desc, root, "#f4f2ec", SITE) + f'''
<body class="home">
{nav(root)}
<main>
<section class="home-hero"><div class="wrap">
  <div class="seal" aria-hidden="true">搞</div>
  <div>
    <p class="eyebrow"><span class="idx">GAO SERIES</span><span class="bar"></span>八个应用</p>
    <h1>搞系列</h1>
    <p class="sub">研究、节奏、积蓄、词元、机灵、门户、文件、操作——八个各管一件事的原生 macOS 应用，数据都留在你自己的 Mac 上。</p>
    <ul class="chips"><li>macOS 14 或更高</li><li>Apple Silicon</li><li>源码公开在 GitHub</li><li>安装包不含个人数据</li></ul>
  </div>
</div></section>
<div class="wrap"><div class="cards">{cards}</div></div>
<section class="section"><div class="wrap">
  <div class="sec-head"><h2>下载说明</h2><p>每个应用独立发版</p></div>
  <div class="home-notes facts">
    <div class="fact"><h3>始终最新</h3><p>下载按钮指向各应用仓库最新正式 Release 中的安装包。本站每小时自动核对一次，页面打开时也会再向 GitHub 查询。</p></div>
    <div class="fact"><h3>签名情况</h3><p>安装包使用 Apple Development 签名（搞文件见其页面说明），均未经 Apple 公证，也未上架 App Store。首次打开可能需要在「隐私与安全性」中允许。</p></div>
    <div class="fact"><h3>校验</h3><p>每个安装包旁都附有同名 <code>.sha256</code> 文件，下载后可用 <code>shasum -a 256 -c</code> 核验。</p></div>
  </div>
</div></section>
</main>
{foot(root)}'''


def main():
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_page())
    for i, app in enumerate(APPS):
        p = os.path.join(ROOT, app["slug"])
        os.makedirs(p, exist_ok=True)
        with open(os.path.join(p, "index.html"), "w", encoding="utf-8") as f:
            f.write(app_page(i, app))
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(head("页面不存在 | 搞系列", "页面不存在", "/gao-apps/", "#f4f2ec", SITE) +
                '<body class="home">' + nav("/gao-apps/") +
                '<main><section class="home-hero"><div class="wrap"><div class="seal" aria-hidden="true">搞</div><div><h1>页面不存在</h1>'
                '<p class="sub"><a href="/gao-apps/">回到搞系列总览</a></p></div></div></section></main>' + foot("/gao-apps/"))
    print("built", len(APPS) + 2, "pages")


if __name__ == "__main__":
    main()
