<!-- Synced from Notion on 2026-11-28. Notion remains the source of truth. -->
# 🧭 VATHEN 全平台产品与工程冻结基线 V1.0

Source: https://app.notion.com/p/426f15aabd2c81549243ed1e72be2ea4

# 文档控制

- 文档编号：ENG-MASTER-FREEZE-001
- 版本：V1.0
- 基线日期：2026-11-28
- 状态：架构与产品边界冻结基线（Frozen Baseline）；云资源采购、生产部署和法律合规事项按文末 Gate 单独批准
- 适用对象：产品经理、架构师、前后端工程师、数据工程师、QA、DevOps、研究运营、开发 Agent、QA Agent
- 权威级别：全平台最高层工程基线

<callout icon="🧭" color="blue_bg">
本文件冻结系统边界、领域职责、数据权威性、接口原则、工程组织和交付纪律。未明确批准的云厂商/区域、付费资源、法律解释、生产密钥和对外发布权限，不得由工程师或 Agent 自行推定。
</callout>

# 1. 产品与系统总定义

VATHEN 是一个以全球产业、技术、经济、资本与政策信息为基础，以证据驱动研究为核心能力，面向外部用户提供研究内容与情报产品的统一平台。

系统由五个业务域构成：

| 业务域 | 产品定位 | 主要用户 | 权威职责 |
| --- | --- | --- | --- |
| Public Website | 对外品牌、研究内容、实体信息与会员服务入口 | 访客、读者、会员 | 呈现经批准公开的数据和内容，不成为事实数据主库 |
| DAC | 私有数据资产中心，登录后的默认入口为全球情报总览 Dashboard | 研究员、数据运营、编辑、管理者 | Source、Document、Evidence、Claim、Entity、Relationship、Event、Metric 等权威数据 |
| Intelligence Workspace | DAC 内部情报工作区，不是平行数据中心 | 分析师、研究员 | 监测对象、变化检测、事件分析、趋势信号、预警和研究候选 |
| Research Studio | 研究项目、证据综合、写作、评测与发布生产系统 | 研究员、编辑、Agent | 研究项目、研究过程、报告版本和内容生产状态 |
| Agent Runtime | 跨业务域的模型、Agent、工具与自动化运行底座 | 内部系统与授权 Agent | Agent 定义、权限、运行记录、模型/工具调用审计、成本和评测 |

<b>产品关系：</b> 一个统一平台、多个业务应用、一个权威数据底座、统一身份与权限、可追溯的研究和内容生产链路。

# 2. 不可违反的系统边界

1. DAC 是事实型数据和证据的唯一权威来源。任何业务页面、情报应用或 Agent 不得另建与 DAC 冲突的实体主库。
2. 官网是公开消费端。官网只访问 Public API / Public Projection，不得直连 DAC 生产数据库、内部 Schema、Raw Vault、ReviewTask、AgentRun、内部管理 API 或内部对象存储。
3. Intelligence Workspace 属于 DAC 应用层。其 Watchlist、监测规则、预警和分析记录可以有独立业务表，但必须引用 DAC 稳定 ID。
4. Research Studio 使用 DAC 的 Source / Evidence / Claim / Entity 等稳定对象 ID；研究过程和报告版本不覆盖原始证据。
5. Agent 只能通过授权 API / MCP / Tool Adapter 访问数据和任务；不得持有数据库超级用户凭证，不得绕过服务层直写核心表。
6. 公开内容、内部研究、受限资料和个人信息必须按分类与权限隔离。许可未知默认拒绝公开、付费展示和向外部模型发送。
7. 旧版工作台、旧采集脚本和历史数据仓库均视为可评估的遗留资产，不自动成为新平台的技术依赖。

# 3. 目标逻辑架构

访问与服务关系如下：

- Public Users → CDN/WAF → Public Web（Next.js）→ Public API → Publication / Public Projection。
- Internal Staff / Agents → Private Access Gateway（VPN / Zero Trust + MFA）→ DAC Admin、Intelligence Dashboard、Research Studio、Agent Runtime。
- DAC Domain Services（FastAPI modular monolith）→ PostgreSQL Canonical Store、私有 Raw Vault、异步 Worker、Quality / Review / Audit。
- Source Adapters → Raw Vault → Parse / Normalize → Entity Resolution → Quality Gate → Review → Canonical Store。
- Public Projection 是唯一允许官网消费的数据出口；缓存和搜索索引均为可重建派生层。

架构原则：模块化单体优先；API 和 Worker 分进程部署；领域边界先于微服务拆分；搜索索引、缓存和向量索引均为可重建派生层，不是事实来源。

# 4. 技术基线与冻结决策

| 层 | 冻结基线 | 约束 |
| --- | --- | --- |
| Web 前端 | Next.js App Router + TypeScript | SSR/SSG/ISR；公共页面可索引；组件与设计 Token 统一 |
| 后端 API | Python + FastAPI | REST /api/v1；OpenAPI 为契约事实来源 |
| 数据库 | PostgreSQL 16 作为首期唯一主关系数据库 | 托管版本/补丁在部署 ADR 锁定；逻辑模型不依赖单一云厂商 |
| ORM / Schema / Migration | SQLAlchemy 2.x / Pydantic 2.x / Alembic | 迁移脚本必须可重复、可回滚或有补偿方案 |
| 原始文件 | S3 兼容私有对象存储 | 原始对象不可静默覆盖；哈希、版本和生命周期记录齐全 |
| 异步任务 | Celery Worker + Redis Broker；PostgreSQL Outbox 为投递事实源 | Redis 可重建，不承载唯一任务事实；统一队列，不得多套并存；先通过本地/Shared Dev 运维 Spike 后进入 Staging |
| 搜索 | 首期 PostgreSQL FTS + pg\_trgm | 真实负载证明不足后再引入 OpenSearch |
| 图关系 | 首期 PostgreSQL 关系表 | 多跳查询性能成为瓶颈后再评估图数据库 |
| 向量检索 | 非首期硬依赖 | 可后续评估 pgvector；向量不得成为事实源 |
| 本地环境 | Docker Compose | Local、Shared Dev、Staging、Production 配置隔离 |
| Identity | OIDC-compatible identity boundary；内部员工/Agent 身份与外部会员身份分离 | 内部管理强制 MFA；RBAC 与 Entitlement 分离；身份供应商需通过地域/合规/预算 ADR |

<b>技术版本纪律：</b> 上述是主版本/技术边界，不代表所有 patch 版本已安装。每个仓库必须提交 lockfile、容器镜像版本和软件物料清单（SBOM）；具体版本只在实际兼容性验证后写入 ADR，不得凭文档臆造“已锁定版本”。

# 5. 仓库与工程组织

目标正式代码仓库建议：dls2049/vathen-platform（当前尚未核实存在，需由任务建立；不得假定已经创建）。

推荐 Monorepo 结构：

- apps/web：Next.js 公共官网
- apps/api：FastAPI 模块化单体
- apps/worker：异步采集/处理/通知 Worker
- apps/admin：DAC 内部管理与情报工作台
- packages/contracts：OpenAPI、事件与共享契约
- packages/ui：Web UI 与 Design System
- packages/domain：领域规则与类型
- packages/adapters：外部来源适配器
- packages/agent\_runtime：Agent、Model Gateway、Tool Registry
- migrations、infra/docker、infra/ci、infra/deploy
- tests/unit、contract、integration、e2e、fixtures
- docs/adr、docs/api、docs/runbooks、docs/security

仓库策略：

- main 仅接收通过 PR、CI 和 review 的代码；保护分支、禁止直接推送。
- 功能分支命名 feat/DOMAIN-TASK-ID，修复 fix/DOMAIN-TASK-ID，紧急修复 hotfix/TASK-ID。
- 每个 PR 必须关联任务 ID、冻结文档版本、测试证据、迁移影响、回滚说明。
- 生产密钥只存在 Secret Manager / GitHub Environments；.env.example 只保留变量名和说明。
- 所有 DB 迁移有唯一 revision、升级/降级策略和空库重建测试。

# 6. 统一数据流与发布流

## 6.1 数据进入 DAC

Source Registry → License Gate → Adapter → Raw Vault → Parse → Normalize → Deduplicate → Entity Resolution → Evidence / Claim Candidate → Quality Gate → Review（按风险）→ Canonical Store。

## 6.2 研究生产

Research Candidate → Research Project → Research Plan → Source / Document → Evidence → Claim → Counter-evidence → Analysis → Report Draft → Fact Check → Editorial Review → Publication。

## 6.3 官网发布

Approved Content / Entity / Event → Publication → Public Projection（字段白名单 + 许可依据 + 审批版本）→ Public API → Website Cache / ISR。

撤回/更正必须产生新版本和审计事件，触发缓存失效；不得通过直接改数据库或删除旧记录完成静默修正。

# 7. 身份、权限与安全模型

- 统一身份域区分外部用户、内部员工、服务账号和 Agent 身份。
- RBAC 角色至少包括：Platform Admin、Data Operator、Researcher、Editor、Reviewer、Engineer、Read-only Analyst、Agent Service。
- 权限采用“主体 × 资源分类 × 动作 × 条件”判定；前端隐藏按钮不构成安全控制。
- 外部用户权益（Free / Paid / Team）与内部员工角色分离；会员权益不赋予 DAC 内部访问权。
- 管理入口必须 MFA；数据库和对象存储不暴露公网；所有敏感操作记录 AuditLog。内部身份接口保持 OIDC 兼容；若首期自建账号，密码使用 Argon2id、会话 Cookie 使用 Secure/HttpOnly/SameSite，刷新凭证轮换并存哈希。外部会员身份与内部员工/Agent 身份隔离。
- Agent 使用短期身份/令牌、工具白名单、资源范围、预算、超时和并发限制。
- 对外模型路由前执行数据分类、供应商条款、调用地域和数据外发策略检查。
- 安全事件、来源撤回、版权投诉、用户数据请求均有可执行 Runbook。

# 8. 中国大陆首发环境与资源边界

已知项目背景：首发市场为中国大陆；运营主体为中国大陆公司。已有资源盘点记录为腾讯云上海轻量服务器 1 台（2 核 / 2 GB / 40 GB / 3 Mbps），未核实到可用的托管 PostgreSQL、COS、Redis、VPC、VPN 等配套生产资源；历史安全组端口开放问题需复核。预算讨论区间为每月人民币 1,500–3,000 元，尚需用同口径报价验证。

冻结原则：

1. 不将现有 2C2G 轻量服务器视为 DAC 生产底座；它最多作为临时测试/跳板候选，须先完成安全复核。
2. 首期云环境按中国大陆市场和适用法规进行数据分类、驻留和跨境评估；中国首发不自动推出所有数据必须境内存储。
3. 腾讯云可作为优先报价候选，但地域、CVM、托管 PostgreSQL、COS、Redis、网络、安全、备份和实际月费未获批准前，不创建资源、不采购。
4. 生产密钥、个人信息、受限全文和重要数据不得未经评估发送到境外模型/分析服务。
5. 生产环境至少与开发/测试隔离；备份具备独立权限，恢复演练先于生产上线。

# 9. 实施顺序与依赖

| 阶段 | 交付目标 | 进入条件 | 退出 Gate |
| --- | --- | --- | --- |
| G0 工程基线 | 仓库、CI、环境、ADR、威胁模型 | 代码资产盘点 | 空环境可启动，主干 CI 通过 |
| G1 DAC Core | ERD、迁移、Source、Raw Vault、核心对象 | G0 通过 | 空库迁移、约束、权限测试通过 |
| G2 数据闭环 | 首个 Adapter、标准化、消歧、质量、审核 | G1 通过 + 来源许可 | 可回放 E2E，许可未知被拦截 |
| G3 内部情报工作台 | DAC Dashboard、实体/事件/来源/质量工作区 | G2 样本数据可用 | 所有 KPI 可下钻且有口径/时间 |
| G4 发布接口 | Publication、Public Projection、Public API | G2 质量与审核可用 | 官网身份无法读取内部数据 |
| G5 官网 MVP | 双语品牌站、研究内容、搜索与实体页 | G0 可并行；真实数据依赖 G4 | 页面/SEO/权限/E2E 通过 |
| G6 商业与高级能力 | 会员支付、监测通知、高级检索、Agent 自动化 | 产品/法律/成本决策 | 端到端验收和运营演练通过 |

官网品牌、静态 UI、内容原型可以与 G1/G2 并行；真实实体/事件数据和会员付费内容接入必须等待 G4。

# 10. 冻结文档权威顺序

1. 本文《全平台产品与工程冻结基线 V1.0》：系统边界、全局架构和跨平台决策。
2. 《DAC 产品与工程冻结规格 V2.0》：DAC 领域模型、内部工作台、数据处理、治理与 API。
3. 《先知官网产品与工程冻结规格 V3.0》：公开站点产品、页面、CMS/发布、SEO、会员边界。
4. ADR：某项技术决策的唯一记录；已批准 ADR 优先于旧提案。
5. OpenAPI / ERD / Design Tokens：机器可验证的接口、数据与视觉契约。
6. 开发任务看板：唯一任务状态来源，不得改写上述规范。
7. 旧 V1.x/V2.x 文档：历史依据或未冲突的参考；冲突时由本套冻结文档取代。

# 11. Definition of Ready / Definition of Done

任务进入 Ready 必须具备：唯一 ID、业务目标、对应冻结条款、输入/输出、依赖、权限与数据分类、验收标准、测试方法、回滚/失败处理。

任务完成必须具备：

- 代码与 PR / Commit 可定位；
- 自动化测试通过，包含适用的 unit / contract / integration / E2E；
- 数据迁移与兼容性说明（如适用）；
- 安全/权限/许可测试通过；
- 部署环境、版本、日志或 CI 证据；
- 已知限制、未完成项和回滚方式；
- 开发 Agent 只能提交待验收，独立 QA/CI 才能自动或人工结项。

# 12. 明确不在本次冻结范围内

- 具体云厂商、地域、付费规格和采购；需预算与账号核验后单独批准。
- 法律意见、跨境数据结论、特定来源商业许可；必须逐项评估。
- 会员价格、具体权益配额、支付渠道和退款政策；需商业/法务冻结。
- 未经真实负载验证的微服务拆分、Kafka、Spark、Neo4j、OpenSearch、独立向量数据库。
- 任何未提供仓库、commit、测试和部署证据的“已实现”声明。

# 13. 变更记录

- V1.0｜2026-11-28：统一官网与 DAC 系统边界、技术基线、数据流、权限、安全、仓库结构、部署约束和开发 Gate；将具体生产资源与法律事项保留为显式批准门槛。

# 14. Agent 自主执行与升级规则

本项目默认采用“授权范围内自主执行 + 独立机器验收 + 自动结项”，不要求负责人逐任务点击批准。

Agent 在任务 Ready 且权限有效时，可以自主读取规格、领取任务、创建分支、开发、运行测试、修复失败、提交 PR/Commit、回填进度和证据。CI/独立 QA Agent 按冻结验收标准自动验收；全部机器门禁通过、交付证据齐全且无风险标记时，可自动结项。

开发 Agent 不得自行批准自己的交付；QA Agent 与开发 Agent 必须职责隔离。失败时自动退回修复并按重试上限重试，超过上限自动标记阻塞并附诊断。

仅以下情况必须升级人工：云资源采购/付费、生产密钥或权限提升、个人信息/受限数据/可能重要数据向外部服务发送、许可或法律边界不明、不可逆生产迁移/删除、真实支付/退款、正式对外发布/代表 VATHEN 承诺、预算超限或安全事件。升级只阻断该高风险动作，不应停止其他无风险任务。

- Agent Run 必须记录 agent\_key/version、task\_id、input/output refs、model/tool calls、cost、trace\_id、commit、测试结果和权限决策。
- 幂等键、并发锁/乐观锁、重试策略、审计和回滚/补偿必须在 Task Bridge 与执行 Runtime 中实现。
- 自动结项条件必须是可机器验证的 Acceptance Criteria；不能以“Agent 自称完成”作为结项依据。

## 11.1 开发任务状态机与 Agent 更新权限（补充冻结）

任务状态采用“Agent 自主推进、独立 QA 验收、系统自动关闭、人工处理例外”。

| 状态 | 允许的状态更新主体 | 进入条件 | 必需记录 |
| --- | --- | --- | --- |
| 待开始 | 任务管理员 / 系统 | 任务已建立、依赖满足 | task\_id、priority、spec\_version、依赖 |
| 进行中 | Agent / 系统 | Agent 原子领取任务并获得授权 | agent\_id、run\_id、started\_at、branch、heartbeat |
| 待验收 | 开发 Agent | 实现完成且提交交付包 | commit/PR、变更摘要、测试结果、预览地址、风险和回滚说明 |
| 验收中 | 独立 QA Agent / 系统 | QA 已领取验收任务 | qa\_run\_id、验收矩阵版本、测试环境、开始时间 |
| 已完成 | 独立 QA Agent / 系统 | 全部阻断级验收项通过，证据可复核 | QA 结论、测试报告、验收时间、交付 commit |
| 验收失败 | 独立 QA Agent / 系统 | 任一阻断级验收项失败 | 失败项、复现步骤、日志、修复建议 |
| 阻塞中 | Agent / 系统 | 依赖、权限、环境或外部决策阻止继续 | blocker\_type、说明、影响范围、所需处理方、下一次检查条件 |

### 权限边界

1. 开发 Agent 可领取任务、更新进行中、提交待验收、补充证据、报告阻塞；不得直接把任务设置为已完成。
2. 独立 QA Agent 使用与开发 Agent 分离的身份和运行记录；不得由同一 Agent Run 同时担任实现者与最终验收者。
3. QA 全部通过后，Task Service 自动将状态更新为已完成；普通任务不需要人工逐项确认。
4. QA 失败自动退回进行中并附失败清单；修复后重新提交验收，保留每次验收历史。
5. 任务状态更新必须通过受控 Task API / MCP Tool，不允许 Agent 直接写数据库或绕过权限服务。
6. 更新采用乐观锁/version 或状态迁移 CAS，支持 Idempotency-Key；重复提交不得造成重复状态迁移。
7. 每次状态迁移写入不可变 Audit Log：actor、actor\_type、from/to、timestamp、reason、task\_version、run\_id、evidence\_refs。
8. Agent 心跳超时由调度器检测；任务可回收并重新分配，但须保留旧 Run 和已有分支/提交，不得静默覆盖。
9. 人工审批仅用于高风险 Gate：生产密钥/权限提升、云资源采购或预算超限、生产数据不可逆删除/迁移、受限数据导出、真实支付/退款、法律/版权不确定事项、安全事件、公开发布或对外承诺。
10. 人工 Gate 只阻断对应高风险动作；Agent 可继续执行其他不依赖该动作的安全任务。

### 自动验收门槛

- CI：lint、type check、unit、contract、integration、build 均按任务适用性通过。
- 交付：PR/commit 与任务 ID、冻结规格版本、ADR、变更文件和迁移说明关联。
- QA：独立 QA 根据任务验收标准运行；不得只采信开发 Agent 自报结果。
- 安全：权限、敏感数据、密钥、公开数据隔离检查通过。
- 可追溯：日志、报告、截图/预览、测试环境和版本可定位。
- 例外：不适用的检查必须记录理由；阻断项不得通过“豁免”静默跳过。

### 推荐看板字段

task\_id、title、status、priority、assignee\_agent\_id、qa\_agent\_id、dependency\_ids、spec\_version、branch、pr\_url、commit\_sha、started\_at、submitted\_at、qa\_started\_at、completed\_at、progress\_note、blocker\_type、blocker\_detail、acceptance\_evidence、task\_version、last\_heartbeat\_at。

此状态机为开发进度看板与未来 Task Bridge 的权威规则。Notion 是当前任务状态的人工可读事实源；网站静态快照不得冒充实时状态。实时任务看板必须经服务端 Task API 读取/写入，并实施身份鉴权、审计和并发控制。
