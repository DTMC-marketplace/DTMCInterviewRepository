# Case 3 – Automated Report Generation Agent

## Context

Reports are currently produced manually using:
- Excel (data)
- Word (templates)

Your task is to design an AI Agent that automates this workflow.
Any API key for OpenAI / DeepSeek / Claude / Gemini / Qwen / Zhipu (ZLM) are in the config file.
Due to the task complexity you can just automate step 1 and 2

---

## Mission

The agent should:
- ask questions to get the data from the user based on the template methodology
- automate entirely the methodology based on methodology document
- Read structured Excel inputs to get more data if existing
- Populate Word report templates
- Ensure numerical & semantic consistency
- Avoid hallucination
- Be reusable across clients and templates

---

## Key Requirements

- Strong data-to-text grounding
- Schema validation
- Traceability (every statement backed by data)
- Graceful failure when data is missing

---

## Deliverables to mia@dtmastercarbon.fr

- System design document
- Demo or core implementation
- Sample test cases with expected outputs
- Time spent on the case and tokens used

---

# 案例3 – 自动化报告生成智能体

## 背景

目前报告是手动生成的，使用：
- Excel（数据）
- Word（模板）

你的任务是设计一个自动化此工作流程的 AI 智能体。
如有需要，我们可提供 OpenAI / DeepSeek / Claude / Gemini / 通义千问 / 智谱（ZLM）的 API 密钥。
所有 OpenAI / DeepSeek / Claude / Gemini / 通义千问 / 智谱（ZLM）的 API 密钥都在配置文件中。 由于任务复杂性，你可以只自动化步骤1和步骤2。

---

## 任务目标

该智能体应能够：
- 问问题以获取用户数据
- 自动化整个方法论
- 读取结构化的 Excel 输入 以获取更多数据
- 填充 Word 报告模板
- 确保数值和语义的一致性
- 避免幻觉
- 可复用于不同的客户和模板
---

## 核心要求

- 强数据到文本的关联性
- Schema 验证
- 可追溯性（每条陈述都有数据支撑）
- 数据缺失时优雅降级

---

## 提交要求 to mia@dtmastercarbon.fr

- 系统设计文档
- 演示或核心实现
- 包含预期输出的测试用例
- 完成案例所花费的时间 和 Tokens
