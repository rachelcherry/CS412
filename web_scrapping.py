import requests #HTTP requests
from bs4 import BeautifulSoup #HTML parser

def main(): 
#start with the URL:
    url = 'https://stores.brooksrunning.com/region/US/MA'

    # download this web page:
    page = requests.get(url)
    # page.text is the content of the web page 
    # tokenize the page into HTML tree 

    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find('div', attrs={'class': 'titles wider'})

    rows = table.findAll('a')

    # go through all stores 
    for row in rows:
        #extract the name and address from <span> tags 
        name = row.find('span', attrs={'class':'name'})
        address = row.find('span', attrs={'class':'address'})
        print(name.strip(), address.text.strip())

if __name__ == "__main__":
    main() 