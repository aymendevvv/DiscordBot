import requests 
import json

cookies = {
    'gr_user_id': '2435d8cc-2808-4d0e-ab6b-e24fe14031e5',
    'csrftoken': 'UiJl9WLNvCwMGiH1VN1z5xiUHsBykNfyXFNtK0GktX2cxignpZFofakC1yRIK0cp',
    '87b5a3c3f1a55520_gr_last_sent_cs1': 'aymenduzzstuff',
    '__stripe_mid': 'f024a447-b260-49a6-a407-776ff82d87fbb2e806',
    'cf_clearance': '2Jb8EWS45Upj7M92UqZzU29NrCPzSWxzpAB1GO4iJHM-1698509669-0-1-cd932ba.a77045b3.5bd86d5a-160.0.0',
    'LEETCODE_SESSION': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNjcwMTM2NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjE2Y2FiMmQxMGE4MjliMTJkN2EwNGFhNzRjOWVjZTVjMDE5NjhhMzZkZGQ0YTUwOWEyNDJkNjg3NDliNDg2MGUiLCJpZCI6NjcwMTM2NiwiZW1haWwiOiJob3VjaGVfYXltZW5Ab3V0bG9vay5jb20iLCJ1c2VybmFtZSI6ImF5bWVuZHV6enN0dWZmIiwidXNlcl9zbHVnIjoiYXltZW5kdXp6c3R1ZmYiLCJhdmF0YXIiOiJodHRwczovL3MzLXVzLXdlc3QtMS5hbWF6b25hd3MuY29tL3MzLWxjLXVwbG9hZC9hc3NldHMvZGVmYXVsdF9hdmF0YXIuanBnIiwicmVmcmVzaGVkX2F0IjoxNzAxNDYwNjgzLCJpcCI6IjE5Ny4yMDYuMS4zMiIsImlkZW50aXR5IjoiZTNmODEwMWM0MWI0MDU3Mjk3MzIyN2QwYTY0NjIwZDAiLCJzZXNzaW9uX2lkIjo0ODkwMjg5NiwiX3Nlc3Npb25fZXhwaXJ5IjoxMjA5NjAwfQ.KgUUhccDY1Ej1xHsWpSuGmF4aAUubattN7Z-vg6oJxU',
    '_gid': 'GA1.2.209487626.1701460684',
    '87b5a3c3f1a55520_gr_session_id': 'd166a924-862c-4508-8c6a-208bc68f8268',
    '87b5a3c3f1a55520_gr_last_sent_sid_with_cs1': 'd166a924-862c-4508-8c6a-208bc68f8268',
    '87b5a3c3f1a55520_gr_session_id_sent_vst': 'd166a924-862c-4508-8c6a-208bc68f8268',
    '__stripe_sid': '4c15739f-8a0b-4f1d-896a-c505093c93861fb57f',
    '87b5a3c3f1a55520_gr_cs1': 'aymenduzzstuff',
    '_gat': '1',
    '_ga': 'GA1.1.627357558.1696465774',
    '_dd_s': 'rum=0&expire=1701461766047',
    '_ga_CDRWKZTDEX': 'GS1.1.1701460688.16.1.1701460931.6.0.0',
}

headers = {
    'authority': 'leetcode.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': '',
    'baggage': 'sentry-environment=production,sentry-release=86193013,sentry-transaction=%2Fu%2F%5Busername%5D,sentry-public_key=2a051f9838e2450fbdd5a77eb62cc83c,sentry-trace_id=e4754b0b748b4bcb96ad35fb33d2317b,sentry-sample_rate=0.03',
    'content-type': 'application/json',
    # 'cookie': 'gr_user_id=2435d8cc-2808-4d0e-ab6b-e24fe14031e5; csrftoken=UiJl9WLNvCwMGiH1VN1z5xiUHsBykNfyXFNtK0GktX2cxignpZFofakC1yRIK0cp; 87b5a3c3f1a55520_gr_last_sent_cs1=aymenduzzstuff; __stripe_mid=f024a447-b260-49a6-a407-776ff82d87fbb2e806; cf_clearance=2Jb8EWS45Upj7M92UqZzU29NrCPzSWxzpAB1GO4iJHM-1698509669-0-1-cd932ba.a77045b3.5bd86d5a-160.0.0; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNjcwMTM2NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjE2Y2FiMmQxMGE4MjliMTJkN2EwNGFhNzRjOWVjZTVjMDE5NjhhMzZkZGQ0YTUwOWEyNDJkNjg3NDliNDg2MGUiLCJpZCI6NjcwMTM2NiwiZW1haWwiOiJob3VjaGVfYXltZW5Ab3V0bG9vay5jb20iLCJ1c2VybmFtZSI6ImF5bWVuZHV6enN0dWZmIiwidXNlcl9zbHVnIjoiYXltZW5kdXp6c3R1ZmYiLCJhdmF0YXIiOiJodHRwczovL3MzLXVzLXdlc3QtMS5hbWF6b25hd3MuY29tL3MzLWxjLXVwbG9hZC9hc3NldHMvZGVmYXVsdF9hdmF0YXIuanBnIiwicmVmcmVzaGVkX2F0IjoxNzAxNDYwNjgzLCJpcCI6IjE5Ny4yMDYuMS4zMiIsImlkZW50aXR5IjoiZTNmODEwMWM0MWI0MDU3Mjk3MzIyN2QwYTY0NjIwZDAiLCJzZXNzaW9uX2lkIjo0ODkwMjg5NiwiX3Nlc3Npb25fZXhwaXJ5IjoxMjA5NjAwfQ.KgUUhccDY1Ej1xHsWpSuGmF4aAUubattN7Z-vg6oJxU; _gid=GA1.2.209487626.1701460684; 87b5a3c3f1a55520_gr_session_id=d166a924-862c-4508-8c6a-208bc68f8268; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=d166a924-862c-4508-8c6a-208bc68f8268; 87b5a3c3f1a55520_gr_session_id_sent_vst=d166a924-862c-4508-8c6a-208bc68f8268; __stripe_sid=4c15739f-8a0b-4f1d-896a-c505093c93861fb57f; 87b5a3c3f1a55520_gr_cs1=aymenduzzstuff; _gat=1; _ga=GA1.1.627357558.1696465774; _dd_s=rum=0&expire=1701461766047; _ga_CDRWKZTDEX=GS1.1.1701460688.16.1.1701460931.6.0.0',
    'origin': 'https://leetcode.com',
    'random-uuid': '3dadef98-2104-d906-1c5c-cd920bbac318',
    'referer': 'https://leetcode.com/aymenduzzstuff/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'e4754b0b748b4bcb96ad35fb33d2317b-bc2d13a766c25988-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-csrftoken': 'UiJl9WLNvCwMGiH1VN1z5xiUHsBykNfyXFNtK0GktX2cxignpZFofakC1yRIK0cp',
    'x-newrelic-id': 'UAQDVFVRGwIAUVhbAAMFXlQ=',
}

json_data = {
    'query': '\n    query recentAcSubmissions($username: String!, $limit: Int!) {\n  recentAcSubmissionList(username: $username, limit: $limit) {\n    id\n    title\n    titleSlug\n    timestamp\n  }\n}\n    ',
    'variables': {
        'username': 'coding_menance',
        'limit': 50,
    },
    'operationName': 'recentAcSubmissions',
}

response = requests.post('https://leetcode.com/graphql/', cookies=cookies, headers=headers, json=json_data)

recent_sub = json.loads(response.content.decode( 'utf8' ))['data']['recentAcSubmissionList']

print(recent_sub)



