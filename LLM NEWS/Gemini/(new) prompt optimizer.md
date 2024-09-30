
## 목적
- 

## 방법
1. prompt template 준비하기
	- 고정적인 부분과 동적인 부분 구분되어 템플릿 준비
```python
INSTRUCTION_TEMPLATE = """
Given a question with some context, provide the correct answer to the question.
"""

CONTEXT_TASK_TEMPLATE = """
Question: {{question}}
Answer: {{target}}
"""
```

1. Cloud Storage bucket에 labeled samples 올리기
	- dsd
```python
{"target":"Here\'s how to tackle those delicious red meats and pork while keeping things healthy:\\n\\n**Prioritize Low and Slow:**\\n\\n* **Braising and Stewing:** These techniques involve gently simmering meat in liquid over low heat for an extended period. This breaks down tough collagen, resulting in incredibly tender and flavorful meat. Plus, since the cooking temperature is lower, it minimizes the formation of potentially harmful compounds associated with high-heat cooking. \\n\\n* **Sous Vide:** This method involves sealing meat in a vacuum bag and immersing it in a precisely temperature-controlled water bath...",
 
 "question":"What are some techniques for cooking red meat and pork that maximize flavor and tenderness while minimizing the formation of unhealthy compounds? \\n\\nnContext:\\nRed meat and pork should be cooked to an internal temperature of 145\\u00b0F (63\\u00b0C) to ensure safety. \\nMarinating meat in acidic ingredients like lemon juice or vinegar can help tenderize it by breaking down tough muscle fibers. \\nHigh-heat cooking methods like grilling and pan-searing can create delicious browning and caramelization, but it\'s important to avoid charring, which can produce harmful compounds. \\n"}
```
1. optimization settings 세팅하기
2. optimization job 실행
3. optimized prompt 얻고 optimization 평가
## reference
- https://developers.googleblog.com/en/enhance-your-prompts-with-vertex-ai-prompt-optimizer/?_gl=1*10k2ea6*_up*MQ..*_ga*OTMwNTE2NjQ2LjE3Mjc0MTMxMzg.*_ga_H733Y2BZES*MTcyNzQxMzEzNy4xLjAuMTcyNzQxMzEzNy4wLjAuMA..