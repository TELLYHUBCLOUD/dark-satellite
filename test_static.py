# Quick Test Script for Flask Static Files

from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CSS Test</title>
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        <h1 class="hero-title">CSS Test</h1>
        <div class="glass-card">
            <p>If you see styling, CSS is working!</p>
        </div>
    </body>
    </html>
    '''

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    print("Starting Flask app...")
    print(f"Static folder: {os.path.abspath('static')}")
    print(f"CSS file exists: {os.path.exists('static/css/style.css')}")
    app.run(debug=True, port=5000)
