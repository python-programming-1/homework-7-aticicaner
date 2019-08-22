import requests
import os
from bs4 import BeautifulSoup
from time import sleep

#get main website
main_url = 'https://www.gocomics.com'
url = main_url + '/pearlsbeforeswine'
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'html.parser')
#extract href stored above 'card-body gc-card__body' 
# with name 'gc-blended-link gc-blended-link--primary'
select = soup.select('div .row')[0].find_all('a', \
    class_='gc-blended-link gc-blended-link--primary')
#select most recent upload
target = main_url + select[0].get('href')

# print(target) #most recent page load check
for i in range (10):
    #new resource set for given url
    res = requests.get(target)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    #acquire image location
    image = soup.find_all('img', {'class' : 'lazyload img-fluid'})
    image_url = image[1].get('src')
    image_res = requests.get(image_url)
    image_res.raise_for_status()
    #download image
    img = open(os.path.basename(str(i)), 'wb')
    for chunk in image_res.iter_content(100000):
        img.write(chunk)
    img.close()

    next_res = soup.select('div .gc-calendar-nav__previous') \
        [0].select('a')
    prev = next_res[1].get('href')

    # Update target
    target = main_url + prev
    sleep(1)