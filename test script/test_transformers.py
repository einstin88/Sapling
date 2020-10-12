
### test loading & savingg transformers
from transformers import AlbertForQuestionAnswering, AlbertTokenizer
import os

modelDir = os.path.join('cfg', 'nlp')
tokPath = os.path.join(modelDir, 'tokenizer')
modPath = os.path.join(modelDir, 'model')

os.path.exists(modPath)

# Test loading locally
tokenizer = AlbertTokenizer.from_pretrained(tokPath)
model = AlbertForQuestionAnswering.from_pretrained(modPath, return_dict = True)

# Test downloading
#tokenizer = AutoTokenizer.from_pretrained("twmkn9/albert-base-v2-squad2")
tokenizer = AlbertTokenizer.from_pretrained("twmkn9/albert-base-v2-squad2")
dir(tokenizer)
tokenizer.save_pretrained(".\\model") #or
tokenizer.save_pretrained("model")

# model = AutoModelForQuestionAnswering.from_pretrained("twmkn9/albert-base-v2-squad2")
model = AlbertForQuestionAnswering.from_pretrained('twmkn9/albert-base-v2-squad2')
dir(model)
model.save_pretrained("model")


####
# test querying
import torch

text = r"""
 🤗 Transformers (formerly known as pytorch-transformers and pytorch-pretrained-bert) provides general-purpose
 architectures (BERT, GPT-2, RoBERTa, XLM, DistilBert, XLNet…) for Natural Language Understanding (NLU) and Natural
 Language Generation (NLG) with over 32+ pretrained models in 100+ languages and deep interoperability between
 TensorFlow 2.0 and PyTorch.
 """

questions = [
    "How many pretrained models are available in 🤗 Transformers?",
     "What does 🤗 Transformers provide?",
     "🤗 Transformers provides interoperability between which frameworks?",
 ]

inputs = tokenizer(questions[0], text, add_special_tokens=True, return_tensors="pt")
input_ids = inputs["input_ids"].tolist()[0]
tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[:]))

test = tokenizer(questions[0], add_special_tokens=True, return_tensors="pt")
test = len(test["input_ids"].tolist()[0])
tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(test['input_ids'].tolist()[0]))
dir(inputs)
dir(input_ids)

text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
output = model(**inputs)
answer_start_scores = output['start_logits']
answer_end_scores = output['end_logits']

answer_start = torch.argmax(answer_start_scores).unsqueeze(0)
answer_end = torch.argmax(answer_end_scores).unsqueeze(0)

start_positions = torch.tensor([90])
end_positions = torch.tensor([input_ids.index(3)])
end_positions = torch.tensor([100])

outputs = model(**inputs, start_positions=answer_start, end_positions=answer_end)
outputs = model(**inputs, start_positions=start_positions, end_positions=end_positions)
loss = outputs.loss.item()
c = dir(outputs.loss)

answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

print(f"Question: {questions[0]}")
print(f"Answer: {answer}")


def test_yield(x):

   for y in range(x):
       if y < 10:
           yield y
   yield y

for i in test_yield(12):
    print(i)

a = {}
a = {1: '', 2: ''}
sorted(a.keys(), reverse=True)
