# BatterVibe for Mac

[产品官网](https://battervibe.zpj.io/) · [使用帮助](https://battervibe.zpj.io/support.html) · [隐私政策](https://battervibe.zpj.io/privacy.html)

这个仓库保存 BatterVibe 的八语种静态官网：简体中文位于根目录，其余为 `zh-Hant/`、`en/`、`ja/`、`ko/`、`de/`、`fr/`、`es/`。每种语言均包含产品、帮助和隐私页面；右上角菜单切换到对应页面，不写语言 Cookie。

翻译源位于 `locales/*.json`，所有页面共用 `site.css`、`site.js` 和 `assets/`。更新翻译后运行 `python3 tools/build-site.py`，再运行 `python3 tools/check-site.py` 核对 24 个页面及语言跳转。本地预览可运行 `python3 -m http.server 4887 --bind 127.0.0.1`。

官网展示独立版 **0.10.6（构建 43）**。八种语言的概况、电池详情、桌面控制和最大功耗测试均在同一台 M2 Max 上从该构建实拍。功耗窗口使用同一次 60 秒测试的结果。网页图位于 `assets/app/0.10.6/<语言>/`，每种语言的分享预览由对应的概况截图裁切得到。品牌图标与当前应用一致。

截至 2026 年 11 月 23 日，中国大陆 Mac App Store 提供 1.0 电池与功率监测版。商店更新 1.1（构建 4）已提交 Apple 审核。网站分别介绍可下载的商店版本、1.1 的功能和独立版的硬件控制。

GitHub Pages 从 `main` 分支根目录发布，自定义域名为 `battervibe.zpj.io`。
