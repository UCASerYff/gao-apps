#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""根据 tools/content.py、tools/i18n.py 和 data/latest.json 生成静态页面。

用法：python3 tools/build_site.py
GitHub Action 在 latest.json 更新后会重新运行本脚本。
页面同时写出中文和英文，默认显示中文；构建号不写入可见文案。
"""
import json, os, sys, datetime, html, re

sys.path.insert(0, os.path.dirname(__file__))
from content import APPS, OWNER
from i18n import UI, EN, STAGE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LATEST = json.load(open(os.path.join(ROOT, "data", "latest.json"), encoding="utf-8"))
BY = {a["slug"]: a for a in LATEST["apps"]}
SITE = "https://ucaseryff.github.io/gao-apps/"
CN = ["零", "一", "二", "三", "四", "五", "六", "七", "八"]
e = html.escape

ICON = (
    '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true">'
    '<path d="M10 3v10m0 0l-4-4m4 4l4-4M4 16h12" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

EARLY = r"""<script>
(function(){
  var l="zh";
  try{
    var q=(new URLSearchParams(location.search).get("lang")||"").toLowerCase();
    var s=localStorage.getItem("gao-lang");
    if(q==="en"||q==="zh"){l=q;localStorage.setItem("gao-lang",q);}
    else if(s==="en")l="en";
  }catch(err){}
  document.documentElement.lang=l==="en"?"en":"zh-CN";
  try{
    var m=JSON.parse(document.getElementById("gao-meta").textContent);
    if(l==="en"){
      document.title=m.title.en;
      var d=document.querySelector('meta[name="description"]');
      if(d)d.setAttribute("content",m.description.en);
      var t=document.querySelector('meta[property="og:title"]');
      if(t)t.setAttribute("content",m.title.en);
      var g=document.querySelector('meta[property="og:description"]');
      if(g)g.setAttribute("content",m.description.en);
    }
  }catch(err){}
})();
</script>
<style>html:not([lang="en"]) .t-en{display:none!important}html[lang="en"] .t-zh{display:none!important}</style>
"""


def check_translations():
    need = ("role", "tagline", "lede", "install", "signing", "features", "notes", "words")
    for app in APPS:
        tr = EN.get(app["slug"])
        if not tr:
            raise SystemExit(f"missing English for {app['slug']}")
        for key in need:
            if key not in tr:
                raise SystemExit(f"missing en {app['slug']}.{key}")
        if len(tr["features"]) != len(app["features"]):
            raise SystemExit(f"feature count mismatch: {app['slug']}")
        if len(tr["notes"]) != len(app["notes"]):
            raise SystemExit(f"notes count mismatch: {app['slug']}")
        if len(tr["words"]) != len(app["stage_words"]):
            raise SystemExit(f"stage word count mismatch: {app['slug']}")
        for key in ("tagline", "lede", "install", "signing", "role"):
            if not str(tr[key]).strip():
                raise SystemExit(f"empty en {app['slug']}.{key}")


def day(iso):
    t = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(
        datetime.timezone(datetime.timedelta(hours=8))
    )
    return t.strftime("%Y-%m-%d")


def mb(n):
    return f"{n / 1e6:.1f} MB"


def script_json(obj):
    return json.dumps(obj, ensure_ascii=False).replace("<", "\\u003c")


def T(zh, en=None):
    """一段可见文案的中英对照。两边相同则只输出一次。"""
    if isinstance(zh, dict):
        zh, en = zh["zh"], zh["en"]
    if zh == en:
        return e(zh)
    return (
        f'<span class="t-zh" lang="zh-CN">{e(zh)}</span>'
        f'<span class="t-en" lang="en">{e(en)}</span>'
    )


def TH(pair):
    """i18n.py 里手写的可信 HTML（含 code），不再转义。"""
    if pair["zh"] == pair["en"]:
        return pair["zh"]
    return (
        f'<span class="t-zh" lang="zh-CN">{pair["zh"]}</span>'
        f'<span class="t-en" lang="en">{pair["en"]}</span>'
    )


def fill_pair(pair, **kw):
    return T(pair["zh"].format(**kw), pair["en"].format(**kw))


def soft_path(path):
    return e(path).replace("/", "/<wbr>")


def soft_hex(value):
    return "<wbr>".join(e(value[i:i + 8]) for i in range(0, len(value), 8))


def copy_button(value, label):
    return (
        f'<button type="button" class="copy" data-copy="{e(value)}">'
        f'<span class="copy-idle">{T(label)}</span>'
        f'<span class="copy-done">{T(UI["copied"])}</span>'
        f"</button>"
    )


def sha_block(d):
    if not d or not d.get("available") or not d.get("sha256"):
        return ""
    cmd = ""
    if d.get("sha256_url") and d.get("file"):
        cmd = copy_button(f"shasum -a 256 -c {d['file']}.sha256", UI["copy_cmd"])
    return (
        f'<p class="sha-file">{e(d["file"])}</p>'
        f'<p class="sha-hex"><span class="sha-k">SHA-256</span> {soft_hex(d["sha256"])}</p>'
        f'<div class="sha-actions">{copy_button(d["sha256"], UI["copy_sha"])}{cmd}</div>'
    )


def meta_line(d):
    size, date = mb(d["size"]), day(d["published_at"])
    return T(
        UI["meta_line"]["zh"].format(size=size, date=date),
        UI["meta_line"]["en"].format(size=size, date=date),
    )


def dl_slot(d):
    if not d or not d.get("available"):
        rel = e((d or {}).get("releases_url") or "#")
        return (
            f'<span class="dl-btn is-off" aria-disabled="true">{T(UI["unavailable"])}</span>'
            f'<span class="dl-meta"><span>{T(UI["no_pkg"])}</span>'
            f'<a href="{rel}">{T(UI["see_releases"])}</a></span>'
        )
    links = f'<a href="{e(d["release_url"])}">{T(UI["release_notes"])}</a>'
    if d.get("sha256_url"):
        links += f' · <a href="{e(d["sha256_url"])}">{T(UI["sha_file"])}</a>'
    links += f' · <a href="{e(d["releases_url"])}">{T(UI["all_versions"])}</a>'
    return (
        f'<a class="dl-btn" href="{e(d["url"])}" download>{ICON}'
        f'<span>{T(UI["download"])} <span class="v">V{e(d["version"])}</span></span></a>'
        f'<span class="dl-meta"><b>{e(d["file"])}</b><span>{meta_line(d)}</span>'
        f"<span>{links}</span></span>"
    )


def head(title, desc, root, theme_color, page_url):
    title_j = script_json(title)
    desc_j = script_json(desc)
    ui_j = script_json(UI)
    return f"""<!doctype html>
<html lang="zh-CN" translate="no" data-root="{root}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title["zh"])}</title>
<meta name="description" content="{e(desc["zh"])}">
<meta name="theme-color" content="{theme_color}">
<meta property="og:title" content="{e(title["zh"])}">
<meta property="og:description" content="{e(desc["zh"])}">
<meta property="og:type" content="website">
<meta property="og:url" content="{page_url}">
<link rel="canonical" href="{page_url}">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/site.css">
<script type="application/json" id="gao-meta">{{"title":{title_j},"description":{desc_j}}}</script>
<script type="application/json" id="gao-ui">{ui_j}</script>
{EARLY}</head>"""


def nav(root, active=None):
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{root}{a["slug"]}/"{cur if a["slug"] == active else ""}>{e(a["name"])}</a>'
        for a in APPS
    )
    return f"""<a class="skip" href="#content">{T(UI["skip"])}</a>
<header class="nav"><div class="wrap">
<a class="brand" href="{root}"><span class="brand-mark">搞</span><span class="brand-text">搞系列</span></a>
<nav class="nav-apps" aria-label="{e(UI["apps_nav"]["zh"])}" data-aria-zh="{e(UI["apps_nav"]["zh"])}" data-aria-en="{e(UI["apps_nav"]["en"])}">{links}</nav>
<div class="lang" role="radiogroup" aria-label="{e(UI["lang_label"]["zh"])}" data-aria-zh="{e(UI["lang_label"]["zh"])}" data-aria-en="{e(UI["lang_label"]["en"])}">
<button type="button" role="radio" data-set-lang="zh" aria-checked="true" tabindex="0">中文</button>
<button type="button" role="radio" data-set-lang="en" aria-checked="false" tabindex="-1">EN</button>
</div>
</div></header>"""


def foot(root):
    return f"""<footer class="foot"><div class="wrap">
<div>{T(UI["credit"])} · <a href="https://github.com/{OWNER}">github.com/{OWNER}</a></div>
<nav aria-label="{e(UI["overview"]["zh"])}" data-aria-zh="{e(UI["overview"]["zh"])}" data-aria-en="{e(UI["overview"]["en"])}"><a href="{root}">{T(UI["overview"])}</a><a href="https://github.com/{OWNER}/gao-apps">{T(UI["source"])}</a><span>{T(UI["hosted"])}</span></nav>
</div></footer>
<p class="sr" id="copy-status" aria-live="polite"></p>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
"""


def words(app, tr):
    out = []
    for i, zh in enumerate(app["stage_words"]):
        out.append(f"<span>{T(zh, tr['words'][i])}</span>")
    return "".join(out)


def stage(app, tr):
    s = app["slug"]
    w = words(app, tr)
    st = STAGE.get(s, {})
    if s == "yanjiu":
        bars = "".join(f'<span style="height:{h}%"></span>' for h in (46, 78, 60, 100, 70, 88, 52))
        return (
            f'<div class="paper"><b>{T(st["archive"])}</b><i></i><i></i><i></i><i></i><i></i>'
            f'<div class="tags">{w}</div></div><div class="city">{bars}</div>'
        )
    if s == "jiezou":
        return (
            f'<div class="ring r2"></div><div class="ring r1"></div><div class="sun"></div>'
            f'<div class="clock"><b>25:00</b><small>{T(st["focusing"])}</small></div>'
            f'<div class="tabs">{w}</div>'
        )
    if s == "jixu":
        rows = '<div class="row"><i></i><em></em></div>' * 4
        return (
            f'<div class="ledger"><header>{w}</header>{rows}'
            f'<div class="goal">{T(st["goal"])}<div></div></div></div>'
            f'<div class="coins"><span></span><span></span><span></span></div>'
        )
    if s == "ciyuan":
        bars = "".join(
            f'<span style="height:{h}%;animation-delay:{i * 60}ms"></span>'
            for i, h in enumerate((34, 52, 41, 70, 58, 86, 64, 92, 48, 75))
        )
        return (
            f'<div class="seg">{w}</div><div class="chart">{bars}</div>'
            f'<div class="stream">input · output · cache read · cache write · input · output</div>'
        )
    if s == "jiling":
        meters = "".join(
            f'<div class="meter">{lab}<div style="--w:{p}%"></div></div>'
            for lab, p in zip(
                [T(zh, en) for zh, en in zip(app["stage_words"], tr["words"])],
                (62, 48, 22, 35, 54),
            )
        )
        spark = (
            '<svg viewBox="0 0 300 70" preserveAspectRatio="none" aria-hidden="true">'
            '<polyline fill="none" stroke="#6ef08a" stroke-width="2" '
            'points="0,52 20,48 40,50 60,30 80,38 100,22 120,34 140,28 160,44 180,18 200,26 220,40 240,24 260,30 280,14 300,22"/>'
            "</svg>"
        )
        return f'<div class="edge"></div><div class="panel">{spark}{meters}</div>'
    if s == "menhu":
        tiles = "".join(
            f'<div class="tile"><i></i>{T(zh, en)}</div>'
            for zh, en in list(zip(app["stage_words"], tr["words"]))[:7]
        )
        tiles += f'<div class="tile folder"><i><b></b><b></b><b></b><b></b></i>{T(st["folder"])}</div>'
        return f'<div class="rail"></div><div class="grid">{tiles}</div><div class="dots"><b></b><b></b><b></b></div>'
    if s == "wenjian":
        src = (
            '<span class="k">\\documentclass</span>{article}\n'
            '<span class="k">\\begin</span>{document}\n'
            f'<span class="k">\\section</span>{{{T(st["section"])}}}\n'
            f'{T(st["body"])}\n'
            f'<span class="c">{T(st["comment"])}</span>\n'
            '<span class="k">\\begin</span>{equation}\n'
            '  <span class="a">E = mc^2</span>\n'
            '<span class="k">\\end</span>{equation}\n'
            '<span class="k">\\end</span>{document}'
        )
        return (
            f"<pre>{src}</pre><div class=\"page\"><h4>{T(st['title'])}</h4>"
            f"<small>{T(st['author'])}</small><b>{T(st['heading'])}</b>"
            f'<i></i><i class="hl"></i><i></i><p class="eq">E = mc²</p><i></i><i style="width:70%"></i></div>'
            f'<span class="sync">⇄ SyncTeX</span>'
        )
    if s == "caozuo":
        return (
            f'<div class="screen"><span></span><span></span><span></span></div>'
            f'<div class="palette">{T(st["search"])}<kbd>⌥⌘O</kbd></div>'
            f'<div class="keys">{w}</div>'
        )
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


COLORS = {
    "yanjiu": "#f5f0e6",
    "jiezou": "#fff7ee",
    "jixu": "#f1f0e9",
    "ciyuan": "#ebe8e3",
    "jiling": "#0c0d0f",
    "menhu": "#f3f2fd",
    "wenjian": "#f8f6f0",
    "caozuo": "#eff4f4",
}


def strip_end(text):
    return text.rstrip("。.")


def app_page(i, app):
    d = BY.get(app["slug"])
    tr = EN[app["slug"]]
    root = "../"
    url = SITE + app["slug"] + "/"
    title = {
        "zh": f"{app['name']} · {strip_end(app['tagline'])} | 搞系列",
        "en": f"{app['name']} · {strip_end(tr['tagline'])} | 搞系列",
    }
    desc = {"zh": app["lede"], "en": tr["lede"]}
    feats = "".join(
        f"<li><h3>{T(zt, et)}</h3><p>{T(zp, ep)}</p></li>"
        for (zt, zp), (et, ep) in zip(app["features"], tr["features"])
    )
    notes = "".join(f"<li>{T(z, en)}</li>" for z, en in zip(app["notes"], tr["notes"]))
    stale = not d or not d.get("available") or d.get("version") != app["notes_version"]
    if d and d.get("available"):
        link_zh = f'<a href="{e(d["release_url"])}">{e(UI["release_notes"]["zh"])}</a>'
        link_en = f'<a href="{e(d["release_url"])}">{e(UI["release_notes"]["en"])}</a>'
        stale_msg = (
            f'<span class="t-zh" lang="zh-CN">{UI["stale"]["zh"].format(version=e(d["version"]), link=link_zh)}</span>'
            f'<span class="t-en" lang="en">{UI["stale"]["en"].format(version=e(d["version"]), link=link_en)}</span>'
        )
    else:
        stale_msg = ""
    prev_a, next_a = APPS[i - 1], APPS[(i + 1) % len(APPS)]
    fmt = UI["dmg_pkg"] if app["kind"] == "dmg" else UI["zip_pkg"]
    n = i + 1
    series = T(
        UI["series_line"]["zh"].format(ordinal=CN[n], role=app["role"]),
        UI["series_line"]["en"].format(n=n, role=tr["role"]),
    )
    reqs = (
        f'<span>{T(UI["chip_os"])}</span><span>{T(UI["chip_silicon"])}</span>'
        f'<span>{T(UI["no_intel_short"])}</span><span>{T(fmt)}</span>'
    )
    fresh_hidden = " hidden" if stale else ""
    stale_hidden = "" if stale else " hidden"
    return head(title, desc, root, COLORS[app["slug"]], url) + f"""
<body class="app theme-{app["slug"]}">
{nav(root, app["slug"])}
<main id="content">
<section class="hero"><div class="wrap">
  <div class="hero-text">
    <p class="eyebrow"><span class="idx">{n:02d}</span><span class="bar"></span>{series}</p>
    <h1 class="title"><img class="icon" src="{root}assets/icons/{app["slug"]}.png" alt="" width="76" height="76">{e(app["name"])}</h1>
    <span class="title-en">{e(app["en"])}</span>
    <p class="tagline">{T(app["tagline"], tr["tagline"])}</p>
    <p class="lede">{T(app["lede"], tr["lede"])}</p>
    <div class="dl" data-app="{app["slug"]}" data-repo="{app["repo"]}" data-dl="{app["slug"]}">
      <div class="dl dl-slot">{dl_slot(d)}</div>
      <p class="dl-req">{reqs}</p>
    </div>
  </div>
  <div class="stage s-{app["slug"]}" aria-hidden="true">{stage(app, tr)}</div>
</div></section>
<nav class="onpage" aria-label="{e(UI["on_page"]["zh"])}" data-aria-zh="{e(UI["on_page"]["zh"])}" data-aria-en="{e(UI["on_page"]["en"])}"><div class="wrap">
  <a href="#features">{T(UI["features"])}</a>
  <a href="#notes">{T(UI["nav_changes"])}</a>
  <a href="#install">{T(UI["install_h"])}</a>
</div></nav>
<section class="section" id="features"><div class="wrap">
  <div class="sec-head"><h2><span class="sec-idx">01</span>{T(UI["features"])}</h2><p>{T(UI["from_readme"])} <a href="https://github.com/{OWNER}/{app["repo"]}#readme">{e(app["repo"])} README</a></p></div>
  <ul class="features n{len(app["features"])}">{feats}</ul>
</div></section>
<section class="section" id="notes"><div class="wrap" data-notes-for="{app["slug"]}" data-notes-version="{e(app["notes_version"])}">
  <div class="sec-head"><h2><span class="sec-idx">02</span>{fill_pair(UI["whats_new"], version=app["notes_version"])}</h2><p>{T(UI["from_notes"])}</p></div>
  <ul class="notes notes-fresh"{fresh_hidden}>{notes}</ul>
  <p class="notes-stale"{stale_hidden}>{stale_msg}</p>
</div></section>
<section class="section" id="install"><div class="wrap">
  <div class="sec-head"><h2><span class="sec-idx">03</span>{T(UI["install_h"])}</h2><p>{T(UI["plain"])}</p></div>
  <div class="facts">
    <div class="fact"><h3>{T(UI["requirements"])}</h3><ul><li>{T(UI["req_os"])}</li><li>{T(UI["req_chip"])}</li><li>{T(UI["req_intel"])}</li></ul></div>
    <div class="fact"><h3>{T(UI["install"])}</h3><p>{T(app["install"], tr["install"])}</p><p class="muted">{T(UI["gate"])}</p></div>
    <div class="fact"><h3>{T(UI["sign_data"])}</h3><p>{T(app["signing"], tr["signing"])} {T(UI["not_store"])}</p><p class="muted">{T(UI["no_personal"])}</p><p class="pathrow"><code>{soft_path(app["data"])}</code>{copy_button(app["data"], UI["copy_path"])}</p><div class="sha" data-sha="{app["slug"]}">{sha_block(d)}</div></div>
  </div>
</div></section>
<div class="wrap"><nav class="pager" aria-label="{e(UI["other_apps"]["zh"])}" data-aria-zh="{e(UI["other_apps"]["zh"])}" data-aria-en="{e(UI["other_apps"]["en"])}">
  <a href="{root}{prev_a["slug"]}/"><small>{T(UI["prev"])}</small><b>{e(prev_a["name"])}</b></a>
  <a class="next" href="{root}{next_a["slug"]}/"><small>{T(UI["next"])}</small><b>{e(next_a["name"])}</b></a>
</nav></div>
</main>
{foot(root)}"""


def index_page():
    root = "./"
    cards = ""
    for i, app in enumerate(APPS):
        d = BY.get(app["slug"])
        tr = EN[app["slug"]]
        if d and d.get("available"):
            ver = f'<span class="ver" data-ver="{app["slug"]}">V{e(d["version"])}</span>'
        else:
            ver = f'<span class="ver off" data-ver="{app["slug"]}">{T(UI["unavailable"])}</span>'
        cards += f"""<a class="card theme-{app["slug"]}" href="{app["slug"]}/" data-app="{app["slug"]}" data-repo="{app["repo"]}">
  <div class="card-top s-mini-{app["slug"]}"><span class="card-num">{i + 1:02d}</span>{mini(app)}</div><img class="card-icon" src="assets/icons/{app["slug"]}.png" alt="" width="72" height="72" loading="lazy">
  <div class="card-body"><h2>{e(app["name"])}<small>{T(app["role"], tr["role"])}</small></h2><p>{T(app["tagline"], tr["tagline"])}</p>
  <div class="card-foot">{ver}<span class="go">{T(UI["more"])}</span></div></div>
</a>"""
    chips = "".join(
        f"<li>{T(UI[k])}</li>" for k in ("chip_os", "chip_silicon", "chip_source", "chip_data")
    )
    return head(UI["home_title"], UI["home_desc"], root, "#f4f2ec", SITE) + f"""
<body class="home">
{nav(root)}
<main id="content">
<section class="home-hero"><div class="wrap">
  <div class="seal" aria-hidden="true"><span>搞</span></div>
  <div>
    <p class="eyebrow"><span class="idx">GAO SERIES</span><span class="bar"></span>{T(UI["home_kicker"])}</p>
    <h1>搞系列</h1>
    <p class="sub">{T(UI["home_sub"])}</p>
    <ul class="chips">{chips}</ul>
  </div>
</div></section>
<div class="wrap"><div class="cards">{cards}</div></div>
<section class="section" id="downloads"><div class="wrap">
  <div class="sec-head"><h2>{T(UI["dl_notes"])}</h2><p>{T(UI["each_ships"])}</p></div>
  <div class="home-notes facts">
    <div class="fact"><h3>{T(UI["always"])}</h3><p>{T(UI["always_p"])}</p></div>
    <div class="fact"><h3>{T(UI["signing_h"])}</h3><p>{T(UI["signing_p"])}</p></div>
    <div class="fact"><h3>{T(UI["checksums"])}</h3><p>{TH(UI["checksums_p"])}</p></div>
  </div>
</div></section>
</main>
{foot(root)}"""


def not_found():
    root = "/gao-apps/"
    return head(UI["not_found_title"], UI["not_found_desc"], root, "#f4f2ec", SITE) + (
        '<body class="home">'
        + nav(root)
        + '<main id="content"><section class="home-hero"><div class="wrap">'
        + '<div class="seal" aria-hidden="true"><span>搞</span></div><div>'
        + f'<h1>{T(UI["not_found"])}</h1>'
        + f'<p class="sub"><a href="{root}">{T(UI["back_home"])}</a></p>'
        + "</div></div></section></main>"
        + foot(root)
    )


BUILD_NUM = re.compile(r"(?:build|构建)\s*\d+", re.I)


def assert_pages(paths):
    for path in paths:
        text = open(path, encoding="utf-8").read()
        rel = os.path.relpath(path, ROOT)
        if BUILD_NUM.search(text):
            raise SystemExit(f"version build number visible in {rel}")
        if 'data-set-lang="en"' not in text or 'data-set-lang="zh"' not in text:
            raise SystemExit(f"language toggle missing in {rel}")
        if 'class="t-en"' not in text or 'class="t-zh"' not in text:
            raise SystemExit(f"bilingual copy missing in {rel}")
        if "gao-apps/releases/latest" in text or "/gao-apps/releases" in text:
            raise SystemExit(f"unexpected repo-level release URL in {rel}")


def main():
    check_translations()
    written = []
    index = os.path.join(ROOT, "index.html")
    with open(index, "w", encoding="utf-8") as f:
        f.write(index_page())
    written.append(index)
    for i, app in enumerate(APPS):
        folder = os.path.join(ROOT, app["slug"])
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, "index.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(app_page(i, app))
        written.append(path)
        page = open(path, encoding="utf-8").read()
        d = BY.get(app["slug"])
        if d and d.get("available"):
            if d["url"] not in page:
                raise SystemExit(f"download URL missing on {app['slug']}")
            if f"V{d['version']}" not in page:
                raise SystemExit(f"marketing version missing on {app['slug']}")
            if d.get("sha256") and d["sha256"] not in page:
                raise SystemExit(f"checksum missing on {app['slug']}")
            if d.get("build") and re.search(rf"build\s*{re.escape(str(d['build']))}", page, re.I):
                raise SystemExit(f"build {d['build']} leaked onto {app['slug']}")
    page404 = os.path.join(ROOT, "404.html")
    with open(page404, "w", encoding="utf-8") as f:
        f.write(not_found())
    written.append(page404)
    assert_pages(written)
    print("built", len(APPS) + 2, "pages")


if __name__ == "__main__":
    main()
