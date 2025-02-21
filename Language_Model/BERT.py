from transformers import BertTokenizer, BertForQuestionAnswering
import torch

# 모델과 토크나이저 로드
model = BertForQuestionAnswering.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# 질문과 문서 준비
question = "대한민국의 수도는 어디야?"
context = "서울특별시는 대한민국의 수도[22]이자 최대도시이며, 대한민국 유일의 특별시이다. ... 역사적으로도 백제, 조선, 대한제국의 수도이자 현재 대한민국의 수도로서 중요성이 ..."

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
