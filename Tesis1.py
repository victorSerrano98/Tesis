
from transformers import pipeline
question_answerer = pipeline("question-answering")
from googletrans import Translator
from vespa.application import Vespa
from vespa.query import Union, WeakAnd, ANN
from random import random
from vespa.query import QueryModel, RankProfile, QueryRankingFeature
import spacy

# questions = "¿Cuánto tiempo tardan en aparecer los síntomas del covid-19?"
def traductor(questions):
    translator = Translator()
    translation = translator.translate(questions, dest='en')
    questions = translation.text
    return questions

def spa(questions):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(questions)
    query = ""
    for chunk in doc.noun_chunks:
        print(chunk.root.text, chunk.root.dep_,
              chunk.root.head.text)
        if chunk.root.dep_=="pobj":
            query="covid-19 "+ chunk.root.text
    return query

def vespa(query):
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
        'hits': 150,
        'query': query,
        'type': 'JournalArticle',
        'ranking': 'bm25'
    }).hits
    # Eliminar repetidos mediante el abstract
    # result = {each["fields"]["abstract-full"]: each for each in query_result}.values()
    return query_result

def respuesta(questions,result):
    list = ""
    for res in result:
        try:
            result = question_answerer(question=questions, context=res["fields"]["abstract-full"])
            x = (round(result['score'], 4))
            if x > 0.90:
                resp = result['answer']
                titulo = res["fields"]["title-full"]
                list = list + '\n \n' + resp + '\n \n '+titulo
        except:
            print("Error")
    return list
