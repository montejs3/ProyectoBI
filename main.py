from typing import Optional

from fastapi import FastAPI, File, UploadFile
import codecs
import csv

from DataModel import DataModel

import pandas as pd
import io

from joblib import load

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from DataModel import DataModel
import pandas as pd
from joblib import load

app = FastAPI()

allowed_origins = [
    "http://localhost:3000",
]

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods if needed
    allow_headers=["*"],  # You can specify specific headers if needed
)



@app.post("/predict")
def make_predictions(dataModel: DataModel):
    model_dump = dataModel.dict()
    df = pd.DataFrame({"Textos_espanol": model_dump["Textos_espanol"]})
    df.to_csv("logEntrada.csv", sep=",", index=False, encoding='utf-8')
    model = load('pipe.joblib')
    df['sdg'] = model.predict(df["Textos_espanol"])
    return df.to_dict(orient="records")




@app.post("/test_error") # El re hpstastaasdt error era que no tenia el formato en JSONNNNNNN
def test_endpoint(data: DataModel):
    
    text = data.Textos_espanol

    #return {"received_text": text}
    return {"received_text": [6]}

@app.post("/uploadCsv")
def uploadCsv(file: UploadFile = File(...)):
    # csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    # data = {}
    # for rows in csvReader:             
    #     key = rows['Textos_espanol'] 
    #     data[key] = rows  
    
    # file.file.close()
    # return data
    data = file.file.read()
    df = pd.read_csv(io.BytesIO(data)) 
    #df = df.replace([pd.np.inf, -pd.np.inf], pd.np.nan)
    
    #records = df.to_dict(orient="records")
    #json_data = df.to_json(orient="records")
    records = df.to_dict(orient="records")
    return records

@app.post("/uploadExcel")
def uploadExcel(file: UploadFile = File(...)):
    #csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    # df = pd.read_csv(file.file, encoding='utf-8')
    
    # return df.to_dict(orient="records")

    # El problema es que el archivo no es como los que tenemos
    # en el directorio sino que es un archivo como tal y tenemos
    # que leer los bytes del archivo procesarlo nosotros mismos
    # ya funciona pero pero el formato no esta cool

    data = file.file.read()
    df = pd.read_excel(io.BytesIO(data), engine="openpyxl") 
    #df = df.replace([pd.np.inf, -pd.np.inf], pd.np.nan)
    
    json_data = df.to_json(orient="records")

    return json_data

    #Esto funciona con csv pero no excel, toca ver por que

    # records = df.to_dict(orient="records")
    # return records


#Si lo quieren correr peguen esto en la terminalllll
#uvicorn main:app --reload