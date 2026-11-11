# Battery Monitor for Mac

[产品官网](https://battery-monitor.zpj.io/) · [使用帮助](https://battery-monitor.zpj.io/support.html) · [隐私政策](https://battery-monitor.zpj.io/privacy.html)

这个仓库保存 Battery Monitor 的八语种静态官网：简体中文位于根目录，其余为 `zh-Hant/`、`en/`、`ja/`、`ko/`、`de/`、`fr/`、`es/`。每种语言均包含产品、帮助和隐私页面；右上角菜单切换到对应页面，不写语言 Cookie。

翻译源位于 `locales/*.json`，所有页面共用 `site.css`、`site.js` 和 `assets/`。更新翻译后运行 `python3 tools/build-site.py`，再运行 `python3 tools/check-site.py` 核对 24 个页面及语言跳转。本地预览可运行 `python3 -m http.server`。概况和详情图保留真实拍摄语言，并在说明中标出。

GitHub Pages 从 `main` 分支根目录发布。App 和 App Store Connect 使用以上永久地址。产品界面图片来自 Mac App Store 版实机截图。
