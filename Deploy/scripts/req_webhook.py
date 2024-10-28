import requests
from dotenv import load_dotenv
import os
import fire

class Webhooks_setttings():
    """

    registration: for connect to api.telegrambot and set weebhook, sent self singet cert from
        '/etc/ssl/certs/nginx_test.pem'
    get_webhook_info: get info from api.telegrambot
    del_webhook: unset weebhook

    for start in CLI python {filepath} function of class [get_webhook_info, del_webhook]

    """

    load_dotenv()
    BOTTOKEN = os.getenv('TOKEN')
    HOST = os.getenv('HOST')
    WEBHOOK_SSL_FILE = os.getenv('WEBHOOK_SSL_FILE') #*.pem

    def _say_answer(self, req):
        print("REQUEST...")
        print(req.json)
        print("HEADERS...")
        print(req.headers)
        print("RESPONSE...")
        print(req.text)

    def registration(self):
        #нужно передать самоподписной сертификат
        try:
            file = open('/home/common_user/test_bot_app/test_bot_deploy/ssl/bot_pub.pem','rb')
        except:
            return 'Error File not Found'
        req = requests.post(f'https://api.telegram.org/bot{self.BOTTOKEN}/setWebhook',

                            json={'url':f'https://{self.HOST}',
                                'certificate':f'{file}'},
                            )
        self._say_answer(req)

    def get_webhook_info(self):
        req = requests.post(f'https://api.telegram.org/bot{self.BOTTOKEN}/getWebhookInfo',
                            headers={'Content-Type': 'application/json'},
                            )
        self._say_answer(req)


    def del_webhook(self):
        req = requests.post(f'https://api.telegram.org/bot{self.BOTTOKEN}/deleteWebhook',
                            headers={'Content-Type': 'application/json'},
                            )

        self._say_answer(req)


if __name__=='__main__':
    fire.Fire(Webhooks_setttings)
