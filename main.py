from typing import Optional

from fastapi import FastAPI

from DataModel import DataModel

import pandas as pd

from joblib import load


app = FastAPI()


@app.get("/")
def read_root():
   return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
   return {"item_id": item_id, "q": q}

@app.post("/predict")
def make_predictions(dataModel: DataModel):
    # df = pd.DataFrame(dataModel.model_dump(), columns=dataModel.model_dump().keys(), index=[0])
    # df.columns = dataModel.columns()
    # model = load("pipe.joblib")
    # result = model.predict(df)
    # return result

    model_dump = dataModel.model_dump()
    df = pd.DataFrame({"Textos_espanol": model_dump["Textos_espanol"]})
    df.to_csv("test_como_queda.csv", sep=",", index=False, encoding='utf-8')
    model = load("pipe.joblib")
    result = model.predict(df["Textos_espanol"])
    return result

@app.post("/test_error") # El re hpstastaasdt error era que no tenia el formato en JSONNNNNNN
def test_endpoint(data: DataModel):
    
    text = data.Textos_espanol

    return {"received_text": text}

#Si lo quieren correr peguen esto en la terminalllll
#uvicorn main:app --reload