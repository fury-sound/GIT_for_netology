# Lesson 8 - requests
import os.path, requests
from pprint import pprint


# Task 1

def find_smartest_hero():
    name_list = ['Hulk', 'Captain America', 'Thanos']
    smartest_hero = []
    url_all = 'https://akabab.github.io/superhero-api/api/all.json'
    json_response = requests.get(url_all)
    # счетчик количества обнаруженных имен, чтобы остановить просмотр списка, как только все имена найдены
    name_counter = len(name_list)
    # прерываем функцию, если список имен пустой
    if name_counter == 0:
        print('Список имен пустой')
        return
    # перебор всех элементов списка
    for element in json_response.json():
        # Нашли имя из списка - уменьшаем значение счетчика имен, если итоговый список пустой, записываем имя и интеллект героя, иначе сравниваем его со следующим найденным и заменяем, если новый умнее
        if element['name'] in name_list:
            name_counter -= 1
            if len(smartest_hero) == 0:
                smartest_hero.append(element['name'])
                smartest_hero.append(element['powerstats']['intelligence'])
            else:
                if smartest_hero[1] < element['powerstats']['intelligence']:
                    smartest_hero[0] = element['name']
                    smartest_hero[1] = element['powerstats']['intelligence']
            if name_counter == 0:
                # Список имен обнулился - больше искать нечего, печатаем имя победителя и прерываем цикл
                print('Список героев:', ', '.join(name_list))
                print('Самый умный:', smartest_hero[0])
                break


# Для запуска задания 1 раскомментировать main()
# find_smartest_hero()


# Task 2
from my_token import TOKEN

HTTP_STATUS_CREATE: int = 201


class YaUploader:
    URL_UPLOAD_LINK: str = 'https://cloud-api.yandex.ru/v1/disk/resources/upload'

    def __init__(self, token: str):
        self.token = token
        self.header = {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def _get_upload_link(self, ya_disk_path: str):
        params = {'path': ya_disk_path, 'overwrite': 'true'}
        response = requests.get(self.URL_UPLOAD_LINK,
                                headers=self.header,
                                params=params)
        upload_url = response.json().get('href')
        return upload_url

    def upload(self, file_path: str, file_list: list):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        print('Готов загружать файл/файлы', end='\n\n')
        for file_name in file_list:
            if not os.path.isfile(f'{file_path}/{file_name}'):
                print(f"Файл {file_path}/{file_name} не существует")
            else:
                print(f'Загружается файл: {file_path}/{file_name}', end='\n\n')
                upload_link = self._get_upload_link(file_name)

                with open(f'{file_path}/{file_name}', 'rb') as file_2_upload:
                    response = requests.put(upload_link, data=file_2_upload)
                if response.status_code == HTTP_STATUS_CREATE:
                    print(f'Загрузка "{file_name}" прошла успешно, получен код:',
                          response.status_code,
                          end='\n\n')
                else:
                    print('Проблема с загрузкой файла, получен код:',
                          response.status_code,
                          end='\n\n')
        return "Функция загрузки отработала"  # response.status_code


# if __name__ == '__main__':
def main():
    # Получить путь к загружаемому файлу и токен от пользователя
    my_path = "test_files"
    print('Введите путь к загружаемому файлу/файлам.')
    print('Или нажмите Enter, чтобы использовать путь по умолчанию')
    print('Текущая папка - символ "."')
    print('Текущий путь по умолчанию: ' + f'{my_path}')
    path_to_file = input('Введите путь к загружаемому файлу: ')

    # Проверка - если путь не пустой, но такого каталога не существует - выход
    # Иначе, если путь пустой, то присваиваем путь по умолчанию
    if path_to_file and not os.path.exists(path_to_file):
        print(f'"{path_to_file}" не является папкой')
        print('Выполнение прервано')
    else:
        if not path_to_file:
            path_to_file = my_path

        print(f'Путь к загружаемым файлам: {path_to_file}', end='\n\n')
        print('Введите имена загружаемого файла или файлов (через пробел)')
        print('Или нажмите Enter. Тогда буду загружены все файлы в папке.')
        file_list = input('Введите имя файла/файлов: ')

        # Проверяем: если список файлов пустой, то читаем все файлы в папке,
        # выбираем файлы с расширением .txt и добавляем их в строку file_list
        if not file_list:
            all_item_list = os.listdir(path_to_file)
            for item in all_item_list:
                # Вытаскиваем файлы с расширением .txt; отрицательный срез последних 4 позиций файла имени с переворачиванием результата. Также исключаем файл final.txt, это имя для результирующего файла
                file_ext = (''.join(reversed(item[:-5:-1])))
                if file_ext == '.txt':
                    file_list += ' ' + item
        # Конвертируем строку в список
        file_list = file_list.split()

        token = TOKEN
        uploader = YaUploader(token)
        # result = uploader.upload(path_to_file, file_list)
        print(uploader.upload(path_to_file, file_list))


# Для запуска задания 2 раскомментировать main()
# main()

################################################################

# Task 3

# Что получилось: скачивается ответ на запрос с тегом python, вроде как после даты в 14 ноября 2022 г. Вывожу в консоль ID вопроса, его тему и дату создания.
# Чтобы дополнительно отфильтровать запросы, поставил фильтр на упоминание Python или python в теме.
# Что не получилось: на stackoverflow стоит ограничение на количество отправляемых данных (по параметру pagesize - не более 100). Как я прочитал, это внутренее ограничение сайта и борьба с этим - весьма нетривиальная задача.

# Есть два варианта решения, scraping_stackoverflow_1() и scraping_stackoverflow_2(). В первом можно получить данные из выдачи, но не ясно, как получить всю выдачу для вычисления общего числа запросов.
# Во втором - получаю через фильтр total общее число запросов - это специально оставлено для подсчета статистики - но при этом никакие больше сведения не передаются.
# Так что я не понимаю, завершено ли задание или нет. Поэтому заранее извиняюсь, много букав и не удалил ненужные комментарии.


from datetime import datetime, date, timedelta

# BASEURL = "https://api.stackexchange.com/2.3/info"
QUESTION_URL = 'https://api.stackexchange.com/2.3/questions'


# "https://api.stackexchange.com/2.2/questions"
# 'https://api.stackexchange.com/2.3/questions?pagesize=5&filter=total&tagged=python&site=stackoverflow'
# 'http://api.stackexchange.com/docs/comments#order=desc&min=1&sort=votes&filter=total&site=stackoverflow&run=true'

def scraping_stackoverflow_1():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }

    current_date = date.today()
    search_fromdate = date.today() - timedelta(days=2)
    print('Текущая дата:', current_date)
    print('Дата начала подсчета числа запросов', search_fromdate)

    params = {
        "tagged": "python",
        "pagesize": 100,
        # "filter" : "creation_date",
        # "offset" : 1000,
        "tab": "newest",
        "fromdate": f"{search_fromdate}",
        # "fromdate" : 1668384000,
        "order": "desc",
        "site": "stackoverflow"
    }

    r = requests.get(QUESTION_URL, headers=headers, params=params)

    # pprint(r.json())
    # pprint(r.text)

    counter = 0
    for element in r.json()['items']:
        if ('python' or 'Python') in element['title']:
            counter += 1
            # print(element)
            ts = int(element['creation_date'])
            print('ID вопроса:', element['question_id'])
            print('Тема:', element['title'])
            print('Дата создания:', datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), end='\n\n')
    print(f"Число вопросов с тегом python от {search_fromdate} на stackoverflow:", counter)
    print('Ограничена выдача - не более 100 запросов на страницу')


def scraping_stackoverflow_2():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }

    current_date = date.today()
    search_fromdate = date.today() - timedelta(days=2)
    print('Текущая дата:', current_date)
    print('Дата начала подсчета числа запросов', search_fromdate)

    params = {
        "tagged": "python",
        "pagesize": 100,
        "filter": "total",
        # "offset" : 1000,
        "tab": "newest",
        "fromdate": f"{search_fromdate}",
        # "fromdate" : 1668384000,
        "order": "desc",
        "site": "stackoverflow"
    }

    r = requests.get(QUESTION_URL, headers=headers, params=params)

    print(f'Число вопросов с тегом python от {search_fromdate} на stackoverflow: {r.json()["total"]}')

# scraping_stackoverflow_1()
# scraping_stackoverflow_2()