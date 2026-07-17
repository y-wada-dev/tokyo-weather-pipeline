from airflow.sdk import dag, task
from datetime import datetime

@dag(
    schedule="@daily",
    start_date=datetime(2026, 6, 1),   # 過去にするとbackfill練習ができる
    catchup=False,                      # まずFalseで。Week5でTrueにして観察
)
def weather_daily():

    @task
    def fetch_weather(ds=None) -> str:
        # TODO: Open-Meteo APIを叩き data/raw/{ds}.json に保存
        # 戻り値はファイルパス(これがXCom経由で次に渡る)
        print(f"fetching for {ds}")
        return f"dummy/{ds}.json"

    @task
    def validate_raw(path: str) -> str:
        print(path)
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