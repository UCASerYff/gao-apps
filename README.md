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

1. `tools/update_latest.py` 读取八个仓库各自的 `releases/latest`（GitHub 自动排除草稿和预发布），挑出 `<仓库名>-<版本>.dmg` 或 `.zip` 安装包，写入 `data/latest.json`（版本、build、文件名、下载地址、大小、SHA-256、发布时间）。源码包和 `.sha256` 不作为下载主文件；没有安装包的应用标为「暂不可下载」。
2. `tools/build_site.py` 根据 `tools/content.py` 的文案和 `data/latest.json` 生成全部页面，不开 JavaScript 也能拿到正确链接。
3. GitHub Action `.github/workflows/update-latest.yml` 每小时、每次推送和手动触发时运行上面两步，有变化才提交。
4. 页面打开时，`assets/site.js` 还会读一次最新的 `latest.json`，再直接向 GitHub API 查询，发现更新版本就当场替换；失败时保留已有链接。

所以某个应用发了新版，只要在它自己的仓库发布正式 Release，并附上 `<仓库名>-<版本>.dmg/zip`，这里的下载按钮就会自动指向新包。

## 维护约定

- 不要把安装包、证书、私钥或应用源码放进本仓库。
- `tools/content.py` 的介绍文字都摘自各应用 README 和正式发布说明，修改前先回原仓库核对。
- 改完文案后运行 `python3 tools/build_site.py`。
