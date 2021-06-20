import requests# allows to send HTTP requests
from bs4 import BeautifulSoup# for pulling data out of HTML and XML files
import pandas as pd# for data manipulation and analysis
from datetime import datetime# for manipulating dates and times
from matplotlib import pyplot as plt# for creating static, animated, and interactive visualizations

# Header for the HTTP request that informs the web server about our OS and browser settings.
USER_AGENT_DATA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/91.0.4472.77 Safari/537.36'}

#searching Linkedin website for jobs with keyword = "Python developer and location = Munich
URL = "https://www.linkedin.com/jobs/search?keywords=Python%20Developer&location=Munich%2C%20Bavaria%2C%20Germany&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0"

# Query for the HTML file containing the newest listings on Linkedin-Job listing
query_response = requests.get(URL, headers=USER_AGENT_DATA)

with open("query_response.html", "w", encoding="utf-8") as file:
    file.write(query_response.text)
# Now let's use BeautifulSoup to parse the HTML for the listings
html_document = query_response.text

soup = BeautifulSoup(html_document, 'html.parser')

# All titles, prices and dates contain a certain class name in the HTML.
# We use this to find the HTML tags of interest in the HTML file.
titles = soup.find_all("h3", class_="base-search-card__title")
companies = soup.find_all("h4", class_="base-search-card__subtitle")
links = soup.find_all("a", class_="hidden-nested-link")
dates = soup.find_all("time", class_="job-search-card__listdate")

# Here we are checking if the number of titles, prices and dates still add up.
#assert(len(titles) == len(companies) == len(links) == len(dates))


# Use string manipulation to get only the text of interest
clean_titles = list(map(lambda word: word.text.strip(),	titles))
clean_companies = list(map(lambda word: word.text.strip(), companies))
clean_links = list(map(lambda word: word.get('href'), links))
clean_dates = list(map(lambda word: word.get('datetime'), dates))

print(len(clean_titles))
print(len(clean_companies))
print(len(clean_links))
print(len(clean_dates))
#variables for the total number of entries for the months respectively.
april_entries = 0
may_entries = 0
june_entries = 0

# Prepare the output format
for idx in range(0, len(clean_dates)):
    if clean_dates[idx] == '':
        dt = '0000-00-00'
    else:
        dt = datetime.strptime(clean_dates[idx],
                               '%Y-%m-%d')  # parses a string representing a time according to a format.
        if dt.month == 4:
            april_entries += 1
        elif dt.month == 5:
            may_entries += 1
        elif dt.month == 6:
            june_entries += 1

    if clean_links[idx] == '':
        clean_links[idx] = 'NA'

for idx in range(0, len(clean_dates)):
    print('{} - {} - {} - {}'.format(
        clean_titles[idx],
        clean_companies[idx],
        clean_links[idx],
        clean_dates[idx]))


#Panda-DataFrame is a 2-dimensional labeled data structure with columns of potentially different types
data = {'Title': clean_titles,
        'Company': clean_companies,
        'Link': clean_links,
        'Date': clean_dates}
# Convert the dictionary into DataFrame
df = pd.DataFrame({key : pd.Series(value) for key, value in data.items()})
df.to_csv('data.csv')
print(df)

#Visualizing the number of entries for the months april, may and june using matplotlib
names = ['April', 'May', 'June']
values = [april_entries, may_entries, june_entries]
plt.figure(figsize=(9, 3))
plt.subplot(131)
plt.bar(names, values)
plt.show()





