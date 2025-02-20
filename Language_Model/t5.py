from transformers import T5Tokenizer, T5ForConditionalGeneration

# T5 모델과 토크나이저 로드
tokenizer = T5Tokenizer.from_pretrained("google-t5/t5-small")
model = T5ForConditionalGeneration.from_pretrained("google-t5/t5-small")

# 질문 입력
input_text_eng = "Hello, what should I eat lunch today?"
input_text_kr = "오늘 점심 뭐먹을까?"
input_text_ch = "Jīntiān wǔfàn chī shénme?"

# 입력 텍스트를 토큰화
input_ids_eng = tokenizer(f"question: {input_text_eng} </s>", return_tensors="pt").input_ids
input_ids_kr = tokenizer(f"question: {input_text_kr} </s>", return_tensors="pt").input_ids
input_ids_ch = tokenizer(f"question: {input_text_ch} </s>", return_tensors="pt").input_ids

# 모델을 사용하여 답변 생성
output_eng = model.generate(input_ids_eng, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)
output_kr = model.generate(input_ids_kr, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)
output_ch = model.generate(input_ids_ch, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)

# 생성된 텍스트 디코딩
answer_eng = tokenizer.decode(output_eng[0], skip_special_tokens=True)
answer_kr = tokenizer.decode(output_kr[0], skip_special_tokens=True)
answer_ch = tokenizer.decode(output_ch[0], skip_special_tokens=True)

# 결과 출력
print("=========English==========")
print("Question:", input_text_eng)
print("Answer:", answer_eng)
print("=========Korean==========")
print("Question:", input_text_kr)
print("Answer:", answer_kr)
print("=========Chinese==========")
print("Question:", input_text_ch)
print("Answer:", answer_ch)
print("==========================")