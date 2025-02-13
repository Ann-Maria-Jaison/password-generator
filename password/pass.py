from flask import Flask, request, jsonify
import random
import string
from flask_cors import CORS  # To handle cross-origin requests

app = Flask(__name__)
CORS(app)  # Allows frontend (HTML) to communicate with backend

def generate_password(length=16, use_lower=True, use_upper=True, use_digits=True, use_special=True):
    lower = string.ascii_lowercase if use_lower else ""
    upper = string.ascii_uppercase if use_upper else ""
    digits = string.digits if use_digits else ""
    special = "!@#$%^&*()_+{}[]:;<>,.?/|\\" if use_special else ""
    
    all_chars = lower + upper + digits + special
    if not all_chars:
        return "Error: Select at least one character type."

    password = "".join(random.choice(all_chars) for _ in range(length))
    return password

@app.route('/generate', methods=['GET'])
def generate():
    try:
        length = int(request.args.get("length", 16))
        use_lower = request.args.get("lowercase", "true") == "true"
        use_upper = request.args.get("uppercase", "true") == "true"
        use_digits = request.args.get("numbers", "true") == "true"
        use_special = request.args.get("special", "true") == "true"

        if length < 12 or length > 64:
            return jsonify({"error": "Password length must be between 12 and 64 characters"}), 400

        password = generate_password(length, use_lower, use_upper, use_digits, use_special)
        return jsonify({"password": password})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
