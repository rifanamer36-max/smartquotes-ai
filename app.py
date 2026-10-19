from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)

analyzer = SentimentIntensityAnalyzer()

def analyze_quote(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']  # النتيجة الشاملة من -1 إلى 1

    if compound >= 0.3:
        sentiment = "Inspirational 💡"
    elif compound > 0.05:
        sentiment = "Positive ✨"
    elif compound <= -0.3:
        sentiment = "Stress / Negative 🌧️"
    elif compound < -0.05:
        sentiment = "Reflective / Deep 🧠"
    else:
        sentiment = "Neutral 📄"

    return sentiment, round(compound, 2)

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

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    