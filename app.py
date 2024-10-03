from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 获取标签路由
@app.route('/get_tags', methods=['POST'])
def get_tags():
    data = request.json
    code = data.get('code', '')

    if not code.strip():
        return jsonify({'error': '未提供任何程式碼'}), 400

    try:
        soup = BeautifulSoup(code, 'html.parser')
        tags = set(element.name for element in soup.find_all(True))
        if not tags:
            return jsonify({'error': '未找到任何標籤'}), 404
        return jsonify(list(tags))
    except Exception as e:
        return jsonify({'error': f'處理失敗: {str(e)}'}), 500

# 提取文字和标签路由
@app.route('/extract', methods=['POST'])
def extract_text_and_tags():
    data = request.json
    code = data.get('code', '')
    selected_tags = data.get('tags', [])

    if not code.strip() or not selected_tags:
        return jsonify({'error': '未提供程式碼或未選擇標籤'}), 400

    try:
        soup = BeautifulSoup(code, 'html.parser')
        text_and_tags = []

        for tag in selected_tags:
            for element in soup.find_all(tag):
                text = element.get_text(strip=True) or '無內容'
                placeholder = element.get('placeholder', None) or '無placeholder'
                text_and_tags.append({
                    'tag': tag,
                    'text': text,
                    'placeholder': placeholder
                })

        if not text_and_tags:
            return jsonify({'error': '未找到相關內容'}), 404

        return jsonify(text_and_tags)
    except Exception as e:
        return jsonify({'error': f'處理失敗: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=10000, host='0.0.0.0', debug=True)
