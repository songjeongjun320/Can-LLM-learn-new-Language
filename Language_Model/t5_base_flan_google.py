from transformers import pipeline

pipe = pipeline("text2text-generation", model="google/flan-t5-base")
question = "This word 안녕 is hello in Korean. 안녕"
result = pipe(question)

print("===========================================")
print("Question: ", question)
print("Answer: ", result[0]['generated_text'])
print("===========================================")
