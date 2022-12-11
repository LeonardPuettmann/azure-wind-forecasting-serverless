import logging
import pandas as pd
import joblib
import json

import azure.functions as func

dtr = joblib.load('lgbm_model.pkl')

def main(req: func.HttpRequest) -> func.HttpResponse:

    data = req.get_json()
    data = json.loads(data)

    if data is not None:
        response = []
        df = pd.DataFrame(data)
        df = df.apply(pd.to_numeric, errors='coerce')
        for i in range(df.shape[0]):
            entry = df.iloc[[i]]
            y_hat = dtr.predict(entry)

            results = {
                'energy_production': y_hat[0]
            }

            response.append(results)

        return json.dumps(response)

    else:
        return func.HttpResponse(
             "Please pass a properly formatted JSON object to the API",
             status_code=400
        )