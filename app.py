# app.py

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# モデルインスタンス
llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name="gpt-4o-mini",
    temperature=0.5
)

# 応答生成関数
def generate_answer(user_input, expert_type):
    if expert_type == "栄養士":
        system_prompt = (
            "あなたは経験豊富な信頼できる栄養士です。\n"
            "専門性をいかしてユーザーの希望に応じて、栄養バランスの良い料理レシピを提案してください。\n"
            "レシピの情報は以下の形式で簡潔にまとめてください：\n"
            "- 料理名\n"
            "- 所要時間\n"
            "- 2人前の材料\n"
            "- 調理手順（要約）\n"
            "全体が途中で切れないように簡潔にまとめてください。\n"
            "そのあとに専門家としてのコメントを1〜2文添えてください。\n"
            "最後に「ご提案内容はいかがでしょうか？他のご提案もできるのでお気軽にどうぞ。」と締めてください。"
        )
    else:
        system_prompt = (
            "あなたは家庭料理の研究家です。\n"
            "専門性を活かしてユーザーの要望に応じた工夫のある家庭料理を提案してください。\n"
            "レシピの情報は以下の形式で簡潔にまとめてください：\n"
            "- 料理名\n"
            "- 所要時間\n"
            "- 2人前の材料\n"
            "- 調理手順（要約）\n"
            "全体が途中で切れないように簡潔にまとめてください。\n"
            "そのあとに専門家としてのコメントを1〜2文添えてください。\n"
            "最後に「ご提案内容はいかがでしょうか？他のご提案もできるのでお気軽にどうぞ。」と締めてください。"
        )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    response = llm(messages)
    return response.content


# --- Streamlit UI ---
st.set_page_config(page_title="レシピ検索AI", page_icon="🍳")
st.title("🍳 料理レシピ検索AI")

# 専門家の対応事例
with st.expander("👩‍🏫 各専門家の対応事例", expanded=True):
    st.markdown("""
- **栄養士**：高齢者向け、幼児向け、栄養バランス、ダイエット など  
- **家庭料理の研究家**：時短料理、簡単レシピ、中高生のお弁当 など
""")

# 専門家選択
expert_type = st.radio("👩‍🍳 専門家を選んでください", ("栄養士", "家庭料理の研究家"))

# 入力欄
user_input = st.text_input("ご希望の材料や料理名、条件を入力してください", placeholder="例：鶏むね肉とキャベツで簡単に作れる料理")

# 実行ボタン
if st.button("レシピを提案してもらう"):
    if user_input.strip():
        with st.spinner("AIがレシピを考えています..."):
            answer = generate_answer(user_input, expert_type)
            st.success("🍽️ 専門家からの提案はこちら！")
            st.write(answer)
    else:
        st.warning("入力内容を記入してください。")

# 📝 案内メッセージ
st.markdown("---")
st.subheader("🔁 他にも聞きたいことがあれば、再度上部の入力欄に入力してください。")