import requests


response = requests.get('https://bit.ly/3riBygR')
open("test.torrent", "wb").write(response.content)