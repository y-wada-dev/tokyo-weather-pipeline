from airflow.sdk import dag, task
from datetime import datetime
import requests
import json
import os

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
        return f"dummy/transformed_{ds}.json"
    
    @task
    def load_to_db(path: str, ds=None) -> None:
        # TODO: DELETE WHERE date = ds してから INSERT
        
        print(f"loading {path} for {ds}")

    load_to_db(transform(validate_raw(fetch_weather())))

weather_daily()