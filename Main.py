import os
from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = os.environ.get("8959181336:AAH2XrxLUq6rfXzaI8BH2M-sB2YIwND_7xY", "")
CHAT_ID   = os.environ.get("6161785377", "")

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    })

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Bot Running OK ✅"})

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = json.loads(request.get_data(as_text=True))
        sig  = data.get("signal", "")
        pair = data.get("pair",   "N/A")
        entry= data.get("entry",  "N/A")
        sl   = data.get("sl",     "N/A")
        tp1  = data.get("tp1",    "N/A")
        tp2  = data.get("tp2",    "N/A")
        tp3  = data.get("tp3",    "N/A")
        score= data.get("score",  "N/A")
        tf   = data.get("timeframe","N/A")
        now  = datetime.utcnow().strftime("%H:%M UTC")

        if sig == "BUY":
            msg = (
                f"━━━━━━━━━━━━━━━━━\n"
                f"✅ *BUY SIGNAL*\n"
                f"━━━━━━━━━━━━━━━━━\n"
                f"📌 Pair: `{pair}`\n"
                f"⏱ TF: `{tf}`\n"
                f"🏆 Score: `{score}/10`\n"
                f"━━━━━━━━━━━━━━━━━\n"
                f"🎯 Entry: `{entry}`\n"
                f"🛑 SL: `{sl}`\n"
                f"✅ TP1: `{tp1}`\n"
                f"✅ TP2: `{tp2}`\n"
                f"🥇 TP3: `{tp3}`\n"
                f"━━━━━━━━━━━━━━━━━\n"
                f"🕐 {now}"
            )
        elif sig == "SELL":
            msg = (
                f"━━━━━━━━━━━━━━━━━\n"
                f"🔴 *SELL SIGNAL*\n"
                f"━━━━━━━━━━━━━━━━━\n"
                f"📌 Pair: `{pair}`\n"
                f"⏱ TF: `{tf}`\n"
                f"🏆 Score: `{score}/10`\n"
                f"━━━━━━━━━━━━━━━━━\n"
                f"🎯 Entry: `{entry}`\n"
                f"🛑 SL: `{sl}`\n"
                f"✅ TP1: `{tp1}`\n"
                f"✅ TP2: `{tp2}`\n"
                f"🥇 TP3: `{tp3}`\n"
                f"━━━━━━━━━━━━━━━━━\n"
                f"🕐 {now}"
            )
        else:
            msg = f"⚡ Alert: {sig} on {pair} at {entry}"

        send_msg(msg)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/test", methods=["GET"])
def test():
    send_msg(
        "━━━━━━━━━━━━━━━━━\n"
        "✅ *BUY SIGNAL* — TEST\n"
        "━━━━━━━━━━━━━━━━━\n"
        "📌 Pair: `XAUUSD`\n"
        "🏆 Score: `8.5/10`\n"
        "🎯 Entry: `2345.50`\n"
        "🛑 SL: `2330.00`\n"
        "✅ TP1: `2360.00`\n"
        "✅ TP2: `2378.00`\n"
        "🥇 TP3: `2400.00`\n"
        "━━━━━━━━━━━━━━━━━\n"
        "🤖 _Inducement Cycles Bot_"
    )
    return jsonify({"status": "Test signal sent ✅"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
