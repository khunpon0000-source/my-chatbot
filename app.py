print("APP STARTED")

from flask import Flask, request, jsonify, render_template
import random
import os

app = Flask(__name__)

# ดึง Dictionary คำตอบจากโค้ดเดิมของคุณ (ย่อเพื่อประหยัดพื้นที่ แต่ให้ใช้ชุดข้อมูลเดิมได้เลย)
replies = {
    'th': {
        'สวัสดี': ["หวัดดีฮะ มีอะไรให้กัดกลับคะ?", "ว่าไง พูดมาสิ อย่าช้า"],
        'ชื่อ': ["ฉันชื่อบอท ไม่ได้ชื่อปัญญาอ่อนเหมือนพวกมึง", "ถามชื่อทำไม? จะชวนไปสุกกี้หม้อรวมหรอ"],
        'default': ["โอ้โห คำถามนี้ปัญญาอ่อนจัง 😆", "ถามมาได้ เรื่องแค่นี้มึงไม่รู้ไงไอควาย 😏"]
    },
    'en': {
        'hello': ["Ugh, what do you want?", "Sup? Make it quick."],
        'name': ["I'm your father, not your buddy.", "Short and boring, just like your question."],
        'default': ["Whoa, that question is stupid 😆", "Honestly, I'm bored. Ask something better."]
    }
    # ... เพิ่ม ru, ja ตามโค้ดเดิมของคุณได้เลย ...
}

def get_reply(user_message, lang_code):
    msg = user_message.lower()
    lang_data = replies.get(lang_code, replies['th'])
    
    # เรียงลำดับ keyword จากยาวไปสั้น
    keywords = sorted([k for k in lang_data.keys() if k != 'default'], key=len, reverse=True)
    
    for kw in keywords:
        if kw in msg:
            return random.choice(lang_data[kw])
    
    return random.choice(lang_data['default'])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    lang = data.get("lang", "th")
    reply = get_reply(user_msg, lang)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    # host='0.0.0.0' เพื่อให้มือถือเข้าผ่าน IP คอมได้
    app.run(host='0.0.0.0', port=5000, debug=True)