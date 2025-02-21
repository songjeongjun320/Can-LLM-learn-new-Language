from transformers import pipeline

pipe = pipeline("fill-mask", model="google-bert/bert-base-uncased")
question = "This word 안녕 is hello in Korean. If I say 안녕 to you. What should you say? [MASK]"
result = pipe(question)

print("===========================================")
print("Question: ", question)
print("Answer: ", result[0]['token_str'])  # 'generated_text' 대신 'token_str' 사용
print("===========================================")
