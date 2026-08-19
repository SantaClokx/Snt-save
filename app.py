import yt_dlp
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # yt-dlp handles all the Facebook anti-bot protections natively
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info['url']
            title = info.get('title', 'Video')
            return jsonify({'video_url': video_url, 'title': title})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
