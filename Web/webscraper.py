# Importing necessary libraries
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# Define a function to retrieve stock prices
def get_stock_price(company):
    try:
        # Define the user-agent header to mimic a web browser
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }

        # Construct the URL to fetch data from Yahoo Finance for the specified company
        url = f'https://finance.yahoo.com/quote/{company}/'

        # Send an HTTP GET request to the URL with the defined headers
        r = requests.get(url, headers=header)
        r.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(r.text, 'html.parser')

        # Extract relevant stock price information and store it in a dictionary
        prices = {
            'Company_name': soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text,
            'price': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[0].text,
            'previous_close': soup.find('table', {'class': 'W(100%)'}).find_all('td')[1].text,
            'open': soup.find('table', {'class': 'W(100%)'}).find_all('td')[3].text,
            'change': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[1].text,
            'change_percent': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[2].text,
            'date': datetime.now().strftime("%Y-%m-%d_%H-%M")
        }

        return prices
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching data for {company}: {e}")
        return None
    except Exception as e:
        print(f"Error for {company}: {e}")
        return None

# Send an HTTP GET request to the page
url = 'https://finance.yahoo.com/trending-tickers'
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error while fetching the trending tickers page: {e}")
    response = None

if response:
    # Initialize an empty list to store the extracted text
    quote_links_list = []

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all anchor elements with 'data-test' attribute set to 'quoteLink'
    quote_links = soup.find_all('a', {'data-test': 'quoteLink'})

    # Extract the text content from all quoteLink anchors and add to the list
    for link in quote_links:
        quote_links_list.append(link.text)

    # Print the list
    print(quote_links_list)
else:
    print("Failed to retrieve the page.")

data = []

for item in quote_links_list:
    stock_data = get_stock_price(item)
    if stock_data:
        data.append({'name': item, **stock_data})

if data:
    csv_file = f'{datetime.now().strftime("%Y-%m-%d_%H-%M")} Stock_data.csv'
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
else:
    print("No data to save to CSV.")
