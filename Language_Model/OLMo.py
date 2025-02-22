from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 모델 & 토크나이저 로드 (OLMo는 trust_remote_code 필요)
model = AutoModelForCausalLM.from_pretrained(
    "allenai/OLMo-7B-hf",
    trust_remote_code=True,
    torch_dtype=torch.bfloat16  # GPU 메모리 절약
)
tokenizer = AutoTokenizer.from_pretrained("allenai/OLMo-7B-hf")

# 추론 파라미터 설정
question = """Hello My name is Jun,
My idea to make LLM learn new language is giving them a circumstance information with the sentences of language.
Answer:"""

inputs = tokenizer(
    question,
    return_tensors="pt",
    max_length=256,
    truncation=True
)

# 생성 설정
outputs = model.generate(
    inputs.input_ids.to(model.device),
    max_new_tokens=150,
    temperature=0.3,  # 창의성 ↓ → 논리적 답변 ↑
    top_p=0.95,
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id  # OLMo 토크나이저 이슈 방지
)

# 결과 디코딩
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(answer)