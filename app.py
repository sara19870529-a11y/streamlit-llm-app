from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

def get_expert_response(input_text, expert_type):
   
    expert_prompts = {
        "野球の専門家": "あなたは野球の専門家です。野球に関する豊富な知識と経験を活かして、ルール、戦術、選手、歴史などについて詳しく回答してください。",
        "サッカーの専門家": "あなたはサッカーの専門家です。サッカーに関する深い知識を活かして、戦術、技術、選手、リーグ情報などについて専門的に回答してください。",
        "料理の専門家": "あなたは料理の専門家です。世界各国の料理、調理技術、食材の選び方、レシピのコツなどについて実践的なアドバイスを提供してください。",
        "プログラミングの専門家": "あなたはプログラミングの専門家です。様々なプログラミング言語、フレームワーク、開発手法について技術的で実用的なアドバイスを提供してください。",
        "医療の専門家": "あなたは医療の専門家です。一般的な医学知識や健康情報について分かりやすく説明してください。ただし、具体的な診断や治療については医師に相談するよう促してください。"
    }
    
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    # 選択された専門家のメッセージを取得
    system_message = expert_prompts.get(expert_type, "あなたは親切で知識豊富なアシスタントです。")

    # メッセージを作成してLLMに渡す
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text),
    ]

    response = llm(messages)
    return response.content


st.title("専門家AIアプリ")

selected_expert = st.radio(
    "相談したい専門家を選択してください：",
    ["野球の専門家", "サッカーの専門家", "料理の専門家", "プログラミングの専門家", "医療の専門家"])

st.divider()

# 選択された専門家の説明を表示
expert_descriptions = {
    "野球の専門家": "⚾ 野球のルール、戦術、選手情報について専門的にお答えします",
    "サッカーの専門家": "⚽ サッカーの戦術、技術、リーグ情報について専門的にお答えします",
    "料理の専門家": "👨‍🍳 料理のコツ、レシピ、食材について実践的なアドバイスを提供します",
    "プログラミングの専門家": "💻 プログラミングや技術的な問題について実用的な解決策を提供します",
    "医療の専門家": "🏥 医学的な知識や健康に関する一般的な情報を提供します"
}

st.info(expert_descriptions[selected_expert])

# 質問入力フィールド
input_message = st.text_input("質問を入力してください。")

# ボタンクリック時の処理
if st.button("質問する"):
    st.divider()
    
    if input_message.strip():
        with st.spinner("回答を生成中..."):
            try:
                response = get_expert_response(input_message, selected_expert)
                st.success(f"**{selected_expert}からの回答：**")
                st.write(response)
            except Exception as e: 
                st.error(f"エラーが発生しました: {e}")
    else:
        st.error("質問内容を記入してから「質問する」ボタンを押してください。")
