from flask import Flask, request, jsonify, send_from_directory
import os
import youtube_dl

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    content_type = data.get('contentType')
    quality = data.get('quality')
    
    if content_type == 'video':
        ydl_opts = {
            'format': f'bestvideo[height<={quality[:-1]}]+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url)
            filename = ydl.prepare_filename(result)
        
        return jsonify({'success': True, 'fileUrl': f'/downloads/{os.path.basename(filename)}'})
    elif content_type == 'image':
        # Image downloading logic
        pass

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory('downloads', filename)

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)