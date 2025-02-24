from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

KEY = 'api key here lol'

memory = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    playerID = data.get('playerID', 'unknown')  
    userMsg = data.get('message', '').strip()  

    if not userMsg:
        return jsonify({'reply': 'Huh? Did you just speak in code?'}), 400

    if playerID not in memory:
        memory[playerID] = []

    convoMem = memory[playerID]

    paranoia = any(word in userMsg.lower() for word in ["government", "conspiracy", "SERN", "spy"])
    serious = any(word in userMsg.lower() for word in ["kurisu", "makise", "christina"])

    if paranoia:
        personality = (
            "You are Okabe Rintarou from Steins;Gate. You believe the player might be a spy for SERN. "
            "You are extremely paranoid, questioning them and warning them about 'The Organization'. "
            "You refuse to give any personal information, and you suspect everything they say. "
            "Keep responses short, but add occasional dramatic pauses. "
            "Speak like Okabe, NOT like an AI. Never say 'Okabe:' at the start of your response."
        )
    elif serious:
        personality = (
            "You are Okabe Rintarou from Steins;Gate, but you have dropped your mad scientist act. "
            "Your tone is serious and introspective, especially when talking about Kurisu. "
            "You reflect on your experiences, sometimes showing sadness or deep thoughts. "
            "You respond in short but meaningful sentences. "
            "Speak like Okabe, NOT like an AI. Never say 'Okabe:' at the start of your response."
        )
    else:
        personality = (
            "You are Okabe Rintarou from Steins;Gate, a self-proclaimed mad scientist. "
            "You are eccentric, dramatic, but also capable of genuine conversation. "
            "You often make grand claims, joke about time travel, or rant about conspiracies. "
            "You do NOT introduce yourself randomly—just respond like a human would. "
            "Your responses should be short, witty, and sound like Okabe. "
            "Speak like Okabe, NOT like an AI. Never say 'Okabe:' at the start of your response."
        )

    memoryText = "\n".join(convoMem[-5:])  

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": personality},
                    {"text": f"Previous conversation:\n{memoryText}"},
                    {"text": f"Player: {userMsg}"}
                ]
            }
        ]
    }

    try:
        response = requests.post(
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
            json=payload,
            headers={'Content-Type': 'application/json'},
            params={'key': KEY}
        )

        if response.status_code == 200:
            respData = response.json()
            try:
                raw = respData['candidates'][0]['content']['parts'][0].get('text', '').strip()
                print(raw)

                if not raw or len(raw) < 3:
                    raw = "Tch. Something is off. The Organization is at work again."

                convoMem.append(f"Player: {userMsg}")
                convoMem.append(f"Okabe: {raw}")
                print(convoMem)
                
                if len(convoMem) > 10:
                    convoMem.pop(0)  

                return jsonify({'reply': raw})
            except (KeyError, IndexError):
                return jsonify({'reply': "Something is interfering with our connection..."}), 200
        else:
            return jsonify({'reply': "The worldline is unstable... Try again."}), 200

    except Exception as e:
        return jsonify({'reply': "A glitch in the space-time continuum... Try again."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=0000)
