# BatterVibe for Mac

[产品官网](https://battervibe.zpj.io/) · [使用帮助](https://battervibe.zpj.io/support.html) · [隐私政策](https://battervibe.zpj.io/privacy.html)

这个仓库保存 BatterVibe 的八语种静态官网：简体中文位于根目录，其余为 `zh-Hant/`、`en/`、`ja/`、`ko/`、`de/`、`fr/`、`es/`。每种语言均包含产品、帮助和隐私页面；右上角菜单切换到对应页面，不写语言 Cookie。

翻译源位于 `locales/*.json`，所有页面共用 `site.css`、`site.js` 和 `assets/`。更新翻译后运行 `python3 tools/build-site.py`，再运行 `python3 tools/check-site.py` 核对 24 个页面及语言跳转。本地预览可运行 `python3 -m http.server 4887 --bind 127.0.0.1`。

产品介绍围绕 Web Coding 的功率、户外 HDR 增亮和合盖运行展开。页面明确说明开发进度、硬件和安装渠道要求；购买方案为 14 天首次免费试用及一次性买断，中国大陆区计划价 ¥6，不自动续费。新版尚未开放下载和购买时，不显示可用的购买或下载按钮。

独立控制面板以功能说明、购买状态与恢复购买、感谢支持为主；具体功能通过应用内对应入口操作。充电上限 FAQ 保留首次添加系统快捷指令、选择目标及到系统电池设置核对结果的步骤。

三张场景图片使用内置 Image Generation 工具生成，均标为 AI 场景示意。原始 PNG 位于 `assets/scenes/originals/`，响应式 WebP 位于 `assets/scenes/`；完整提示词和来源说明见 `docs/generated-scene-prompts.json`。历史实机截图仍保留为旧素材，不用于当前页面。

GitHub Pages 从 `main` 分支根目录发布。当前 CNAME、canonical、Open Graph 与语言 alternate 地址统一指向 `battervibe.zpj.io`，语言路径保持不变。DNS、GitHub Pages 自定义域名与外部应用链接的切换由发布步骤单独处理；仓库内地址更新不代表线上域名已经可用。
