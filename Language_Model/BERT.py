from transformers import BertTokenizer, BertForQuestionAnswering
import torch

# 모델과 토크나이저 로드
model = BertForQuestionAnswering.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# 질문과 문서 준비
question = "혹시 한국말 할줄 아나?"
context = ""

# 입력 데이터 준비
inputs = tokenizer(question, context, return_tensors="pt")

# 모델에 입력하여 답변 예측
with torch.no_grad():
    outputs = model(**inputs)
    
start_scores = outputs.start_logits
end_scores = outputs.end_logits

# 답변 추출
start_index = torch.argmax(start_scores)
end_index = torch.argmax(end_scores)

# 토큰을 다시 텍스트로 변환
answer_tokens = inputs.input_ids[0][start_index:end_index + 1]
answer = tokenizer.decode(answer_tokens)

print(f"Answer: {answer}")
