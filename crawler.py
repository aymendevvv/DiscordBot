import requests 
import json

cookies = {
    'gr_user_id': '2435d8cc-2808-4d0e-ab6b-e24fe14031e5',
    '87b5a3c3f1a55520_gr_last_sent_cs1': 'aymenduzzstuff',
    '__stripe_mid': 'f024a447-b260-49a6-a407-776ff82d87fbb2e806',
    'cf_clearance': '2Jb8EWS45Upj7M92UqZzU29NrCPzSWxzpAB1GO4iJHM-1698509669-0-1-cd932ba.a77045b3.5bd86d5a-160.0.0',
    '__gads': 'ID=ceb77aee9e283458:T=1701547372:RT=1701547372:S=ALNI_MbtZGFCfCRM6cTTeToJ3eJD0PibNA',
    '__gpi': 'UID=00000ca2ac0a7bd9:T=1701547372:RT=1701547372:S=ALNI_MbL2xw-E4bjiFL_NFxDMlf9xvWUKA',
    '_gid': 'GA1.2.1151576200.1704311396',
    '87b5a3c3f1a55520_gr_session_id': '2dc24592-fa12-48f2-892c-947c3fa577e8',
    '87b5a3c3f1a55520_gr_last_sent_sid_with_cs1': '2dc24592-fa12-48f2-892c-947c3fa577e8',
    '87b5a3c3f1a55520_gr_session_id_sent_vst': '2dc24592-fa12-48f2-892c-947c3fa577e8',
    'csrftoken': 'N2HXmJXQusZXwK6uzLCtVQEiBSsbwVsppPcc8ovlwrS6ArSuFLqnAQTnBGYGoxuO',
    'messages': 'W1siX19qc29uX21lc3NhZ2UiLDAsMjUsIlN1Y2Nlc3NmdWxseSBzaWduZWQgaW4gYXMgYXltZW5kdXp6c3R1ZmYuIl1d:1rL7KW:XncJNp8XxaR5gz9K6oEPYyjPNWeiBRE5SjwdrhDQ7BY',
    'LEETCODE_SESSION': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNjcwMTM2NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjE2Y2FiMmQxMGE4MjliMTJkN2EwNGFhNzRjOWVjZTVjMDE5NjhhMzZkZGQ0YTUwOWEyNDJkNjg3NDliNDg2MGUiLCJpZCI6NjcwMTM2NiwiZW1haWwiOiJob3VjaGVfYXltZW5Ab3V0bG9vay5jb20iLCJ1c2VybmFtZSI6ImF5bWVuZHV6enN0dWZmIiwidXNlcl9zbHVnIjoiYXltZW5kdXp6c3R1ZmYiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvZGVmYXVsdF9hdmF0YXIuanBnIiwicmVmcmVzaGVkX2F0IjoxNzA0MzExNzA4LCJpcCI6IjEwNS4xMDcuNjMuMTcwIiwiaWRlbnRpdHkiOiI5YzFjZTI3ZjA4YjE2NDc5ZDJlMTc3NDMwNjJiMjhlZCIsInNlc3Npb25faWQiOjUyODE5MzIzLCJfc2Vzc2lvbl9leHBpcnkiOjEyMDk2MDB9.337rTueiXOHXgnqKtdP0HcTjXRpshjnJhkG5lRVhy8w',
    '_dd_s': 'rum=0&expire=1704312666890',
    '__stripe_sid': 'e5d45072-c99e-4806-a4fe-68edcecc9f30c35589',
    '87b5a3c3f1a55520_gr_cs1': 'aymenduzzstuff',
    '_ga': 'GA1.2.627357558.1696465774',
    '_gat': '1',
    '_ga_CDRWKZTDEX': 'GS1.1.1704311434.23.1.1704311829.45.0.0',
}

headers = {
    'authority': 'leetcode.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': '',
    'baggage': 'sentry-environment=production,sentry-release=8c964d1c,sentry-transaction=%2Fu%2F%5Busername%5D,sentry-public_key=2a051f9838e2450fbdd5a77eb62cc83c,sentry-trace_id=5c96c854dba84d20bcf2671a341f8f53,sentry-sample_rate=0.03',
    'content-type': 'application/json',
    # 'cookie': 'gr_user_id=2435d8cc-2808-4d0e-ab6b-e24fe14031e5; 87b5a3c3f1a55520_gr_last_sent_cs1=aymenduzzstuff; __stripe_mid=f024a447-b260-49a6-a407-776ff82d87fbb2e806; cf_clearance=2Jb8EWS45Upj7M92UqZzU29NrCPzSWxzpAB1GO4iJHM-1698509669-0-1-cd932ba.a77045b3.5bd86d5a-160.0.0; __gads=ID=ceb77aee9e283458:T=1701547372:RT=1701547372:S=ALNI_MbtZGFCfCRM6cTTeToJ3eJD0PibNA; __gpi=UID=00000ca2ac0a7bd9:T=1701547372:RT=1701547372:S=ALNI_MbL2xw-E4bjiFL_NFxDMlf9xvWUKA; _gid=GA1.2.1151576200.1704311396; 87b5a3c3f1a55520_gr_session_id=2dc24592-fa12-48f2-892c-947c3fa577e8; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=2dc24592-fa12-48f2-892c-947c3fa577e8; 87b5a3c3f1a55520_gr_session_id_sent_vst=2dc24592-fa12-48f2-892c-947c3fa577e8; csrftoken=N2HXmJXQusZXwK6uzLCtVQEiBSsbwVsppPcc8ovlwrS6ArSuFLqnAQTnBGYGoxuO; messages=W1siX19qc29uX21lc3NhZ2UiLDAsMjUsIlN1Y2Nlc3NmdWxseSBzaWduZWQgaW4gYXMgYXltZW5kdXp6c3R1ZmYuIl1d:1rL7KW:XncJNp8XxaR5gz9K6oEPYyjPNWeiBRE5SjwdrhDQ7BY; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNjcwMTM2NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjE2Y2FiMmQxMGE4MjliMTJkN2EwNGFhNzRjOWVjZTVjMDE5NjhhMzZkZGQ0YTUwOWEyNDJkNjg3NDliNDg2MGUiLCJpZCI6NjcwMTM2NiwiZW1haWwiOiJob3VjaGVfYXltZW5Ab3V0bG9vay5jb20iLCJ1c2VybmFtZSI6ImF5bWVuZHV6enN0dWZmIiwidXNlcl9zbHVnIjoiYXltZW5kdXp6c3R1ZmYiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvZGVmYXVsdF9hdmF0YXIuanBnIiwicmVmcmVzaGVkX2F0IjoxNzA0MzExNzA4LCJpcCI6IjEwNS4xMDcuNjMuMTcwIiwiaWRlbnRpdHkiOiI5YzFjZTI3ZjA4YjE2NDc5ZDJlMTc3NDMwNjJiMjhlZCIsInNlc3Npb25faWQiOjUyODE5MzIzLCJfc2Vzc2lvbl9leHBpcnkiOjEyMDk2MDB9.337rTueiXOHXgnqKtdP0HcTjXRpshjnJhkG5lRVhy8w; _dd_s=rum=0&expire=1704312666890; __stripe_sid=e5d45072-c99e-4806-a4fe-68edcecc9f30c35589; 87b5a3c3f1a55520_gr_cs1=aymenduzzstuff; _ga=GA1.2.627357558.1696465774; _gat=1; _ga_CDRWKZTDEX=GS1.1.1704311434.23.1.1704311829.45.0.0',
    'origin': 'https://leetcode.com',
    'random-uuid': '3dadef98-2104-d906-1c5c-cd920bbac318',
    'referer': 'https://leetcode.com/aymenduzzstuff/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '5c96c854dba84d20bcf2671a341f8f53-8d01c7d3481e9213-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-csrftoken': 'N2HXmJXQusZXwK6uzLCtVQEiBSsbwVsppPcc8ovlwrS6ArSuFLqnAQTnBGYGoxuO',
    'x-newrelic-id': 'UAQDVFVRGwIAUVhbAAMFXlQ=',
}

json_data = {
    'query': '\n    query recentAcSubmissions($username: String!, $limit: Int!) {\n  recentAcSubmissionList(username: $username, limit: $limit) {\n    id\n    title\n    titleSlug\n    timestamp\n  }\n}\n    ',
    'variables': {
        'username': '',
        'limit': 15,
    },
    'operationName': 'recentAcSubmissions',
}


def get_recent_submissions(username):
    
    json_data['variables']['username'] = username

    response = requests.post('https://leetcode.com/graphql/', cookies=cookies, headers=headers, json=json_data)
    recent_sub = json.loads(response.content.decode('utf8'))['data']['recentAcSubmissionList']
    return recent_sub

def verifiy_existance(username) :
    resp = requests.get(f"https://leetcode.com/{username}/")
    if resp.status_code == 200 : 
        return True 
    else : 
        return False
    


verifiy_existance("aymenduzzstuff")

#print(len(get_recent_submissions("rohitraj2k04")))



