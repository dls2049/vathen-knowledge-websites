<!-- Synced from Notion on 2026-11-28. Notion remains the source of truth. -->
# 🏛️ VATHEN DAC 产品与工程冻结规格 V2.0

Source: https://app.notion.com/p/426f15aabd2c8156abd5e51bd4de68db

## 配套机器实现契约

<mention url="https://app.notion.com/p/426f15aabd2c81ffa512f057074386d2">VATHEN DAC 核心数据字典、状态机与 API 契约 V2.0</mention> 是本文件的实施附录，冻结字段字典、索引、状态机、API 路由组和权限矩阵。数据库迁移与 OpenAPI 必须以两份文件为共同基线。

# 文档控制

- 文档编号：DAC-PRD-ENG-001
- 版本：V2.0
- 基线日期：2026-11-28
- 状态：产品与工程冻结基线（Frozen Baseline）；来源许可、生产资源和具体法规适用性逐项 Gate
- 适用对象：DAC 产品经理、数据架构师、后端、数据工程、前端、QA、DevOps、研究运营和 Agent

# 1. 产品定义与成功标准

DAC（VATHEN Data Asset Center）是 VATHEN 私有数据资产和情报基础设施，不是普通数据库，也不是官网 CMS。它承担六项核心能力：Store（存储）、Acquire（采集）、Judge（判断与质量）、Provenance（来源与证据追溯）、Serve（受控服务）和 Govern（权限、许可、审计与生命周期治理）。

DAC 登录后的默认首页是「全球情报总览 Dashboard」。全球情报中心属于 DAC 内部应用域，不是独立于 DAC 的第二套系统。

成功标准：

- 每条规范事实可追溯来源、版本、采集时间、证据和审核状态。
- 所有采集均通过统一 Adapter / Pipeline，不允许 Agent 直接写正式事实表。
- 许可未知、实体未消歧、高风险关系未经审核的数据不能进入公开服务层。
- 内部 Dashboard 的每个 KPI 可下钻到记录，并展示口径、更新时间和数据状态。
- 官网只能消费已批准的 Public Projection / Public API。

# 2. DAC 信息架构（内部工作台）

| 顺序 | 一级模块 | 主要页面/能力 |
| --- | --- | --- |
| 01 | 全球情报总览 | 资产规模、全球动态、重点实体、产业技术分布、趋势信号、数据健康、AI 简报 |
| 02 | 实体情报中心 | 人物、企业/组织、机构、行业、技术；档案、别名、标识符、关系、历史变化 |
| 03 | 技术与科研情报 | 论文、作者、机构、专利、技术路线、研发信号 |
| 04 | 企业与资本情报 | 公司公告、财报、股票/市场数据、融资、并购、供应链 |
| 05 | 新闻与事件中心 | 新闻流、转载聚类、事件、影响实体、事件时间线 |
| 06 | Research Radar | 趋势信号、变化发现、研究候选、研究项目转化 |
| 07 | 数据源管理 | Source Registry、许可、Adapter、采集计划、运行历史、配额 |
| 08 | 数据质量与审核 | 实体消歧、重复、证据、冲突、质量问题、Review Queue、发布审核 |
| 09 | AI 情报分析 | Agent 运行、研究简报、分析草稿、反证、不确定性 |
| 10 | 系统运行与治理 | 用户/角色、API 健康、Worker、成本、审计、备份和恢复 |

## 2.1 角色与权限

- Platform Admin：系统设置、账号、权限和安全策略。
- Data Operator：来源注册、采集计划、失败任务和数据质量处理。
- Researcher / Analyst：研究查看、实体/事件分析、趋势候选和证据提交。
- Editor：研究内容编辑、稿件流程管理。
- Reviewer：按授权审核 Claim、Relationship、Event、Publication。
- Engineer / Agent Operator：运行状态、日志、工具和系统诊断；不自动获得业务发布权。
- Read-only Analyst：按数据分类只读访问。
- Agent Service：仅能通过白名单工具操作获授权资源。

数据运营者不得因能管理采集而自动拥有公开发布审批权；开发 Agent 不得自行把任务或内容标记为业务验收完成。

# 3. 数据域与核心对象

## 3.1 核心对象清单

| 对象 | 作用 | 关键字段/约束 |
| --- | --- | --- |
| Source | 信源主体 | source\_key、名称、域名、类型、地区、语言、状态 |
| SourceLicense | 来源许可快照 | terms\_url、license\_id/version、用途权限、商用/缓存/展示/再分发、有效期、审核状态 |
| SourceSnapshot | 一次来源获取的快照 | source\_id、external\_id、fetched\_at、source\_updated\_at、hash、raw\_uri |
| Document | 可识别文档/内容 | 类型、标题、语言、来源、外部标识、状态 |
| DocumentVersion | 不可覆盖的文档版本 | document\_id、version、content\_hash、raw\_object\_uri、parser\_version |
| Evidence | 支持某项判断的精确证据 | document\_version\_id、locator/page/offset、quote/snippet、hash、classification |
| Claim | 可检验陈述 | subject、predicate、object/value、valid\_time、confidence rationale、status |
| ClaimEvidenceLink | Claim 与 Evidence 多对多 | relation\_type、support/refute/context、权重/说明 |
| Entity | 规范实体 | UUID、type、canonical\_name、slug、status、primary\_language |
| EntityAlias | 多语言名称/别名 | entity\_id、locale、alias、alias\_type |
| EntityIdentifier | 外部稳定标识 | entity\_id、namespace、value、source\_id、validity |
| EntityProfile / Translation | 类型化档案和本地化字段 | 不因语言重复 Entity 主记录 |
| EntityRelationship | 实体间关系 | subject\_id、predicate、object\_id、valid\_from/to、status |
| RelationshipEvidence | 关系证据 | relationship\_id、evidence\_id、support/refute |
| Event | 现实世界事件 | event\_type、occurred\_at、status、impact/importance |
| EventSource / EventEntityLink | 事件来源和影响实体 | 必须可追溯 |
| MetricDefinition | 指标口径 | key、unit、currency、periodicity、methodology |
| MetricObservation | 指标观测 | entity\_id、value、unit、period、dimensions、evidence\_id、reported\_at、restatement |
| IngestionJob / ProcessingRun | 采集和处理任务 | cursor、watermark、attempt、status、metrics、error\_class |
| QualityIssue / ReviewTask | 质量问题和审核任务 | target、rule、severity、decision、reviewer、reason |
| AuditLog | 不可静默覆盖的审计 | actor、action、target、before/after hash、request\_id、time |
| AgentDefinition / AgentRun | Agent 定义与运行 | version、tools、input/output refs、risk、cost、trace |
| ModelCall / ToolCall | 模型和工具调用 | provider/model/prompt/tool version、scope、latency、cost、result ref |
| Publication / PublicProjection | 发布工作流与公开数据投影 | approved\_fields、license\_basis、version、approval、published/withdrawn |

## 3.2 统一字段与时间

- 主键统一 UUID；外部 ID、slug、ticker、DOI、CIK、ROR、Wikidata ID 只能作为 Identifier，不作为 DAC 主键。
- 时间存 UTC timestamptz；保留 published\_at、occurred\_at、acquired\_at、processed\_at、valid\_from/to、recorded\_at、superseded\_at。
- 数值存 value + unit + currency + period + dimensions + methodology；禁止丢失财报口径、期间和维度。
- 原始来源和 DocumentVersion 不可静默覆盖；修订创建新版本并建立 supersedes 关系。
- Claim、Relationship、Event 的历史变化可回溯；事实有效时间与系统获知时间分开。

## 3.3 分类与权利字段

每项资产必须可判定 classification：public / internal / confidential / restricted；rights\_status：unknown / metadata\_only / link\_only / licensed\_fulltext / open\_fulltext / restricted / expired；public\_status：not\_eligible / pending\_review / approved / published / withdrawn。

unknown 默认拒绝公开展示、付费分发、批量导出和外部模型处理。许可权限需细分采集、存储、摘要、全文、商用、缓存、衍生数据库、再分发、模型处理、地域和期限。

# 4. 数据状态机与质量门禁

## 4.1 数据处理状态

queued → fetching → fetched → parsed → normalized → deduplicated → entity\_resolved → quality\_checked → review\_pending → approved / rejected / quarantined → published。

失败分为 transient、rate\_limited、auth、permanent、schema\_changed、license\_blocked；仅可重试的类别使用指数退避与抖动。所有任务支持幂等键、checkpoint、attempt、cursor/watermark 和 DLQ。

## 4.2 Claim 状态

proposed → supported / partially\_supported / disputed / refuted / outdated / withdrawn。

Claim 状态变化必须保存操作者、时间、理由和 Evidence。多个模型复述同一来源不构成独立佐证。

## 4.3 实体状态

draft → pending\_review → published → deprecated / merged。

合并必须保存 survivor ID、redirect、旧 ID、字段冲突决策、关联迁移和审计；高风险实体不得只凭姓名相似自动合并。

## 4.4 质量分层 T0–T4

- T0 Raw：原始资料隔离，仅内部授权角色访问。
- T1 Parsed Candidate：已解析候选，不代表规范事实。
- T2 Normalized：已规范化，来源和许可字段齐全，但可能待审核。
- T3 Reviewed：通过规则及必要审核，可按字段策略公开。
- T4 High Assurance：高影响信息完成独立证据复核、人工审核和版本记录。

禁止自动发布：许可未知；关键实体未消歧；高影响 Claim 无合格证据；任职/控股/财务等高风险关系未审核；存在重大来源冲突；来源撤回或许可到期。

# 5. Source Adapter 与数据流水线

每个 Adapter 实现统一契约：

- source\_key、capabilities()、validate\_config()、health\_check()
- plan\_sync(scope, cursor)、fetch\_page(plan, cursor)
- parse(raw\_response)、normalize(source\_record)
- checkpoint(cursor, watermark)、classify\_error(error)

统一 Envelope 至少包含：source\_key、external\_record\_id、record\_type、source\_record\_url、fetched\_at、source\_updated\_at、raw\_object\_uri、content\_hash、license\_id、rights\_status、adapter\_version、parser\_version、normalized\_payload。

流水线：

1. Source Registry 与许可门禁。
2. Schedule：按来源频率、配额和优先级生成任务。
3. Fetch：认证、限速、分页、条件请求。
4. Raw Vault：先落原始响应，SHA-256，私有存储，不覆盖。
5. Parse / Normalize：保留映射和解析版本。
6. Deduplicate：外部 ID、DOI、专利号、监管 accession、URL、内容 hash。
7. Entity Resolution：候选匹配、理由和置信度；高风险合并人工审查。
8. Evidence / Claim Candidate：定位原文片段，记录抽取模型与版本。
9. Quality Gate：Schema、来源、许可、时效、冲突、独立性检查。
10. Review：按风险和数据域派发。
11. Publish：只发布获准字段。
12. Reconcile：来源更新、删除、撤稿、版本漂移对账。

## 5.1 首批来源顺序

- Pilot 0：Wikidata 定向实体子集，用于验证 Identifier / Alias / Entity / Relationship 候选闭环；正式启用前仍须记录当前条款与许可快照。
- P0 扩展：ROR、Crossref、OpenAlex、SEC EDGAR；按来源许可、字段用途、API 稳定性和真实研究价值逐项接入。
- P1：EPO OPS、Europe PMC；GDELT 仅在商业用途、缓存和再分发许可审查通过后接入。
- ORCID Public API 不进入营收产品自动化生产链路，除非取得适用授权。
- 不全量镜像数据源；优先围绕 VATHEN 重点实体、主题和研究任务定向采集。

# 6. DAC 全球情报总览 Dashboard

Dashboard 默认首页展示：

1. 核心资产：人物、企业、机构、技术、论文、专利、新闻、事件数量。
2. 全球动态：近 24h / 7d 重要事件、关联实体、来源等级和审核状态。
3. 重点监测：关注等级、最新变化、待核验、长期未更新对象。
4. 产业与技术：行业、技术主题、国家/地区分布。
5. 趋势信号：Research Radar 候选、证据强度、反证和研究转化状态。
6. 数据健康：来源可用性、采集成功率、队列积压、重复/未解析、证据覆盖和许可待审。
7. AI 简报：重点变化、潜在影响、反证、不确定性和原始证据入口。

每个 KPI 必须具备定义、计算窗口、分母/过滤条件、更新时间、状态拆分和下钻路径。状态至少区分 candidate、verified、source\_linked、endpoint\_tested、ingesting、reviewed、published。候选建档不等于实时监测；来源绑定不等于 API 已连通；接口测试不等于持续采集；已审核不等于许可允许公开。

无真实数据时显示「尚未接入 / 待验证」，不得用模拟数据伪装实时数据。Dashboard 的图表、列表和数量必须能下钻到记录。

# 7. API 与服务边界

- 内部 API：/api/v1/internal/...，仅私有网络/授权身份；按 RBAC 和资源分类过滤。
- Admin API：写操作需角色授权、审计、幂等键和字段白名单。
- Public API：/api/v1/public/...，只读 PublicProjection；独立只读数据库角色/Schema 或发布服务；禁止访问内部表。
- Adapter 不允许直写 PublicProjection。
- API 使用 JSON、OpenAPI、统一错误结构 code/message/details/request\_id；cursor 分页优先；过滤/排序字段白名单。
- 对象存储默认私有；外部下载使用短时签名 URL，并校验发布状态和许可。
- API 版本、字段弃用、缓存、速率限制和错误码进入契约测试。

# 8. 安全、权限与运营

- PostgreSQL 不暴露公网；生产环境私有子网；管理访问经 VPN/零信任 + MFA。
- 密钥进入 Secret Manager；禁止在 Git、Notion 正文、日志和 URL query 中出现。
- 原始对象加密、版本化、生命周期管理；开发环境只用合成或脱敏样本。
- Agent 通过工具白名单访问；无数据库超级权限；写操作需要 schema validation、权限判定和审计。
- 模型路由必须执行数据分类、供应商条款、区域、预算和质量策略；不合规时 fail closed。
- 每日备份/PITR 为设计要求候选；最终 RPO/RTO 与保留周期通过部署 ADR 和恢复演练确定。
- 监控：采集/处理成功率、延迟、重试、DLQ、来源配额、许可到期、解析失败、实体未解析、重复率、Evidence 覆盖、API 延迟、成本和异常访问。

# 9. DAC 首期交付范围

P0 必须完成：

- DAC Core ERD、SQL Migration、数据分类/权限字段、审计基础。
- Source Registry、SourceLicense、Raw Vault、统一 Adapter SDK。
- 一个获准来源的端到端 Adapter Pilot。
- Document / Evidence / Claim / Entity / Relationship 最小闭环。
- Quality Gate、Review Queue、发布状态与 PublicProjection 最小版本。
- DAC Dashboard 基础框架，真实数据接通后展示可下钻 KPI。
- 内部 API / Public API 隔离、RBAC、权限测试和 CI。
- 空环境部署、备份与恢复演练 Runbook。

P1：

- P0 来源扩展、新闻聚类、事件时间线、指标观察、Entity Resolution 精度提升。
- Admin 完整运营流程、情报筛选和研究候选。
- 多模型 Gateway、Agent Runtime、评测与成本治理。
- 官网发布接口完整撤回/更正/缓存失效。

P2：

- 复杂产业链图谱、多跳检索、个性化监测、自动简报、机构 API、分析仓库。
- 只有真实用户价值、数据许可和运维成本验证后才启动。

# 10. 验收测试矩阵

| 测试域 | 必测场景 | 通过标准 |
| --- | --- | --- |
| Migration | 空库升级、重复执行、回滚/补偿 | schema 与 ERD 一致；无手工步骤 |
| Provenance | Entity/Claim/Relationship 回溯 | 100% 正式事实有来源定位和时间 |
| License | unknown/restricted 数据发布尝试 | 100% 被拦截 |
| Adapter | timeout、429、503、401、分页中断、schema drift | 限速、重试、checkpoint、quarantine 正确 |
| Idempotency | 同一来源同一版本重复运行 | 不产生重复规范记录 |
| Entity Resolution | 同名、别名、多语言、母子公司 | 高风险匹配进入审核；合并可审计 |
| Review | 退回、通过、撤回、更正 | 状态和审计完整 |
| Public Isolation | Public API 尝试读取内部对象 | 权限拒绝；无内部字段泄漏 |
| Dashboard | KPI 下钻、无数据、过期数据 | 口径、时间、状态和空状态清晰 |
| Resilience | Worker 中断、对象存储失败、队列积压 | 可恢复、可重放、可告警 |
| Security | 越权、密钥扫描、对象私有访问 | 阻断项全通过 |

# 11. Gate 与未决项

<b>架构冻结项：</b> DAC 属于私有数据底座；Dashboard 是默认首页；模块化单体 + Worker；PostgreSQL 主库；Raw Vault 私有对象存储；Adapter 统一契约；T0–T4 数据门禁；Public Projection 隔离；Agent 不直写核心表。

<b>生产启用前阻塞：</b>

- 云厂商/地域/规格/网络/备份与月费须依据实际报价和预算批准。
- 逐来源许可矩阵必须明确采集、存储、商用、摘要、缓存、展示、再分发和模型处理权限。
- 中国大陆适用的隐私、网络数据、版权、跨境和行业规则需专业合规评估；本文件不构成法律意见。
- 真实用户/会员数据的身份、保留、删除和访问策略需另行批准。
- 269 条候选实体历史基线只能标为候选监测对象，除非重新核验不得展示为实时监测实体。

# 12. 文档权威性与变更

本文件 V2.0 取代旧《DAC 总体架构 V1.2》《核心数据模型 V1.0/V1.1 扩展建议》《Sprint 0 执行包》中与本文件冲突的提案。旧文档保留为来源和历史记录；未冲突的来源研究、字段说明和 Adapter 细节继续参考。物理 ERD / OpenAPI / SQL Migration 由后续任务生成并与本文件保持一致。

- V2.0｜2026-11-28：合并产品定位、Dashboard、数据模型、状态机、许可、Adapter、质量、API、权限和验收要求，建立 DAC 单一冻结入口。
