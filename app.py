from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob

app = Flask(__name__)
CORS(app)

def analyze_quote(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.3:
        sentiment = "Inspirational 💡"
    elif polarity > 0:
        sentiment = "Positive ✨"
    elif polarity < 0:
        sentiment = "Reflective / Deep 🧠"
    else:
        sentiment = "Neutral 📄"

    return sentiment, round(polarity, 2)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    quote_text = data.get('quote', '')
    
    if not quote_text:
        return jsonify({'error': 'No quote provided'}), 400

    sentiment, score = analyze_quote(quote_text)
    
    return jsonify({
        'quote': quote_text,
        'sentiment': sentiment,
        'polarity_score': score
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)