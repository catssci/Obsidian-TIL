
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
2. optimization settings 세팅하기
3. optimization job 실행
4. optimized prompt 얻고 optimization 평가
## reference
- https://developers.googleblog.com/en/enhance-your-prompts-with-vertex-ai-prompt-optimizer/?_gl=1*10k2ea6*_up*MQ..*_ga*OTMwNTE2NjQ2LjE3Mjc0MTMxMzg.*_ga_H733Y2BZES*MTcyNzQxMzEzNy4xLjAuMTcyNzQxMzEzNy4wLjAuMA..