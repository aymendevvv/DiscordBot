import requests
import json 
import pandas as pd 

cookies = {
    'gr_user_id': '2435d8cc-2808-4d0e-ab6b-e24fe14031e5',
    'csrftoken': 'UiJl9WLNvCwMGiH1VN1z5xiUHsBykNfyXFNtK0GktX2cxignpZFofakC1yRIK0cp',
    '87b5a3c3f1a55520_gr_last_sent_cs1': 'aymenduzzstuff',
    '__stripe_mid': 'f024a447-b260-49a6-a407-776ff82d87fbb2e806',
    'cf_clearance': '2Jb8EWS45Upj7M92UqZzU29NrCPzSWxzpAB1GO4iJHM-1698509669-0-1-cd932ba.a77045b3.5bd86d5a-160.0.0',
    '_gid': 'GA1.2.209487626.1701460684',
    'LEETCODE_SESSION': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNjcwMTM2NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjE2Y2FiMmQxMGE4MjliMTJkN2EwNGFhNzRjOWVjZTVjMDE5NjhhMzZkZGQ0YTUwOWEyNDJkNjg3NDliNDg2MGUiLCJpZCI6NjcwMTM2NiwiZW1haWwiOiJob3VjaGVfYXltZW5Ab3V0bG9vay5jb20iLCJ1c2VybmFtZSI6ImF5bWVuZHV6enN0dWZmIiwidXNlcl9zbHVnIjoiYXltZW5kdXp6c3R1ZmYiLCJhdmF0YXIiOiJodHRwczovL3MzLXVzLXdlc3QtMS5hbWF6b25hd3MuY29tL3MzLWxjLXVwbG9hZC9hc3NldHMvZGVmYXVsdF9hdmF0YXIuanBnIiwicmVmcmVzaGVkX2F0IjoxNzAxNTQ3MzY2LCJpcCI6IjEwNS4xMDcuOTMuMTIyIiwiaWRlbnRpdHkiOiJlM2Y4MTAxYzQxYjQwNTcyOTczMjI3ZDBhNjQ2MjBkMCIsInNlc3Npb25faWQiOjQ4OTAyODk2LCJfc2Vzc2lvbl9leHBpcnkiOjEyMDk2MDB9.evTESJfRBMTiPjQv_1mnvPeIw1pnTJ1J-FwCIBa_qwM',
    '87b5a3c3f1a55520_gr_session_id': '7f9dc6ca-1d36-4378-807e-86fea249deac',
    '87b5a3c3f1a55520_gr_last_sent_sid_with_cs1': '7f9dc6ca-1d36-4378-807e-86fea249deac',
    '87b5a3c3f1a55520_gr_session_id_sent_vst': '7f9dc6ca-1d36-4378-807e-86fea249deac',
    '__gads': 'ID=ceb77aee9e283458:T=1701547372:RT=1701547372:S=ALNI_MbtZGFCfCRM6cTTeToJ3eJD0PibNA',
    '__gpi': 'UID=00000ca2ac0a7bd9:T=1701547372:RT=1701547372:S=ALNI_MbL2xw-E4bjiFL_NFxDMlf9xvWUKA',
    '_dd_s': 'rum=0&expire=1701548305775',
    '__stripe_sid': '6d88dadd-bfa0-410f-b102-5e4add581d3076de0e',
    '_gat': '1',
    '87b5a3c3f1a55520_gr_cs1': 'aymenduzzstuff',
    '_ga': 'GA1.1.627357558.1696465774',
    '_ga_CDRWKZTDEX': 'GS1.1.1701547368.20.1.1701547746.28.0.0',
}

headers = {
    'authority': 'leetcode.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': '',
    'content-type': 'application/json',
    # 'cookie': 'gr_user_id=2435d8cc-2808-4d0e-ab6b-e24fe14031e5; csrftoken=UiJl9WLNvCwMGiH1VN1z5xiUHsBykNfyXFNtK0GktX2cxignpZFofakC1yRIK0cp; 87b5a3c3f1a55520_gr_last_sent_cs1=aymenduzzstuff; __stripe_mid=f024a447-b260-49a6-a407-776ff82d87fbb2e806; cf_clearance=2Jb8EWS45Upj7M92UqZzU29NrCPzSWxzpAB1GO4iJHM-1698509669-0-1-cd932ba.a77045b3.5bd86d5a-160.0.0; _gid=GA1.2.209487626.1701460684; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNjcwMTM2NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjE2Y2FiMmQxMGE4MjliMTJkN2EwNGFhNzRjOWVjZTVjMDE5NjhhMzZkZGQ0YTUwOWEyNDJkNjg3NDliNDg2MGUiLCJpZCI6NjcwMTM2NiwiZW1haWwiOiJob3VjaGVfYXltZW5Ab3V0bG9vay5jb20iLCJ1c2VybmFtZSI6ImF5bWVuZHV6enN0dWZmIiwidXNlcl9zbHVnIjoiYXltZW5kdXp6c3R1ZmYiLCJhdmF0YXIiOiJodHRwczovL3MzLXVzLXdlc3QtMS5hbWF6b25hd3MuY29tL3MzLWxjLXVwbG9hZC9hc3NldHMvZGVmYXVsdF9hdmF0YXIuanBnIiwicmVmcmVzaGVkX2F0IjoxNzAxNTQ3MzY2LCJpcCI6IjEwNS4xMDcuOTMuMTIyIiwiaWRlbnRpdHkiOiJlM2Y4MTAxYzQxYjQwNTcyOTczMjI3ZDBhNjQ2MjBkMCIsInNlc3Npb25faWQiOjQ4OTAyODk2LCJfc2Vzc2lvbl9leHBpcnkiOjEyMDk2MDB9.evTESJfRBMTiPjQv_1mnvPeIw1pnTJ1J-FwCIBa_qwM; 87b5a3c3f1a55520_gr_session_id=7f9dc6ca-1d36-4378-807e-86fea249deac; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=7f9dc6ca-1d36-4378-807e-86fea249deac; 87b5a3c3f1a55520_gr_session_id_sent_vst=7f9dc6ca-1d36-4378-807e-86fea249deac; __gads=ID=ceb77aee9e283458:T=1701547372:RT=1701547372:S=ALNI_MbtZGFCfCRM6cTTeToJ3eJD0PibNA; __gpi=UID=00000ca2ac0a7bd9:T=1701547372:RT=1701547372:S=ALNI_MbL2xw-E4bjiFL_NFxDMlf9xvWUKA; _dd_s=rum=0&expire=1701548305775; __stripe_sid=6d88dadd-bfa0-410f-b102-5e4add581d3076de0e; _gat=1; 87b5a3c3f1a55520_gr_cs1=aymenduzzstuff; _ga=GA1.1.627357558.1696465774; _ga_CDRWKZTDEX=GS1.1.1701547368.20.1.1701547746.28.0.0',
    'origin': 'https://leetcode.com',
    'random-uuid': '3dadef98-2104-d906-1c5c-cd920bbac318',
    'referer': 'https://leetcode.com/problemset/all/?page=59',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'uuuserid': 'd4bb616a7cb1f63663fca4d981a0e3d5',
    'x-csrftoken': 'UiJl9WLNvCwMGiH1VN1z5xiUHsBykNfyXFNtK0GktX2cxignpZFofakC1yRIK0cp',
    'x-newrelic-id': 'UAQDVFVRGwIAUVhbAAMFXlQ=',
}

json_data = {
    'query': '\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      topicTags {\n        name\n        id\n        slug\n      }\n      hasSolution\n      hasVideoSolution\n    }\n  }\n}\n    ',
    'variables': {
        'categorySlug': '',
        'skip': 0,
        'limit': 5000,
        'filters': {},
    },
    'operationName': 'problemsetQuestionList',
}

response = requests.post('https://leetcode.com/graphql/', cookies=cookies, headers=headers, json=json_data)


qsts = json.loads(response.content.decode( 'utf8' ))['data']['problemsetQuestionList']['questions']


#empty dataframe 

qsts_list = []
for qst in qsts :

    flattened_data = {
    'acRate': qst['acRate'],
    'difficulty': qst['difficulty'],
    'frontendQuestionId': qst['frontendQuestionId'],
    'isFavor': qst['isFavor'],
    'paidOnly': qst['paidOnly'],
    'title': qst['title'],
    'titleSlug': qst['titleSlug'],
    'hasSolution': qst['hasSolution'],
    'hasVideoSolution': qst['hasVideoSolution']
    }

    flattened_data['topicTags'] = ', '.join(tag["name"] for tag in qst['topicTags'] ) if 'topicTags' in qst else None 
    
    qsts_list.append(flattened_data)
    
    
df = pd.DataFrame(qsts_list)

df.to_csv("challenges.csv" , index=False)



print(len(qsts))
