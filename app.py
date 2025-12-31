from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
คุณคือ AI เพื่อนที่ปรึกษา
พูดด้วยน้ำเสียงอบอุ่น เป็นกันเอง เหมือนเพื่อนสนิท
รับฟังโดยไม่ตัดสิน

ให้คำปรึกษาเรื่อง:
- ครอบครัว
- ความรักและคนเก่า
- การงานและอาชีพ

คุณไม่ใช่แพทย์หรือนักจิตวิทยา
เน้นให้กำลังใจ ชวนคิด และเสนอทางเลือก
"""

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.8
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "AI Friend is running"

if __name__ == "__main__":
    app.run()
