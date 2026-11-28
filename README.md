# VATHEN Knowledge Operating System

先知 VATHEN 的结构化知识入口。网站按战略、产品能力、运营交付和档案追溯组织知识，而不是按 Notion 原始页面顺序展示。

## Architecture 3.0

1. **方向与定位**：战略与商业、品牌与体验
2. **产品与能力**：产品与体验、研究与内容、数据与情报、技术与智能体
3. **运营与治理**：运营与治理、项目与交付
4. **档案与追溯**：原始资料与历史档案

当前快照覆盖 59 篇知识页面和 51 条项目任务记录，共 110 条。每个模块提供使命、核心认知、运行模型、依赖关系、适用边界和来源文档。

## Pages

- Website: https://dls2049.github.io/vathen-knowledge-websites/
- Architecture: `/data/knowledge-architecture.json`
- Agent index: `/data/agent-index.json`
- Delivery workspace: `/knowledge-hub/engineering/`

## Source of truth and limitations

- Notion remains the source of truth for source documents and current task status.
- This website is a static snapshot, not live Notion synchronization.
- The task list is not a real-time execution view.
- Task Bridge, server-side credentials, SSO/RBAC enforcement, Agent Runtime, independent QA and autonomous task closure must not be considered deployed until separately implemented and verified.
- Secrets and Notion tokens must remain server-side; never place them in this static website.
