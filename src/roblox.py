from src.arkoselabs import get_token
from httpcloak      import Session

from base64     import b64encode, b64decode
from src        import Log, Utils, Headers
from json       import loads, dumps

class Roblox:
    def __init__(self, proxy: str = None, hv: str = "auto") -> None:
        self.session = Session(
            preset="android-chrome-144",
            tls_only=True,
            http_version=hv,
            timeout=120
        )
        self.session.set_proxy(proxy)
        
    def signup(self) -> None:
        self.username = Utils.generate_name()
        xcsrf = self.session.post("https://auth.roblox.com/v2/signup", headers=Headers.SIGNUP_NO_CAPTCHA).headers.get("x-csrf-token")[0] # <-- returns a fuckass list??

        payload_signup = {
            "locale": "en-us",
            "agreementIds": ["306cc852-3717-4996-93e7-086daafd42f6", "2ba6b930-4ba8-4085-9e8c-24b919701f15"],
            "gender": "Male",
            "username": self.username,
            "isTosAgreementBoxChecked": True,
            "birthday": "1995-1-1T12:00:00.000Z",
            "accountBlob": "",
            "password": "545tg2g02j4r02rfds24"
        }
        response_signup = self.session.post(
            "https://auth.roblox.com/v2/signup", 
            json=payload_signup, 
            headers={
                **Headers.SIGNUP_NO_CAPTCHA,
                "x-csrf-token": xcsrf,
                "traceparent": Utils.generate_traceparent()
            }
        )
        blob: str = ""

        if response_signup.headers.get("rblx-challenge-type")[0] == "deviceintegrity": 
            payload_continue = {
                "challengeMetadata": "{\"integrityType\":\"playintegrity\",\"redemptionToken\":\"\"}",
                "challengeType": "deviceintegrity",
                "challengeId": response_signup.headers.get("rblx-challenge-id")[0]
            }

            response_continue = self.session.post(
                "https://apis.roblox.com/challenge/v1/continue", 
                json=payload_continue, 
                headers={
                    **Headers.CONTINUE,
                    "x-csrf-token": xcsrf,
                    "traceparent": Utils.generate_traceparent()
                }
            )
            blob = loads(response_continue.json().get("challengeMetadata", {})).get("dataExchangeBlob", None)

        else:
            blob = loads(b64decode(response_signup.headers.get("rblx-challenge-metadata")[0]).decode()).get("dataExchangeBlob")

        token = get_token(blob, self.session)

        payload_continue2 = "{\"challengeId\":\"" + response_signup.headers.get("rblx-challenge-id")[0] + "\",\"challengeType\":\"captcha\",\"challengeMetadata\":\"{\\\"unifiedCaptchaId\\\":\\\"" + response_signup.headers.get("rblx-challenge-id")[0] + "\\\",\\\"captchaToken\\\":\\\"" + token + "\\\",\\\"actionType\\\":\\\"Signup\\\"}\"}"
        self.session.post(
            "https://apis.roblox.com/challenge/v1/continue", 
            data=payload_continue2, 
            headers={
                **Headers.CONTINUE,
                "x-csrf-token": xcsrf,
                "traceparent": Utils.generate_traceparent()
            }
        )

        metadata = {
            "captchaToken": "",
            "unifiedCaptchaId": response_signup.headers.get("rblx-challenge-id")[0],
            "dataExchangeBlob": blob,
            "actionType": "Signup",
            "requestPath": "/v2/signup",
            "requestMethod": "POST",
            "sharedParameters": {
                    "shouldAnalyze": False,
                    "genericChallengeId": response_signup.headers.get("rblx-challenge-id")[0],
                    "useContinueMode": False,
                    "renderNativeChallenge": False,
                    "delayParameters": None
                }
            }

        response_signup_captcha = self.session.post(
            "https://auth.roblox.com/v2/signup", 
            json=payload_signup, 
            headers={
                **Headers.SIGNUP_CAPTCHA,
                "x-csrf-token": xcsrf,
                "traceparent": Utils.generate_traceparent(),
                "rblx-challenge-metadata": b64encode(str('"' + dumps(metadata) + '"').encode()).decode(),
                "rblx-challenge-id": response_signup.headers.get("rblx-challenge-id")[0]
            }
        )

        if response_signup_captcha.ok:
            with open("output/cookies.txt", "a") as f:
                for cookie in response_signup_captcha.cookies:
                    if cookie.name == ".ROBLOSECURITY":
                        f.write(cookie.value + "\n") # <--list
                        break
            
            self.session.close()
            Log.success("Created account with name: " + self.username)

        else:
            self.session.close()
            raise Exception("Failed to create account: " +  response_signup_captcha.text)
