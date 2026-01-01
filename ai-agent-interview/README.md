# AI Agent Engineering Interview

This repository contains the official technical interview cases for the AI Agent Engineer position. If needed we can provide any API key for OpenAI / DeepSeek / Claude / Gemini / Qwen / Zhipu (ZLM) / Mistral.

Please read each case carefully before starting.
```
ai-agent-interview/
├── README.md                    
├── LICENSE                      
│
├── cases/
│   ├── case-1-factory-agent/
│   │   ├── README.md            
│   │   ├── rubric.md          
│   │   └── examples/
│   │       ├── input_example.json
│   │       └── output_example.json
│   │
│   ├── case-2-rag-hallucination/
│   │   ├── README.md               
│   │   └── rubric.md
│   │
│   ├── case-3-automation-agent/
│   │   ├── README.md               
│   │   └── rubric.md
│   │
│   └── case-4-risk-detection-agent/
│       ├── README.md               
│       └── rubric.md
│
├── submission/
│   └── expected-structure.md    
└── reviewers/
    ├── evaluation-checklist.md     
    └── scoring-template.md         
```


# AI Agent Engineering Interview

This repository contains the official technical interview cases for the **AI Agent Engineer** position.

The interview focuses on **real-world agent engineering**, not toy demos:
- Retrieval accuracy & grounding
- Hallucination reduction
- Multi-agent reasoning
- Automation of enterprise workflows (Excel / Word)

---

## Case Complexity (1-4)

- **Case 1 – Physical Factory Search Agent**: Medium. Tests retrieval precision, evidence tracking, and binary exclusion rules (Round 1 gate).
- **Case 2 – RAG Hallucination Reduction**: Complex. Requires diagnosing failure modes and proposing single- and multi-agent mitigations.
- **Case 3 – Automated Report Generation Agent**: Complex. Requires Excel/Word automation with strict grounding and schema enforcement.
- **Case 4 – AI Risk Detection Agent**: Medium. Demands multi-label classification, severity scoring, and evidence extraction over long documents.

---

## Interview Process

The interview consists of **three rounds**:

1. **Round 1** (Medium Difficulty)
   - Choose one: Case 1 (Factory Agent) OR Case 4 (Risk Detection)
   
2. **Round 2** (Complex Difficulty)
   - After passing Round 1, you will proceed to Round 2.
   - Choose one: Case 2 (RAG Hallucination) OR Case 3 (Report Automation)
   
3. **Final Round**
   - System design discussion with CEO & Tech Lead

Only candidates who pass Round 1 will proceed to Round 2.
For candidates who got an offer at final round, we will provide a signing bonus of 2000 RMB
---

## Allowed Tools & Models

Candidates may use:
- OpenAI / DeepSeek / Claude / Gemini / Qwen / Zhipu (ZLM) / Mistral
- LangGraph / CrewAI / AutoGen or similar open-source frameworks
- Public web data, open datasets, maps, satellite imagery (optional)

Please ask for API keys from the interviewer or use your own.

---

## Submission

Please submit:
- Code
- Technical documentation
- Time spent on the case
- Time deadlines - 1 week maximum to submit the case interview

📩 Send to: **mia@dtmastercarbon.fr**

---

Good luck.

---

# AI 智能体工程师面试

本仓库包含 AI 智能体工程师职位的官方技术面试案例。

请在开始之前仔细阅读每个案例。

```
ai-agent-interview/
├── README.md                    
├── LICENSE                      
│
├── cases/                       # 案例目录
│   ├── case-1-factory-agent/
│   │   ├── README.md            # 案例1 题目说明
│   │   ├── rubric.md            # 案例1 评分标准
│   │   └── examples/
│   │       ├── input_example.json
│   │       └── output_example.json
│   │
│   ├── case-2-rag-hallucination/
│   │   ├── README.md            # 案例2 题目说明
│   │   └── rubric.md
│   │
│   ├── case-3-automation-agent/
│   │   ├── README.md            # 案例3 题目说明
│   │   └── rubric.md
│   │
│   └── case-4-risk-detection-agent/
│       ├── README.md            # 案例4 题目说明
│       └── rubric.md
│
├── submission/                  # 提交目录
│   └── expected-structure.md    # 候选人提交代码结构规范
│
└── reviewers/                   # 评审目录
    ├── evaluation-checklist.md  # 内部评审检查清单
    └── scoring-template.md      # 打分模板
```

本面试聚焦于**真实的智能体工程实践**，而非简单的演示项目：
- 检索准确性与信息溯源
- 幻觉问题的减少
- 多智能体推理
- 企业工作流自动化（Excel / Word）

---

## 案例复杂度（1-4）

- **案例1 – 实体工厂搜索智能体**：中等难度，考察检索精度、证据链以及硬性排除规则。
- **案例2 – RAG 幻觉治理**：高难度，需要定位失效根因并提出单/多智能体的降低幻觉方案。
- **案例3 – 自动化报告生成智能体**：高难度，聚焦 Excel/Word 自动化、强校验和严格的数据对齐。
- **案例4 – AI 风险检测智能体**：中等难度，要求跨类别多标签分类、严重程度评分与长文本证据提取。

---

## 面试流程

本次面试共分为**三轮**：

1. **第一轮**（中等难度）
   - 选择一道：案例1（工厂搜索智能体）或 案例4（风险检测智能体）
   
2. **第二轮**（高难度）
   - 通过第一轮后，进入第二轮
   - 选择一道：案例2（RAG幻觉治理）或 案例3（报告自动化）
   
3. **终面**
   - 与 CEO 及技术负责人进行系统设计讨论

只有通过第一轮的候选人才能进入第二轮。
通过终面并获得录用的候选人，将获得2000元人民币的签约奖金。

---

## 允许使用的工具和模型

候选人可以使用：
- OpenAI / DeepSeek / Claude / Gemini / 通义千问 / 智谱（ZLM）/ Mistral
- LangGraph / CrewAI / AutoGen 或类似的开源框架
- 公开网络数据、开放数据集、地图、卫星影像（可选）

请向面试官索取 API 密钥，或使用您自己的密钥。

---

## 提交要求

请提交以下内容：
- 代码
- 技术文档
- 完成案例所花费的时间
- 时间限制 
- 提交案例面试最多1周

📩 发送至：**mia@dtmastercarbon.fr**

---

祝你好运！
