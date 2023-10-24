from typing import Optional

from fastapi import FastAPI

from DataModel import DataModel

import pandas as pd

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
    # df = pd.DataFrame(dataModel.model_dump(), columns=dataModel.model_dump().keys(), index=[0])
    # df.columns = dataModel.columns()
    # model = load("pipe.joblib")
    # result = model.predict(df)
    # return result
    model_dump = dataModel.dict()
    df = pd.DataFrame({"Textos_espanol": model_dump["Textos_espanol"]})
    df.to_csv("test_como_queda.csv", sep=",", index=False, encoding='utf-8')
    model = load('pipe.joblib')
    df['sdg'] = model.predict(df["Textos_espanol"])
    return df.to_dict(orient="records")

@app.post("/test_error") # El re hpstastaasdt error era que no tenia el formato en JSONNNNNNN
def test_endpoint(data: DataModel):
    
    text = data.Textos_espanol

    return {"received_text": text}

#Si lo quieren correr peguen esto en la terminalllll
#uvicorn main:app --reload