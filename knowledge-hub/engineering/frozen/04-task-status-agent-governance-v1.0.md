# VATHEN 开发任务状态机与 Agent 更新权限

> 版本：V1.0｜日期：2026-11-28｜权威来源：Notion《VATHEN 全平台产品与工程冻结基线 V1.0》补充章节

## 核心原则

**Agent 自主推进，独立 QA 验收，系统自动关闭，人工只处理例外。** 开发 Agent 可以提交“待验收”，不能自行设置“已完成”。

## 状态机

| 状态 | 更新主体 | 进入条件 |
|---|---|---|
| 待开始 | 管理员/系统 | 任务已建立且依赖满足 |
| 进行中 | Agent/系统 | Agent 原子领取任务 |
| 待验收 | 开发 Agent | 实现完成，交付证据齐全 |
| 验收中 | 独立 QA Agent/系统 | QA 独立领取并运行验收 |
| 已完成 | 独立 QA Agent/系统 | 全部阻断级验收项通过，自动关闭 |
| 验收失败 | 独立 QA Agent/系统 | 任一阻断级验收失败，自动退回进行中 |
| 阻塞中 | Agent/系统 | 依赖、权限、环境或外部决策阻塞 |

## 权限规则

1. 开发 Agent 可领取任务、更新进行中、提交待验收、补充证据和报告阻塞；不能直接设置已完成。
2. 开发与验收身份分离；同一 Agent Run 不得既实现又最终验收。
3. QA 全部通过后 Task Service 自动设置已完成；不要求用户逐项人工确认。
4. QA 失败自动退回进行中，附失败项、复现步骤和日志；修复后重新验收并保留历史。
5. 所有状态变更必须通过受控 Task API/MCP Tool，禁止直写数据库。
6. 使用 task_version 乐观锁/CAS 与 Idempotency-Key，防止重复/并发写入。
7. 每次迁移记录 actor、actor_type、from/to、timestamp、reason、task_version、run_id 和 evidence_refs。
8. Agent 心跳超时可由调度器回收任务；保留旧 Run 和提交，禁止静默覆盖。

## 人工审批 Gate

只对以下高风险动作要求人工批准：生产密钥/权限提升、云资源采购或预算超限、不可逆生产数据删除/迁移、受限数据导出、真实支付/退款、法律/版权不确定、安全事件、对外公开发布或承诺。Gate 只阻断相关动作，不阻断其他安全工作。

## 自动验收门槛

- CI：lint、type check、unit、contract、integration、build 按任务适用性通过。
- 交付：PR/commit 关联 task_id、冻结规格版本、ADR、变更文件、迁移/回滚说明。
- QA：独立 QA 按验收矩阵执行，不采信开发 Agent 自报作为唯一依据。
- 安全：权限、敏感数据、密钥、公开数据隔离检查通过。
- 证据：报告、日志、预览地址、测试环境和版本可追溯。

## 建议字段

task_id、title、status、priority、assignee_agent_id、qa_agent_id、dependency_ids、spec_version、branch、pr_url、commit_sha、started_at、submitted_at、qa_started_at、completed_at、progress_note、blocker_type、blocker_detail、acceptance_evidence、task_version、last_heartbeat_at。

## 数据权威与安全

当前 Notion 任务库是任务状态的可读事实源；GitHub 官网是静态知识快照，不是实时任务控制台。未来实时看板必须通过服务端 Task API 读取/写入，具备身份鉴权、最小权限、审计、幂等与并发控制。不得把 Notion Token、GitHub Token 或服务密钥放入浏览器静态代码。

## Notion 规范

参见 [全平台产品与工程冻结基线](https://app.notion.com/p/426f15aabd2c81549243ed1e72be2ea4)。
