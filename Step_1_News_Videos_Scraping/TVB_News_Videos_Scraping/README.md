# TVB News Scraper

This Jypyter Notebook is a pipeline for **scraping, processing, and downloading news videos from TVB (Television Broadcasts Limited)**. It is primarily designed for research purposes, such as building a dataset for tasks like lip reading, video classification, or speech-to-text alignment.

## Project Overview

The pipeline consists of the following stages:

### 1. **Scraping Video Metadata**
- Accesses the TVB news API and retrieves paginated metadata (in JSON format) for local news videos.
- Saves each page of JSON responses locally.
- Combines all JSON pages into a single consolidated file (`combined_content.json`).

### 2. **Extracting and Cleaning Metadata**
- Extracts key fields such as `id`, `title`, `publish_datetime`, video `url_hd`, and tags from the combined content.
- Converts the extracted metadata into a structured DataFrame.
- Filters out entries without video URLs and saves a clean version (`cleaned_data.csv` and `.pkl`).

### 3. **Downloading Videos via FFmpeg**
- Appends `?profile=ios` to the `url_hd` links to retrieve actual `.m3u8` stream URLs.
- Downloads videos using FFmpeg and saves them as `.mp4` files with the video ID as the filename.
- Supports multi-threaded downloading with progress tracking using `ThreadPoolExecutor` and `tqdm`.

## Directory Structure

```
project_root/
│
├── JSONs/                       # Raw scraped JSON files
├── combined_content.json        # Merged JSON metadata
├── cleaned_data.csv             # Cleaned CSV with valid download links
├── cleaned_data.pkl             # Pickled version for quick loading
├── download_videos.py           # FFmpeg-based downloader
├── scrape_tvb_news.py           # Main scraping script
└── README.md                    # Project description
```

## Requirements

- Python 3.8+
- Chrome + ChromeDriver (for Selenium, although only initialized here)
- FFmpeg
- Python packages:
  - `requests`
  - `pandas`
  - `tqdm`
  - `concurrent.futures` (standard lib)

You can install the dependencies via:

```bash
pip install requests pandas tqdm
```

## Usage

1. **Scrape metadata**:
   ```bash
   python scrape_tvb_news.py
   ```

2. **Download videos**:
   ```bash
   python download_videos.py
   ```

Videos will be saved to the directory specified by `SAVE_DIR`.

## Notes

- This scraper is tailored for the TVB news API and assumes a consistent JSON structure.
- Error handling is included for failed downloads and malformed JSON entries.
- The multi-threaded downloader skips already-downloaded videos to avoid duplicates.