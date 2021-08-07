import torch
import spacy
import json
import pandas as pd
import csv
import time
from transformers import pipeline
from googletrans import Translator



if torch.cuda.is_available():
    device = torch.device("cuda")
    print('There are %d GPU(s) available.' % torch.cuda.device_count())
    print('We will use the GPU:', torch.cuda.get_device_name(0))
else:
    print('No GPU available, using the CPU instead.')
    device = torch.device("cpu")

from transformers import AutoTokenizer, AutoModelForQuestionAnswering

tokenizer = AutoTokenizer.from_pretrained("graviraja/covidbert_squad")
model = AutoModelForQuestionAnswering.from_pretrained("graviraja/covidbert_squad")
model.cuda()

questions = "¿Que es el COVID?"

translator = Translator()
texto = questions
translation = translator.translate(texto, dest='en')
print(translation.text)
questions = translation.text
question_answerer = pipeline("question-answering")

title = []
doi = []
abstract = []
url = []
publish_time = []
respuesta = []
score = []
start=time.process_time()
with open('C:/Users/USUARIO/Desktop/Articulos20_21.csv', encoding="utf8") as File:
    reader = csv.reader(File, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    num_rows = 0

    contador = 62000
    i = 31500
    for row in reader:
        if contador < 1:
            if i < 1:
                break
            i = i - 1
            print(i)
            num_rows += 1
            # print(num_rows)

            result = question_answerer(question=questions, context=row[2])
            x = (round(result['score'], 4))
            if x > 0.90:
                title.append(row[0])
                doi.append(row[1])
                abstract.append(row[2])
                url.append(row[3])
                publish_time.append(row[4])
                respuesta.append(result['answer'])
                score.append(round(result['score'], 4))
                print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}")
                print(row[0])
        else:
            contador = contador - 1

data = {'title': title,
        'doi': doi,
        'abstract': abstract,
        'url': url,
        'publish_time': publish_time,
        'respuesta': respuesta,
        'score': score}
df = pd.DataFrame(data, columns=['title', 'doi', 'abstract', 'url', 'publish_time', 'respuesta', 'score'])
# df.to_csv('SintomasV2_95%.csv')
df.to_csv('CovidPregunta90_Que_Es_2.csv', sep=';')
end=time.clock()
print("Tiempo ejecución: ",end-start)