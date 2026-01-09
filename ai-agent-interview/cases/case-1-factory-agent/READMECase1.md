# Case 1 – The "Needle in the Haystack" Consistency Check

## Objective

Validate User Verbal Claims vs. Technical Reality.

Build an AI Agent that can hold extensive documentation in memory (100k+ tokens) and intelligently cross-reference user claims against technical specifications in real-time during an interview.

If needed we can provide any API key for OpenAI / DeepSeek / Claude / **Gemini** / Qwen / Zhipu (ZLM).

---

## Context

The user uploads the following documents:
- Model Card
- Data Governance Policy  
- API Specification

**Total context**: 100k+ tokens

---

## The Interview Interaction

**User**: "Our model does not process sensitive personal data."

**Agent (Imposing LCF KPI)**: "I have analyzed your API Specification (uploaded file `api_v2.pdf`). On page 42, the JSON schema includes a field for `biometric_vector`. This contradicts your statement and triggers Article 9 of GDPR. Explain this discrepancy or I will classify this as 'High Risk'."

---

## Gemini Capability

**Gemini 2.5 Pro (2M Context)** to hold the entire documentation in memory while interviewing.

---

## Technical Requirements

- Agent framework: LangGraph / CrewAI / AutoGen (or equivalent)
- **Must use Gemini 2.5 Pro** for Long Context capability
- Context management: Load and maintain 100k+ token context
- Document parsing: Support for PDF, JSON, YAML specifications
- Real-time cross-referencing between user claims and document content
- Must include a technical document explaining:
  - How context is managed across the 2M token window
  - Contradiction detection logic
  - Evidence citation methodology
  - Risk classification criteria

---

## Output Format (Recommended)

Each consistency check should include:
- `claim` (user's verbal statement)
- `document_reference` (file, page, section)
- `contradicting_evidence` (extracted text from document)
- `regulation_triggered` (e.g., GDPR Article 9)
- `risk_classification` (Low/Medium/High)
- `follow_up_question` (agent's response)
- `confidence_score`

---

## Deliverables

- System design document
- Demo or core implementation  
- Sample test cases with expected outputs
- Time spent on the case and tokens used

📩 Send to: **mia@dtmastercarbon.fr**

---

# 案例1 – "大海捞针"一致性检查

## 目标

验证用户口头声明与技术现实的一致性。

构建一个AI智能体，能够在内存中保持大量文档（100k+ tokens），并在面试过程中实时智能地将用户声明与技术规范进行交叉对照。

如有需要，我们可提供 OpenAI / DeepSeek / Claude / **Gemini** / 通义千问 / 智谱（ZLM）的 API 密钥。

---

## 背景

用户上传以下文档：
- 模型卡
- 数据治理政策
- API 规范

**总上下文**：100k+ tokens

---

## 面试交互示例

**用户**："我们的模型不处理敏感个人数据。"

**智能体（强制执行 LCF KPI）**："我已分析您的 API 规范（上传文件 `api_v2.pdf`）。在第42页，JSON schema 包含一个 `biometric_vector` 字段。这与您的声明相矛盾，并触发了 GDPR 第9条。请解释这一差异，否则我将其分类为'高风险'。"

---

## Gemini 能力

**Gemini 2.5 Pro (2M 上下文)** 在面试过程中将整个文档保存在内存中。

---

## 技术要求

- 智能体框架：LangGraph / CrewAI / AutoGen（或同类框架）
- **必须使用 Gemini 2.5 Pro** 以实现长上下文能力
- 上下文管理：加载并维护 100k+ token 上下文
- 文档解析：支持 PDF、JSON、YAML 规范
- 用户声明与文档内容的实时交叉引用
- 必须包含技术文档，说明：
  - 如何在 2M token 窗口内管理上下文
  - 矛盾检测逻辑
  - 证据引用方法
  - 风险分类标准

---

## 输出格式（建议）

每个一致性检查应包含：
- `claim`（用户的口头声明）
- `document_reference`（文件、页码、章节）
- `contradicting_evidence`（从文档中提取的文本）
- `regulation_triggered`（例如，GDPR 第9条）
- `risk_classification`（低/中/高）
- `follow_up_question`（智能体的回应）
- `confidence_score`（置信度）

---

## 提交要求

- 代码实现
- 技术文档
- 包含预期输出的测试用例
- 完成案例所花费的时间和 Tokens

📩 发送至：**mia@dtmastercarbon.fr**