from quart import Quart, request, jsonify, send_file, send_from_directory
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controller import ScrapeEbanglaLibrary

# Define paths
BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR / 'static'

app = Quart(__name__, static_folder=str(STATIC_DIR))

# Serve frontend static files
@app.route('/')
async def serve_frontend():
    return await send_from_directory(str(STATIC_DIR), 'index.html')

@app.route('/<path:path>')
async def static_files(path):
    return await send_from_directory(str(STATIC_DIR), path)


@app.route('/get-download-link', methods=['POST'])
async def get_download_link():
    """
    Endpoint to scrape and generate EPUB download link
    
    Request body:
    {
        "url": "https://www.ebanglalibrary.com/lessons/..."
    }
    
    Response:
    {
        "success": true,
        "download_link": "/download/user_id/title.epub",
        "title": "Book Title",
        "author": "Author Name",
        "user_id": "uuid",
        "file_path": "epub/user_id/title.epub"
    }
    """
    try:
        data = await request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'error': 'URL is required in request body'
            }), 400
        
        url = data['url']
        
        # Initialize scraper
        scraper = ScrapeEbanglaLibrary(url)
        
        # Fetch PDF URLs and convert to EPUB
        scraper.fetch_pdf_urls()
        scraper.md_to_epub()
        
        # Clean up temporary markdown files
        scraper.clean_up()
        
        # Get the epub file path
        epub_path = scraper.get_epub_path()
        
        # Check if file exists
        if not os.path.exists(epub_path):
            return jsonify({
                'success': False,
                'error': 'EPUB file was not generated successfully'
            }), 500
        
        # Generate download link
        download_link = f"/download/{scraper.user_id}/{scraper.title}.epub"
        
        return jsonify({
            'success': True,
            'download_link': request.host_url.rstrip('/') + download_link,
            'title': scraper.title,
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/download/<user_id>/<filename>', methods=['GET'])
async def download_file(user_id, filename):
    """
    Endpoint to download the generated EPUB file
    """
    try:
        file_path = f"epub/{user_id}/{filename}"
        
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        return await send_file(
            file_path,
            as_attachment=True,
            attachment_filename=filename,
            mimetype='application/epub+zip'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
async def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'eBangla Library Scraper API'
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
