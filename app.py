from flask_cors import CORS # Tambahkan di area import atas

app = Flask(__name__)
CORS(app) # Tambahkan tepat di bawah inisialisasi app



from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from google import genai

# file .env
load_dotenv()

app = Flask(__name__)

# Konfigurasi AI
API_KEY = os.getenv("AI_API_KEY")
client = genai.Client(api_key=API_KEY)

#  System Instruction
instruksi_sekolah = """
Kamu adalah asisten virtual resmi untuk SMA Trisakti. 
Tugas utamamu adalah menjawab pertanyaan seputar sekolah ini.
Data sekolah:
- Alamat: Jl. Contoh Sekolah No. 1, Jakarta
- Jurusan: IPA, IPS, dan Bahasa
- Fasilitas: Perpustakaan 3 lantai, Lab Komputer, Lapangan Basket.
Jika pengguna bertanya hal di luar konteks sekolah, tolak dengan sopan dan katakan bahwa kamu hanya bisa menjawab informasi sekolah.
"""

@app.route('/')
def beranda():
    return {"pesan": "Backend Chatbot Sekolah Menyala!"}

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    pesan_user = data.get("pesan")

    if not pesan_user:
        return jsonify({"error": "Pesan tidak boleh kosong"}), 400

    try:
        # Mengirim pesan menggunakan cara terbaru dari google.genai
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=pesan_user,
            config=genai.types.GenerateContentConfig(
                system_instruction=instruksi_sekolah
            )
        )
        return jsonify({"balasan": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
