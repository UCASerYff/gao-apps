# -*- coding: utf-8 -*-
"""界面文案与英文译文。

中文产品事实以 tools/content.py 为准。这里的英文只翻译已经写在页面上的句子，
不新增功能、口号、版本或系统要求。改完后运行 python3 tools/build_site.py。
"""


def S(zh, en):
    return {"zh": zh, "en": en}


# 导航、页脚、下载块、首页说明等共用句子。
UI = {
    "skip": S("跳到正文", "Skip to content"),
    "apps_nav": S("八个应用", "Eight apps"),
    "lang_label": S("语言", "Language"),
    "overview": S("总览", "Overview"),
    "source": S("本站源码", "Site source"),
    "hosted": S(
        "安装包均托管在各应用仓库的 GitHub Releases",
        "Installers are hosted on each app’s GitHub Releases",
    ),
    "credit": S(
        "搞系列 · 作者 非凡（Feifan Yu）",
        "搞系列 · Author 非凡 (Feifan Yu)",
    ),
    "not_found": S("页面不存在", "Page not found"),
    "not_found_title": S("页面不存在 | 搞系列", "Page not found | 搞系列"),
    "not_found_desc": S("页面不存在", "Page not found"),
    "back_home": S("回到搞系列总览", "Back to the 搞系列 overview"),
    "home_title": S(
        "搞系列 · 八个原生 macOS 应用",
        "搞系列 · Eight native macOS apps",
    ),
    "home_desc": S(
        "搞系列：搞研究、搞节奏、搞积蓄、搞词元、搞机灵、搞门户、搞文件、搞操作，八个原生 macOS 应用的介绍与下载。",
        "搞系列: 搞研究, 搞节奏, 搞积蓄, 搞词元, 搞机灵, 搞门户, 搞文件, and 搞操作 — introductions and downloads for eight native macOS apps.",
    ),
    "home_kicker": S("八个应用", "Eight apps"),
    "home_sub": S(
        "研究、节奏、积蓄、词元、机灵、门户、文件、操作——八个各管一件事的原生 macOS 应用，数据都留在你自己的 Mac 上。",
        "Research, rhythm, savings, tokens, alertness, portals, files, and actions — eight native macOS apps, each responsible for one thing, with data kept on your own Mac.",
    ),
    "chip_os": S("macOS 14 或更高", "macOS 14 or later"),
    "chip_silicon": S("Apple Silicon", "Apple Silicon"),
    "chip_source": S("源码公开在 GitHub", "Source is public on GitHub"),
    "chip_data": S("安装包不含个人数据", "Installers contain no personal data"),
    "more": S("了解 →", "Details →"),
    "unavailable": S("暂不可下载", "Not available"),
    "no_pkg": S("暂无正式安装包", "No stable installer yet"),
    "see_releases": S("查看发布页", "View releases"),
    "download": S("下载", "Download"),
    "release_notes": S("发布说明", "Release notes"),
    "sha_file": S("SHA-256 校验文件", "SHA-256 file"),
    "all_versions": S("所有版本", "All versions"),
    "meta_line": S("{size} · {date} 发布", "{size} · Released {date}"),
    "no_intel_short": S("暂无 Intel 版", "No Intel version"),
    "zip_pkg": S("ZIP 安装包", "ZIP installer"),
    "dmg_pkg": S("DMG 安装包", "DMG installer"),
    "features": S("能做什么", "What it does"),
    "from_readme": S("摘自", "From the"),
    "whats_new": S("V{version} 更新", "What's new in V{version}"),
    "from_notes": S("摘自正式发布说明", "From the stable release notes"),
    "stale": S(
        "最新版本已更新为 V{version}，更新内容请看 {link}。",
        "The latest version is now V{version}. See the {link} for what changed.",
    ),
    "install_h": S("安装与校验", "Install and verify"),
    "plain": S("如实说明，不做夸大", "As stated, without embellishment"),
    "requirements": S("系统要求", "Requirements"),
    "req_os": S("macOS 14 或更高版本", "macOS 14 or later"),
    "req_chip": S("Apple Silicon（M 系列芯片）", "Apple Silicon (M-series)"),
    "req_intel": S("暂未提供 Intel 版本", "No Intel version is offered"),
    "install": S("安装", "Install"),
    "gate": S(
        "如果 macOS 拦截打开，先确认下载来源，再到「系统设置 → 隐私与安全性」允许打开。",
        "If macOS blocks the app, confirm the download source, then allow it in System Settings → Privacy & Security.",
    ),
    "sign_data": S("签名与数据", "Signing and data"),
    "not_store": S("未上架 App Store。", "Not listed on the App Store."),
    "no_personal": S(
        "安装包不含任何个人数据。本地数据目录：",
        "The installer contains no personal data. Local data directory:",
    ),
    "prev": S("← 上一个", "← Previous"),
    "next": S("下一个 →", "Next →"),
    "other_apps": S("其他应用", "Other apps"),
    "on_page": S("本页", "On this page"),
    "nav_changes": S("更新", "Changes"),
    "dl_notes": S("下载说明", "About downloads"),
    "each_ships": S("每个应用独立发版", "Each app ships on its own"),
    "always": S("始终最新", "Always current"),
    "always_p": S(
        "下载按钮指向各应用仓库最新正式 Release 中的安装包。本站每小时自动核对一次，页面打开时也会再向 GitHub 查询。",
        "Each download button points to the installer in that app’s own latest stable Release. This site checks once an hour, and asks GitHub again when the page opens.",
    ),
    "signing_h": S("签名情况", "Signing"),
    "signing_p": S(
        "安装包使用 Apple Development 签名（搞文件见其页面说明），均未经 Apple 公证，也未上架 App Store。首次打开可能需要在「隐私与安全性」中允许。",
        "Installers are signed with Apple Development (搞文件 explains its own wording on its page). None are notarized by Apple or listed on the App Store. The first open may need to be allowed under Privacy & Security.",
    ),
    "checksums": S("校验", "Checksums"),
    "checksums_p": S(
        "每个安装包旁都附有同名 <code>.sha256</code> 文件，下载后可用 <code>shasum -a 256 -c</code> 核验。",
        "Each installer is accompanied by a <code>.sha256</code> file of the same name. After downloading, verify with <code>shasum -a 256 -c</code>.",
    ),
    "copy_sha": S("复制 SHA-256", "Copy SHA-256"),
    "copy_path": S("复制路径", "Copy path"),
    "copy_cmd": S("复制校验命令", "Copy verify command"),
    "copied": S("已复制", "Copied"),
    "copy_fail": S("未能复制", "Couldn’t copy"),
    "series_line": S("搞系列之{ordinal} · {role}", "No. {n} in 搞系列 · {role}"),
}


# 舞台里的短字，中英都写在这里（content.py 的 stage_words 仍是中文词表）。
STAGE = {
    "yanjiu": {"archive": S("研究档案", "Research archive")},
    "jiezou": {"focusing": S("专注中", "Focusing")},
    "jixu": {"goal": S("攒钱目标", "Savings goal")},
    "menhu": {"folder": S("文件夹", "Folder")},
    "wenjian": {
        "section": S("引言", "Introduction"),
        "body": S("本文讨论……", "This paper discusses…"),
        "title": S("论文标题", "Paper title"),
        "author": S("作者", "Author"),
        "heading": S("1 引言", "1 Introduction"),
        "comment": S("% SyncTeX 双向定位", "% two-way SyncTeX"),
    },
    "caozuo": {"search": S("搜索操作", "Search actions")},
}


# 各应用正文的英文。键与 tools/content.py 里的中文一一对应。
EN = {
    "yanjiu": {
        "role": "Research output",
        "tagline": "Papers, results, and submissions, kept in one academic studio.",
        "lede": "A standalone macOS app with this module’s full workflow, a game scene, and WidgetKit widgets. It runs without the other 搞系列 apps; linked features need the related apps installed as well.",
        "features": [
            ("Papers and results", "Manage papers, results, certificates, and submission status. Status updates and Archived are tabs inside submission tracking. Research funding is now managed in 搞积蓄."),
            ("Research attachments", "Save and open research attachments such as PDFs, and view journal metrics. Attachments live in the app’s own data directory."),
            ("A floating 3D research city", "Buildings and expansions follow research progress, so the work shows up on the city."),
            ("Settings and widgets", "Open Settings from the menu or with ⌘,. It includes appearance, module settings, and an entry to the local data directory, plus Desktop and Notification Center widgets."),
        ],
        "notes": [
            "The project-management section and project reminders are removed. Historical project records and Trash data are kept.",
            "Fixes the height, category axis, count labels, and narrow-window layout of the result-category chart.",
            "Daily automatic backups, manual full backups, migration backups, and upgrade snapshots are no longer created.",
        ],
        "install": "Unzip and drag 搞研究.app into the Applications folder. Launch it once, then add widgets from the system widget list.",
        "signing": "Signed with Apple Development. Not notarized by Apple.",
        "words": ["Papers", "Results", "Certificates", "Submissions", "Journal metrics"],
    },
    "jiezou": {
        "role": "Focus and daily rhythm",
        "tagline": "Focus, sleep, and habits, arranged to the rhythm of a day.",
        "lede": "A standalone macOS app with focus, sleep, habits, health, footprints, a game scene, and WidgetKit widgets.",
        "features": [
            ("Five workspaces", "Today, Rhythm, Health, Footprints, and Park. Older notifications and deep links still open the original features."),
            ("Focus and routine", "Focus timer, manual sleep, habits, chores, goals, and statistics, recorded in one unified lightweight card window."),
            ("Health records", "Today, all records, statistical trends, and quick items. All records can be filtered by type and time, and searched."),
            ("Focus in the background", "After the window closes, focus continues in the background. Click the Dock icon or press ⌘0 to open it again. ⌘Q saves, pauses, and quits."),
            ("Park", "The farm, pasture, fishing, field guide, deserted island, and travel train all live in Park."),
            ("Widgets", "Desktop and Notification Center widgets for this app."),
        ],
        "notes": [
            "Fixes a slight jump at the top when switching the Footprints module.",
            "Tightens vertical spacing on the map page so the five modules line up at the top.",
            "All records, estate progress, settings, and widgets are kept.",
        ],
        "install": "Unzip and drag 搞节奏.app into the Applications folder. Launch it once, then add widgets from the system widget list.",
        "signing": "Signed with Apple Development. Not notarized by Apple.",
        "words": ["Today", "Rhythm", "Health", "Footprints", "Park"],
    },
    "jixu": {
        "role": "Bookkeeping and saving",
        "tagline": "Every transaction is recorded, and every savings goal is visible.",
        "lede": "A standalone macOS bookkeeping and savings app, with a personal ledger, recurring cash flow, savings goals, a hero adventure, and Desktop widgets.",
        "features": [
            ("Four workspaces", "Overview, Cash flow, Savings, and Adventure. Transactions and savings records are grouped by date."),
            ("Daily ledger", "Everyday entries, asset accounts, balance adjustments, transfers, budgets, income and expense reports, and recurring entries."),
            ("Recurring cash flow", "Recurring income only creates a forecast, and is posted after the money actually arrives. Recurring expenses and benefits manage subscriptions, payment history, and reminders."),
            ("Savings goals", "Savings goals and savings records. A confirmed recurring expense can be recorded as spending, and the same payment number is never posted twice."),
            ("Hero adventure", "Equipment, skills, pets, wishes, and achievements. Game resources are stored separately from real financial records."),
            ("Widgets", "Open Settings from the menu or with ⌘,. Desktop and Notification Center widgets are included."),
        ],
        "notes": [
            "The research module and research-only materials are fully removed.",
            "Personal accounts, recurring cash flow, the game, and widgets are kept.",
            "The top workspace is Overview, Cash flow, Savings, and Adventure.",
        ],
        "install": "Unzip and drag 搞积蓄.app into the Applications folder. Launch it once, then add widgets from the system widget list.",
        "signing": "Signed with Apple Development. Not notarized by Apple.",
        "words": ["Overview", "Cash flow", "Savings", "Adventure"],
    },
    "ciyuan": {
        "role": "Agent usage",
        "tagline": "Quotas and token use for Agent apps, clear on one page.",
        "lede": "A standalone macOS app for Agent-app quotas and usage, with a compact overview, Agent-app management, usage analysis, platform connections, and a floating panel. Reading third-party data requires that software and an existing login on this Mac.",
        "features": [
            ("Four compact pages", "Overview, Agent apps, Usage analysis, and Platform connections. Supports dynamic light and dark appearance, and a floating panel."),
            ("Agent apps only", "Manage real quotas, billing connections, and local usage for Agent apps. New large-model API or custom API balance accounts are no longer added."),
            ("Usage analysis", "View token use by tool, model, time, and other dimensions, and check duplicate logs and records from more than one source."),
            ("Tokscale scan engine", "Includes the Tokscale scan engine and local revisions. The version and source patches are public in the repository."),
            ("Export", "Settings offer appearance, data sources, and export to CSV or usage JSON. Desktop and Notification Center widgets are no longer provided."),
        ],
        "notes": [
            "A new compact four-page interface: Overview, Agent apps, Usage analysis, and Platform connections.",
            "The platform model is now real Agent apps only. On launch, old LLM and custom API data, and their credentials, are cleared.",
            "Full-data backups, daily automatic backups, and the restore entry are removed. Existing Agent accounts, usage history, and settings are kept.",
        ],
        "install": "Unzip and drag 搞词元.app into the Applications folder. Note: from V4.13, old LLM and custom API accounts are permanently deleted on launch.",
        "signing": "Signed with Apple Development. Not notarized by Apple.",
        "words": ["By tool", "By model", "By time"],
    },
    "jiling": {
        "role": "System monitoring",
        "tagline": "The small movements of your Mac, clear at a glance.",
        "lede": "A native macOS edge system monitor, using SwiftUI, AppKit, Mach/IOKit/libproc, and SQLite. Monitoring records stay on this Mac. No third-party runtime, no AI, and no account.",
        "features": [
            ("Edge panel", "When collapsed it is only a vertical line at the screen edge. Hover or click to expand. The default shortcut is ⌥⌘G."),
            ("Live monitoring", "CPU, memory pressure, compressed memory, swap, network and disk throughput, per-app rankings, and sensors that are readable on the current Mac model."),
            ("History and tasks", "Review trends for the last 24 hours. Manually record the duration, average, and peak of tasks such as compiles and renders, and export them."),
            ("Cleanup and storage analysis", "A limited set of old caches, logs, and Xcode compilation products can be moved to the Trash after confirmation, and restored by batch. Storage analysis and the disk map are read-only and do not delete."),
            ("Volumes and images", "From V1.15, read-only analysis of this Mac’s built-in volume information and of ordinary NTFS volume images."),
            ("App management and memory reclaim", "Uninstall an app after confirming it, and restore it. Shows real memory readings and reclaim results, and does not promise a speedup."),
        ],
        "notes": [
            "Removes data backups taken during an upgrade install, rollback archives of the previous app, and the automatic safety backup before a restore.",
            "Exporting yourself, and restoring from a file you choose, are still available.",
            "Signing changed from the old ad-hoc identity to Apple Development. System permissions are not carried over automatically; grant them again in System Settings when needed.",
        ],
        "install": "Open the DMG and drag 搞机灵.app into Applications. When updating, quit the old version before replacing it. History, tasks, and settings stay in a separate data directory.",
        "signing": "Signed with Apple Development. Not Developer ID signed or notarized. Switched over from the old ad-hoc signature, so system permissions need to be granted again.",
        "words": ["CPU", "MEM", "SWAP", "NET", "DISK"],
    },
    "menhu": {
        "role": "Website launcher",
        "tagline": "Put the sites you use often on a Launchpad, like apps.",
        "lede": "A macOS website launcher that includes file downloads and native mail. Drag to reorder, group folders, and assign a browser and a login account to each site. The app was originally named 门道.",
        "features": [
            ("Site Launchpad", "Arranged like Launchpad. Drag to reorder and to group folders. Swipe sideways with two fingers to change pages, and import the Chrome or Edge bookmarks bar."),
            ("Choose a browser", "Each site can use Chrome, Edge, Safari, or Firefox. After 搞门户助手 is installed in Chrome or Edge, account autofill is supported."),
            ("Edge-docked panel", "Collapses to a thin strip on the left or right and expands on hover, showing recent and frequent sites first. Search by name, URL, pinyin, or short name."),
            ("Work scenes", "Open several sites at once, each with its chosen browser and account."),
            ("Downloads and native mail", "Review the URL and the save folder in the app, then manage the download queue. Native mail supports the inbox, drafts, and attachments, and only sends or receives after you connect it explicitly."),
        ],
        "notes": [
            "Fixes ⌘W for the download and mail windows: adds Window → Close Window.",
            "Closing a window keeps the background download queue, and keeps draft saving and send protection for mail.",
            "If the app refuses to quit, replacement stops and this round’s install staging files are cleaned up.",
        ],
        "install": "Open the DMG, drag 搞门户.app into Applications, and launch it. For autofill, load the in-app BrowserExtension from the Chrome or Edge extensions page in developer mode.",
        "signing": "Signed with Apple Development. Not notarized by Apple.",
        "words": ["Mail", "Docs", "Courses", "Papers", "Code", "Drive", "Calendar", "Downloads"],
    },
    "wenjian": {
        "role": "Writing and compiling",
        "tagline": "A local desk for LaTeX and Markdown, compiled offline.",
        "lede": "A local macOS workbench centered on writing and compiling LaTeX and Markdown. Accounts, network sync, and AI features are not in development for now.",
        "features": [
            ("LaTeX", "Detects the main file and % !TeX root, with outline navigation and smart completion; structured diagnostics; two-way SyncTeX. Offline compile with the included Tectonic, and also with XeLaTeX, pdfLaTeX, or LuaLaTeX already on the Mac."),
            ("Markdown", "Live block editing, source and split view, an outline, tables, math, Mermaid, and code highlighting, with export to HTML or PDF."),
            ("PDF editing", "Read, search, annotate, and fill forms; insert text and images; rotate, crop, reorder, merge, and split pages. Includes an entry that hands off to OCR."),
            ("Office and tables", "Read-only preview for Word, Excel, and PowerPoint. CSV and TSV can switch between source and a table, with filter, sort, and adding rows or columns."),
            ("Desktop notes", "Rich text with image and PDF attachments, six color groups, search, and a trash. A separate desktop window that can stay on top and turn translucent."),
        ],
        "notes": [
            "The workbench is redesigned: warm white and deep graphite, a forest-green accent, with the LaTeX and Markdown entries first.",
            "PDF editing and OCR are in the same group, Office viewing is a single entry, and recent files can be continued directly.",
            "Automatic backups such as pre-save history snapshots and workspace ZIP backups are removed. A conflict with an external edit still blocks overwriting.",
        ],
        "install": "Open the DMG and drag 搞文件 into Applications. The default location is /Applications/搞文件.app.",
        "signing": "Not notarized by Apple. The README calls it 本地签名 (locally signed). The V1.11 release notes say each component is signed with a fixed Apple Development identity.",
        "words": [],
    },
    "caozuo": {
        "role": "Extra actions",
        "tagline": "Files, windows, the clipboard, and screenshots, gathered into one action library.",
        "lede": "A native macOS tool for extra actions. File handling, window controls, the clipboard, archives, and custom actions sit in one action library, and can be called from the main window, the menu bar, a quick palette, the Finder menu, system Services, and input rules.",
        "features": [
            ("Action palette", "Search actions and favorite the ones you use. The default shortcut is ⌥⌘O. It can also be called from the Finder context menu, system Services, and the menu bar."),
            ("File tools", "New text files, Markdown, and folders; copy a path and a SHA-256; preview a batch rename; convert and scale images; QR codes."),
            ("Archive tools", "Create ZIP and 7Z, with encryption, splitting, and 7Z solid compression. You can view the list inside an archive and choose what to extract. Items with the same name are not overwritten silently."),
            ("Window controls", "Left and right halves, top and bottom halves, four corners, thirds, center, and move to another display. Optional snapping when a window is dragged to a screen edge."),
            ("Clipboard and input rules", "A clipboard stack and phrases (capture is off by default). Custom shortcuts, mouse buttons, and Option + right-click direction gestures. Combined actions run in order."),
            ("Screenshots and recording", "From V1.15: screenshots, scrolling capture, annotation, OCR, pinned images, screen and audio recording, GIF, and translation on this Mac."),
        ],
        "notes": [
            "The opening workbench is redone: a teal palette, system light and dark appearance, four main entries, personal favorites, and quick file actions.",
            "The sidebar is regrouped, and page titles and the file-selection bar are simplified.",
            "Backup generation for data, phrases, screenshots, input settings, and the install flow is removed. The original data path and Keychain items are kept.",
        ],
        "install": "Open the DMG and put 搞操作 into Applications. Window and input features need Accessibility and related permissions in System Settings.",
        "signing": "Signed with a fixed Apple Development identity. Developer ID is not used. Not notarized by Apple.",
        "words": ["⌘", "⇧", "⌥", "⌃"],
    },
}
