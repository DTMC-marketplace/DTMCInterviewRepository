# Case 2 – Reducing Hallucination in a RAG Agent

## Context

We have an internal RAG-based Agent with a **high hallucination rate**.
You will be given:
- The agent's generated answer
- The correct answer

Your task is to **diagnose and fix the problem**.
If needed we can provide any API key for OpenAI / DeepSeek / Claude / Gemini / Qwen / Zhipu (ZLM).
We provide the code of the agent, you can use it as a reference and two Azure openai api key.
Please read agent.md for more details.
---

## Required Answers

### 1. Diagnosis
Why is hallucination high in this RAG system?

### 2. Single-Agent Solution
Design or rebuild again a concrete, deployable solution.

### 3. Multi-Agent Strategy
How would you use multiple agents to reduce hallucination?

### 4. Multi-Agent Implementation
Provide a system-level design.

### 5. Other Methods
Any additional hallucination mitigation techniques.

---


## Deliverables to mia@dtmastercarbon.fr

- System design document
- Demo or core implementation
- Sample test cases with expected outputs
- Time spent on the case and tokens used




---

# 案例2 – 降低 RAG 智能体的幻觉问题

## 背景

我们内部有一个基于 RAG 的小 Agent，用于检索数据并生成答案，但当前 hallucination 比率很高。
我们会提供：
- Agent 的输出（Answer A）
- 对应的正确答案（Ground Truth / Answer B）（以及必要的上下文/检索片段，如你需要）
- 两个 Azure OpenAI API 密钥
- 如有需要，我们可提供 OpenAI / DeepSeek / Claude / Gemini / Qwen / Zlm 等 API。
- 请阅读 agent.md 了解更多详情。

## 任务

请按以下 5 个问题组织你的回答与方案，要求工程化、可执行、有衡量指标：

### 1. 问题诊断

解释为什么该 RAG 方案 hallucination 高
至少覆盖以下维度（可自拟结构）：

检索失败/召回不足/Query 不稳定

Chunking/Embedding/Index 设计不合理

上下文污染（irrelevant context）

生成端没有“引用约束/证据约束”

多文档冲突、时效性问题、来源可信度问题

数据标准化、实体对齐失败（company/site/entity mismatch）

### 2. 单 Agent 改进方案

提出一个能明显降低 hallucination 的 端到端技术方案，需包含：

架构图或流程图（文字描述也可）

检索策略（hybrid search、rerank、filters、metadata、query rewrite）

生成策略（grounded generation、citations、refusal rules、schema output）

校验策略（fact-check、consistency check、source scoring）

评估方法与指标（hallucination rate 定义、exact match、faithfulness、coverage、latency、cost）

### 3. 如果用 Multi-Agent 降低 hallucination，你会怎么做？

说明你的 multi-agent 角色设计与协作方式，例如：

Retriever / Researcher / Extractor / Verifier / Judge

何时并行、何时串行

冲突如何仲裁（voting / judge / confidence / source priority）

如何避免 multi-agent 自身放大 hallucination（必须回答）

### 4. Multi-Agent 方案落地

给出可落地方案（工程层面），包括：

模块分层与接口（输入输出契约）

状态管理与缓存策略

成本与延迟控制（token budget、并发策略）

可观测性（trace、log、eval dataset、回归测试）

### 5. 其他降低 hallucination 的方法

除 RAG/多 Agent 以外，再补充可选路线，例如：

tool calling 强约束（DB query、schema validator）

结构化 extraction + constrained decoding

DPO/RLHF 或基于偏好/拒答样本的微调策略（若适用）

置信度校准与拒答策略（abstain）

数据治理（来源白名单、版本控制、时效性）

“答案必须引用证据”的产品级硬约束

## 提交材料（Deliverables）to mia@dtmastercarbon.fr

- 文档（必需）：按回答 1–5 结构写清楚
- 代码（可选但加分）：提供一个最小可运行 demo 或伪代码实现关键模块
- 包含预期输出的测试用例
- 完成案例所花费的时间 和 Tokens

## 同时请附上： 

完成该 Case 花费时间（小时）


## 提交方式

请将 代码 + 文档 打包发送至：mia@dtmastercarbon.fr

- 代码实现
- 技术文档
- 包含预期输出的测试用例
- 完成案例所花费的时间 和 Tokens

审核通过后进入最终 Oral Interview。

