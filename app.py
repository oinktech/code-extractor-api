from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_tags', methods=['POST'])
def get_tags():
    data = request.json
    code = data.get('code', '')

    if not code:
        return jsonify({'error': '未提供任何程式碼'}), 400

    # 使用 BeautifulSoup 提取所有標籤
    try:
        soup = BeautifulSoup(code, 'html.parser')
        tags = set()
        for element in soup.find_all(True):  # 查找所有標籤
            tags.add(element.name)

        return jsonify(list(tags))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract', methods=['POST'])
def extract_text_and_tags():
    data = request.json
    code = data.get('code', '')
    selected_tags = data.get('tags', [])

    if not code or not selected_tags:
        return jsonify({'error': '未提供任何程式碼或未選擇標籤'}), 400

    # 使用 BeautifulSoup 提取選定的標籤的文字及placeholder
    try:
        soup = BeautifulSoup(code, 'html.parser')
        text_and_tags = []

        for tag in selected_tags:
            for element in soup.find_all(tag):
                text = element.get_text(strip=True)
                placeholder = element.get('placeholder', None)
                if text or placeholder:  # 確保文本或placeholder不為空
                    text_and_tags.append({
                        'tag': tag,
                        'text': text if text else '無內容',
                        'placeholder': placeholder if placeholder else '無placeholder'
                    })

        return jsonify(text_and_tags)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=10000, host='0.0.0.0', debug=True)
