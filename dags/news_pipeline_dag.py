import json
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
}

def load_api_configs():
    """Load API configurations - Đọc thẳng từ thư mục dags để test UI"""
    # Tìm file api_sources.json nằm cùng cấp với file DAG này
    config_path = os.path.join(os.path.dirname(__file__), 'api_sources.json')
    
    if not os.path.exists(config_path):
        print("⚠️ Không tìm thấy file JSON. Dùng mock data để vẽ DAG.")
        return [{"api_id": "mock_api_1", "is_active": True}]

    print(f"✅ Loading config from: {config_path}")
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_and_transform(api_config: dict, **kwargs):
    """Task: Extract từ API → Transform → Lưu file JSON staging"""
    try:
        from src.clients.base_client import APIClient
        from src.adapters.factory import AdapterFactory

        print(f"🚀 Starting extract for: {api_config['api_id']}")

        client = APIClient()
        raw_data = client.fetch(api_config)

        if not raw_data:
            print(f"⚠️ No data from {api_config['api_id']}")
            return 0

        # Transform
        adapter = AdapterFactory.get_adapter(api_config.get("adapter_type"), raw_data)
        clean_records = adapter.normalize()

        # Save to staging
        staging_dir = '/opt/airflow/test_output'
        os.makedirs(staging_dir, exist_ok=True)
        
        output_file = os.path.join(staging_dir, f"{api_config['api_id']}_staging.json")
        
        dict_records = [record.to_dict() for record in clean_records]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dict_records, f, ensure_ascii=False, indent=4)

        print(f"✅ Saved {len(clean_records)} records from {api_config['api_id']}")
        return len(clean_records)

    except Exception as e:
        print(f"❌ Error processing {api_config.get('api_id')}: {e}")
        raise


def load_to_warehouse(**kwargs):
    """Task: Load tất cả file JSON trong staging vào Database"""
    try:
        from src.db.news_loader import NewsLoader
        
        print("📦 Starting load to PostgreSQL...")
        loader = NewsLoader()
        
        # Optional: Tạo bảng nếu chưa có
        # loader.init_database()
        
        staging_dir = '/opt/airflow/test_output'
        loader.load_json_to_db(staging_dir)
        
        print("🎉 Load phase completed!")
        
    except Exception as e:
        print(f"❌ Load failed: {e}")
        raise


# ==================== DAG DEFINITION ====================
with DAG(
    dag_id='news_lake_daily_pipeline',
    default_args=default_args,
    description='News Lake Pipeline - Extract → Transform → Load',
    schedule='@hourly',           # hoặc '@daily'
    start_date=datetime(2026, 6, 1),
    catchup=False,
    tags=['news', 'etl', 'pipeline'],
    max_active_runs=1,            # Tránh chạy chồng chéo
) as dag:

    start = EmptyOperator(task_id='start_pipeline')
    end = EmptyOperator(task_id='end_pipeline')

    load_task = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_warehouse,
    )

    api_configs = load_api_configs()

    for config in api_configs:
        if config.get("is_active", False):
            task_id = f"extract_{config['api_id']}"

            extract_task = PythonOperator(
                task_id=task_id,
                python_callable=extract_and_transform,
                op_kwargs={'api_config': config},
            )

            # Flow
            start >> extract_task >> load_task

    load_task >> end