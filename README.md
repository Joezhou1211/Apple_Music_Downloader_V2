# Apple Music Downloader V2

Apple_Music_Downloader can now download songs automatically, with just song names as input.
Selenium is used for browser automation and Requests for file downloading.

## How It Works

Adding any song you want to download by editing 'songs.txt' file, then running main.py, songs will be downloaded automatically.
It took 10~20 seconds for a single song to be downloaded on my Mac, plan your time properly.
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


