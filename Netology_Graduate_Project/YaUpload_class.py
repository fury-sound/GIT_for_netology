import requests
import os.path
from requests import HTTPError, RequestException
from tqdm import tqdm

HTTP_STATUS_OK: int = 200
HTTP_STATUS_CREATE: int = 201
HTTP_STATUS_EXISTING: int = 409


class YaUpload:

    URL_UPLOAD_LINK: str = 'https://cloud-api.yandex.ru/v1/disk/resources/upload'
    URL_FOLDER_CREATE: str = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token: str):
        self.token = token
        self.header = {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def hello_func(self):
        print('Yandex Uploader is here\n')

    def _get_upload_link(self, ya_disk_path: str):
        params = {'path': ya_disk_path, 'overwrite': 'true'}
        try:
            response = requests.get(self.URL_UPLOAD_LINK,
                                    headers=self.header,
                                    params=params)
        except RequestException as req_err:
            print(f'Ошибка соединения {req_err}')
        except HTTPError as http_err:
            print(f'Ошибка HTTP: {http_err}')
        except Exception as err:
            print(f'Неизвестная ошибка: {err}')
        return (response.status_code, response)

    def folder_create(self, file_path):
        params = {'path': f'{file_path}'}
        try:
            response = requests.put(self.URL_FOLDER_CREATE, headers=self.header,
                                    params=params)
        except RequestException as req_err:
            print('Ошибка соединения {req_err}')
        except HTTPError as http_err:
            print(f'Ошибка HTTP: {http_err}')
        except Exception as err:
            print(f'Неизвестная ошибка: {err}')
        return response.status_code

    def upload(self, file_path_local: str, file_path_remote: str, file_list: list):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        print('Готов загружать файл/файлы', end='\n\n')
        folder_exists = False
        success_file_list = []
        if len(os.listdir(file_path_remote)) == 0:
            return f'Пустая папка {file_path_remote}, скачивать нечего\n\n'
        else:
            for file_name in tqdm(file_list, ncols=60, desc='Закачано'):
                # print('1', file_name)
                if not os.path.isfile(f'{file_path_local}/{file_name}'):
                    tqdm.write(f"\nФайл {file_path_local}/{file_name} не существует")
                else:
                    if file_path_remote != '.':
                        if not folder_exists:
                            resp_folder = self.folder_create(file_path_remote)
                            folder_exists = True
                            if resp_folder == HTTP_STATUS_CREATE:
                                output_line = f'\nПапка {file_path_remote} на Яндекс диске создана'
                            elif resp_folder == HTTP_STATUS_EXISTING:
                                output_line = f'\nПапка {file_path_remote} на Яндекс диске уже есть'
                            else:
                                return f'\nОшибка при создании папки {file_path_remote} на Яндекс диске'
                        full_path = f'{file_path_remote}/{file_name}'
                    else:
                        full_path = f'{file_name}'

                    # a= b/0
                    upload_link = self._get_upload_link(full_path)

                    if upload_link[0] == HTTP_STATUS_OK:
                        upload_url = upload_link[1].json().get('href')

                        with open(f'{file_path_local}/{file_name}', 'rb') as file_2_upload:
                            response = requests.put(upload_url, data=file_2_upload)
                        if response.status_code == HTTP_STATUS_CREATE:
                            success_file_list.append(f"{file_name}")
                        else:
                            tqdm.write(f'\nПроблема с загрузкой файла, получен код: {response.status_code}')
                        tqdm.write(f'\nПроблема с получением URL файла, получен код: {upload_link[0]}')
            print(output_line)
            return f"\nУспешно загружены файлы {success_file_list}. Функция загрузки отработала\n\n"  # response.status_code

