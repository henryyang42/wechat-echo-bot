from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply, VoiceReply

from flask import Flask, request

app = Flask(__name__)

WECHAT_TOKEN = "wechat_token"


def verify_backend(request):
    # Get the parameters from the query string
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')

    try:
        # If the signature is correct, output the same "echostr" provided by
        # the WeChat server as a parameter
        check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        return echostr
    except InvalidSignatureException:
        return ''


@app.route('/wechat', methods=['GET', 'POST'])
def echo_server():
    error = None
    if request.method == 'GET':
        # The WeChat server will issue a GET request in order to verify the chatbot backend server upon configuration.
        return verify_backend(request)

    elif request.method == 'POST':
        # Messages will be POSTed from the WeChat server to the chatbot backend server,
        message = parse_message(request.data)
        print(message)
        if message.type == 'text':
            reply = TextReply(content=message.content, message=message)
        elif message.type == 'image':
            reply = VoiceReply(media_id=message.media_id, message=message)
        elif message.type == 'voice':
            reply = VoiceReply(media_id=message.media_id, message=message)
        return reply.render()
