import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HEADERS = {
    "authority": "alpha-api.lotuslms.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "vi,en-US;q=0.9,en;q=0.8",
    "origin": "https://bvl.lotuslms.com",
    "referer": "https://bvl.lotuslms.com/admin/conf/dashboard",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": "name=value",
}


class Lms:
    def __init__(self, dmn: str, user_code: str = ""):
        self.api = os.getenv("API_URL")
        self.user_code = user_code if user_code else dmn
        self.param = {
            "submit": "1",
            "_sand_ajax": "1",
            "_sand_platform": "3",
            "_sand_readmin": "1",
            "_sand_is_wan": "false",
            "_sand_ga_sessionToken": "",
            "_sand_ga_browserToken": "",
            "_sand_masked": "",
            "_sand_domain": dmn,
        }
        self.password = os.getenv("API_PASSWORD")
        self.user = self.get_token()

    def send(self, url, payload={}, method="POST"):

        url = f"{self.api}{url}"
        payload.update(self.param)
        method = method if method else self.method_default
        response = requests.request(
            method=method,
            url=url,
            data=payload,
            headers=HEADERS,
            verify=False,
        )
        if response.status_code != 200:
            print(f"Lỗi {response.status_code}: {response.text}")
            return
        try:
            return response.json()
        except:
            return response.text

    def get_token(self):
        url = "/user/login"
        payload = {"lname": self.user_code, "pass": self.password}
        response = self.send(url, payload).get("result", "")
        if "token" not in response:
            print(f"Login fail with user: {self.user_code} and pass: {self.password}")
            return

        print(f"Login with: {self.user_code}")
        self.param.update(
            {
                "_sand_token": response["token"],
                "_sand_uiid": response["iid"],
                "_sand_uid": response["id"],
            }
        )
        return response

    def get_round(self, contest_iid):
        url = "/exam-round/schema-form/get-exam-rounds-for-select-box"
        payload = {"contest_iid": contest_iid}
        return self.send(url, payload).get("result", [])

    def get_rank(self, contest_iid, exam_round_iid, page=1, items_per_page=-1):
        url = "/contest/score/rank"
        payload = {
            "criteria": "score",
            "contest_iid": contest_iid,
            "exam_round_iid": exam_round_iid,
            "page": page,
            "items_per_page": items_per_page,
        }
        return self.send(url, payload).get("result", [])
