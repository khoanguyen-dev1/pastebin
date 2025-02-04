from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/bypass', methods=['GET'])
def get_paste():
    paste_url = request.args.get('url')
    if not paste_url:
        return jsonify({'error': 'Vui lòng cung cấp URL'}), 400

    parsed_url = urlparse(paste_url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    if len(path_parts) < 1:
        return jsonify({'error': 'URL không hợp lệ'}), 400

    paste_id = path_parts[-1]
    raw_url = f'https://pastebin.com/raw/{paste_id}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(raw_url, headers=headers)
        response.raise_for_status()
        return jsonify({'text': response.text})
    except requests.exceptions.HTTPError:
        return jsonify({'error': 'Không tìm thấy paste hoặc paste không công khai'}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Lỗi khi lấy dữ liệu: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
