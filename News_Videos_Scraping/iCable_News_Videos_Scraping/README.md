### i-Cable News Videos Scraper

## Overview

This Jupyter Notebook is designed to scrape News Videos from the news section of the i-Cable website (`https://www.i-cable.com/category/新聞資訊/`), extract relevant metadata (URL, source, title, description), and optionally retrieve video URLs (e.g., `.m3u8` URLs) for posts containing videos. The scraped data is saved as a CSV file and pickled for persistence. Additionally, the notebook includes functionality to download video files using `ffmpeg` and organize them into categorized folders based on specific program titles.

## Features

- Scrapes news post metadata (URL, source, title, description) from multiple pages of the i-Cable news section.
- Extracts `.m3u8` video URLs from individual post pages.
- Saves scraped data to CSV and pickle files for reuse.
- Downloads `.m3u8` video files using `ffmpeg`.
- Cleans and filters video URLs to exclude invalid playlists (e.g., `playlist.m3u8`).
- Organizes downloaded videos into folders based on program names (e.g., "有理有得傾", "同行45載，與你相伴連繫").
- Tracks progress with flags like `visited` and `downloaded` to avoid redundant processing.

## Prerequisites

To run this notebook, you need the following software and Python packages installed:

### Software

- **Google Chrome**: Required for Selenium WebDriver.
- **ChromeDriver**: Must be compatible with your Chrome version. Download from [here](https://chromedriver.chromium.org/downloads) and ensure it's in your system PATH or specify its path in the code.
- **FFmpeg**: Required for downloading `.m3u8` videos. Install FFmpeg and ensure it's accessible from the command line. Download from [here](https://ffmpeg.org/download.html).

### Python Packages

Install the required Python packages using pip:

```bash
pip install pandas selenium webdriver-manager subprocess
```

### Directory Setup

- Ensure you have write permissions in the directories where files will be saved (e.g., `./icable Scraped Videos` and `./icable_categorized`).
- Create the destination folders for categorized videos if they don't exist.

## Installation

1. Clone or download this repository to your local machine.

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

   (Create a `requirements.txt` file with the above packages if needed.)

3. Install ChromeDriver:

   - Use `webdriver-manager` to automatically handle ChromeDriver installation:

     ```python
     pip install webdriver-manager
     ```

   - Alternatively, manually download and place ChromeDriver in your PATH.

4. Install FFmpeg and add it to your system PATH.

## Usage

1. **Open the Jupyter Notebook**

2. **Configure the Notebook**:

   - Update the `url_base` variable if scraping a different section of the i-Cable website:

     ```python
     url_base = "https://www.i-cable.com/category/%E6%96%B0%E8%81%9E%E8%B3%87%E8%A8%8A/"
     ```

   - Adjust the page range (`start_page`, `end_page`) in the `scrape_blog_posts` function if needed:

     ```python
     df = scrape_blog_posts(url_base, 2188, 4469)
     ```

   - Update file paths for saving CSVs, pickle files, and videos (e.g., `./icable Scraped Videos`).

3. **Run the Notebook**:

   - Execute cells sequentially to:
     - Scrape news post metadata.
     - Save the data to `icable_data.csv` and `datapd_nodup.pkl`.
     - Extract `.m3u8` URLs and save to `datapd_with_m3u8.pkl`.
     - Download videos to the specified folder.
     - Categorize videos into program-specific folders (e.g., `有理有得傾`, `同行45載，與你相伴連繫`).
   - The final cleaned dataset is saved as `latest_datapd_icable.pkl`.

4. **Key Functions**:

   - `scrape_blog_posts(url_base, start_page, end_page)`: Scrapes metadata from news across specified pages.
   - `get_post_data(element)`: Extracts metadata (URL, source, title, description) from a single post element.
   - `save_variable_to_pickle(variable, filename)`: Saves a variable to a pickle file.
   - `load_variable_from_pickle(filename)`: Loads a variable from a pickle file.
   - `download_m3u8_ffmpeg(m3u8_url, output_file)`: Downloads an `.m3u8` video using FFmpeg.
   - File organization loops: Move videos to program-specific folders based on titles.

5. **Output Files**:

   - `icable_data.csv`: Initial scraped data.
   - `datapd_nodup.pkl`: Deduplicated dataset.
   - `datapd_with_m3u8.pkl`: Dataset with `.m3u8` URLs.
   - `datapd_with_m3u8_visited.pkl`: Dataset with `visited` and `m3u8_url` columns.
   - `updated_download_status.csv`: Dataset with download status.
   - `latest_datapd_icable.pkl`: Final cleaned dataset.
   - Videos saved to `./icable Scraped Videos` and categorized subfolders.

## Notes

- **Error Handling**: The notebook handles `TimeoutException`, `NoSuchElementException`, and other exceptions to ensure robust scraping and downloading.
- **Performance**: Scraping thousands of pages and downloading videos can be time-consuming. Consider running in smaller batches or using a cloud environment for large-scale tasks.
- **JavaScript Disabling**: The notebook disables JavaScript in some sections to improve scraping reliability. Adjust `chrome_options` if JavaScript is required for certain pages.
- **Data Cleaning**: The notebook filters out invalid `.m3u8` URLs (e.g., containing `playlist.m3u8`) and categorizes videos based on program titles. Add more program names to the filtering logic as needed.
- **Storage**: Ensure sufficient disk space for downloaded videos, as `.m3u8` files can be large.

## Example Workflow

1. Scrape posts from pages 2188 to 4469 and save metadata to `icable_data.csv`.
2. Load `datapd_nodup.pkl` and scrape `.m3u8` URLs for each post, saving to `datapd_with_m3u8.pkl`.
3. Download videos for unprocessed rows and update `downloaded` status in `updated_download_status.csv`.
4. Categorize videos into folders like `有理有得傾` and `同行45載，與你相伴連繫`.
5. Save the final dataset as `latest_datapd_icable.pkl`.

## Troubleshooting

- **ChromeDriver Issues**: Ensure Chrome and ChromeDriver versions match. Use `webdriver-manager` to simplify setup.

- **FFmpeg Errors**: Verify FFmpeg is in your PATH and accessible via `ffmpeg -version`.

- **Timeouts**: Increase the `WebDriverWait` timeout (e.g., from 5 to 10 seconds) if pages load slowly:

  ```python
  wait = WebDriverWait(driver, 10)
  ```

- **File Not Found**: Check file paths for CSVs, pickle files, and video directories.

- **Memory Issues**: For large datasets, consider processing in smaller chunks or using a machine with more RAM.


## Acknowledgments

- Built using [Selenium](https://www.selenium.dev/), [Pandas](https://pandas.pydata.org/), and [FFmpeg](https://ffmpeg.org/).
- Thanks to the open-source community for providing robust tools for web scraping and video processing.