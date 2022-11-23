# Graduate Task

import os, os.path, requests, time
from requests import HTTPError
from tqdm import tqdm
# import alive_progress
# import google-api-python-client

from VK_class import VK
from YaUpload_class import YaUpload
from transporter import Transporter

from VK_token import TOKEN, USER_ID
from Ya_token import YA_TOKEN

# комментированный блок импортов для работы с Гугл-диском. Дальше есть еще блоки, относящиеся к этому.
# не успел закончить :-(
# from GD_class import GD_Uploader
# from GD_token import GD_TOKEN
# from google.oauth2 import service_account
# from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
# from googleapiclient.discovery import build
# import io

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'GD_token.json'

HTTP_STATUS_CREATE: int = 201

# credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# service = build('drive', 'v3', credentials=credentials)

# results = service.files().list(pageSize=10,
#                                fields="nextPageToken, files(id, name, mimeType)").execute()
# pprint(results)
# print('\n\n##############################\n\n')



def set_user_id(user_id_actual, vk_inst):
  print(f'Текущий VK ID = {user_id_actual}')
  print('Введите ID или имя профиля ВК.')
  print('Либо нажмите Ввод, чтобы не менять текущий профиль.')
  temp_id = input('Введите VK ID: ')
  if temp_id:
    if temp_id != user_id_actual:
      response = vk_inst.get_user_id(temp_id)
      response_user_params = response[1].json()
      if 'error' in response_user_params.keys():
        return (
          f"Ошибка ВК, код {response_user_params['error']['error_code']}", 0)

      if not (len(response_user_params['response']['items']) == 1):
        return (
          'Ошибка ID. Возможно, профиль деактивирован или забанен. Будет использован текущий ID',
          0)
      if 'blacklisted' in response_user_params['response']['items'][0].keys() \
              and response_user_params['response']['items'][0]['blacklisted'] == 1:
        return (
          f'Вы в черном списке у профиля {temp_id}. Просмотр альбомов невозможен.', 0)
      if (
        (f"{response_user_params['response']['items'][0]['is_closed']}") and
        (not f"{response_user_params['response']['items'][0]['is_friend']}")):
        return ('Профиль закрыт. Просмотр альбомов невозможен.', 0)
      elif ((f"{response_user_params['response']['items'][0]['is_closed']}")
            and
            (f"{response_user_params['response']['items'][0]['is_friend']}")):
        print(
          'Профиль закрыт. Но вы в друзьях. Можно попробовать посмотреть, что доступно из альбомов.'
        )
        user_id_actual = f"{response_user_params['response']['items'][0]['id']}"
  return (user_id_actual, 1)


def set_number_of_photos(number_of_photos_actual):
  print(f'Текущее к-во фото для скачивания: {number_of_photos_actual}')
  print('Введите нужное число.')
  print('Либо нажмите Ввод, чтобы не менять текущее значение.')
  print(
    'Если актуальное число превышает к-во изображений в альбоме, то скачаются все имеющиеся.'
  )
  temp_num = input('Введите число: ')
  if temp_num:
    if temp_num.isdigit():
      number_of_photos_actual = int(temp_num)
    else:
      print('Введено не целое число')
      print('Будет использовано текущее значение')
  return number_of_photos_actual


def set_vk_album(album_name_actual):
  print(f'Текущий альбом в ВК: {album_name_actual}')
  print('Введите нужное имя альбома.')
  print('Либо нажмите Ввод, чтобы не менять текущее значение.')
  print(
    'Служебные имена альбомов, доступные в большинстве открытых профилей: profile и wall.'
  )
  print('Альбом saved часто заблокирован.')
  print(
    'На данном этапе корректность имени и доступность альбома не проверяются.')
  print(
    'Если имя альбома введено неправильно, альбом или профиль закрыты, то вы получите ошибку на этапе скачивания.',
    end='\n\n')
  temp_name = input('Введите имя альбома: ')
  if temp_name:
    album_name_actual = temp_name
  return album_name_actual


def set_local_download_folder(image_path_local_actual):
  print(
    f'Текущее имя локальной папки для скачивания: {image_path_local_actual}')
  print('Папка расположена в каталоге программы')
  print(
    'Введите нужное имя либо нажмите Ввод, чтобы не менять текущее значение.')
  print('Если такой папки не существует, то она будет создана.')
  print(
    'Если имя или путь к папке введены некорректно, то текущее имя не изменится.'
  )
  temp_local_folder = input('Введите имя папки: ')
  if temp_local_folder:
    if not os.path.isdir(temp_local_folder):
      try:
        os.mkdir(temp_local_folder)
      except Exception as err:
        print(f'Ошибка при создании папки: {err}')
        print('Папка для скачивания не изменилась')
        return image_path_local_actual
      else:
        print(f'Папка {temp_local_folder} создана')
        return temp_local_folder
  else:
    # print('Папка ', image_path_local_actual, os.path.isdir(image_path_local_actual))
    if not os.path.isdir(image_path_local_actual):
      try:
        os.mkdir(image_path_local_actual)
      except Exception as err:
        print(f'Ошибка при создании папки: {err}')
        print('Папка для скачивания не изменилась')
        return image_path_local_actual
      else:
        print(f'Папка {image_path_local_actual} создана')
    return image_path_local_actual



def set_yandex_folder(ya_inst, image_path_remote_actual):
  print('Задайте имя папки на Яндекс-диске')
  print(
    'Если имя папки на Яндекс-диске некорректны, то для загрузки файлов будет использована папка по умолчанию'
  )
  print('Папка по умолчанию: ', image_path_remote_actual)
  print('Введите имя папки либо нажмите Ввод, чтобы не менять текущее значение.')
  new_folder = input('Введите имя папки: ')
  # print(new_folder)
  if (not new_folder) or (new_folder == image_path_remote_actual):
    print('Имя папки не изменилось')
    return image_path_remote_actual
  else:
    res = ya_inst.folder_create(new_folder)
    if res == 200 or res == 201:
      print(f'Папка {new_folder} успешно создана, код {res}')
      return new_folder
    else:
      print(f'Ошибка создания новой папки {new_folder}, код {res}.')
      return image_path_remote_actual


def file_local_download(vk_inst, transporter_inst, image_path_local_actual,
                        album_name_actual, number_of_photos_actual):

  print('Подготовка к скачиванию файлов', end='\n\n')

  try:
    response = vk_inst.get_photos_url(album_name_actual)
  except HTTPError as http_err:
    return f'Ошибка HTTP при получении URL: {http_err}'
  except Exception as err:
    return f'Неизвестная ошибка при получении URL: {err}'
  else:
    print("URL получен!")
    if 'error' in response[1].json().keys():
      err = response[1].json()
      if (err['error']['error_code']) == 200:
        return f'Доступ к альбому профиля {vk_inst.id} запрещен'
      else:
        return f"Ошибка ВК, код {err['error']['error_code']}"

  photos_dict = transporter_inst.select_vk_images(response[1].json())
  if not os.path.isdir(image_path_local_actual):
    try:
      os.mkdir(image_path_local_actual)
    except Exception as err:
      print(f'Ошибка при создании папки: {err}')
      print('Папка для скачивания не изменилась')
      return image_path_local_actual
    else:
      print(f'Папка {image_path_local_actual} создана')
  print('Скачиваем\n')

  # for i in tqdm(range(transporter_inst.number_of_photos)): # прогресс-бар от tqdm
  # with alive_bar(number_of_photos) as bar: # прогресс-бар от progress-alive 1
  # for i in range(number_of_photos): # прогресс-бар от progress-alive 2
  # for item in photos_dict:
  for item in tqdm(photos_dict, ncols=60, desc='Скачалось'):
    photo_name = item
    photo_url = photos_dict[item]
    try:
      vk_inst.file_download(photo_url, image_path_local_actual, photo_name)
    except HTTPError as http_err:
      return f'Ошибка HTTP: {http_err}'
    except OSError as os_err:
      return f'Локальная ошибка ОС: {os_err}'
    except Exception as err:
      return f'Неизвестная ошибка: {err}'
      # else:
      #   tqdm.write(f"\nСкачивание {photo_name} завершено")
      # bar()
  return '\nСкачивание изображений в локальную папку завершено'


def file_yandex_upload(ya_inst, image_path_local_actual,
                       image_path_remote_actual):
  print(f'Папка с загружаемыми файлами: {image_path_local_actual}', end='\n\n')
  print('Введите имена загружаемого файла или файлов (через пробел)')
  print('Или нажмите Enter. Тогда буду загружены все файлы jpg из папки.')
  file_list = input('Введите имя файла/файлов: ')

  # Проверяем: если список файлов пустой, то читаем все файлы в папке,
  # выбираем файлы с расширением .jpg и добавляем их в строку file_list
  if not file_list:
    all_item_list = os.listdir(image_path_local_actual)
    for item in all_item_list:
      # Вытаскиваем файлы с расширением .jpg; отрицательный срез последних 4 позиций файла имени с переворачиванием результата.
      file_ext = (''.join(reversed(item[:-5:-1])))
      if file_ext == '.jpg':
        file_list += ' ' + item


# Конвертируем строку в список
  file_list = file_list.split()
  return ya_inst.upload(image_path_local_actual, image_path_remote_actual,
                        file_list)


def main():
  user_id_vk = USER_ID
  access_token_vk = TOKEN
  access_token_ya = YA_TOKEN
  # access_token_gd = '111'  #GD_TOKEN
  album_name = 'profile'
  number_of_photos = 5
  image_path_local = 'Images'
  image_path_remote = 'Images'
  vk = VK(access_token_vk, user_id_vk)
  ya = YaUpload(access_token_ya)
  transporter = Transporter(number_of_photos)

  print('Утилита скачивания фотографий из профиля ВК', end='\n\n')
  print(("#" * 50), end='\n\n')
  print()
  while True:
    user_input = input('Введите команду: ')
    print()
    if user_input == 'v':
      set_user_res = set_user_id(user_id_vk, vk)
      if set_user_res[1] == 0:
        print(set_user_res[0])
        vk.id = user_id_vk
      else:
        user_id_vk = vk.id = set_user_res[0]
        print('Текущий VK ID: ', vk.id, end='\n\n')
    elif user_input == 'a':
      album_name = set_vk_album(album_name)
      print('Текущее имя альбома ВК: ', album_name, end='\n\n')
    elif user_input == 'n':
      transporter.number_of_photos = set_number_of_photos(number_of_photos)
      print('К-во фотографий для скачивания: ', transporter.number_of_photos, end='\n\n')
    elif user_input == 'lf':
      image_path_local = set_local_download_folder(image_path_local)
      print('Имя папки для скачивания фотографий: ',
            image_path_local,
            end='\n\n')
    elif user_input == 'ld':
      print(file_local_download(vk, transporter, image_path_local, album_name,
                                number_of_photos),
            end='\n\n')
    elif user_input == 'yf':
      image_path_remote = set_yandex_folder(ya, image_path_remote)
      print('Текущая папка на Яндекс-диске: ', image_path_remote)
    elif user_input == 'y':
      print(file_yandex_upload(ya, image_path_local, image_path_remote))

    # elif user_input == 'gf':
    #   print(set_gd_folder())
    # elif user_input == 'g':
    #   print(file_gd_upload())

    elif user_input == 'h' or user_input == '?' or user_input == 'help':
      print('Список команд',
            'v - ввести/изменить VK ID',
            'a - ввести/изменить альбом в VK',
            'n - ввести/изменить к-о скачиваемых фото',
            'lf - ввести/изменить локальную папку для скачивания',
            'ld - скачать файлы на локальный диск',
            'yf - ввести/изменить папку на Яндекс диске',
            'y – закачать файлы на Яндекс диск',
            # 'gf - ввести/изменить папку на Гугл диске',
            # 'g – закачать файлы на Гугл диск',
            'h/?/help - данная справка',
            sep='\n',
            end='\n\n')
    elif user_input == 'q':
      print('До свидания!')
      break


main()
