from datetime import datetime

from airflow.sdk import dag, task

from src.pipelines.news_pipeline import NewsPipeline


@dag(
    dag_id="news_pipeline",
    schedule="0 */6 * * *",
    start_date=datetime(2025, 1, 1),
    catchup=False,
)
def news_pipeline():

    @task
    def run_pipeline():

        pipeline = NewsPipeline()

        pipeline.run()

    run_pipeline()


news_pipeline()