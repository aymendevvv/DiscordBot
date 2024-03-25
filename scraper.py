import requests 
import json
from requests_html import HTMLSession


cookies = {
    'gr_user_id': '2435d8cc-2808-4d0e-ab6b-e24fe14031e5',
    '87b5a3c3f1a55520_gr_last_sent_cs1': 'aymenduzzstuff',
    '__stripe_mid': 'f024a447-b260-49a6-a407-776ff82d87fbb2e806',
    'cf_clearance': '2Jb8EWS45Upj7M92UqZzU29NrCPzSWxzpAB1GO4iJHM-1698509669-0-1-cd932ba.a77045b3.5bd86d5a-160.0.0',
    'csrftoken': 'iJFOmWIwrj43CEuhPNpgBU3qH0nmeyT0hC3uGnjKS9uPXW7kWKwXUludeOAkLw8H',
    'LEETCODE_SESSION': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNjcwMTM2NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjE2Y2FiMmQxMGE4MjliMTJkN2EwNGFhNzRjOWVjZTVjMDE5NjhhMzZkZGQ0YTUwOWEyNDJkNjg3NDliNDg2MGUiLCJpZCI6NjcwMTM2NiwiZW1haWwiOiJob3VjaGVfYXltZW5Ab3V0bG9vay5jb20iLCJ1c2VybmFtZSI6ImF5bWVuZHV6enN0dWZmIiwidXNlcl9zbHVnIjoiYXltZW5kdXp6c3R1ZmYiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvZGVmYXVsdF9hdmF0YXIuanBnIiwicmVmcmVzaGVkX2F0IjoxNzA4MTkyNDU1LCJpcCI6IjEwNS4xMDYuMTc1LjE5NCIsImlkZW50aXR5IjoiOWZlYTcwMWE2MjdhNTdkMGM0NThkYjJlMWNiNjBkNjIiLCJzZXNzaW9uX2lkIjo1NDkwNTU0MywiX3Nlc3Npb25fZXhwaXJ5IjoxMjA5NjAwfQ.DyeK0LGx8Uld9vWe6juQss5GBwCj2UoaQkEgxAsp_2Y',
    '_gid': 'GA1.2.212519538.1708192456',
    '_gat': '1',
    '87b5a3c3f1a55520_gr_session_id': 'd6221949-ba3e-46af-b8fc-9bf46208b4f4',
    '87b5a3c3f1a55520_gr_last_sent_sid_with_cs1': 'd6221949-ba3e-46af-b8fc-9bf46208b4f4',
    '87b5a3c3f1a55520_gr_session_id_sent_vst': 'd6221949-ba3e-46af-b8fc-9bf46208b4f4',
    '__gads': 'ID=ceb77aee9e283458:T=1701547372:RT=1708192460:S=ALNI_MbtZGFCfCRM6cTTeToJ3eJD0PibNA',
    '__gpi': 'UID=00000ca2ac0a7bd9:T=1701547372:RT=1708192460:S=ALNI_MbL2xw-E4bjiFL_NFxDMlf9xvWUKA',
    '__eoi': 'ID=82077cc06794c22e:T=1707008405:RT=1708192460:S=AA-Afjb0agE3jlmDj-opk_vDCtum',
    'FCNEC': '%5B%5B%22AKsRol9FWh1ER62WTiWt2FZYTMBewvfur_T48wPOd91IG9fy_9t_TkCS-rvyxJftgrmvHrx6a9DGncacQ6Iud48MW5PZs6b-wdSevG3Q6ksTDmaQkBhMqm3tvLvVv5kFIwd5xftwZs3XJPFnsF1EFrJum3EJ0fq9Gg%3D%3D%22%5D%5D',
    '_dd_s': 'rum=0&expire=1708193370210',
    '__stripe_sid': '25f7553b-7655-4266-9ee4-ccc6fc3915ab7e1544',
    '87b5a3c3f1a55520_gr_cs1': 'aymenduzzstuff',
    '_ga_CDRWKZTDEX': 'GS1.1.1708192457.31.1.1708192508.9.0.0',
    '_ga': 'GA1.1.627357558.1696465774',
}

headers = {
    'authority': 'leetcode.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
    'authorization': '',
    'baggage': 'sentry-environment=production,sentry-release=7366c15b,sentry-transaction=%2Fu%2F%5Busername%5D,sentry-public_key=2a051f9838e2450fbdd5a77eb62cc83c,sentry-trace_id=982321149e9347e092c51be3b1825b1e,sentry-sample_rate=0.03',
    'content-type': 'application/json',
    # 'cookie': 'gr_user_id=2435d8cc-2808-4d0e-ab6b-e24fe14031e5; 87b5a3c3f1a55520_gr_last_sent_cs1=aymenduzzstuff; __stripe_mid=f024a447-b260-49a6-a407-776ff82d87fbb2e806; cf_clearance=2Jb8EWS45Upj7M92UqZzU29NrCPzSWxzpAB1GO4iJHM-1698509669-0-1-cd932ba.a77045b3.5bd86d5a-160.0.0; csrftoken=iJFOmWIwrj43CEuhPNpgBU3qH0nmeyT0hC3uGnjKS9uPXW7kWKwXUludeOAkLw8H; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNjcwMTM2NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjE2Y2FiMmQxMGE4MjliMTJkN2EwNGFhNzRjOWVjZTVjMDE5NjhhMzZkZGQ0YTUwOWEyNDJkNjg3NDliNDg2MGUiLCJpZCI6NjcwMTM2NiwiZW1haWwiOiJob3VjaGVfYXltZW5Ab3V0bG9vay5jb20iLCJ1c2VybmFtZSI6ImF5bWVuZHV6enN0dWZmIiwidXNlcl9zbHVnIjoiYXltZW5kdXp6c3R1ZmYiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvZGVmYXVsdF9hdmF0YXIuanBnIiwicmVmcmVzaGVkX2F0IjoxNzA4MTkyNDU1LCJpcCI6IjEwNS4xMDYuMTc1LjE5NCIsImlkZW50aXR5IjoiOWZlYTcwMWE2MjdhNTdkMGM0NThkYjJlMWNiNjBkNjIiLCJzZXNzaW9uX2lkIjo1NDkwNTU0MywiX3Nlc3Npb25fZXhwaXJ5IjoxMjA5NjAwfQ.DyeK0LGx8Uld9vWe6juQss5GBwCj2UoaQkEgxAsp_2Y; _gid=GA1.2.212519538.1708192456; _gat=1; 87b5a3c3f1a55520_gr_session_id=d6221949-ba3e-46af-b8fc-9bf46208b4f4; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=d6221949-ba3e-46af-b8fc-9bf46208b4f4; 87b5a3c3f1a55520_gr_session_id_sent_vst=d6221949-ba3e-46af-b8fc-9bf46208b4f4; __gads=ID=ceb77aee9e283458:T=1701547372:RT=1708192460:S=ALNI_MbtZGFCfCRM6cTTeToJ3eJD0PibNA; __gpi=UID=00000ca2ac0a7bd9:T=1701547372:RT=1708192460:S=ALNI_MbL2xw-E4bjiFL_NFxDMlf9xvWUKA; __eoi=ID=82077cc06794c22e:T=1707008405:RT=1708192460:S=AA-Afjb0agE3jlmDj-opk_vDCtum; FCNEC=%5B%5B%22AKsRol9FWh1ER62WTiWt2FZYTMBewvfur_T48wPOd91IG9fy_9t_TkCS-rvyxJftgrmvHrx6a9DGncacQ6Iud48MW5PZs6b-wdSevG3Q6ksTDmaQkBhMqm3tvLvVv5kFIwd5xftwZs3XJPFnsF1EFrJum3EJ0fq9Gg%3D%3D%22%5D%5D; _dd_s=rum=0&expire=1708193370210; __stripe_sid=25f7553b-7655-4266-9ee4-ccc6fc3915ab7e1544; 87b5a3c3f1a55520_gr_cs1=aymenduzzstuff; _ga_CDRWKZTDEX=GS1.1.1708192457.31.1.1708192508.9.0.0; _ga=GA1.1.627357558.1696465774',
    'origin': 'https://leetcode.com',
    'random-uuid': '3dadef98-2104-d906-1c5c-cd920bbac318',
    'referer': 'https://leetcode.com/rohitraj2k04/',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '982321149e9347e092c51be3b1825b1e-9c416bd4cf96e39a-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'uuuserid': '1d0898c41a3664bd6eefb6a3826d0051',
    'x-csrftoken': 'iJFOmWIwrj43CEuhPNpgBU3qH0nmeyT0hC3uGnjKS9uPXW7kWKwXUludeOAkLw8H',
    'x-newrelic-id': 'UAQDVFVRGwIAUVhbAAMFXlQ=',
}




json_data = {
    'query': '\n    query recentAcSubmissions($username: String!, $limit: Int!) {\n  recentAcSubmissionList(username: $username, limit: $limit) {\n    id\n    title\n    titleSlug\n    timestamp\n  }\n}\n    ',
    'variables': {
        'username': '',
        'limit': 2000,
    },
    'operationName': 'recentAcSubmissions',
}


def get_recent_submissions(username):
    
    json_data['variables']['username'] = username

    response = requests.post('https://leetcode.com/graphql/', cookies=cookies, headers=headers, json=json_data)
    recent_sub = json.loads(response.content.decode('utf8'))['data']['recentAcSubmissionList']
    return recent_sub

def verify_existance(username) :
        
    session = HTMLSession()
    response = session.get(f'https://leetcode.com/{username}/')

    print(response.status_code)
    if response.status_code == 200 : 
        return True 
    else : 
        return False
    


#

#print(get_recent_submissions("rohitraj2k04"))


