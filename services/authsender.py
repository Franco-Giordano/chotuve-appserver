import requests
import os

# TODO hace cualquier cosa!
class AuthSender():

    url = os.environ['CH_AUTHSV_URL']

    @classmethod
    def is_valid_token(cls, token):
        # r = requests.post(cls.url + '/video', data={'videoId': vid_id, 'url': fb_url})

        return True

    @classmethod
    def get_uuid_from_token(cls, token):
        #

        return int(token)

    @classmethod
    def get_user_info(cls, user_id):
        pass

    @classmethod
    def register_user(cls, fullname, email, method):
        
        # r = requests.post(...)

        return {'message': 'User created'}, 201