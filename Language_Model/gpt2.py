# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

# 모델과 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2")

# 질문 입력
input_text_eng = "Hello, what should I eat lunch today?"
input_text_kr = "오늘 점심 뭐먹을까?"
input_text_ch = "Jīntiān wǔfàn chī shénme?"

# 입력 텍스트를 토큰화
input_ids_eng = tokenizer.encode(input_text_eng, return_tensors="pt")
input_ids_kr = tokenizer.encode(input_text_kr, return_tensors="pt")
input_ids_ch = tokenizer.encode(input_text_ch, return_tensors="pt")

# 모델을 사용하여 텍스트 생성
output_eng = model.generate(
    input_ids_eng,
    max_length=50,  # 생성할 최대 길이
    num_return_sequences=1,  # 생성할 시퀀스 수
    no_repeat_ngram_size=2,  # 반복 방지
    top_k=50,  # Top-k 샘플링
    top_p=0.95,  # Top-p (nucleus) 샘플링
    temperature=0.7,  # 창의성 조절 (낮을수록 보수적)
)

# 모델을 사용하여 텍스트 생성
output_kr = model.generate(
    input_ids_kr,
    max_length=50,  # 생성할 최대 길이
    num_return_sequences=1,  # 생성할 시퀀스 수
    no_repeat_ngram_size=2,  # 반복 방지
    top_k=50,  # Top-k 샘플링
    top_p=0.95,  # Top-p (nucleus) 샘플링
    temperature=0.7,  # 창의성 조절 (낮을수록 보수적)
)

# 모델을 사용하여 텍스트 생성
output_ch = model.generate(
    input_ids_ch,
    max_length=50,  # 생성할 최대 길이
    num_return_sequences=1,  # 생성할 시퀀스 수
    no_repeat_ngram_size=2,  # 반복 방지
    top_k=50,  # Top-k 샘플링
    top_p=0.95,  # Top-p (nucleus) 샘플링
    temperature=0.7,  # 창의성 조절 (낮을수록 보수적)
)

# 생성된 텍스트 디코딩
generated_text_eng = tokenizer.decode(output_eng[0], skip_special_tokens=True)
generated_text_kr = tokenizer.decode(output_kr[0], skip_special_tokens=True)
generated_text_ch = tokenizer.decode(output_ch[0], skip_special_tokens=True)

# 결과 출력
print("=========English==========")
print("Question:", input_text_eng)
print("Answer:", generated_text_eng)
print("=========Korean==========")
print("Question:", input_text_kr)
print("Answer:", generated_text_kr)
print("=========Chinese==========")
print("Question:", input_text_ch)
print("Answer:", generated_text_ch)
print("==========================")