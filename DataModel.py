from pydantic import BaseModel
from typing import List

class DataModel(BaseModel):

# Estas varibles permiten que la librería pydantic haga el parseo entre el Json recibido y el modelo declarado.
    Textos_espanol: List[str]
    #Textos_espanol: List[dict], este es un cambio que se podría discutir en equipo
                    # pero siento que no es necesario ya que no afecta la implementación


#Esta función retorna los nombres de las columnas correspondientes con el modelo esxportado en joblib.
    def columns(self):
        return ["Textos_espanol"]
