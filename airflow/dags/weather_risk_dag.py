from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="weather_risk_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "retries":2,
        "retry_delay" : timedelta(minutes=2)
    }
) as dag:

    extract = BashOperator(
        task_id ="extract_weather",
        bash_command="python /opt/airflow/src/extract_weather.py",
    )

    transform = BashOperator(
        task_id ="transform_weather",
        bash_command="python /opt/airflow/src/transform.py",
    )

    gold = BashOperator(
        task_id ="calculate_weather_risk",
        bash_command="python /opt/airflow/src/gold.py",
    )

    load = BashOperator(
        task_id = "load_to_postgresql",
        bash_command="python /opt/airflow/src/load.py"
    )

    extract >> transform >> gold >> load