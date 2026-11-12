/* 搞系列
 * 语言切换、校验值复制，以及各应用自己仓库的最新安装包。
 * 1. 页面里已经写好的链接来自 data/latest.json；
 * 2. 再读一次最新的 data/latest.json；
 * 3. 最后向该应用仓库的 releases/latest 查询，有更新的发行版本才替换。
 * 任何一步失败都保留上一步的结果。发行版本号只显示营销版本。 */
(function () {
  "use strict";

  var UI = {};
  try { UI = JSON.parse(document.getElementById("gao-ui").textContent); } catch (err) {}

  function lang() {
    return document.documentElement.lang.indexOf("en") === 0 ? "en" : "zh";
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function bi(pair) {
    if (!pair) return "";
    if (pair.zh === pair.en) return esc(pair.zh);
    return '<span class="t-zh" lang="zh-CN">' + esc(pair.zh) + "</span>"
      + '<span class="t-en" lang="en">' + esc(pair.en) + "</span>";
  }

  function fillText(pair, map) {
    function one(s) {
      return String(s).replace(/\{(\w+)\}/g, function (_, k) {
        return map[k] != null ? String(map[k]) : "";
      });
    }
    return bi({ zh: one(pair.zh), en: one(pair.en) });
  }

  function applyChrome() {
    var l = lang();
    document.querySelectorAll("[data-aria-zh]").forEach(function (el) {
      el.setAttribute("aria-label", el.getAttribute(l === "en" ? "data-aria-en" : "data-aria-zh") || "");
    });
    document.querySelectorAll("[data-set-lang]").forEach(function (btn) {
      var on = btn.getAttribute("data-set-lang") === l;
      btn.setAttribute("aria-checked", on ? "true" : "false");
      btn.tabIndex = on ? 0 : -1;
    });
    var metaEl = document.getElementById("gao-meta");
    if (!metaEl) return;
    try {
      var meta = JSON.parse(metaEl.textContent);
      document.title = meta.title[l];
      var desc = document.querySelector('meta[name="description"]');
      if (desc) desc.setAttribute("content", meta.description[l]);
      var ogt = document.querySelector('meta[property="og:title"]');
      if (ogt) ogt.setAttribute("content", meta.title[l]);
      var ogd = document.querySelector('meta[property="og:description"]');
      if (ogd) ogd.setAttribute("content", meta.description[l]);
    } catch (err) {}
  }

  function setLang(next) {
    var l = next === "en" ? "en" : "zh";
    try { localStorage.setItem("gao-lang", l); } catch (err) {}
    document.documentElement.lang = l === "en" ? "en" : "zh-CN";
    try {
      var url = new URL(location.href);
      url.searchParams.set("lang", l);
      history.replaceState(null, "", url.pathname + url.search + url.hash);
    } catch (err) {}
    applyChrome();
  }

  document.querySelectorAll(".lang").forEach(function (group) {
    var buttons = function () { return [].slice.call(group.querySelectorAll("[data-set-lang]")); };
    group.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-set-lang]");
      if (!btn || !group.contains(btn)) return;
      setLang(btn.getAttribute("data-set-lang"));
    });
    group.addEventListener("keydown", function (e) {
      var btns = buttons();
      if (!btns.length) return;
      var i = btns.indexOf(document.activeElement);
      if (i < 0) i = 0;
      var next = null;
      if (e.key === "ArrowRight" || e.key === "ArrowDown") next = (i + 1) % btns.length;
      else if (e.key === "ArrowLeft" || e.key === "ArrowUp") next = (i - 1 + btns.length) % btns.length;
      else if (e.key === "Home") next = 0;
      else if (e.key === "End") next = btns.length - 1;
      else return;
      e.preventDefault();
      setLang(btns[next].getAttribute("data-set-lang"));
      btns[next].focus();
    });
  });

  applyChrome();

  var currentLink = document.querySelector(".nav-apps a[aria-current]");
  if (currentLink && currentLink.parentElement) {
    var scroller = currentLink.parentElement;
    var left = currentLink.offsetLeft - (scroller.clientWidth - currentLink.offsetWidth) / 2;
    scroller.scrollLeft = Math.max(0, left);
  }

  var live = document.getElementById("copy-status");
  var copyTimer = 0;
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand("copy") ? resolve() : reject(new Error("copy"));
      } catch (err) {
        reject(err);
      }
      ta.remove();
    });
  }
  document.addEventListener("click", function (e) {
    var btn = e.target.closest(".copy");
    if (!btn) return;
    var value = btn.getAttribute("data-copy");
    if (!value) return;
    copyText(value).then(function () {
      document.querySelectorAll(".copy.is-done").forEach(function (el) { el.classList.remove("is-done"); });
      btn.classList.add("is-done");
      if (live && UI.copied) live.textContent = UI.copied[lang()];
      clearTimeout(copyTimer);
      copyTimer = setTimeout(function () { btn.classList.remove("is-done"); }, 1600);
    }, function () {
      if (live && UI.copy_fail) live.textContent = UI.copy_fail[lang()];
    });
  });

  var onpage = document.querySelectorAll(".onpage a[href^='#']");
  if (onpage.length && "IntersectionObserver" in window) {
    var byId = {};
    onpage.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        onpage.forEach(function (a) { a.removeAttribute("aria-current"); });
        var link = byId[entry.target.id];
        if (link) link.setAttribute("aria-current", "true");
      });
    }, { rootMargin: "-20% 0px -60% 0px", threshold: 0.01 });
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) io.observe(el);
    });
  }

  var root = document.documentElement.getAttribute("data-root") || "./";
  var slugs = {};
  document.querySelectorAll("[data-app]").forEach(function (el) {
    slugs[el.getAttribute("data-app")] = el.getAttribute("data-repo");
  });
  if (!Object.keys(slugs).length || !UI.download) return;

  var ICON = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M10 3v10m0 0l-4-4m4 4l4-4M4 16h12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function size(n) { return (n / 1e6).toFixed(1) + " MB"; }
  function day(iso) {
    try {
      return new Intl.DateTimeFormat("en-CA", {
        timeZone: "Asia/Shanghai", year: "numeric", month: "2-digit", day: "2-digit"
      }).format(new Date(iso));
    } catch (err) { return String(iso).slice(0, 10); }
  }
  function newer(a, b) {
    var x = String(a).split("."), y = String(b).split(".");
    for (var i = 0; i < Math.max(x.length, y.length); i++) {
      var p = parseInt(x[i] || 0, 10), q = parseInt(y[i] || 0, 10);
      if (p !== q) return p > q;
    }
    return false;
  }

  function groupHex(value) {
    return esc(value).replace(/([0-9a-f]{8})/gi, "$1<wbr>");
  }

  function copyBtn(value, label) {
    return '<button type="button" class="copy" data-copy="' + esc(value) + '">'
      + '<span class="copy-idle">' + bi(label) + "</span>"
      + '<span class="copy-done">' + bi(UI.copied) + "</span></button>";
  }

  function shaInner(d) {
    if (!d || !d.sha256) return "";
    var actions = copyBtn(d.sha256, UI.copy_sha);
    if (d.sha256_url && d.file) actions += copyBtn("shasum -a 256 -c " + d.file + ".sha256", UI.copy_cmd);
    return '<p class="sha-file">' + esc(d.file) + "</p>"
      + '<p class="sha-hex"><span class="sha-k">SHA-256</span> ' + groupHex(d.sha256) + "</p>"
      + '<div class="sha-actions">' + actions + "</div>";
  }

  var current = {};

  function render(slug, d) {
    current[slug] = d;
    document.querySelectorAll('[data-dl="' + slug + '"]').forEach(function (el) {
      var slot = el.querySelector(".dl-slot");
      if (!slot) return;
      if (!d || !d.available) {
        slot.innerHTML = '<span class="dl-btn is-off" aria-disabled="true">' + bi(UI.unavailable) + "</span>"
          + '<span class="dl-meta"><span>' + bi(UI.no_pkg) + '</span><a href="'
          + esc(d && d.releases_url) + '">' + bi(UI.see_releases) + "</a></span>";
        return;
      }
      var links = '<a href="' + esc(d.release_url) + '">' + bi(UI.release_notes) + "</a>"
        + (d.sha256_url ? ' · <a href="' + esc(d.sha256_url) + '">' + bi(UI.sha_file) + "</a>" : "")
        + ' · <a href="' + esc(d.releases_url) + '">' + bi(UI.all_versions) + "</a>";
      slot.innerHTML = '<a class="dl-btn" href="' + esc(d.url) + '" download>' + ICON
        + "<span>" + bi(UI.download) + ' <span class="v">V' + esc(d.version) + "</span></span></a>"
        + '<span class="dl-meta"><b>' + esc(d.file) + "</b><span>"
        + fillText(UI.meta_line, { size: size(d.size), date: day(d.published_at) })
        + "</span><span>" + links + "</span></span>";
    });
    document.querySelectorAll('[data-ver="' + slug + '"]').forEach(function (el) {
      if (d && d.available) {
        el.textContent = "V" + d.version;
        el.classList.remove("off");
      } else {
        el.innerHTML = bi(UI.unavailable);
        el.classList.add("off");
      }
    });
    document.querySelectorAll('[data-sha="' + slug + '"]').forEach(function (el) {
      el.innerHTML = shaInner(d);
    });
    document.querySelectorAll('[data-notes-for="' + slug + '"]').forEach(function (el) {
      var fresh = el.querySelector(".notes-fresh");
      var stale = el.querySelector(".notes-stale");
      if (!fresh || !stale) return;
      var mismatch = !d || !d.available || d.version !== el.getAttribute("data-notes-version");
      fresh.hidden = mismatch;
      stale.hidden = !mismatch;
      if (mismatch && d && d.available && UI.stale) {
        var linkZh = '<a href="' + esc(d.release_url) + '">' + esc(UI.release_notes.zh) + "</a>";
        var linkEn = '<a href="' + esc(d.release_url) + '">' + esc(UI.release_notes.en) + "</a>";
        function put(template, link) {
          return String(template).replace("{version}", esc(d.version)).replace("{link}", link);
        }
        stale.innerHTML = '<span class="t-zh" lang="zh-CN">' + put(UI.stale.zh, linkZh) + "</span>"
          + '<span class="t-en" lang="en">' + put(UI.stale.en, linkEn) + "</span>";
      }
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
    } catch (err) {}
    return fetch("https://api.github.com/repos/UCASerYff/" + repo + "/releases/latest", {
      headers: { Accept: "application/vnd.github+json" }
    }).then(function (r) {
      if (!r.ok) throw r.status;
      return r.json();
    }).then(function (rel) {
      try { sessionStorage.setItem(key, JSON.stringify({ t: Date.now(), r: rel })); } catch (err) {}
      return rel;
    });
  }

  function refresh(slug) {
    var repo = slugs[slug];
    return fromApi(slug).then(function (rel) {
      if (!rel || rel.draft || rel.prerelease) return;
      var re = new RegExp("^" + repo + "-(\\d+(?:\\.\\d+)*)\\.(dmg|zip)$", "i");
      var list = (rel.assets || []).filter(function (a) { return re.test(a.name); });
      list.sort(function (a, b) {
        return (/\.dmg$/i.test(a.name) ? 0 : 1) - (/\.dmg$/i.test(b.name) ? 0 : 1);
      });
      var asset = list[0];
      if (!asset) return;
      var ver = asset.name.match(re)[1];
      var cur = current[slug];
      if (cur && cur.available && !newer(ver, cur.version)) return;
      var sha = (rel.assets || []).filter(function (x) { return x.name === asset.name + ".sha256"; })[0];
      var digest = asset.digest && asset.digest.indexOf("sha256:") === 0 ? asset.digest.slice(7) : null;
      render(slug, {
        slug: slug,
        available: true,
        version: ver,
        file: asset.name,
        url: asset.browser_download_url,
        size: asset.size,
        published_at: rel.published_at,
        release_url: rel.html_url,
        releases_url: "https://github.com/UCASerYff/" + repo + "/releases",
        sha256: digest,
        sha256_url: sha ? sha.browser_download_url : null
      });
    }).catch(function () {});
  }

  fromJson().then(function () { Object.keys(slugs).forEach(refresh); });
})();
