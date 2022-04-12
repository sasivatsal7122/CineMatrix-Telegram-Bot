import requests

def get_shorturl(long_url):
    for i in range(2):
        username = "o_2a5l1i8nk1"
        password = "ap31et0975"

        auth_res = requests.post("https://api-ssl.bitly.com/oauth/access_token", auth=(username, password))
        if auth_res.status_code == 200:
            access_token = auth_res.content.decode()
            #print("[!] Got access token:", access_token)
        else:
            #print("[!] Cannot get access token, exiting...")
            exit()
            
        headers = {"Authorization": f"Bearer {access_token}"}

        groups_res = requests.get("https://api-ssl.bitly.com/v4/groups", headers=headers)
        if groups_res.status_code == 200:
            groups_data = groups_res.json()['groups'][0]
            guid = groups_data['guid']
        else:
            #print("[!] Cannot get GUID, exiting...")
            exit()
            
        shorten_res = requests.post("https://api-ssl.bitly.com/v4/shorten", json={"group_guid": guid, "long_url": long_url}, headers=headers)
        if shorten_res.status_code == 200:
            short_url = shorten_res.json().get("link")
        if i==1:
            return short_url
 
