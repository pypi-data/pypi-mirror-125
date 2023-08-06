import requests
from uuid import uuid4
from user_agent import generate_user_agent
import random
import secrets
E = '\033[1;31m'
G = '\033[1;32m'
S = '\033[1;33m'
Z = '\033[1;31m' 
X = '\033[1;33m' 
Z1 = '\033[2;31m'
F = '\033[2;32m'
A = '\033[2;39m' 
C = '\033[2;35m' 
B = '\033[2;36m'
Y = '\033[1;34m' 
Markos = """
 \033[1;96m ------------------------
 \033[1;32m < COD BY MARKO-TOOLS >
 \033[1;96m ------------------------
\033[1;91m  __  __    _    ____  _  _____  
\033[1;92m |  \/  |  / \  |  _ \| |/ / _ \ 
\033[1;91m | |\/| | / _ \ | |_) | ' / | | |
\033[1;92m | |  | |/ ___ \|  _ <| . \ |_| |
\033[1;91m |_|  |_/_/   \_\_| \_\_|\_\___/ 
          \033[1;93m _____ ___   ___  _     ____    
         \033[1;92m |_   _/ _ \ / _ \| |   / ___|   
         \033[1;91m   | || | | | | | | |   \___ \   
         \033[1;92m   | || |_| | |_| | |___ ___) |  
         \033[1;91m   |_| \___/ \___/|_____|____/   
\033[1;32m--------------------------------------------------
\033[1;95m
 AUTHOR     : MARKO-TOOLS
 Telegram   : MARKO-TOOLS
 YOUTUBE    : MARKO - TOOLS
 GITHUB     : GITHUB.COM/MARKO-TOOLS
\033[1;32m
--------------------------------------------------
"""  
Markoo = """
 \033[1;96m ------------------------
 \033[1;32m < COD BY MARKO-TOOLS >
 \033[1;96m ------------------------
\033[1;91m  __  __    _    ____  _  _____  
\033[1;92m |  \/  |  / \  |  _ \| |/ / _ \ 
\033[1;91m | |\/| | / _ \ | |_) | ' / | | |
\033[1;92m | |  | |/ ___ \|  _ <| . \ |_| |
\033[1;91m |_|  |_/_/   \_\_| \_\_|\_\___/ 
          \033[1;93m _____ ___   ___  _     ____    
         \033[1;92m |_   _/ _ \ / _ \| |   / ___|   
         \033[1;91m   | || | | | | | | |   \___ \   
         \033[1;92m   | || |_| | |_| | |___ ___) |  
         \033[1;91m   |_| \___/ \___/|_____|____/   
\033[1;32m--------------------------------------------------
\033[1;95m
 AUTHOR     : MARKO-TOOLS
 Telegram   : MARKO-TOOLS
 YOUTUBE    : MARKO - TOOLS
 GITHUB     : GITHUB.COM/MARKO-TOOLS
\033[1;32m
--------------------------------------------------
"""  
uid = str(uuid4)
class Marko:
    def Login_instagram(username,password):
        URL_INSTA = 'https://i.instagram.com/api/v1/accounts/login/'
        HEADERS_INSTA = {
        'User-Agent': 'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)',
        'Accept': "*/*",
        'Cookie': 'missing',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US',
        'X-IG-Capabilities': '3brTvw==',
        'X-IG-Connection-Type': 'WIFI',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'i.instagram.com'}
        DATA_INSTA = {'uuid': uid,'password': password,'username': username,'device_id': uid,'from_reg': 'false','_csrftoken': 'missing','login_attempt_countn': '0'}
        RESPON = requests.post(URL_INSTA,headers=HEADERS_INSTA,data=DATA_INSTA)
        if ('logged_in_user') in RESPON.text:
            user = RESPON.json()['logged_in_user']['username']
            cookie = secrets.token_hex(8)*2
            head = {
                        'HOST': "www.instagram.com",
                        'KeepAlive' : 'True',
                        'user-agent' : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36",
                        'Cookie': cookie,
                        'Accept' : "*/*",
                        'ContentType' : "application/x-www-form-urlencoded",
                        "X-Requested-With" : "XMLHttpRequest",
                        "X-IG-App-ID": "936619743392459",
                        "X-Instagram-AJAX" : "missing",
                        "X-CSRFToken" : "missing",
                        "Accept-Language" : "en-US,en;q=0.9"
            }
            url_id = f'https://www.instagram.com/{user}/?__a=1'
            req_id= requests.get(url_id,headers=head).json()
            name    = str(req_id['graphql']['user']['full_name'])
            id    = str(req_id['graphql']['user']['id'])
            followes    = str(req_id['graphql']['user']['edge_followed_by']['count'])
            following    = str(req_id['graphql']['user']['edge_follow']['count'])
            data = {
            'username':f'{user}',
            'password':f'{password}',
            'name':f'{name}',
            'id':f'{id}',
            'followes':f'{followes}',
            'following':f'{following}',
            'The resulting':'True',
            }
            return data
        elif ('check your username') in RESPON.text:
            data = {
            'username':username,
            'password':password,
            'The resulting':'Band username',
            }
            return data
        elif ('challenge_required') in RESPON.text:
            data = {
            'username':username,
            'password':password,
            'The resulting':'Secure',
            }
            return data
        elif ('Please wait a few minutes') in RESPON.text:
            data = {
            'username':username,
            'password':password,
            'The resulting':'block ip',
            }
            return "block ip"
        else:
            data = {
            'username':username,
            'password':password,
            'The resulting':'False password',
            }
            return data

def By():
    return Markos