import re
import requests
import os

csrf_token_pattern = r'name=["\']csrf_token["\'] value=["\'](.*?)["\']'
ftaa_pattern = r'window._ftaa = ["\'](.*?)["\']'
bfaa_pattern = r'window._bfaa = ["\'](.*?)["\']'
GROUP_ID = 'FLVn1Sc504'
LANG_MAP = {
    'cpp': 54,
    'java': 60,
    'pas': 4
}


class CodeforcesInteractor:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        }

    def login(self):
        url = 'https://codeforces.com/enter'
        result = self.session.get(url, headers=self.headers)

        self.csrf_token = re.findall(csrf_token_pattern, result.text)[0]
        self.ftaa = re.findall(ftaa_pattern, result.text)[0]
        self.bfaa = re.findall(bfaa_pattern, result.text)[0]
        data = {
            'csrf_token': self.csrf_token,
            'ftaa': self.ftaa,
            'bfaa': self.bfaa,
            '_tta': 487,
            # stuff
            'action': 'enter',
            'handleOrEmail': self.username,
            'password': self.password,
        }
        login_result = self.session.post(url, data=data, headers=self.headers)
        return self.check_login()

    def check_login(self):
        url = 'https://codeforces.com/settings/general'
        result = self.session.get(
            url, headers=self.headers, allow_redirects=False)
        if not result.is_redirect:
            print(self.username + " logged to codeforces.")
            return True

        print('Codeforces login failed!')
        return False

    def check_in_group(self):
        url = f'https://codeforces.com/group/{GROUP_ID}/contests'
        result = self.session.get(
            url, headers=self.headers, allow_redirects=False)
        if result.is_redirect:
            print("Please join VNOI group before run this code.", url)
            return False
        return True

    def submit(self, name, code, lang, contest, id):

        print(
            f"Submitting problem {name} to https://codeforces.com/group/FLVn1Sc504/contest/{contest}")
        url = f'https://codeforces.com/group/{GROUP_ID}/contest/{contest}/submit'
        result = self.session.get(url, headers=self.headers)
        self.csrf_token = re.findall(csrf_token_pattern, result.text)[0]
        self.ftaa = re.findall(ftaa_pattern, result.text)[0]
        self.bfaa = re.findall(bfaa_pattern, result.text)[0]
        data = {
            'csrf_token': self.csrf_token,
            'ftaa': self.ftaa,
            'bfaa': self.bfaa,
            '_tta': 410,
            'action': 'submitSolutionFormSubmitted',
            'submittedProblemIndex': id,
            'tabSize': 4,
            'sourceFile': '',
            'source': code,
            'programTypeId': LANG_MAP[lang]
        }
        r = self.session.post(
            url, params=data, headers=self.headers, allow_redirects=False)
        print("done")

    def submit_package_solutions(self, mashup_id):
        url = 'https://codeforces.com/gym/{0}'.format(mashup_id)
        result = self.session.get(url, headers=self.headers)
        self.csrf_token = re.findall(csrf_token_pattern, result.text)[0]
        self.ftaa = re.findall(ftaa_pattern, result.text)[0]
        self.bfaa = re.findall(bfaa_pattern, result.text)[0]
        data = {
            'csrf_token': self.csrf_token,
            'ftaa': self.ftaa,
            'bfaa': self.bfaa,
            '_tta': 377
        }
        r = self.session.post(
            url + '/submitPackageSolutionsPage', params=data, headers=self.headers)
        print(r.text)
        return
