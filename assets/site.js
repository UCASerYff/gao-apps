/* 搞系列 · 下载入口
 * 1. 先用页面里已经生成好的链接（来自 data/latest.json，构建时写入）；
 * 2. 再读取最新的 data/latest.json（每小时由 GitHub Action 更新）；
 * 3. 最后直接向 GitHub API 查询各仓库 releases/latest，若有更新版本则替换。
 * 任何一步失败都保留上一步的结果；没有安装包时显示「暂不可下载」，不给空链接。 */
(function () {
  "use strict";
  var root = document.documentElement.getAttribute("data-root") || "./";
  var slugs = {};
  document.querySelectorAll("[data-app]").forEach(function (el) {
    slugs[el.getAttribute("data-app")] = el.getAttribute("data-repo");
  });
  if (!Object.keys(slugs).length) return;

  var ICON = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M10 3v10m0 0l-4-4m4 4l4-4M4 16h12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function size(n) { return (n / 1e6).toFixed(1) + " MB"; }
  function day(iso) {
    try { return new Intl.DateTimeFormat("zh-CN", { timeZone: "Asia/Shanghai", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date(iso)).replace(/\//g, "-"); }
    catch (e) { return String(iso).slice(0, 10); }
  }
  function vlabel(d) { return "V" + d.version + (d.build ? " · build " + d.build : ""); }
  function newer(a, b) { // a > b ?
    var x = String(a).split("."), y = String(b).split(".");
    for (var i = 0; i < Math.max(x.length, y.length); i++) {
      var p = parseInt(x[i] || 0, 10), q = parseInt(y[i] || 0, 10);
      if (p !== q) return p > q;
    }
    return false;
  }

  var current = {};

  function render(slug, d) {
    current[slug] = d;
    document.querySelectorAll('[data-dl="' + slug + '"]').forEach(function (el) {
      if (!d || !d.available) {
        el.querySelector(".dl-slot").innerHTML =
          '<span class="dl-btn is-off" aria-disabled="true">暂不可下载</span>' +
          '<span class="dl-meta"><span>暂无正式安装包</span><a href="' + esc(d && d.releases_url) + '">查看发布页</a></span>';
        return;
      }
      el.querySelector(".dl-slot").innerHTML =
        '<a class="dl-btn" href="' + esc(d.url) + '" download>' + ICON + '<span>下载 <span class="v">V' + esc(d.version) + '</span></span></a>' +
        '<span class="dl-meta"><b>' + esc(d.file) + '</b><span>' + size(d.size) + ' · ' + day(d.published_at) + ' 发布' + (d.build ? ' · build ' + esc(d.build) : '') + '</span>' +
        '<span><a href="' + esc(d.release_url) + '">发布说明</a>' + (d.sha256_url ? ' · <a href="' + esc(d.sha256_url) + '">SHA-256 校验文件</a>' : '') + ' · <a href="' + esc(d.releases_url) + '">所有版本</a></span></span>';
    });
    document.querySelectorAll('[data-ver="' + slug + '"]').forEach(function (el) {
      if (d && d.available) { el.textContent = vlabel(d); el.classList.remove("off"); }
      else { el.textContent = "暂不可下载"; el.classList.add("off"); }
    });
    document.querySelectorAll('[data-sha="' + slug + '"]').forEach(function (el) {
      el.textContent = d && d.sha256 ? d.file + "\nSHA-256 " + d.sha256 : "";
    });
    document.querySelectorAll('[data-notes-for="' + slug + '"]').forEach(function (el) {
      var stale = !d || !d.available || d.version !== el.getAttribute("data-notes-version");
      el.querySelector(".notes-fresh").hidden = stale;
      var s = el.querySelector(".notes-stale");
      s.hidden = !stale;
      if (stale && d && d.available) s.innerHTML = '最新版本已更新为 V' + esc(d.version) + '，更新内容请看 <a href="' + esc(d.release_url) + '">发布说明</a>。';
    });
  }

  function fromJson() {
    return fetch(root + "data/latest.json", { cache: "no-cache" }).then(function (r) { return r.json(); }).then(function (j) {
      (j.apps || []).forEach(function (a) { if (a.slug in slugs) render(a.slug, a); });
    }).catch(function () {});
  }

  function fromApi(slug) {
    var repo = slugs[slug];
    var key = "gao-rel-" + repo;
    try {
      var c = JSON.parse(sessionStorage.getItem(key) || "null");
      if (c && Date.now() - c.t < 15 * 60 * 1000) return Promise.resolve(c.r);
    } catch (e) {}
    return fetch("https://api.github.com/repos/UCASerYff/" + repo + "/releases/latest", { headers: { Accept: "application/vnd.github+json" } })
      .then(function (r) { if (!r.ok) throw r.status; return r.json(); })
      .then(function (rel) {
        try { sessionStorage.setItem(key, JSON.stringify({ t: Date.now(), r: rel })); } catch (e) {}
        return rel;
      });
  }

  function refresh(slug) {
    var repo = slugs[slug];
    return fromApi(slug).then(function (rel) {
      if (!rel || rel.draft || rel.prerelease) return;
      var re = new RegExp("^" + repo + "-(\\d+(?:\\.\\d+)*)\\.(dmg|zip)$", "i");
      var list = (rel.assets || []).filter(function (a) { return re.test(a.name); });
      list.sort(function (a, b) { return (/\.dmg$/i.test(a.name) ? 0 : 1) - (/\.dmg$/i.test(b.name) ? 0 : 1); });
      var a = list[0];
      if (!a) return;
      var ver = a.name.match(re)[1];
      var cur = current[slug];
      if (cur && cur.available && !newer(ver, cur.version)) return; // 已是最新
      var sha = (rel.assets || []).filter(function (x) { return x.name === a.name + ".sha256"; })[0];
      render(slug, {
        slug: slug, available: true, version: ver, build: null, file: a.name, url: a.browser_download_url,
        size: a.size, published_at: rel.published_at, release_url: rel.html_url,
        releases_url: "https://github.com/UCASerYff/" + repo + "/releases",
        sha256: a.digest && a.digest.indexOf("sha256:") === 0 ? a.digest.slice(7) : null,
        sha256_url: sha ? sha.browser_download_url : null
      });
    }).catch(function () { /* 失败时保留 latest.json 的结果 */ });
  }

  fromJson().then(function () { Object.keys(slugs).forEach(refresh); });
})();
