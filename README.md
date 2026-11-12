# 搞系列 · 介绍与下载站

八个原生 macOS 应用的介绍与下载页面：搞研究、搞节奏、搞积蓄、搞词元、搞机灵、搞门户、搞文件、搞操作。

**网址：<https://ucaseryff.github.io/gao-apps/>**

| 页面 | 地址 | 应用仓库 |
| --- | --- | --- |
| 总览 | [/gao-apps/](https://ucaseryff.github.io/gao-apps/) | — |
| 搞研究 | [/yanjiu/](https://ucaseryff.github.io/gao-apps/yanjiu/) | [GaoYanJiu](https://github.com/UCASerYff/GaoYanJiu) |
| 搞节奏 | [/jiezou/](https://ucaseryff.github.io/gao-apps/jiezou/) | [GaoJieZou](https://github.com/UCASerYff/GaoJieZou) |
| 搞积蓄 | [/jixu/](https://ucaseryff.github.io/gao-apps/jixu/) | [GaoJiXu](https://github.com/UCASerYff/GaoJiXu) |
| 搞词元 | [/ciyuan/](https://ucaseryff.github.io/gao-apps/ciyuan/) | [GaoCiYuan](https://github.com/UCASerYff/GaoCiYuan) |
| 搞机灵 | [/jiling/](https://ucaseryff.github.io/gao-apps/jiling/) | [GaoJiLing](https://github.com/UCASerYff/GaoJiLing) |
| 搞门户 | [/menhu/](https://ucaseryff.github.io/gao-apps/menhu/) | [GaoMenHu](https://github.com/UCASerYff/GaoMenHu) |
| 搞文件 | [/wenjian/](https://ucaseryff.github.io/gao-apps/wenjian/) | [GaoWenJian](https://github.com/UCASerYff/GaoWenJian) |
| 搞操作 | [/caozuo/](https://ucaseryff.github.io/gao-apps/caozuo/) | [GaoCaoZuo](https://github.com/UCASerYff/GaoCaoZuo) |

## 下载链接如何保持最新

安装包**不放在本仓库**。每个应用在自己的仓库独立发版，本站只链接过去：

1. `tools/update_latest.py` 读取八个仓库各自的 `releases/latest`（GitHub 自动排除草稿和预发布），挑出 `<仓库名>-<版本>.dmg` 或 `.zip` 安装包，写入 `data/latest.json`（发行版本、构建号、文件名、下载地址、大小、SHA-256、发布时间）。源码包和 `.sha256` 不作为下载主文件；没有安装包的应用标为「暂不可下载」。
2. `tools/build_site.py` 根据 `tools/content.py`、`tools/i18n.py` 和 `data/latest.json` 生成全部页面，不开 JavaScript 也能拿到正确链接。
3. GitHub Action `.github/workflows/update-latest.yml` 每小时、每次推送和手动触发时运行上面两步，有变化才提交。
4. 页面打开时，`assets/site.js` 还会读一次最新的 `latest.json`，再直接向该应用自己的 GitHub API 查询，发现更新的发行版本就当场替换；失败时保留已有链接。不会使用本仓库的 `/releases/latest`。

所以某个应用发了新版，只要在它自己的仓库发布正式 Release，并附上 `<仓库名>-<版本>.dmg/zip`，这里的下载按钮就会自动指向新包。

## 语言

默认中文。每一页导航右侧都有「中文 / EN」。切换后整页界面和正文一起换语言，选择记在 `localStorage`（键 `gao-lang`），地址栏也会带上 `?lang=zh` 或 `?lang=en`，方便把当前语言分享出去。`document.documentElement.lang` 会设成 `zh-CN` 或 `en`。

英文是现有中文的对照翻译，不另外编功能、口号或系统要求。应用名保持中文：搞研究、搞节奏、搞积蓄、搞词元、搞机灵、搞门户、搞文件、搞操作。中文事实在 `tools/content.py`，界面句子和英文译文在 `tools/i18n.py`。

语言开关是一组单选按钮，可以用 Tab 聚焦，再用左右或上下方向键切换。

## 版本号

页面只显示发行版本，例如 V4.14、V1.19。`data/latest.json` 里仍会保存 `build`（来自 CFBundleVersion 或发布说明），给更新脚本留着，但总览卡片、应用页、标题、页脚、下载按钮和 `assets/site.js` 都不会把它写出来。

安装页在有 SHA-256 时可以一键复制校验值；若发布里带了同名 `.sha256` 文件，还可以复制 `shasum -a 256 -c` 命令。数据目录路径也可以复制。

## 维护约定

- 不要把安装包、证书、私钥或应用源码放进本仓库。
- `tools/content.py` 的介绍文字都摘自各应用 README 和正式发布说明，修改前先回原仓库核对，并在 `tools/i18n.py` 里改对应英文。
- 改完文案后运行 `python3 tools/build_site.py`。脚本会检查英文是否齐全，并拒绝把构建号写进页面。
