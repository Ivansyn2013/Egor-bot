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
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    WEBHOOK_PORT = os.getenv('WEBHOOK_PORT')
    WEBHOOK_SSL_CERT = os.getenv('WEBHOOK_SSL_CERT') #*.pem
    WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
    def _say_answer(self, req):
        print(f"URL: {req.url}")
        print("REQUEST...")
        print(req.json)
        print("HEADERS...")
        print(req.headers)
        print("RESPONSE...")
        print(req.text)

    def registration(self, ssl_path):
        #нужно передать самоподписной сертификат
        try:
            if not ssl_path:
                file = open(self.WEBHOOK_SSL_CERT,'rb')
            else:
                file = open(ssl_path,'rb')

        except:
            return 'Error File not Found'
        req = requests.post(f'https://api.telegram.org/bot{self.BOTTOKEN}/setWebhook',

                            json={'url':f'{self.WEBHOOK_URL}{self.WEBHOOK_PATH}:{self.WEBHOOK_PORT}',
                                'certificate':f'{file}'},
                            )
        print(f'Webhook registering on this adress: {self.WEBHOOK_URL}:{self.WEBHOOK_PORT}{self.WEBHOOK_PATH}')
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
