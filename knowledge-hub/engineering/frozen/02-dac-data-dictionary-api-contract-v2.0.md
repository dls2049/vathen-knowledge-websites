<!-- Synced from Notion on 2026-11-28. Notion remains the source of truth. -->
# 🧩 VATHEN DAC 核心数据字典、状态机与 API 契约 V2.0

Source: https://app.notion.com/p/426f15aabd2c81ffa512f057074386d2

# 文档控制

- 文档编号：DAC-CONTRACT-001
- 版本：V2.0
- 日期：2026-11-28
- 状态：DAC 冻结规格的机器实现附录；与《DAC 产品与工程冻结规格 V2.0》共同生效
- 用途：供后端、数据工程、前端、QA 和开发 Agent 实现数据库、API、状态机和契约测试

# 1. 通用数据库规范

- 主键：UUID；数据库内部主键不使用外部 ID、slug、ticker、DOI 或 URL。
- 时间：UTC timestamptz；日期型业务值保留原始时区/来源时区说明。
- JSON：仅用于来源原始 payload、类型化属性扩展、限定条件和审计差异；可查询核心字段必须有正式列。
- 命名：数据库表和字段使用 snake\_case；API JSON 使用 snake\_case；枚举值使用 lowercase snake\_case。
- 软删除：核心事实对象不做无痕物理删除；采用 withdrawn/deprecated/superseded/merged 状态并保留审计。
- 多语言：Entity 主记录不按语言复制；EntityAlias / EntityTranslation 分离。
- 所有业务表至少具有 created\_at、updated\_at；需要操作者追踪的表增加 created\_by、updated\_by。
- 所有外部来源对象必须保留 source\_id、external\_record\_id 或可复核的 source locator。

# 2. 核心表字段字典（V2.0）

以下为首期必需字段。工程师可增加非破坏性字段，但不得删除、改义或放宽关键约束；破坏性变更必须提交 ADR 和迁移计划。

## 2.1 source\_registry

| 字段 | 类型 | 约束/说明 |
| --- | --- | --- |
| id | UUID | PK |
| source\_key | varchar(100) | NOT NULL UNIQUE，稳定机器键 |
| name | varchar(255) | NOT NULL |
| source\_type | enum | official\_site/api/regulator/research/publisher/media/open\_dataset/manual |
| base\_url | text | 来源主页或 API 根地址 |
| country\_code | char(2) | ISO 3166-1 alpha-2，可空 |
| languages | text\[\] | BCP 47 语言标签 |
| source\_grade | enum | S/A/B/C/D；评级必须附理由 |
| status | enum | draft/active/paused/blocked/retired |
| owner\_role | varchar(80) | 维护责任角色 |
| auth\_secret\_ref | text | 仅存 Secret Manager 引用，不存密钥 |
| rate\_limit\_per\_second | numeric | 来源级限速 |
| max\_concurrency | int | 来源级并发上限 |
| last\_success\_at | timestamptz | 最近成功采集 |
| created\_at / updated\_at | timestamptz | UTC |

唯一约束：source\_key 唯一；同域名可有多个 source\_key（不同 API/许可/用途）。

## 2.2 source\_license

| 字段 | 类型 | 约束/说明 |
| --- | --- | --- |
| id | UUID | PK |
| source\_id | UUID | FK source\_registry |
| license\_key / version | varchar | 许可标识与版本 |
| terms\_url | text | 条款地址 |
| rights\_status | enum | unknown/metadata\_only/link\_only/licensed\_fulltext/open\_fulltext/restricted/expired |
| can\_collect / can\_store | boolean | 采集与存储 |
| can\_summarize / can\_process\_with\_model | boolean | 摘要与模型处理 |
| can\_commercial\_use | boolean | 商业用途 |
| can\_cache / can\_display / can\_redistribute | boolean | 缓存、展示、再分发 |
| attribution\_required | boolean | 是否要求署名 |
| allowed\_regions | text\[\] | 允许处理/展示地区 |
| effective\_from / effective\_to | timestamptz | 许可有效期 |
| review\_status | enum | pending/approved/rejected/expired |
| reviewed\_by / reviewed\_at | UUID/timestamptz | 审核记录 |
| review\_note | text | 理由和限制 |

许可变更创建新版本，不覆盖历史版本。任何公开/付费发布必须引用适用的 source\_license 版本。

## 2.3 source\_snapshot

字段：id UUID PK；source\_id FK；external\_record\_id；source\_record\_url；source\_updated\_at；acquired\_at；http\_status；etag；last\_modified；source\_version；raw\_object\_uri；content\_hash（SHA-256）；mime\_type；byte\_size；rights\_status；license\_id FK；adapter\_version；parser\_version；created\_at。

唯一/幂等键建议：(source\_id, external\_record\_id, source\_version, content\_hash)。没有 external\_record\_id 时以规范 URL + hash 作为回退键。

## 2.4 document / document\_version

Document 字段：id、doc\_type（news/article/report/paper/patent/filing/dataset/announcement/other）、title、canonical\_url、language、publisher\_entity\_id、source\_id、external\_record\_id、published\_at、acquired\_at、status、classification、created\_at、updated\_at。

DocumentVersion 字段：id、document\_id、version\_no、content\_hash、raw\_object\_uri、extracted\_text\_uri、mime\_type、byte\_size、parser\_version、supersedes\_version\_id、created\_at。document\_id + version\_no 唯一；新版本不可覆盖旧版本。

## 2.5 evidence

字段：id、document\_version\_id FK、locator\_type（page/paragraph/line/char\_range/table\_cell/json\_pointer/url\_fragment）、locator\_value、quote\_text（按许可和最小必要原则保存）、excerpt\_hash、language、classification、created\_at、created\_by。

Evidence 必须精确定位 DocumentVersion；定位失效时标记 needs\_revalidation，不静默改写 locator。

## 2.6 claim / claim\_evidence\_link

Claim 字段：id、subject\_entity\_id nullable、predicate、object\_entity\_id nullable、value\_json nullable、claim\_type（fact/analysis/forecast/attribution/metric）、polarity、status（proposed/supported/partially\_supported/disputed/refuted/outdated/withdrawn）、valid\_from、valid\_to、recorded\_at、superseded\_by\_claim\_id、extraction\_method、model\_ref、classification、created\_at、updated\_at。

约束：subject\_entity\_id 与 object\_entity\_id/value\_json 至少满足一种有效表达；事实 Claim 必须有 Evidence Link 才能进入审核通过状态。

ClaimEvidenceLink 字段：id、claim\_id、evidence\_id、support\_type（supports/refutes/contextualizes）、rationale、created\_at。claim\_id + evidence\_id + support\_type 唯一。

## 2.7 entity / alias / identifier / translation

Entity 字段：id、entity\_type（person/organization/industry/technology/topic/product/location/concept）、canonical\_name、slug、primary\_language、summary、status（draft/pending\_review/published/deprecated/merged）、merged\_into\_entity\_id、profile\_json、classification、created\_at、updated\_at、last\_verified\_at。

EntityAlias：id、entity\_id、locale、alias、normalized\_alias、alias\_type（official/short/former/transliteration/translation/other）；按 entity\_id + locale + normalized\_alias 去重。

EntityIdentifier：id、entity\_id、namespace、value、source\_id、is\_primary、valid\_from、valid\_to；namespace + value 唯一（允许按明确命名空间规则配置多主体情况）。

EntityTranslation：id、entity\_id、locale、display\_name、summary、seo\_title、seo\_description、updated\_at；entity\_id + locale 唯一。

## 2.8 entity\_relationship / relationship\_evidence

Relationship 字段：id、subject\_entity\_id、predicate、object\_entity\_id、qualifiers\_json、valid\_from、valid\_to、status（candidate/pending\_review/verified/disputed/rejected/expired/withdrawn）、risk\_level（low/medium/high）、classification、created\_at、updated\_at。

关系谓词必须来自受控词表，至少登记 predicate、domain、range、inverse\_predicate、temporal\_required、minimum\_evidence\_grade、risk\_level。首期词表包括 founded\_by、found、employs、ceo\_of、board\_member\_of、owns、subsidiary\_of、invested\_in、supplies\_to、customer\_of、partner\_of、competes\_with、located\_in、develops、uses\_technology、researches、acquired、spun\_off\_from。不得把相似关系当作同义词混用。

RelationshipEvidence：id、relationship\_id、evidence\_id、support\_type、rationale、created\_at。高风险关系至少需要独立来源复核或明确人工审批。

## 2.9 event / event\_source / event\_entity\_link

Event 字段：id、event\_type、title、summary、occurred\_at、occurred\_to、detected\_at、importance（low/medium/high/critical）、status（candidate/pending\_review/verified/disputed/withdrawn）、event\_cluster\_key、classification、created\_at、updated\_at。

EventSource：event\_id、document\_id、source\_id、independence\_group、is\_primary\_source、created\_at。转载源共享同一 independence\_group，不重复计为独立佐证。

EventEntityLink：event\_id、entity\_id、role（subject/actor/target/affected/mentioned）、created\_at。

## 2.10 metric\_definition / metric\_observation

MetricDefinition：id、metric\_key UNIQUE、name、description、unit、currency、periodicity、aggregation\_method、methodology\_version、status。

MetricObservation：id、entity\_id、metric\_definition\_id、value\_numeric、value\_text、unit、currency、period\_start、period\_end、instant\_date、dimensions\_json、source\_document\_version\_id、evidence\_id、reported\_at、restated\_from\_id、status。数值口径不同的观察值不得直接聚合。

## 2.11 ingestion\_job / processing\_run

IngestionJob：id、source\_id、job\_type、scope\_json、cursor、watermark、status（queued/running/succeeded/partial/failed/canceled）、attempt、max\_attempts、started\_at、finished\_at、error\_class、error\_message\_redacted、metrics\_json、idempotency\_key UNIQUE。

ProcessingRun：id、snapshot\_id、pipeline\_version、step\_key、status、input\_hash、output\_hash、started\_at、finished\_at、error\_class、metrics\_json。

## 2.12 quality\_issue / review\_task / audit\_log

QualityIssue：id、object\_type、object\_id、rule\_key、rule\_version、severity、status（detected/triaged/assigned/investigating/resolved/accepted\_risk/false\_positive）、owner\_role、resolution、created\_at、resolved\_at。

ReviewTask：id、target\_type、target\_id、review\_type、risk\_level、assigned\_role、status（queued/assigned/approved/rejected/needs\_changes/canceled）、decision、decision\_note、reviewer\_id、created\_at、resolved\_at。

AuditLog：id、actor\_type、actor\_id、action、target\_type、target\_id、before\_hash、after\_hash、request\_id、trace\_id、reason、created\_at。只追加，不允许应用层 UPDATE/DELETE；访问受限。

## 2.13 agent\_definition / agent\_run / model\_call / tool\_call

AgentDefinition：id、agent\_key、version、purpose、input\_schema、output\_schema、allowed\_tools、risk\_level、status、created\_at；agent\_key + version 唯一。

AgentRun：id、agent\_definition\_id、trigger\_type、task\_ref、input\_refs、output\_refs、status、started\_at、finished\_at、trace\_id、approval\_state、cost\_total、error\_class。

ModelCall：id、agent\_run\_id、provider、model\_id、model\_version、prompt\_version、region、input\_tokens、output\_tokens、cost、latency\_ms、status、data\_policy\_decision。

ToolCall：id、agent\_run\_id、tool\_key、tool\_version、permission\_scope、resource\_refs、request\_hash、result\_ref、approval\_id、status、started\_at、finished\_at。

模型和工具日志默认保存引用、哈希和必要元数据，不在普通日志中保存完整敏感 Prompt 或原始个人数据。

## 2.14 publication / public\_projection

Publication：id、target\_type、target\_id、version、status（draft/pending\_approval/approved/published/withdrawn/rejected）、review\_task\_id、approved\_by、approved\_at、published\_at、withdrawn\_at、change\_summary、created\_at。

PublicProjection：id、publication\_id、projection\_type、source\_object\_id、approved\_fields、payload\_json、payload\_version、license\_basis、review\_state、published\_at、withdrawn\_at、content\_hash。

Public API 只读 PublicProjection；不允许通过 Entity.public\_status 布尔值替代独立发布记录。

# 3. 核心索引与约束

- 全部 FK 使用明确 ON DELETE RESTRICT 或业务上安全的 SET NULL；核心历史事实不级联删除。
- source\_registry.source\_key、entity.slug（按站点/语言策略）、entity\_identifier(namespace,value)、document\_version(document\_id,version\_no)、metric\_definition.metric\_key 唯一。
- 常用查询索引：entity(entity\_type,status)、entity\_alias(normalized\_alias)、relationship(subject\_entity\_id,predicate,status)、relationship(object\_entity\_id,predicate,status)、document(source\_id,published\_at)、event(occurred\_at,status)、ingestion\_job(status,created\_at)、review\_task(status,risk\_level,created\_at)。
- 全文检索首期使用 PostgreSQL FTS；别名与模糊匹配使用 pg\_trgm。索引可重建，不成为数据事实源。
- 需要分区时先以真实表大小和查询负载评估；首期不提前分库分表。

# 4. 状态机与转换规则

- IngestionJob：queued→running→succeeded/partial/failed/canceled；失败可重试时重新 queued，并递增 attempt；auth/license/schema-breaking 不无限重试。
- ReviewTask：queued→assigned→approved/rejected/needs\_changes/canceled；审批人必须具备对应 review\_type 权限。
- Publication：draft→pending\_approval→approved→published→withdrawn；更正产生新 version，不回写旧发布历史。
- Entity：draft→pending\_review→published→deprecated/merged；merge 必须产生 redirect 和审计。
- Claim：proposed→supported/partially\_supported/disputed/refuted/outdated/withdrawn；任何状态变化保留 Evidence 和理由。

任何状态转换都必须通过领域服务校验，不允许客户端直接写 status 字段绕过规则。

# 5. API 契约（首期路由组）

统一前缀 /api/v1；所有写请求校验身份、角色、资源分类和状态转换。以下为逻辑路由基线，最终 OpenAPI 必须为每个 operation 定义 request/response schema、错误码和权限。

| 路由 | 方法 | 用途 | 权限 |
| --- | --- | --- | --- |
| /internal/sources | GET/POST | 来源列表/注册 | Data Operator+ |
| /internal/sources/\{id\} | GET/PATCH | 来源详情/配置 | Data Operator+ |
| /internal/sources/\{id\}/licenses | GET/POST | 许可快照 | Data Operator+ / Reviewer |
| /internal/sources/\{id\}/sync | POST | 创建同步任务 | Data Operator+ |
| /internal/ingestion-jobs | GET | 采集任务列表 | Data Operator+ |
| /internal/ingestion-jobs/\{id\}/retry | POST | 失败任务重试 | Data Operator+ |
| /internal/documents | GET/POST | 文档查询/候选导入 | Researcher+ |
| /internal/entities | GET/POST | 实体查询/候选建档 | Researcher+ |
| /internal/entities/\{id\} | GET/PATCH | 实体详情/编辑 | Researcher+ |
| /internal/entities/\{id\}/merge-candidates | GET | 合并候选 | Reviewer+ |
| /internal/relationships | GET/POST | 关系候选/查询 | Researcher+ |
| /internal/claims | GET/POST | Claim 查询/候选提交 | Researcher+ |
| /internal/reviews | GET | 审核队列 | Reviewer+ |
| /internal/reviews/\{id\}/decision | POST | 审核决定 | Reviewer+ |
| /internal/quality-issues | GET/PATCH | 质量问题处理 | Data Operator+ |
| /internal/dashboard/summary | GET | Dashboard 汇总指标 | Internal role |
| /internal/publications | GET/POST | 发布记录 | Editor+ |
| /internal/publications/\{id\}/approve | POST | 审批 | Reviewer+ |
| /internal/publications/\{id\}/publish | POST | 发布 | Publisher role |
| /internal/publications/\{id\}/withdraw | POST | 撤回 | Publisher role |
| /public/articles | GET | 已发布文章列表 | Public |
| /public/articles/\{slug\} | GET | 已发布文章详情 | Public / entitlement |
| /public/entities/\{type\}/\{slug\} | GET | 已批准实体投影 | Public |
| /public/events/\{slug\} | GET | 已批准事件投影 | Public |
| /public/search | GET | 公开搜索 | Public |

## 5.1 API 通用约定

成功响应：data + meta（request\_id、pagination、generated\_at）。错误响应：code、message、details、request\_id。列表 cursor 分页优先；page\_size 默认 20、最大 100。所有写操作支持 Idempotency-Key；并发更新支持 If-Match / version，冲突返回 409，不允许覆盖更新。

公共接口不得返回 classification != public、rights\_status 不允许展示、review\_state 非 approved 或已撤回的对象。

# 6. 权限矩阵（最低要求）

| 动作 | Admin | Data Operator | Researcher | Editor | Reviewer | Agent |
| --- | --- | --- | --- | --- | --- | --- |
| 来源配置 | ✓ | ✓ | 只读 | — | 许可审核 | 按工具授权 |
| 原始资料读取 | ✓ | ✓ | 按分类 | — | 按审核范围 | 按工具授权 |
| 实体/Claim 候选写入 | ✓ | ✓ | ✓ | — | 审核 | 候选接口 |
| 高风险关系审核 | ✓ | — | — | — | ✓ | — |
| 内容编辑 | ✓ | — | 研究草稿 | ✓ | 只读 | 草稿工具 |
| 公开发布批准 | 按职责 | — | — | 提交 | ✓ | — |
| 发布/撤回执行 | ✓ | — | — | 授权发布人 | 批准 | 默认禁止 |
| 权限/密钥管理 | ✓ | — | — | — | — | 禁止 |

# 7. 契约测试最低集合

1. 迁移：空库升级、重复升级、版本回退/补偿。
2. 来源：许可 unknown 拒绝采集/公开；许可过期撤销发布资格。
3. 幂等：同一 source/external\_id/version 重放不产生重复记录。
4. 状态机：非法状态跳转返回 409/422。
5. 审核：开发 Agent 无法审批自己的高风险内容或任务。
6. 并发：旧 version 写入被拒绝，不覆盖新状态。
7. 发布：Public API 只能读取批准字段；撤回后缓存与索引失效。
8. 审计：关键写操作均有 actor、target、reason、request\_id 和时间。
9. 数据隔离：受限对象不出现在公共列表、搜索结果、摘要和附件下载。
10. 故障：Worker 中断、对象存储失败、429/503 和 schema drift 可恢复。

# 8. 实施纪律

本附录冻结逻辑表、核心字段、约束、状态机和 API 路由组。SQLAlchemy 具体模型、Alembic migration 和 OpenAPI YAML 是实现产物，必须由代码生成/维护并通过 CI 验证，不得反向改变本附录定义。新增字段可向后兼容；删除/改义/放宽权限必须 ADR 批准。

- V2.0｜2026-11-28：将 DAC 逻辑数据对象具体化为字段字典、索引约束、状态机、API 路由与权限契约。
