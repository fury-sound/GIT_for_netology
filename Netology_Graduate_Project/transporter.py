import json

class Transporter:

    def __init__(self, number_of_photos):
        self.number_of_photos = number_of_photos

    def select_vk_images(self, vk_response: dict):
        item_range = len(vk_response['response']['items'])
        stored_photos = {}
        list_4_json = []
        photo_size_dict = {}
        print(self.number_of_photos)
        if item_range < self.number_of_photos:
            self.number_of_photos = item_range
        print('Общее число изображений в альбоме:', item_range)
        print('Скачиваем изображения наибольшего размера для указанного числа фотографий: ',
              self.number_of_photos, end='\n\n')

        for item_4_range in range(self.number_of_photos):
            likes_count = vk_response['response']['items'][item_4_range]['likes'][
                'count']
            photo_name = f'photo_{likes_count}.jpg'
            if photo_name in stored_photos.keys():
                photo_date = vk_response['response']['items'][item_4_range]['date']
                photo_name = f'photo_{likes_count}_{photo_date}.jpg'
            stored_photos[photo_name] = 'url'
            size_range = len(vk_response['response']['items'][item_4_range]['sizes'])
            size_char_list = []

            for item_4_sizes in range(size_range):
                size_var_char = vk_response['response']['items'][item_4_range]['sizes'][
                    item_4_sizes]['type']
                size_char_list.append((size_var_char, item_4_sizes))
            sorted(size_char_list)
            photo_url = vk_response['response']['items'][item_4_range]['sizes'][
                size_char_list[-1][1]]['url']
            photo_size = vk_response['response']['items'][item_4_range]['sizes'][
                size_char_list[-1][1]]['type']
            stored_photos[photo_name] = photo_url
            photo_size_dict = {'file_name' : photo_name, 'size' : photo_size}
            list_4_json.append(photo_size_dict)

        print(store_file_data_json(list_4_json))
        return stored_photos

def store_file_data_json(json_list):
    json_string = json.dumps(json_list, indent=4)
    try:
        with open("data.json", "w") as jsonFile:
            jsonFile.write(json_string)
        return 'Файл JSON успешно сохранен'
    except Exception as err:
        return f'Ошибка создания файла JSON, код {err}'

