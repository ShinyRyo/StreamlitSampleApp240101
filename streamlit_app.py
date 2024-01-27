import streamlit as st
import requests
import os
import json
from google.oauth2 import service_account
from google.cloud import bigquery
import datetime
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む（ローカル開発の場合）
load_dotenv()

# 環境変数からBigQueryの設定とAPIキー、カスタム検索エンジンIDを取得
project_id = os.getenv('BIGQUERY_PROJECT_ID')
dataset_name = os.getenv('BIGQUERY_DATASET_NAME')
table_name = os.getenv('BIGQUERY_TABLE_NAME')
api_key = os.getenv('GOOGLE_API_KEY')
cse_id = os.getenv('GOOGLE_CSE_ID')

# JSONキーファイルのパスを指定
service_account_file_path = './bigqueryry0-8a061de05cf8.json'

# ファイルからサービスアカウントキーを読み込む
with open(service_account_file_path) as f:
    service_account_info = json.load(f)
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# BigQueryクライアントを初期化
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# 検索用の関数
def google_search(query, api_key, cse_id, **kwargs):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id
    }
    params.update(kwargs)  # 任意の追加パラメータを含める
    response = requests.get(search_url, params=params)
    return response.json()

# BigQueryに結果を挿入する関数
def insert_results_to_bigquery(results, query):
    table_id = f"{project_id}.{dataset_name}.{table_name}"
    rows_to_insert = [
        {
            "query": query,
            "title": result.get('title'),
            "snippet": result.get('snippet'),
            "url": result.get('link'),
            # datetimeオブジェクトをISO形式の文字列に変換
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"  # BigQueryのタイムスタンプ形式に合わせる
        }
        for result in results.get('items', [])
    ]

    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        st.error("BigQueryへの挿入に失敗しました。エラー: {}".format(errors))
    else:
        st.success("検索結果をBigQueryに挿入しました。")

# 検索ボックス
query = st.text_input('検索', '')

# 検索ボタン
if st.button('検索'):
    results = google_search(query, api_key, cse_id, num=5)
    
    for result in results.get('items', []):
        title = result.get('title')
        snippet = result.get('snippet')
        link = result.get('link')
        
        st.subheader(title)
        st.write(snippet)
        st.markdown(f"[リンク]({link})")
    
    # BigQueryに結果を挿入
    insert_results_to_bigquery(results, query)
