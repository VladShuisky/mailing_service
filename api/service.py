import json
from datetime import datetime, timedelta

from vk_api import VkApi
from vk_api import exceptions as vk_exceptions

from settings import TOKENS, USER_IDS
from my_responses import response_detail

from api.db_manager import VkManagerObjects, VkUserObjects, VkCityObjects, save_objects


class vkApiAccount():
    def __init__(self, token:str, users_ids:list=[]) -> None:
        self.token = token
        self.addfriends_limit_reached = False
        self.users_ids = users_ids
        self.api = self.get_api()
        self.id = self.get_info()

    def get_info(self):
        return self.api.account.getProfileInfo().get('id', None)

    def get_api(self):
        try:
            api = VkApi(token=self.token).get_api()
            healthcheck = api.account.getInfo()
            return api
        except vk_exceptions.ApiError as e:
            return response_detail(e)
        
    def friendship_request(self, user_id:str, message:str=None) -> dict:
        '''Возвращает результат одного запроса в виде словаря, содержащим ключи message, code и status'''
        '''НО'''
        try:
            response_code = self.api.friends.add(
                user_id=user_id
            )
            result = response_code
        except vk_exceptions.ApiError as error:
            result = error.get('error_code'),
            if result==29:
                self.limit_reached = True
        finally:
            return result


class VkFriendingService():
    '''main class for mailing requests of friendship'''
    def __init__(self) -> None:
        pass

    @property
    def blank_users(self):
    # возвращает список пользователей из бд, у которых пустое поле manager_id
    # следовательно, они не взаимодействовали с менеджером
        blank_users = VkUserObjects.filter(manager_id=None)
        return blank_users


    @property
    def active_managers(self):
    # Возвращает список менеджеров из бд, у которых есть дневная квота на сегодня
    # т.е. день последней активности != сегодняшний день
        managers = VkManagerObjects.get_all()
        return list(filter(lambda m: m.last_activity.day != datetime.now().day), managers)

    @property
    def accounts(self):
        'return list of VkApiAccounts'
        return [vkApiAccount(acc.token) for acc in self.active_managers]

    def bulk_friends_request(self) -> dict:
        '''return dict like a {1232213: 1, 12124121: 1}(id: result-code)'''
        res_dict = {} 
        for account in self.accounts:
            while not account.addfriends_limit_reached:
                try:
                    current_user = self.blank_users[0]
                    response_code = account.friendship_request(
                        user_id=current_user.vk_id)
                    if response_code != 29:
                        current_user.status = response_code
                        save_objects(current_user)
                        res_dict[current_user.id] = response_code
                        self.blank_users.pop(0)
                except IndexError:
                    print('All users ids was processed,'
                          'bulk_friends_requests done')
                    return res_dict
        return {**res_dict, **dict.fromkeys([self.blank_users], None)}






