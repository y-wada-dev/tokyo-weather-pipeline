from airflow.sdk import dag, task
from datetime import datetime
import requests
import json
import os
import pandas as pd

@dag(
    schedule="@daily",
    start_date=datetime(2026, 6, 1),   # 過去にするとbackfill練習ができる
    catchup=False,                      # まずFalseで。Week5でTrueにして観察
)
def weather_daily():

    @task
    def fetch_weather(ds=None) -> str:
        # 戻り値はファイルパス(これがXCom経由で次に渡る)

        url="https://api.open-meteo.com/v1/forecast"
        
        response = requests.get(
            url,
            params={
                'latitude':'35',
                'longitude':'139',
                'hourly':'temperature_2m',
                'timezone':'Asia/Tokyo',
                'start_date':ds,
                'end_date':ds,
                }
            )
        response.raise_for_status()
        data = response.json()

        path = f"/opt/airflow/data/raw/{ds}.json"
        dirname = os.path.dirname(path)
        os.makedirs(dirname, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Complete fetch for {ds}")
        return path

    @task
    def validate_raw(path: str) -> str:
        print(path)
        with open(path) as f:
            data = json.load(f)

        required_keys = ["latitude", "longitude", "hourly"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"missing key: {key}")
            
        if not isinstance(data["hourly"], dict):
            raise ValueError("hourly must be an object")
            
        return path

    @task
    def transform(path: str, ds=None) -> str:
        print(path)
        save_path = f"/opt/airflow/data/transformed/transformed_{ds}.csv"
        dirname = os.path.dirname(save_path)
        os.makedirs(dirname, exist_ok=True)
        
        with open(path, encoding='utf-8') as f:
            d = json.load(f)
        df = pd.DataFrame(d["hourly"])
        # column1=time, type:string (ISO8601 format, e.g. 2026-07-24T00:00)
        # column2=temperature_2m, type:float
        df.to_csv(save_path, index=False)
        return save_path
    
    @task
    def load_to_db(path: str, ds=None) -> None:
        # TODO: DELETE WHERE date = ds してから INSERT
        
        print(f"loading {path} for {ds}")

    load_to_db(transform(validate_raw(fetch_weather())))

weather_daily()