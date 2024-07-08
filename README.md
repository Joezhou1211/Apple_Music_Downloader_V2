# Apple Music Downloader V2

This script leverages Selenium for browser automation and the Requests library for file downloading.

## How It Works

To download songs, simply add the desired song names to the 'songs.txt' file and run main.py. The script will automatically download the songs. On a Mac, each song typically takes about 10 to 20 seconds to download, so please plan accordingly.
![ap](https://github.com/Joezhou1211/AppleMusicDownloader_V2/assets/121386280/4479c8d9-f51e-4b50-ab86-62f4efe94d06)

## Disclaimer

This project is intended for educational purposes only. It should not be used for any commercial or profit-making activities.

## Setup Instructions

### Step 1: Clone and Set Up the Environment

```bash
git clone https://github.com/Joezhou1211/Apple_Music_Downloader_V2.git
pip install -r requirements.txt
```

### Step 2: Browser Configuration
#### For macOS (Safari)

- Enable Remote Automation in Safari:
- Open Safari.
- Go to Preferences > Advanced.
- Check the box for Show Develop menu in menu bar.
- In the menu bar, go to Develop > Allow Remote Automation.

#### For Windows (Chrome) (Not Verified)
- Download ChromeDriver:
- Download the ChromeDriver that matches your Chrome version from https://sites.google.com/a/chromium.org/chromedriver/downloads.
- Add the ChromeDriver executable to your system PATH.
- Change webdriver to Chrome


