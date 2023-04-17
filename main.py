import json

from settings import TOKEN, USER_IDS
from service import response_detail
from vk_api import VkApi
from vk_api import exceptions as vk_exceptions


class vkApiAccount():
    def __init__(self, token:str, users_ids:list=[]) -> None:
        self.token = token
        self.addfriends_limit_reached = False
        self.users_ids = users_ids
        self.api = self.get_api()

    def get_api(self):
        try:
            api = VkApi(token=self.token).get_api()
            healthcheck = api.account.getInfo()
            return api
        except vk_exceptions.ApiError as e:
            return response_detail(e)
        
    def friendship_request(self, user_id:str, message:str=None) -> dict:
        '''Возвращает результат одного запроса в виде словаря, содержащим ключи message, code и status'''
        try:
            response_code = self.api.friends.add(
                user_id=user_id
            )
            result = response_detail(response_code)
        except vk_exceptions.ApiError as error:
            result = response_detail(error)
            if result['error_code']==29:
                self.limit_reached = True
        except Exception as e:
            result = response_detail(e)
        finally:
            return result


class VkApiFriendsRequestMailing():
    '''main class for mailing requests of friendship'''
    def __init__(self, users_ids: list, accounts_tokens: list) -> None:
        self.users_ids = users_ids
        self.accounts_tokens = accounts_tokens

    @property
    def accounts(self):
        'return list of VkApiAccounts'
        return [vkApiAccount(token) for token in self.accounts_tokens]

    def bulk_friends_request(self) -> dict:
        res_dict = {} 
        for account in self.accounts:
            while not account.addfriends_limit_reached:
                try:
                    id = self.users_ids.pop(0)
                    friend = account.friendship_request(
                        user_id=id)
                    res_dict[id] = (friend['response_msg'] 
                                    if friend['response_msg'] 
                                    else friend['response_status'])
                except IndexError:
                    print('All users ids was processed,'
                          'bulk_friends_requests done')
                    return res_dict

        return {**res_dict, **dict.fromkeys(self.users_ids, None)}


mailing = VkApiFriendsRequestMailing(
    users_ids=USER_IDS,
    accounts_tokens=[TOKEN]
)
bulk_request = mailing.bulk_friends_request()
with open('file_json.json', 'w') as json_file:
    json_file.write(json.dumps(bulk_request))



