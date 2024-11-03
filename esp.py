import requests
from bs4 import BeautifulSoup
import time

# Replace with the URL you want to scrape
url = 'http://192.168.130.145/'  # Change this to the actual URL

def get_html_content():
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text  # Return the entire HTML content
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    while True:
        html_content = get_html_content()
       

        if html_content is not None:
            int_list = list(map(int, html_content.split(',')))
            print(int_list)  # Print the entire HTML content
        else:
            print("Failed to retrieve HTML content.")
        
        # Wait for a specified interval before scraping again
        # Scrape every 5 seconds

if __name__ == "__main__":
    main()