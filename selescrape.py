from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to scrape blog data from a given page using Selenium
def scrape_blog_page_selenium(url, driver):
    try:
        # Adding a delay to avoid rapid requests
        time.sleep(2)

        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Lists to store extracted data
        titles = []
        dates = []
        image_urls = []
        likes_counts = []

        # Loop through each blog post on the page
        for post in soup.find_all('article', class_='blog-item'):
            # Extract blog title
            title = post.find('h6').text.strip()
            titles.append(title)

            # Extract blog date
            date = post.find('div', class_='bd-item').find('span').text.strip()
            dates.append(date)

            # Extract blog image URL
            image_url = post.find('div', class_='img').find('a')['data-bg']
            image_urls.append(image_url)

            # Extract blog likes count
            likes_count = post.find('a', class_='zilla-likes').find('span').text.strip().split()[0]
            likes_counts.append(likes_count)

        # Create a DataFrame to organize the data
        data = {'Title': titles, 'Date': dates, 'Image URL': image_urls, 'Likes Count': likes_counts}
        df = pd.DataFrame(data)

        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to scrape blog data from multiple pages using Selenium
def scrape_multiple_pages_selenium(base_url, num_pages, driver):
    all_data = pd.DataFrame()

    for page_num in range(1, num_pages + 1):
        url = f"{base_url}/page/{page_num}"
        df = scrape_blog_page_selenium(url, driver)

        if df is not None:
            all_data = pd.concat([all_data, df], ignore_index=True)

    return all_data

# Set the base URL and the number of pages to scrape
base_url = "https://rategain.com/blog"
num_pages_to_scrape = 20

# Set the User-Agent header for Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Use headless mode if you don't want a browser window to open
driver = webdriver.Chrome(options=options)

# Scrape data from multiple pages using Selenium
result_data = scrape_multiple_pages_selenium(base_url, num_pages_to_scrape, driver)

# Save the combined DataFrame to CSV
result_data.to_csv('blog_data_combined.csv', index=False)

# Save the combined DataFrame to Excel
result_data.to_excel('blog_data_combined.xlsx', index=False)

# Close the Selenium WebDriver
driver.quit()
