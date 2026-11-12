# BatterVibe 官网更新 · 2026-11-12

本次在现有 GitHub Pages 仓库实现，不改域名、CNAME、组织或语言路径。所有首页、帮助、隐私、SEO 标题及站点品牌统一为 **BatterVibe**。

## 页面内容

- 首页按 Web Coding / Vibe Coding 的工作情境组织：实时功率 → 户外 HDR 增亮 → 合盖继续任务。
- 菜单栏和独立控制面板属于一套产品。购买方案为首次 14 天免费试用、中国大陆区 ¥6 一次性买断、不自动续费；其他地区使用 Apple 购买页的当地价格。
- 不宣传屏幕常亮，不区分商业“版本档位”。HDR 只说明已验证的 Mac14,6 内置 XDR 屏幕；合盖运行明确官网安装后台组件和系统授权要求。
- 充电上限仅在帮助 FAQ 作为辅助能力说明：正在准备的新版包含此能力，要求 Apple 芯片 Mac + macOS 26.4 或以上；商店安装渠道首次添加一次官方系统快捷指令。明确启动快捷指令不等于设置完成，以系统读回为准。
- 发布区如实说明当前送审的是此前的监测版本，新体验和购买流程尚未开放。CTA 进入工作场景、发布状态和使用帮助，未伪造 App Store 或下载入口。

## 图片与来源

三张图片由内置 `image_gen__imagegen` 生成，原图均已审看。照片中的通用代码与网页画面是场景的一部分，页面明确标为 AI 场景示意；没有把它们作为 BatterVibe 实机截图。

| 场景 | 原图 | 尺寸 | 网页版 |
|---|---|---|---|
| 湖畔编码主视觉 | `assets/scenes/originals/outdoor-coding.png` | 1672 × 941 | `assets/scenes/outdoor-coding.webp` 与 `-800.webp` |
| 日光庭院 HDR 场景 | `assets/scenes/originals/daylight-screen.png` | 1536 × 1024 | `assets/scenes/daylight-screen.webp` 与 `-800.webp` |
| 固定桌面合盖场景 | `assets/scenes/originals/closed-lid.png` | 1536 × 1024 | `assets/scenes/closed-lid.webp` 与 `-800.webp` |

完整最终提示词与工具来源在 `docs/generated-scene-prompts.json`。WebP 仅使用 `cwebp` 压缩和缩放，未修改画面；原始 PNG 保留在仓库内。旧实机截图保留但不再用于首页。

## 构建与验收

翻译源为 `locales/*.json`，24 个 HTML 页面由 `python3 tools/build-site.py` 生成。`python3 tools/check-site.py` 已核对 24 页、192 个语言跳转、资源、当前语言和 canonical 地址；`git diff --check` 通过。

使用 Ego Browser 的共用 TaskSpace 81 / p2 本地验收。八语首页在桌面 1440 和手机 390 CSS 像素的全部 16 种组合均无横向溢出；已审看完整中文桌面，以及中文、英文、德文手机版截图，三张图均实际加载。德语长标签换行时的三列功率数字已按共同基线对齐。

实际点击验证了简中帮助 → 英文帮助 → 德文帮助的语言切换，保持对应页面；充电上限 FAQ 可展开。语言菜单可用 Escape 关闭，焦点返回语言选择。另检查了英文隐私页 7 段内容的手机排版。截图和 JSON 运行记录在被 Git 忽略的 `artifacts/website-verification/`，不作为产品素材发布。

Ego 在本机浏览器缩放下的通用截图封装存在截边问题，采用文档允许的 CDP 截图并按实际 CSS 尺寸和 DPR 计算范围；这不是页面的溢出。一次 FAQ 自动滚入视口失败后，先观察目标并即时滚入，再真实点击成功；没有据工具派发就判定交互成功。未验证线上部署，也未将浏览器视口模拟表述为真实 iPhone 测试。

本地预览：`python3 -m http.server 4887 --bind 127.0.0.1`，访问 `http://127.0.0.1:4887/`。最终推送与发布由主代理统一处理，本次网站子任务未推送。

## 后续修订：域名与面板定位

用户随后要求域名随品牌统一。仓库中的 CNAME、生成器 BASE、24 页 canonical / Open Graph / alternate 地址，以及 README 当前入口已改为 `https://battervibe.zpj.io`。原语言路径、视觉结构和图片保持原样；本步骤未配置 DNS 或 GitHub Pages，也未提交或推送，线上域名切换由主代理处理。

八种语言的控制面板说明改为功能说明、购买状态与恢复购买、感谢支持。具体操作保留在应用内的相应入口；充电上限说明保留首次添加系统快捷指令、选择受支持目标、在系统电池设置中确认实际结果的事实。首页和 FAQ 不再把普通防休眠描述为产品能力，商店合盖能力仍标注验证中。新版下载、试用和购买尚未开放的说明保留。

本次运行现有 build/check 和 `git diff --check` 均通过，并额外核对 24 页所有 canonical、OG URL、OG image 与八语 alternate 的域名，以及 CNAME。先前的 TaskSpace 81 和本地预览服务已结束，本次未重新建立浏览器空间；没有改动视觉结构、CSS、脚本或图片，新增文案尚未做新一轮渲染检查。
