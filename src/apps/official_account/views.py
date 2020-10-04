from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from defusedxml.cElementTree import fromstring

from django_improved_view.views import APIView
from django_improved_view import exceptions
from OpenWeChat.compat import complex_json
from OpenWeChat.messages import reply
from OpenWeChat.consts import MessageType, EventType
from OpenWeChat.messages.handler import Handler

from . import models


class MessageHandler(Handler):
    def __init__(self, wx_app, wechat_account):
        super().__init__()
        self.wx_app = wx_app
        self.wechat_account = wechat_account
        self.event_handler_mapping = {
            EventType.SUBSCRIBE: self.handle_subscribe,
            EventType.SCAN: self.handle_scan,
        }
        self.message_handler_mapping = {
            MessageType.TEXT: self.handle_text,
        }
        self.event_replies_manager = self.wechat_account.event_replies

    def get_event_handler(self, event_type):
        return self.event_handler_mapping.get(event_type)

    def get_message_handler(self, message_type):
        return self.message_handler_mapping.get(message_type)

    def get_template_context(self, message):
        context = {}
        openid = message.FromUserName
        follower = models.Follower.objects.filter(
            wechat_account=self.wechat_account, openid=openid).first()
        if follower:
            context['nickname'] = complex_json.loads(
                follower.user_info)['nickname']
        return context

    def render_event_reply(self, event_reply, message):
        if not event_reply:
            return reply.BlankResponse()
        context = self.get_template_context(message)
        reply_msg = event_reply.reply_template.generate_reply(
            message, **context)
        return reply_msg

    def handle_subscribe(self, message):
        event_reply = self.event_replies_manager.filter(
            event=EventType.SUBSCRIBE.value).first()
        self.update_follower_info(message.FromUserName)
        return self.render_event_reply(event_reply, message)

    def handle_event(self, event_type, event_value, message):
        event_reply = self.event_replies_manager.filter(
            event=event_type, value=event_value).first()
        content = self.render_event_reply(event_reply, message)
        return content

    def handle_text(self, message):
        return self.handle_event('text', message.Content, message)

    def handle_scan(self, message):
        return self.handle_event(EventType.SCAN.value, message.EventKey, message)

    def update_follower_info(self, openid):
        user_info = self.wx_app.get_user_info(openid)
        defaults = {
            'unionid': user_info['unionid'],
            'user_info': complex_json.dumps(user_info, ensure_ascii=False),
        }
        return models.Follower.objects.update_or_create(
            openid=openid,
            wechat_account=self.wechat_account,
            defaults=defaults)


class CallbackView(APIView):
    def validate_callback_api(self, request, appid):
        # check request is from wechat or not
        wechat_account = models.OpenWeChatAccount.objects.filter(
            appid=appid).first()
        if not wechat_account:
            raise exceptions.NotFound()
        wx_app = wechat_account.wx_app
        nonce = request.query_params.get('nonce', '')
        timestamp = request.query_params.get('timestamp', '')
        signature = request.query_params.get('signature', '')
        if not wx_app.validate_callback_api(nonce, timestamp, signature):
            raise exceptions.Forbidden()
        return wx_app, wechat_account

    def get(self, request, appid=None):
        wx_app, wechat_account = self.validate_callback_api(request, appid)
        echo_str = request.query_params.get('echostr', '')
        return HttpResponse(status=400)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, appid=None):
        wx_app, wechat_account = self.validate_callback_api(request, appid)
        message_handler = MessageHandler(wx_app, wechat_account)
        xml_data = fromstring(request.body)
        resp_content = message_handler.handle_request(xml_data)
        return HttpResponse(resp_content)
