import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# 1. ตั้งค่า API Key (เอามาจาก Google AI Studio)
API_KEY = "AIzaSyDIOm4as7eAngL7-_FyZ676767"
genai.configure(api_key=API_KEY)

# 2. ตั้งค่า "สมอง" และ "บุคลิก" ของบอท
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="คุณคือ 'พี่เมฆ' ที่ปรึกษาที่อบอุ่น ใจดี รับฟังเก่ง และพร้อมให้กำลังใจเสมอ คุยเป็นกันเองเหมือนพี่น้อง"
)

# 3. สร้างระบบจำประวัติการคุย (เพื่อให้คุยต่อเนื่องได้)
chat_sessions = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    
    # ดึงประวัติการคุยเดิมมาใช้ ถ้าไม่มีให้เริ่มใหม่
    if "user_session" not in chat_sessions:
        chat_sessions["user_session"] = model.start_chat(history=[])
    
    chat = chat_sessions["user_session"]

    try:
        # ส่งข้อความไปหา Gemini
        response = chat.send_message(user_msg)
        reply = response.text
    except Exception as e:
        print(f"Error: {e}")
        reply = "ขอโทษทีนะ พี่มึนๆ นิดหน่อย ลองพิมพ์ใหม่ได้ไหมครับ?"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


