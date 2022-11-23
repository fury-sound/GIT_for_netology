import requests
from requests import HTTPError
import requests.exceptions

HTTP_STATUS_CREATE: int = 201


class VK:

  def __init__(self, access_token, user_id, version='5.131'):
    self.token = access_token
    self.id = user_id
    self.version = version
    self.params = {'access_token': self.token, 'v': self.version}

  def get_user_id(self, test_id):
    url = 'https://api.vk.com/method/users.search'
    params = {'q': test_id, 'fields': 'blacklisted, is_friend, deactivated'}
    try:
      response = requests.get(url, params={**self.params, **params})
    except requests.RequestException as req_err:
      print(f'Ошибка соединения {req_err}')
    except HTTPError as http_err:
      print(f'Ошибка HTTP: {http_err}')
    except Exception as err:
      print(f'Неизвестная ошибка: {err}')
    return (response.status_code, response)

  def get_photos_url(self, album_name):
    url = 'https://api.vk.com/method/photos.get'
    params = {
      'owner_id': self.id,
      'album_id': album_name,
      'extended': 1,
      'photo_sizes': 1
    }
    try:
      response = requests.get(url, params={**self.params, **params})
    except requests.RequestException as req_err:
      print('Ошибка получения URL альбома {req_err}')
    except HTTPError as http_err:
      print(f'Ошибка HTTP: {http_err}')
    except Exception as err:
      print(f'Неизвестная ошибка: {err}')

    return (response.status_code, response)


  def file_download(self, file_url, image_path, image_name):
    try:
      send = requests.get(file_url)  #делаем запрос
    except requests.RequestException as req_err:
      print('Ошибка получения URL альбома {req_err}')
    except HTTPError as http_err:
      print(f'Ошибка HTTP: {http_err}')
    except Exception as err:
      print(f'Неизвестная ошибка: {err}')
    try:
      with open(f'{image_path}/{image_name}', 'wb') as new_file:
        new_file.write(send.content)  #записываем результат
    except Exception as err:
      print(f'Ошибка сохранения файла: {err}')
