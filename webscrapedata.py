import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to scrape blog data from a given page
def scrape_blog_page(url, headers):
    try:
        # Adding a delay to avoid rapid requests
        time.sleep(2)

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

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
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to scrape blog data from multiple pages
def scrape_multiple_pages(base_url, num_pages, headers):
    all_data = pd.DataFrame()

    for page_num in range(1, num_pages + 1):
        url = f"{base_url}/page/{page_num}"
        df = scrape_blog_page(url, headers)

        if df is not None:
            all_data = pd.concat([all_data, df], ignore_index=True)

    return all_data

# Set the base URL and the number of pages to scrape
base_url = "https://rategain.com/blog"
num_pages_to_scrape = 20

# Set the User-Agent header
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Scrape data from multiple pages
result_data = scrape_multiple_pages(base_url, num_pages_to_scrape, headers)

# Save the combined DataFrame to CSV
result_data.to_csv('blog_data_combined.csv', index=False)

# Save the combined DataFrame to Excel
result_data.to_excel('blog_data_combined.xlsx', index=False)
