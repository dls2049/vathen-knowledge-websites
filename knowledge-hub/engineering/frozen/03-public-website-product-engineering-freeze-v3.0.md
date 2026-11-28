<!-- Synced from Notion on 2026-11-28. Notion remains the source of truth. -->
# 🌐 VATHEN 先知官网产品与工程冻结规格 V3.0

Source: https://app.notion.com/p/426f15aabd2c81f49989fef87fae821c

# 文档控制

- 文档编号：WEB-PRD-ENG-001
- 版本：V3.0
- 基线日期：2026-11-28
- 状态：产品与工程冻结基线（Frozen Baseline）；会员价格、支付渠道、法律文案和真实数据发布按 Gate 批准
- 适用对象：官网产品经理、设计师、前端、后端、内容运营、SEO、QA、DevOps 和开发 Agent

# 1. 产品定义

VATHEN 官网是面向公众的品牌与研究内容门户，负责让目标用户理解 VATHEN、发现研究、阅读研究、探索实体与主题，并在商业规则获批后完成注册、订阅和个人情报服务。

官网不是 DAC、不是内部情报 Dashboard、不是 Agent 工作台，也不是事实数据权威编辑端。所有实体事实、来源、关系、事件和指标来自 DAC 已审核的 Public API / Public Projection。文章正文通过受控内容工作流管理，并关联 DAC 的 Entity / Evidence / Claim 等对象。

核心价值路径：<br />认识 VATHEN → 发现研究 → 阅读与理解 → 探索相关实体/主题 → 建立账户/订阅（后续）→ 关注与持续使用（后续）。

# 2. 用户与关键任务

| 用户 | 关键任务 | 首期体验重点 |
| --- | --- | --- |
| 新访客 | 快速理解品牌、研究范围和可信度 | 首页、About、Methodology、精选研究 |
| 主动研究型读者 | 找到值得读的专题和报告 | Research 列表、筛选、文章详情、引用来源 |
| 投资/战略专业用户 | 理解公司、行业、技术和事件之间的关系 | 实体详情、时间线、相关研究、来源 |
| 回访读者 | 继续阅读和发现新内容 | 搜索、主题页、相关推荐 |
| 会员用户（后续） | 获取完整研究、关注对象和个性化情报 | 账户、权益、Watchlist、通知 |
| 编辑/运营 | 管理稿件、版本、预览、发布和撤回 | 内部内容工作流；不在公开前台操作 |

目标受众不是单一股民群体。官网内容和产品信息架构应同时服务主动研究型投资者、企业创始人/高管、战略与投资部门、科技产业从业者和专业研究人员；实际优先级由用户访谈、阅读行为和付费实验验证。

# 3. 信息架构与路由冻结

## 3.1 公共主导航

1. Home
2. Research
3. Industries
4. Intelligence（公开可用内容的实体/事件入口；内部情报中心不对外开放）
5. Methodology
6. About
7. Pricing（商业策略批准后开放）
8. Search
9. Account（登录后显示工作区入口）

## 3.2 路由约定

- 语言前缀：/zh-CN/...、/en/...；默认语言重定向策略在部署域名和 SEO 验证后冻结。
- 首页：/\{locale\}。
- 研究列表：/\{locale\}/research；研究详情：/\{locale\}/research/\{slug\}。
- 行业：/\{locale\}/industries/\{slug\}。
- 公司：/\{locale\}/companies/\{slug\}。
- 人物：/\{locale\}/people/\{slug\}。
- 技术：/\{locale\}/technologies/\{slug\}。
- 事件：/\{locale\}/events/\{slug\}。
- 主题：/\{locale\}/topics/\{slug\}。
- 搜索：/\{locale\}/search。
- 品牌/方法：/\{locale\}/about、/\{locale\}/methodology。
- 商业：/\{locale\}/pricing；联系：/\{locale\}/contact。
- 账户：/\{locale\}/login、/\{locale\}/register、/\{locale\}/account。
- 会员工作区与 Watchlist 为后续版本，不得用静态假数据伪装已接通能力。
- Admin 不使用公开路由和公开会话；优先归属 DAC 内部 Admin。

# 4. 页面规格与验收要求

所有页面必须定义 title、description、canonical、hreflang、OpenGraph、结构化数据（适用时）、面包屑、响应式布局、键盘可操作性和 Loading / Empty / Error / Unauthorized / Not Found 状态。

## 4.1 首页

模块顺序：

1. 品牌主张：全球视野、深度观察、独立思考；Slogan「看见变化，理解未来」。
2. 编辑精选：最新/精选研究内容，明确内容类型与发布时间。
3. 研究领域：六大研究领域入口。
4. 关键趋势/产业专题：只展示有发布许可且已审核的摘要。
5. 实体/情报探索入口：公司、人物、行业、技术和事件。
6. 方法与可信度：研究流程、证据与来源标准。
7. 订阅/注册 CTA：只有商业规则获批后启用。
8. Footer：About、Methodology、Contact、Privacy、Terms、版权与语言切换。

首页不展示未经审核的预测、不使用无来源的市场数字，不把内部 Dashboard 指标当作公开品牌数字。

## 4.2 Research 列表与专题页

- 支持内容类型：News Brief、Trend Brief、Deep Research、Industry Map、Future Outlook、Annual Outlook。
- 列表筛选：研究领域、内容类型、发布时间、主题标签；筛选参数可分享。
- 卡片字段：标题、摘要、内容类型、领域、作者/编辑署名、发布日期、阅读时长（有真实数据时）、访问级别。
- 分页 cursor 优先；空结果、筛选无结果和错误有独立状态。
- 仅显示已发布版本；草稿、待审核和已撤回内容不进入公共列表。

## 4.3 研究详情页

- 头部：标题、副标题、内容类型、领域、作者、发布日期、更新时间、阅读时长（计算口径明确）。
- 正文：目录、标题层级、图表/表格、引用、脚注/来源、相关实体和延伸阅读。
- 研究结论按 FACT / ANALYSIS / OUTLOOK / OPEN QUESTION 或等效视觉标识区分。
- 每条关键事实可链接来源或证据；来源展示符合授权范围。
- 付费内容由服务端判断 entitlement；客户端隐藏不构成权限控制。
- 版本更新需显示修订时间和重要更正；撤回页面返回明确状态，不泄漏旧付费正文。

## 4.4 实体详情页（公司/人物/行业/技术）

统一模板：

- 概览：名称、类型、简介、主要标识、更新时间和数据状态。
- 核心档案：按实体类型配置字段，不将缺失值编造为事实。
- 关键关系：有证据、时间边界和审核状态的关系；只展示公开字段。
- 相关事件/时间线：事件时间与来源时间分开。
- 相关研究：关联研究文章和专题。
- 来源与方法：展示允许公开的来源摘要/链接。
- 多语言：Entity 主记录共享 ID，翻译字段按 locale 独立；缺少翻译时按策略展示原文，不伪造翻译。
- 合并实体的旧 slug 应重定向至 survivor；不存在实体返回 404。

## 4.5 事件与主题页

事件区分 Event 与 News Item：多篇新闻可指向同一事件；转载聚类不得被计为多个独立来源。事件页显示时间、影响实体、重要性/审核状态、独立来源和相关研究。主题页聚合实体、事件、研究与时间线，所有聚合规则必须可解释。

## 4.6 搜索

- 首期支持 Research、Entity、Topic 的基础全文与别名搜索；News/Event 在数据接通后加入。
- 权限过滤必须在服务端执行，搜索索引不得泄漏受限内容标题或摘要。
- 支持 locale、类型、领域筛选；提供 query、filters、sort、cursor。
- 无结果、拼写建议、服务不可用状态明确；记录搜索埋点但遵守隐私最小化。

## 4.7 About / Methodology / Pricing / Contact

- About：品牌使命、研究范围、团队/组织信息（已确认后发布）。
- Methodology：证据等级、研究流程、事实/分析/展望区分、纠错机制。
- Pricing：仅展示已批准的价格、权益、税务说明、自动续费/取消/退款规则；未批准时页面不公开或显示等待开放。
- Contact：受控联系表单、反垃圾、隐私告知和提交确认。

# 5. 内容模型与 CMS / 发布边界

官网不维护实体事实副本。核心内容对象：

- Article / ResearchReport：内容主记录，稳定 ID、slug、locale、type、domain、author、access\_level、status。
- ArticleRevision：不可覆盖的正文版本、content\_hash、editor、created\_at、change\_summary。
- ArticleEntityLink：文章与 DAC Entity 的关系。
- ArticleEvidenceLink：文章关键结论与 DAC Evidence / Claim 的关联。
- Topic / Taxonomy：受控词表，不允许自由文本无限生长。
- Publication：审批、版本、发布时间、撤回时间和操作审计。
- PublicProjection：公开字段白名单、许可依据、审核状态和 payload version。

推荐状态：draft → editorial\_review → fact\_check → legal\_or\_rights\_review（适用时）→ approved → scheduled → published → updated / withdrawn。回退状态必须记录原因。AI 生成稿不得自动跳过事实核查和编辑审核。

内容编辑/审核界面归属内部工作台（DAC Admin / Research Studio），不另建一套与 DAC 权限割裂的 CMS。官网前端只消费已发布内容 API。

# 6. 会员、身份与支付边界

身份与会员权益必须分开：

- Authentication：用户身份、登录会话、验证和安全。
- Authorization：内部 RBAC 与资源权限。
- Entitlement：外部会员等级、单篇购买、访问额度和有效期。
- Billing：订单、支付、退款、续费、Webhook 和对账。

P0 官网不以支付为上线前置条件；先完成公开研究内容和基础账户骨架。会员/支付进入 P1/P2，前置决策包括价格、权益、退款、税务、支付商户资格、微信/支付宝/国际支付渠道、账单和客服流程。任何付费访问必须由服务端验证 entitlement；Webhook 签名、幂等、重放防护和异常对账是上线阻断项。

# 7. 设计系统与交互规范

品牌基调：理性、克制、编辑式、全球产业研究感；避免泛科技渐变、赛博朋克装饰和过度卡片化。

- Design Tokens：颜色、字体、字号、行高、间距、圆角、阴影、断点、层级和动效。
- 基础组件：Header、Footer、Breadcrumb、Button、Input、SearchBox、ResearchCard、EntityCard、EventRow、MetricCard、Timeline、RelationshipList、Citation、Table、Chart、TOC、Tabs、PaywallGate、Pagination、Skeleton、EmptyState、ErrorState、Toast。
- 每个组件需定义用途、props、变体、响应式、状态、键盘行为、ARIA 和测试。
- 断点候选：mobile \<640px、tablet 640–1023px、desktop ≥1024px、wide ≥1440px；最终由设计稿和真实设备测试确认。
- 长文阅读优先，正文列宽、字号、行距需用真实研究文章校准；表格在移动端可横向滚动或提供替代呈现。
- 目标 WCAG 2.2 AA：键盘可达、焦点可见、对比度、图像 alt、语义结构和减少动态效果偏好。

# 8. 技术实现与 API 契约

- Web：Next.js App Router + TypeScript；公共页面优先 SSR/SSG/ISR，按内容更新频率设置缓存与 revalidation。
- API：FastAPI /api/v1；官网使用 Public API，不直连数据库。
- 内容/API 主要契约以 OpenAPI 为准；统一错误 code/message/details/request\_id。
- cursor 分页优先；过滤、排序字段白名单；API 响应不得带内部备注、原始全文或 Agent 运行数据。
- 图片与附件经授权的媒体服务/CDN；受限文件私有存储、短时签名访问。
- 前端埋点只记录产品分析必要事件；不得将敏感研究内容、个人信息或全文写入第三方分析工具。

# 9. SEO、性能、安全与合规

SEO：

- 每个可索引页面有唯一 title/description/canonical/hreflang。
- XML sitemap 分语言生成；robots、分页、404/410、重定向正确。
- Article / Organization / Person / Event 等结构化数据只输出真实字段。
- 不将草稿、搜索参数页、登录页、受限付费正文错误索引。

性能：

- 设定 Core Web Vitals 预算并用真实数据监测；图片响应式、现代格式、延迟加载。
- 首屏不加载全部文章正文；合理分页、缓存和 CDN。
- ISR 更新必须与发布版本关联，撤回/更正要清缓存。

安全：

- 服务端鉴权与 entitlement；安全 Cookie；CSRF/XSS/SQLi 防护；CSP、安全响应头、速率限制、输入验证。
- 管理端 MFA、审计、最小权限；密钥不进入客户端 bundle。
- Webhook 验签和幂等；敏感 API 需滥用防护。
- 用户隐私、Cookie/分析告知、数据导出/删除、保留期限和跨境服务使用需合规审查。

版权：

- 允许访问 URL 不代表允许全文复制、商业展示或再分发。
- 文章引用、新闻摘要、论文/专利/图片和数据均遵守来源许可。
- Public Projection 必须携带 license\_basis 和字段级发布审批。

# 10. MVP 分期与明确非目标

## P0：公开内容门户

- 双语路由和 Design System。
- 首页、Research 列表/详情、About、Methodology、Contact、基础搜索。
- 内容草稿/审校/发布/撤回流程（由内部工作台提供）。
- SEO、响应式、可访问性、性能、错误监控和预览环境。
- Public API 最小只读契约；在 DAC G4 通过前只允许使用明确标记的本地 fixture/静态演示数据，不得伪装真实生产数据。

## P1：实体与发现

- 公司、人物、行业、技术、事件和主题详情页。
- DAC Public API 集成、实体关系、来源摘要、时间线。
- 搜索升级、筛选和相关推荐。

## P2：会员与个人情报

- 注册、会员权益、支付、订单、收藏、Watchlist、通知和个人工作区。
- 产业链图谱、数据导出、自然语言问答和团队功能，需独立评审许可、成本与安全。

明确非目标：官网首期不建设内部 DAC Dashboard；不直连内部数据库；不复制实体事实库；不承诺自动预测/自动投资建议；不在未确认商户资格与退款规则前接入真实支付。

# 11. 页面级验收矩阵

| 页面 | 数据依赖 | 核心验收 |
| --- | --- | --- |
| Home | 已发布精选研究、领域词表 | 模块完整、真实内容、CTA 状态正确、SEO |
| Research List | Published Article | 筛选、分页、空/错状态、不可见草稿 |
| Research Detail | ArticleRevision、Entity/Evidence links | 版本、引用、目录、付费权限服务端校验 |
| Entity Detail | Public Entity Projection | 来源、时间、关系、语言和 404/redirect |
| Event Detail | Public Event Projection | 新闻聚类、独立来源和事件时间 |
| Topic/Industry | Published taxonomy + related objects | 聚合口径明确、链接有效 |
| Search | Public Search API | 服务端权限过滤、筛选、分页、无结果 |
| About/Methodology | 已批准静态内容 | 品牌与方法准确，不作未经证实承诺 |
| Pricing | 批准的商业配置 | 价格、权益、自动续费/取消/退款一致 |
| Login/Register | Identity API | 验证、限流、会话安全、错误提示 |
| Account | Identity + Entitlement | 用户只能查看自身信息与权益 |

# 12. 测试与 Definition of Done

- Unit：组件、格式化、权限展示、内容渲染。
- Contract：OpenAPI 与前端类型一致，API schema 变更有兼容测试。
- Integration：内容发布→Public Projection→API→页面更新/撤回。
- E2E：双语切换、研究列表/详情、搜索、移动端导航、权限拒绝、404/redirect。
- SEO：sitemap、canonical、hreflang、结构化数据、robots。
- A11y：键盘、焦点、对比度、屏幕阅读器关键路径。
- Security：未登录访问受限内容、用户越权、缓存泄漏、XSS、CSRF、Webhook 重放。
- Visual QA：桌面/平板/移动端截图与设计基线对比。

DoD：PR/commit、预览 URL、自动测试报告、SEO/a11y 检查、数据权限验证、发布/回滚记录、已知问题清单齐全。开发 Agent 提交待验收；独立 QA 依据矩阵验收。

# 13. 冻结边界与待批准事项

已冻结：官网为公开消费端；Next.js + TypeScript；双语路由；页面信息架构；Public API only；DAC Public Projection；内容版本与发布流程；SEO、安全、可访问性和测试要求。

待批准 Gate：

- 会员价格、权益额度、单篇购买、退款、自动续费和税务说明。
- 微信/支付宝/Stripe 等支付渠道与商户资格。
- 最终域名、备案、隐私政策、Cookie/分析工具和法律文本。
- 首批公开实体/研究内容及其来源许可、图片/全文/摘要使用权。
- 真实 DAC Public API 未通过验收前，官网只能用显式标记的 fixture/静态内容。

# 14. 文档权威性与变更

本文件 V3.0 取代旧《官网产品与工程总蓝图 V2.0/V2.1》及《官网完整开发手册 V1.0》中与本文件冲突的部分。旧文档保留历史细节和参考价值；页面/接口/组件实现以本冻结文件、Design Tokens 和 OpenAPI 为准。

- V3.0｜2026-11-28：统一产品定位、用户任务、路由、页面规格、内容模型、发布流程、会员边界、技术实现、SEO、安全、MVP 范围与验收矩阵。

# 15. 前后端 API 契约补充

公共 API 由 DAC Public API 提供；官网可通过服务端 BFF 封装读取，但不得连接 DAC 内部数据库。

| Endpoint | 方法 | 目的 | 可见性 |
| --- | --- | --- | --- |
| /api/v1/public/articles | GET | 已发布研究列表、筛选和分页 | Public |
| /api/v1/public/articles/\{slug\} | GET | 已发布研究详情和版本元数据 | Public / entitlement |
| /api/v1/public/entities/\{type\}/\{slug\} | GET | 已批准的实体公开投影 | Public |
| /api/v1/public/events/\{slug\} | GET | 已批准事件公开投影 | Public |
| /api/v1/public/taxonomies | GET | 公开领域、主题和内容类型词表 | Public |
| /api/v1/public/search | GET | 公开研究/实体/主题搜索 | Public |
| /api/v1/internal/content/articles | GET/POST | 内部稿件查询与创建 | Editor+ |
| /api/v1/internal/content/articles/\{id\}/revisions | GET/POST | 版本查询与新修订 | Editor+ |
| /api/v1/internal/publications/\{id\}/preview | GET | 鉴权预览 | Editor+ |
| /api/v1/internal/publications/\{id\}/submit | POST | 提交审校 | Editor+ |

统一响应包含 data、meta（request\_id、generated\_at、pagination）；错误包含 code、message、details、request\_id。列表使用 cursor 分页；筛选/排序参数白名单。公共接口只返回 approved + published + license-eligible 字段。付费正文的 entitlement 必须由服务端验证；缓存键必须包含 locale、发布版本和权益上下文，避免跨用户缓存泄漏。

OpenAPI 文件是实现时的机器契约；路由、字段或权限发生破坏性变化必须先更新本冻结规格/ADR，再更新 OpenAPI 和契约测试。

## 性能预算补充（P0）

以真实用户数据 p75 作为持续验收口径：LCP ≤ 2.5s、INP ≤ 200ms、CLS ≤ 0.1。上线前以 Lighthouse/Playwright 形成实验室基线；上线后接入真实用户监测（如合规和预算允许）。超出预算必须登记性能问题和修复计划；不得只提交一次 Lighthouse 截图宣称长期达标。
