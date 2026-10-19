import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)

analyzer = SentimentIntensityAnalyzer()

# قائمة الكلمات السلبية الحاسمة التي تمنع التصنيف الإيجابي الخاطئ
NEGATIVE_TRIGGER_WORDS = {'ugly', 'sad', 'hurt', 'mean', 'bad', 'hate', 'cry', 'worst', 'lonely', 'depressed'}

def analyze_quote(text):
    text_lower = text.lower()
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']

    # فحص الكلمات السلبية القاطعة
    has_negative_trigger = any(word in text_lower for word in NEGATIVE_TRIGGER_WORDS)

    if has_negative_trigger and compound > 0:
        # خفض النتيجة إذا وُجدت كلمات سلبية حاسمة رغم وجود كلمات إيجابية
        compound = -abs(compound) if compound != 0 else -0.35

    if compound >= 0.35:
        sentiment = "Inspirational 💡"
        category = "positive"
    elif compound > 0.05:
        sentiment = "Positive ✨"
        category = "positive"
    elif compound <= -0.35:
        sentiment = "Negative / Sensitive 🌧️"
        category = "negative"
    elif compound < -0.05:
        sentiment = "Reflective / Deep 🧠"
        category = "reflective"
    else:
        sentiment = "Neutral 📄"
        category = "neutral"

    return sentiment, round(compound, 2), category

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    quote_text = data.get('quote', '')
    
    if not quote_text:
        return jsonify({'error': 'No quote provided'}), 400

    sentiment, score, category = analyze_quote(quote_text)
    
    return jsonify({
        'quote': quote_text,
        'sentiment': sentiment,
        'polarity_score': score,
        'category': category
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    