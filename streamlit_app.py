import streamlit as st
import requests
from dotenv import load_dotenv
import os

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

# .envファイルを読み込む
load_dotenv()

# 環境変数からAPIキーとカスタム検索エンジンIDを取得
api_key = os.getenv('GOOGLE_API_KEY')
cse_id = os.getenv('GOOGLE_CSE_ID')

# 取得した値をチェック
if not api_key or not cse_id:
    st.error("環境変数からAPIキーまたは検索エンジンIDを取得できませんでした。")
    st.stop()

# 検索ボックス
query = st.text_input('検索', '')

# 検索ボタン
if st.button('検索'):
    # 検索を実行
    results = google_search(query, api_key, cse_id, num=5)

    # 結果を表示
    for result in results.get('items', []):
        title = result.get('title')
        snippet = result.get('snippet')
        link = result.get('link')
        
        st.subheader(title)
        st.write(snippet)
        st.markdown(f"[リンク]({link})")

