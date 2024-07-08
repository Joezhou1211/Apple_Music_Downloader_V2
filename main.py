import logging
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.safari.options import Options

downloaded = 0

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Selenium configuration options for efficiency
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')  # Disable GPU usage
options.add_argument('--no-sandbox')  # Disable sandbox mode
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

# Initialize Safari browser
driver = webdriver.Safari(options=options)

# Dictionary to store download links
download_links = {}

session = requests.Session()


# Function to perform search and get share links with retry
def get_share_links(song_name):
    for attempt in range(2):  # Try twice
        try:
            driver.get('https://music.apple.com/us/search')
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Search"]'))
            )
            search_box.clear()
            search_box.send_keys(song_name)
            search_box.send_keys(u'\ue007')  # Press Enter

            # Wait for the search results to load and iterate over each result
            search_results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.top-search-lockup'))
            )

            for result in search_results:
                description = result.find_element(By.CSS_SELECTOR, 'div.top-search-lockup__description')
                if 'Song' in description.text:
                    more_button = result.find_element(By.XPATH, './/span[@aria-label="MORE"]')
                    more_button.click()

                    # Wait for the contextual menu to appear and click the share button
                    share_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//span[text()="Share"]'))
                    )
                    share_button.click()

                    # Wait for the "Copy Link" option to appear and click it
                    copy_link_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//span[text()="Copy Link"]'))
                    )
                    copy_link_button.click()

                    # Wait for a moment to ensure the link is copied
                    time.sleep(1)

                    # Get the copied link
                    link = driver.execute_script("return navigator.clipboard.readText();")
                    download_links[song_name] = link
                    logging.info(f"Link for {song_name}: {link}")
                    return  # Exit the function after finding the first valid song link

            logging.error(f"No valid song link found for {song_name}")
            return

        except Exception as e:
            logging.error(f"Error processing {song_name} on attempt {attempt + 1}: {e}")
            if attempt == 1:
                download_links[song_name] = None


# Function to download songs.txt using links from primary source
def download_song(song_name, link):
    global downloaded
    try:
        if link is None:
            raise Exception("No link found")
        driver.get('https://apple-music-downloader.com')
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-input"))
        )
        input_box.clear()
        input_box.send_keys(link)
        start_button = driver.find_element(By.ID, "search-submit")
        start_button.click()
        download_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#info > div > div:nth-child(3) > input.get-download-submit"))
        )
        info_div = driver.find_element(By.ID, "info")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", info_div)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", download_button)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#info > h3"))
        )
        info_div = driver.find_element(By.ID, "info")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", info_div)

        song_name_element = driver.find_element(By.CSS_SELECTOR, "#info > h3")
        artist_name_element = driver.find_element(By.CSS_SELECTOR, "#info > p")
        song_name = song_name_element.text
        artist_name = artist_name_element.text
        WebDriverWait(driver, 30).until(
            lambda d: d.find_element(By.CSS_SELECTOR, "#download_mp3 > a.download-btn").get_attribute('href') != ''
        )
        download_link_element = driver.find_element(By.CSS_SELECTOR, "#download_mp3 > a.download-btn")
        download_url = download_link_element.get_attribute('href')
        logging.info(f"Download URL: {download_url}")

        if download_url:
            response = session.get(download_url)
            file_name = f"{song_name}-{artist_name}.mp3"
            with open(file_name, 'wb') as file:
                file.write(response.content)
            logging.info(f"File downloaded and saved as: {file_name} for link: {link}")
            downloaded += 1
        else:
            logging.error(f"Download URL not found for link: {link}")
            # If primary download fails, use the backup method
            download_song_from_aplmate(link)

    except Exception as e:
        logging.error(f"Error processing {song_name} with link {link}: {e}")
        # If primary download fails, use the backup method
        download_song_from_aplmate(link)


# Function to download songs.txt from aplmate.com (backup method)
def download_song_from_aplmate(song_url):
    global downloaded
    try:
        driver.get('https://aplmate.com')

        # Locate the input box and enter the song URL
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "url"))
        )
        input_box.clear()
        input_box.send_keys(song_url)

        # Click the download button
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "send"))
        )
        download_button.click()

        # Wait for the download link to appear and get the href attribute
        download_link = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//a[contains(@class, "abutton is-success is-fullwidth") and .//span[text()="Download Mp3"]]'))
        )
        download_url = download_link.get_attribute('href')
        logging.info(f"Download URL: {download_url}")

        # Extract the song name and artist from the page
        song_name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.aplmate-downloader-middle h3 div'))
        )
        artist_name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.aplmate-downloader-middle p span'))
        )
        song_name = song_name_element.get_attribute('title')
        artist_name = artist_name_element.text

        if download_url:
            response = session.get(download_url)
            file_name = f"{song_name}-{artist_name}.mp3"
            with open(file_name, 'wb') as file:
                file.write(response.content)
            logging.info(f"File downloaded and saved as: {file_name} from URL: {song_url}")
            downloaded += 1
        else:
            logging.error(f"Download URL not found for song: {song_url}")

    except Exception as e:
        logging.error(f"Error processing song URL {song_url}: {e}")


# Main function to process all songs.txt
def main():
    start_time = time.time()
    logging.info("Starting the program...")

    # Read song names from file
    with open('songs.txt', 'r') as file:
        song_names = file.readlines()
    song_names = [song.strip() for song in song_names]
    songs_num = len(song_names)

    # Get share links
    for song in song_names:
        get_share_links(song)

    # Download songs.txt
    for song_name, link in download_links.items():
        download_song(song_name, link)

    # Close the browser
    driver.quit()

    # Stop the timer and calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    logging.info(
        f"Program completed in {elapsed_time:.2f} seconds. {downloaded} out of {songs_num} songs downloaded successfully.")


if __name__ == "__main__":
    main()
