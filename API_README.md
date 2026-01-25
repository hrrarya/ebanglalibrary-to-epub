# eBangla Library Scraper API

This API allows you to scrape books from eBangla Library and generate downloadable EPUB files.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Run the API server:
```bash
python apis/app.py
```

The server will start on `http://0.0.0.0:5000`

## API Endpoints

### 1. Get Download Link

**Endpoint:** `POST /get-download-link`

**Description:** Scrapes the book from eBangla Library and generates an EPUB file.

**Request Body:**
```json
{
  "url": "https://www.ebanglalibrary.com/lessons/..."
}
```

**Response:**
```json
{
  "success": true,
  "download_link": "/download/user_id/title.epub",
  "title": "Book Title",
  "author": "Author Name",
  "user_id": "uuid",
  "file_path": "epub/user_id/title.epub"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/get-download-link \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.ebanglalibrary.com/lessons/%e0%a6%a6%e0%a7%8d%e0%a6%af-%e0%a6%a1%e0%a6%bf%e0%a6%ad%e0%a7%8b%e0%a6%b6%e0%a6%a8-%e0%a6%85%e0%a6%ac-%e0%a6%b8%e0%a6%be%e0%a6%b8%e0%a6%aa%e0%a7%87%e0%a6%95%e0%a7%8d%e0%a6%9f-%e0%a6%8f%e0%a6%95/"}'
```

### 2. Download File

**Endpoint:** `GET /download/<user_id>/<filename>`

**Description:** Downloads the generated EPUB file.

**Example:**
```bash
curl -O http://localhost:5000/download/user_id/title.epub
```

### 3. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "eBangla Library Scraper API"
}
```

## Project Structure

```
.
├── apis/               # API folder
│   ├── __init__.py
│   └── app.py         # Quart API application
├── controller/         # Controller folder
│   ├── __init__.py
│   └── scraper.py     # ScrapeEbanglaLibrary class
├── epub/              # Generated EPUB files
├── md/                # Temporary markdown files
├── main.py            # CLI script
└── pyproject.toml     # Dependencies
```

## Usage as CLI

You can still use the original CLI script:

```bash
python main.py
```

Edit the `main.py` file to change the URL.
