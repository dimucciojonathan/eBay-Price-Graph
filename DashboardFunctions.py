import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from matplotlib.dates import DateFormatter
import io


def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print('Server Responded: ', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


# Not implemented in site, but a quick function that removes rows from dataframe based on words in title
def remove_by_keyword(df, keyword):
    df = df[df['Title'].str.contains(keyword) == False]
    return df


# Function that averages price of each day then makes a line graph
def line_graph_prices(df):
    df = df[['Date', 'Price']]
    df = df.set_index(df['Date']).drop('Date', axis=1)
    return df.resample('D').mean().plot()


def box_plot(df):
    fig = plt.figure(figsize=(37,5))
    ax1 = fig.add_subplot(1,2,1)
    myFmt = DateFormatter("%m/%d")
    seaborn.set(font_scale=1.5)
    return seaborn.boxplot(y='Price', x='Date', data=df, width=.5, ax=ax1)


# Given a 'sold listings' ebay search URL, returns a dataframe with all previous sales.
# Data includes 5 columns. Listing Title, Date, Date with Time, Price, and Link to the post.
def get_sold_info_dataframe(url, pages):
    df = pd.DataFrame(columns=('Title', 'Date', 'Date2', 'Price', 'Link'))
    for i in range(pages):

        # Page must start at 1 then increment
        if i == 0:
            i = 1
        else:
            i = i + 1
        print("We are on page #:",i,'\n')

        # Generate soup for correct page number
        urltrue = url + '&_pgn=' + str(i)
        soup = get_page(urltrue)

        for post in soup.find_all('li', {'class': 's-item'}):
            # Find Title
            try:
                h = post.find('a', {'class': 's-item__link'})
                title_and_date = h.text
                title = title_and_date.split('2019')[1]
            except:
                title = 'NaN'
                date = 'NaN'

            #Find date
            try:
                date = title_and_date.split('2019')[0] + '2019'
                date = date[6:]
            except:
                date = '0'

            try:
                date2 = post.find('span',{'class': 's-item__ended-date s-item__endedDate'}).text
            except:
                date2 = '0'

            # Find Price
            try:
                price = post.find('span', {'class': 's-item__price'}).text
            except:
                price = '00000000'

            # Find Link
            try:
                link = h['href']
            except:
                link = 'NaN'
            row = [title,date,date2,price,link]
            # Append dataframe with row data
            df = df.append({'Title': title, 'Date': date, 'Date2': date2, 'Price': price, 'Link': link},
                           ignore_index=True)
    df['Date'] = pd.to_datetime(df['Date'],errors='coerce')

    # Remove rows where the price is structured as '$___ to $____' and failed cases
    df = df[df['Price'].map(len) < 8]

    # Remove '$' sign
    df.Price = df['Price'].str[1:].astype(float)
    return df


# From a given dataframe, creates a Seaborn plot then returns it's bytesIO image that can be easily used in flask
def box_to_bytes(df):
    bytes_image = io.BytesIO()
    box_graph = box_plot(df)
    fig = box_graph.get_figure()
    fig.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image

