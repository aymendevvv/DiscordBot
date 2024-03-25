from requests_html import HTMLSession

session = HTMLSession()

r = session.get('https://leetcode.com/aymenduzzstuff/')
print(r.status_code)