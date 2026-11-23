import os
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MemberJoinedEvent

# 토큰과 시크릿은 파일에 적지 않고, 호스팅 사이트의 "환경 변수"에 넣어요.
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

# 환영 문구는 여기서 바꾸세요
WELCOME_TEXT = """우리의 미식가님!🍒

🦢 𝓒𝓱𝓮𝓻𝓲𝓼𝓱 🍷방에 오신걸 환영합니다

오른쪽 상단 -> 「노트」

①자기소개 • 족보 댓글에 작성

②필독 공지 확인

③ 완료 후 관리자 태그 (🍸)

10분 내 미완료 • 공지 미숙지 시 강퇴
!!"""

app = Flask(__name__)
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/")
def home():
    return "bot is running"


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


# 새 멤버가 채팅방에 들어오면 이 함수가 실행돼요
@handler.add(MemberJoinedEvent)
def welcome(event):
    with ApiClient(configuration) as api_client:
        MessagingApi(api_client).reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=WELCOME_TEXT)],
            )
        )
