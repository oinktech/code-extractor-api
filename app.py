from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_text_and_tags():
    data = request.json
    code = data.get('code', '')
    
    # 使用 BeautifulSoup 提取文字和标签
    soup = BeautifulSoup(code, 'html.parser')
    text_and_tags = []
    
    for element in soup.find_all():
        if element.string:
            text_and_tags.append({'tag': element.name, 'text': element.string.strip()})
    
    return jsonify(text_and_tags)

if __name__ == '__main__':
    app.run(debug=True)
