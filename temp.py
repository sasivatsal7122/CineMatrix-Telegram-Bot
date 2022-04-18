import requests



payload = {'api_key': '2402386ac7b63b99cd029e035bb5a7bd', 'url': 'https://yts.torrentbay.to/api/v2/list_movies.json?query_term=Inception'}
r = requests.get('http://api.scraperapi.com', params=payload).json()
print (r)
# Scrapy users can simply replace the urls in their start_urls and parse function
# ...other scrapy setup code



# intial_response = requests.get(f'https://yts.torrentbay.to/api/v2/list_movies.json?query_term=aquaman')
# movies_json = intial_response.json()
# print(movies_json)
