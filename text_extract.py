from bs4 import BeautifulSoup
import requests


url = "https://stud.kz/referat/show/38143"

response = requests.get(url, verify=False)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
text = soup.find('span', 'nocopy')
text_normal = text.text.replace('...', ' ')
with open('testing.txt', 'w', encoding='utf8') as f:
    f.write(text.text)
    # print(text.text)