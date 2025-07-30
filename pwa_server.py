"""
PWA File Server - Serves manifest.json, sw.js, and PWA files
Run this alongside your Streamlit app for full PWA functionality
"""

from flask import Flask, send_file, send_from_directory, Response
import os
from pathlib import Path

app = Flask(__name__)

# Set the base directory to the current working directory
BASE_DIR = Path(__file__).parent

@app.route('/manifest.json')
def serve_manifest():
    """Serve the manifest.json file with correct MIME type"""
    try:
        return send_file(
            BASE_DIR / 'manifest.json',
            mimetype='application/json',
            as_attachment=False
        )
    except FileNotFoundError:
        return Response("Manifest file not found", status=404)

@app.route('/sw.js')
def serve_service_worker():
    """Serve the service worker with correct MIME type"""
    try:
        return send_file(
            BASE_DIR / 'sw.js',
            mimetype='application/javascript',
            as_attachment=False
        )
    except FileNotFoundError:
        return Response("Service worker not found", status=404)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (icons, etc.)"""
    try:
        return send_from_directory(BASE_DIR / 'static', filename)
    except FileNotFoundError:
        return Response("File not found", status=404)

@app.route('/pwa.html')
def serve_pwa_page():
    """Serve the PWA landing page"""
    try:
        return send_file(
            BASE_DIR / 'pwa.html',
            mimetype='text/html'
        )
    except FileNotFoundError:
        return Response("PWA page not found", status=404)

@app.route('/bhagavad_gita_verses.csv')
def serve_csv():
    """Serve the Gita verses CSV for offline caching"""
    try:
        return send_file(
            BASE_DIR / 'bhagavad_gita_verses.csv',
            mimetype='text/csv',
            as_attachment=False
        )
    except FileNotFoundError:
        return Response("CSV file not found", status=404)

@app.route('/Public/Images/<path:filename>')
def serve_images(filename):
    """Serve images from Public/Images directory"""
    try:
        return send_from_directory(BASE_DIR / 'Public' / 'Images', filename)
    except FileNotFoundError:
        return Response("Image not found", status=404)

@app.route('/')
def root():
    """Redirect to Streamlit app or serve PWA page"""
    return send_file(BASE_DIR / 'pwa.html', mimetype='text/html')

if __name__ == '__main__':
    print("🕉️  WisdomWeaver PWA File Server")
    print("=" * 40)
    print("Starting PWA file server on port 5000...")
    print("Manifest: http://localhost:5000/manifest.json")
    print("Service Worker: http://localhost:5000/sw.js")
    print("PWA Page: http://localhost:5000/pwa.html")
    print("Static Files: http://localhost:5000/static/")
    print("\nRun your Streamlit app on port 8501:")
    print("streamlit run app.py")
    print("=" * 40)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
