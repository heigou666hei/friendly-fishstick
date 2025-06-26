from flask import Flask, request, Response
import openai
import requests

# === 配置：你的密钥和 Token 已经填好，无需改 ===
TELEGRAM_TOKEN = '8034625263:AAG8tXWLTl2RrRXju-Hh8TWeGxen4Lnk3Cs'
OPENAI_API_KEY = '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'

openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

# GPT 回复逻辑
def reply_to_message(chat_id, user_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_text}],
            temperature=0.7
        )
        reply_text = response.choices[0].message.content
    except Exception as e:
        reply_text = "⚠️ 出现错误，请稍后再试。

" + str(e)

    send_message(chat_id, reply_text)

# 向 Telegram 发送消息
def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

# webhook 路由（必须返回明确响应）
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    print("🛰 收到 Telegram 数据：", data)

    if data and "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]
        reply_to_message(chat_id, user_text)

    return Response("OK", status=200, mimetype='text/plain')

# 本地调试入口（生产部署无影响）
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
