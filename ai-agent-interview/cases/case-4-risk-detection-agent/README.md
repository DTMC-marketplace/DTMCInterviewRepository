# Case 4 – The Multimodal "Human Oversight" Audit

## Objective

Visually verify Article 14 (Human Oversight) compliance.

Build an AI Agent that can analyze uploaded UI/UX designs (screenshots, mockups) and assess whether they meet EU AI Act requirements for human oversight mechanisms in high-risk AI systems.

If needed we can provide any API key for OpenAI / DeepSeek / Claude / **Gemini** / Qwen / Zhipu (ZLM).

---

## Context

The Fundamental Rights Impact Assessment (FRIA) requires proof that a human operator can intervene/stop the AI system.

---

## The Interview Interaction

**Agent**: "Upload a screenshot of the Operator Dashboard."

**User**: *(Uploads image)*

**Agent (Imposing Visual Grounding KPI)**: "Scanning image... I see a dashboard, but there is no prominent 'Emergency Stop' or 'Override' button visible in the main viewport. This design may fail Article 14 requirements for high-stress environments. Please highlight the intervention mechanism or upload a compliant design."

---

## Gemini Capability

**Native Multimodality (Vision)** to critique UI/UX designs for legal compliance.

---

## Technical Requirements

- Agent framework: LangGraph / CrewAI / AutoGen (or equivalent)
- **Must use Gemini** for native vision capabilities
- Image analysis: Screenshot, mockup, and dashboard interpretation
- Compliance checking against EU AI Act Article 14 requirements
- Visual element detection: Buttons, controls, emergency mechanisms
- Must include a technical document explaining:
  - Vision model integration approach
  - UI element detection and classification logic
  - Compliance rule mapping (Article 14 requirements)
  - Visual grounding methodology
  - Accessibility and usability assessment criteria

---

## Article 14 Compliance Criteria to Check

The agent should verify the presence and visibility of:
- Emergency stop / shutdown controls
- Override mechanisms
- Human intervention buttons
- Real-time monitoring indicators
- Alert/warning systems
- Manual control options
- Decision review capabilities
- System state visibility

---

## Output Format (Recommended)

Each visual compliance check should include:
- `screenshot_reference` (filename, uploaded timestamp)
- `detected_elements` (list of UI elements found)
- `missing_elements` (required but not found)
- `article_14_compliance` (Pass/Fail/Partial)
- `specific_issues` (detailed list of problems)
- `evidence_regions` (bounding boxes or coordinates of relevant areas)
- `recommendations` (specific design improvements)
- `confidence_score`

---

## Deliverables

- System design document
- Demo or core implementation
- Sample test cases with expected outputs
- Time spent on the case and tokens used

📩 Send to: **mia@dtmastercarbon.fr**

---

# 案例4 – 多模态"人类监督"审计

## 目标

视觉验证第14条（人类监督）合规性。

构建一个AI智能体，能够分析上传的UI/UX设计（截图、原型图），并评估它们是否符合EU AI Act对高风险AI系统人类监督机制的要求。

如有需要，我们可提供 OpenAI / DeepSeek / Claude / **Gemini** / 通义千问 / 智谱（ZLM）的 API 密钥。

---

## 背景

基本权利影响评估（FRIA）要求证明人类操作员可以干预/停止AI系统。

---

## 面试交互示例

**智能体**："请上传操作员仪表板的截图。"

**用户**：*（上传图片）*

**智能体（强制执行视觉定位 KPI）**："正在扫描图像... 我看到一个仪表板，但在主视窗中没有看到明显的'紧急停止'或'覆盖'按钮。此设计可能不符合高压力环境下第14条的要求。请标注干预机制或上传符合要求的设计。"

---

## Gemini 能力

**原生多模态（视觉）** 用于评审UI/UX设计的法律合规性。

---

## 技术要求

- 智能体框架：LangGraph / CrewAI / AutoGen（或同类框架）
- **必须使用 Gemini** 以实现原生视觉能力
- 图像分析：截图、原型图和仪表板解读
- 针对 EU AI Act 第14条要求的合规检查
- 视觉元素检测：按钮、控件、紧急机制
- 必须包含技术文档，说明：
  - 视觉模型集成方法
  - UI元素检测和分类逻辑
  - 合规规则映射（第14条要求）
  - 视觉定位方法
  - 可访问性和可用性评估标准

---

## 需检查的第14条合规标准

智能体应验证以下元素的存在和可见性：
- 紧急停止/关机控件
- 覆盖机制
- 人工干预按钮
- 实时监控指示器
- 警报/警告系统
- 手动控制选项
- 决策审查功能
- 系统状态可见性

---

## 输出格式（建议）

每个视觉合规检查应包含：
- `screenshot_reference`（文件名、上传时间戳）
- `detected_elements`（找到的UI元素列表）
- `missing_elements`（必需但未找到的元素）
- `article_14_compliance`（通过/失败/部分通过）
- `specific_issues`（问题详细列表）
- `evidence_regions`（相关区域的边界框或坐标）
- `recommendations`（具体设计改进建议）
- `confidence_score`（置信度）

---

## 提交要求

- 代码实现
- 技术文档
- 包含预期输出的测试用例
- 完成案例所花费的时间和 Tokens

📩 发送至：**mia@dtmastercarbon.fr**
