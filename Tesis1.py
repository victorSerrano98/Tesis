import requests
import spacy
import time
import json
import pandas as pd
import torch
from transformers import pipeline
from googletrans import Translator
from vespa.application import Vespa
from vespa.query import Union, WeakAnd, ANN
from random import random
from vespa.query import QueryModel, RankProfile, QueryRankingFeature

if torch.cuda.is_available():
    device = torch.device("cuda")
    print('There are %d GPU(s) available.' % torch.cuda.device_count())
    print('We will use the GPU:', torch.cuda.get_device_name(0))
else:
    print('No GPU available, using the CPU instead.')
    device = torch.device("cpu")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

from transformers import AutoTokenizer, AutoModelForQuestionAnswering

tokenizer = AutoTokenizer.from_pretrained("graviraja/covidbert_squad")
model = AutoModelForQuestionAnswering.from_pretrained("graviraja/covidbert_squad")
if torch.cuda.is_available():
    model.cuda()
else:
    print("Do Nothing. Run as CPU")

question_answerer = pipeline("question-answering")
# questions = "¿Cuánto tiempo tardan en aparecer los síntomas del covid-19?"
def traductor(questions):
    translator = Translator()
    texto = questions
    translation = translator.translate(texto, dest='en')
    print(translation.text)
    questions = translation.text
    return questions



nlp = spacy.load("en_core_web_sm")
doc = nlp(questions)
query = ""
for chunk in doc.noun_chunks:
    print(chunk.root.text, chunk.root.dep_,
          chunk.root.head.text)
    if chunk.root.dep_=="pobj":
        query="covid-19 "+ chunk.root.text

print(query)


app = Vespa(url="https://api.cord19.vespa.ai")

match_phase = Union(
    WeakAnd(hits=10),
    ANN(
        doc_vector="title_embedding",
        query_vector="title_vector",
        hits=10,
        label="title"
    )
)

rank_profile = RankProfile(name="bm25", list_features=True)

query_model = QueryModel(
    query_properties=[QueryRankingFeature(
        name="title_vector",
        mapping=lambda x: [random() for x in range(768)]
    )],
    match_phase=match_phase, rank_profile=rank_profile
)

query_result = app.query(body={
    'yql': 'select title-full, abstract-full,url,doi from sources * where userQuery();',
    'hits': 100,
    'query': query,
    'type': 'JournalArticle',
    'ranking': 'bm25'
}).hits
print(query_result)
# Eliminar repetidos mediante el abstract
unique = {each["fields"]["abstract-full"] : each for each in query_result }.values()

for res in unique:
    try:
        result = question_answerer(question=questions, context=res["fields"]["abstract-full"])
        x = (round(result['score'], 4))
        if x > 0.90:
            print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}")
            print(res["fields"]["title-full"])
    except:
        x = "nada"

# search_request_all = {
#     'yql': 'select id,title, abstract, doi from sources * where userQuery();',
#     'hits': 250,
#     'type': 'JournalArticle',
#     'summary': 'short',
#     'timeout': '1.0s',
#     'query': 'covid-19 symptoms time',
#     'ranking': 'default'
# }
# response = requests.post('https://api.cord19.vespa.ai/search/', json=search_request_all)
# print(response.text)
# with open('datos100.json', 'w') as file:
#     json.dump(json.loads(response.text), file, indent=4)


# for res in json.loads(response.text)["root"]["children"]:
#     try:
#         result = question_answerer(question=questions, context=res["fields"]["abstract"])
#         x = (round(result['score'], 4))
#         if x > 0.90:
#             print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}")
#     except:
#         x="nada"
