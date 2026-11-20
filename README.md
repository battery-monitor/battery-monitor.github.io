# BatterVibe for Mac

[产品官网](https://battervibe.zpj.io/) · [使用帮助](https://battervibe.zpj.io/support.html) · [隐私政策](https://battervibe.zpj.io/privacy.html)

这个仓库保存 BatterVibe 的八语种静态官网：简体中文位于根目录，其余为 `zh-Hant/`、`en/`、`ja/`、`ko/`、`de/`、`fr/`、`es/`。每种语言均包含产品、帮助和隐私页面；右上角菜单切换到对应页面，不写语言 Cookie。

翻译源位于 `locales/*.json`，所有页面共用 `site.css`、`site.js` 和 `assets/`。更新翻译后运行 `python3 tools/build-site.py`，再运行 `python3 tools/check-site.py` 核对 24 个页面及语言跳转。本地预览可运行 `python3 -m http.server 4887 --bind 127.0.0.1`。

官网记录中国大陆 Mac App Store 的公开版本与更新进度。已上架的 1.0 提供电量和功率监测，1.1 更新包含预计续航、终端命令、HDR 增亮和充电上限。兼容设备的高级控制通过控制面板试用或一次性应用内购买，购买可恢复。

`assets/app/0.10.1/` 保存 0.10.1 实际应用界面，覆盖八种语言。户外使用和合盖场景图由 Image Generation 生成，页面以图注标明。原图、生成说明和早期素材可在 `assets/` 与 `docs/generated-scene-prompts.json` 查看。

GitHub Pages 从 `main` 分支根目录发布。当前 CNAME、canonical、Open Graph 与语言 alternate 地址统一指向 `battervibe.zpj.io`，语言路径保持不变。DNS、GitHub Pages 自定义域名与外部应用链接的切换由发布步骤单独处理；仓库内地址更新不代表线上域名已经可用。
