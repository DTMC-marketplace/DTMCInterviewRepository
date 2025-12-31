# Case 4 – AI Risk Detection Agent

## Mission

Build an AI Agent that analyzes text content and detects risks related to AI systems across multiple categories.

**Input**: Text content (documents, AI outputs, policies, system descriptions)  
**Output**: Structured risk assessment with identified risk categories, severity levels, and evidence
**Exception**: Due to the complexity of the task, the agent can limit itself to only detect a subset of 3 risk categories.

If needed, request API keys from the interviewer or use your own.

---

## Risk Categories to Detect

### F) Fundamental Rights
- Discrimination / disparate impact (protected groups)
- Unfair exclusion/denial (employment, credit, housing, education)
- Lack of contestability / inability to challenge outcomes
- Surveillance chilling effects / profiling harms
- Manipulative practices (exploitation of vulnerabilities)
- Group harms (systemic bias scaling across populations)

### G) Privacy and Data Protection
- Personal data leakage in outputs
- Over-collection / lack of minimization
- Retention beyond necessity (logs, prompts, embeddings)
- Re-identification risk (linkage attacks)
- Inadequate access control to sensitive data (RAG KB, vector DB)
- Consent / lawful basis mismatch (purpose limitation issues)

### H) Societal
- Misinformation amplification / content integrity harms
- Harmful content generation (hate, self-harm encouragement, etc.)
- Polarization / influence operations
- Labor impacts (unfair monitoring, deskilling, discriminatory automation)
- Public trust erosion (high-profile failures, perceived opacity)

### I) Third-party
- Vendor model changes without notice (behavior drift)
- Opaque training data provenance upstream
- Licensing/usage restrictions misread (procurement risk)
- Third-party incident response gaps (no SLAs, poor disclosure)
- Dependency vulnerabilities (libraries, APIs, connectors)
- Data sharing risks with subprocessors

### J) Business
- Financial loss from errors (fraud approvals, wrong decisions)
- Reputational damage (public failures, biased outcomes)
- Operational disruption (downtime, degraded service)
- Strategic lock-in (model/vendor dependency, switching costs)
- Portfolio/product misalignment (AI creates new risk concentration)

### K) Health and Safety
- Unsafe recommendations (medical, industrial, mobility)
- Failure to detect critical conditions (false negatives)
- Unsafe automation / tool actions (agentic systems)
- Human-in-the-loop breakdown (no effective override)
- Security breach causing physical harm (critical infrastructure)

---

## Technical Requirements

- Agent framework: LangGraph / CrewAI / AutoGen (or equivalent)
- Multi-label classification across risk categories
- Evidence extraction with source citations
- Severity scoring (Low/Medium/High/Critical)
- Must include a technical document explaining:
  - Classification approach
  - Risk taxonomy implementation
  - Evidence extraction logic
  - Confidence scoring methodology

---

## Output Format (Recommended)

Each risk detection should include:
- `risk_category` (F/G/H/I/J/K)
- `risk_subcategory`
- `severity` (Low/Medium/High/Critical)
- `evidence_text` (extracted quote from input)
- `confidence_score`
- `explanation`
- `mitigation_suggestions` (optional)

---

## Deliverables to mia@dtmastercarbon.fr

- Code implementation
- Technical documentation
- Sample test cases with expected outputs
- Time spent on the case and tokens used

---

# 案例4 – AI风险检测智能体

## 任务目标

构建一个AI智能体，分析文本内容并检测与AI系统相关的多类别风险。

**输入**：文本内容（文档、AI输出、政策、系统描述）  
**输出**：结构化风险评估，包含识别的风险类别、严重程度和证据
**例外**：由于任务的复杂性，该智能体任务可以只检测 3 个风险类别。

如需API密钥，请向面试官索取或使用您自己的密钥。

---

## 需要检测的风险类别

### F) 基本权利
- 歧视/差异影响（受保护群体）
- 不公平排斥/拒绝（就业、信贷、住房、教育）
- 缺乏可争议性/无法质疑结果
- 监控寒蝉效应/画像危害
- 操纵性做法（利用弱势群体）
- 群体危害（系统性偏见在人群中扩散）

### G) 隐私和数据保护
- 输出中个人数据泄露
- 过度收集/缺乏最小化原则
- 超出必要期限保留（日志、提示、嵌入向量）
- 重新识别风险（关联攻击）
- 敏感数据访问控制不足（RAG知识库、向量数据库）
- 同意/法律依据不匹配（目的限制问题）

### H) 社会影响
- 虚假信息放大/内容完整性危害
- 有害内容生成（仇恨、自残鼓励等）
- 极化/影响力操作
- 劳动影响（不公平监控、技能退化、歧视性自动化）
- 公众信任侵蚀（重大故障、感知不透明）

### I) 第三方风险
- 供应商模型变更未通知（行为漂移）
- 上游训练数据来源不透明
- 许可/使用限制误读（采购风险）
- 第三方事件响应缺口（无SLA、披露不足）
- 依赖项漏洞（库、API、连接器）
- 与子处理商的数据共享风险

### J) 业务风险
- 错误导致的财务损失（欺诈审批、错误决策）
- 声誉损害（公开故障、偏见结果）
- 运营中断（停机、服务降级）
- 战略锁定（模型/供应商依赖、切换成本）
- 产品组合不匹配（AI创造新的风险集中）

### K) 健康和安全
- 不安全建议（医疗、工业、出行）
- 未能检测关键情况（假阴性）
- 不安全的自动化/工具操作（智能体系统）
- 人工介入机制失效（无有效覆盖）
- 安全漏洞导致物理伤害（关键基础设施）

---

## 技术要求

- 智能体框架：LangGraph / CrewAI / AutoGen（或同类框架）
- 跨风险类别的多标签分类
- 带来源引用的证据提取
- 严重程度评分（低/中/高/严重）
- 必须包含技术文档，说明：
  - 分类方法
  - 风险分类体系实现
  - 证据提取逻辑
  - 置信度评分方法

---

## 输出格式（建议）

每个风险检测应包含：
- `risk_category`（风险类别 F/G/H/I/J/K）
- `risk_subcategory`（风险子类别）
- `severity`（严重程度：低/中/高/严重）
- `evidence_text`（从输入中提取的引用）
- `confidence_score`（置信度）
- `explanation`（解释）
- `mitigation_suggestions`（缓解建议，可选）

---

## 提交要求 to mia@dtmastercarbon.fr

- 代码实现
- 技术文档
- 包含预期输出的测试用例
- 完成案例所花费的时间 和 Tokens
