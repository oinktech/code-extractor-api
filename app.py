from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup, NavigableString
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_text_and_tags():
    data = request.json
    code = data.get('code', '')

    if not code:
        return jsonify({'error': '未提供任何程式碼'}), 400

    # 使用 BeautifulSoup 提取文字和標籤
    try:
        soup = BeautifulSoup(code, 'html.parser')
        text_and_tags = []

        for element in soup.find_all():
            # 只提取可見的文字
            if isinstance(element, NavigableString) and element.strip():
                text_and_tags.append({'tag': element.parent.name, 'text': element.strip()})

        return jsonify(text_and_tags)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=10000, host='0.0.0.0', debug=True)
