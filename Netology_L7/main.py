# Для проверки заданий 1 и 2 раскомментируйте строку 116 main() и запустите файл на исполнение :-)
# Task 1
import pprint, os.path


def get_my_recipes(file_name):
    cook_book = dict()
    try:
        with open(file_name) as file_with_recipes:
            for file_lines in file_with_recipes:
                key_name = file_lines.rstrip('\n')
                number_of_items = int(file_with_recipes.readline())
                elements_list = []
                for item in range(number_of_items):
                    elements = file_with_recipes.readline().split(' | ')
                    components = {
                        'ingredient_name': elements[0].strip(),
                        'quantity': int(elements[1]),
                        'measure': elements[2].strip()
                    }
                    elements_list.append(components)
                cook_book[key_name] = elements_list
                file_with_recipes.readline()
        return (cook_book)

    except FileNotFoundError:
        return (f'Файл с рецептами "{file_name}" не существует')
    except:
        return (f'Ошибка форматирования файла книги рецептов "{file_name}"')


def get_dishes_only(recipes):
    my_cook_book = get_my_recipes(recipes)
    print('Список блюд в книге рецептов', '\n')
    for item in my_cook_book.keys():
        print(item)
    print()


# Task 2
def get_shop_list_by_dishes(dishes, person_count, recipes):
    my_cook_book = get_my_recipes(recipes)
    shop_list = dict()
    dish_list = dishes.split()
    for dish_number in range(len(dish_list)):
        if dish_list[dish_number] not in my_cook_book.keys():
            return (
                f"Блюда '{dish_list[dish_number]}' в книге рецептов нет. Введите блюдо из текущей книги рецептов '{recipes}'")
        else:
            for elem in my_cook_book[dish_list[dish_number]]:
                elements_list = dict()
                elements_list['quantity'] = int(elem['quantity']) * int(person_count)
                elements_list['measure'] = elem['measure'].strip()
                # Проверка, нет ли уже таких же ингредиентов в списке покупок.
                # Если да, то просто прибавляем количество ингредиента к уже имеющемуся в списке
                if elem['ingredient_name'] in shop_list.keys():
                    shop_list[elem["ingredient_name"]]["quantity"] += elements_list['quantity']
                else:
                    shop_list[elem['ingredient_name']] = elements_list

    return (shop_list)


# Вызов функций вывода рецепта и списка покупок, если нужно вызвать их по отдельности
# print(get_my_recipes('recipes.txt'))
# print()
# pprint.pformat(get_shop_list_by_dishes('Утка по-пекински', 3,
#                                          'recipes.txt')))


def main():
    cook_book = 'recipes.txt'
    while True:
        print(
            'Просмотр книги рецептов, выбор блюд и числа персон для списка покупок')
        print('По умолчанию книга рецептов - файл receipts.txt')
        print('Список команд - h/?/help')
        user_input = input('Введите команду: ')
        print()
        if user_input == 'd':
            print(f'Текущий файл рецептов: {cook_book}')
            get_dishes_only(cook_book)
        if user_input == 'r':
            print(f'Текущий файл рецептов: {cook_book}')
            pprint.pprint(get_my_recipes(cook_book))
        elif user_input == 'f':
            cook_book = input('Имя файла новой книги рецептов: ')
            if os.path.exists(cook_book):
                print(f'Новая книга рецептов - файл {cook_book}')
            else:
                print(f'Файл {cook_book} не существует')
                cook_book = 'recipes.txt'

        elif user_input == 's':
            dish_name = input('Введите блюдо для списка покупок (через пробел): ')
            person_number = input('Введите число персон: ')
            print()
            # print(dish_name, person_number)
            print('Ваш список покупок\n')
            pprint.pprint(get_shop_list_by_dishes(dish_name, person_number, cook_book))
            print()

        elif user_input == 'h' or user_input == '?' or user_input == 'help':
            print('Список команд',
                  'd - вывести только названия блюд из книги рецептов',
                  'f - задать новую книгу с рецептами',
                  'r - вывести всю книгу рецептов',
                  's - задать блюдо и количество персон, вывести список для покупок',
                  'q - завершить программу',
                  'h/?/help - данная справка',
                  sep='\n',
                  end='\n\n')
        elif user_input == 'q':
            print('До свидания!')
            break


# main()

# Task 3
# Для вызова функции чтения и записи отсортированного содержимого файлов раскомментируйте строку 162, file_sorter_main()

def file_content_sorter(path: str):
    files_in_path = os.listdir(path)

    # Проверяем, не пустая ли папка
    if (len(files_in_path)) == 0:
        return f'Папка {path} не содержит файлов'
    final_list = []
    final_dict = {}
    # Пробегаем по списку файлов
    for item in files_in_path:
        # Вытаскиваем файлы с расширением .txt; отрицательный срез последних 4 позиций файла имени с переворачиванием результата. Также исключаем файл final.txt, это имя для результирующего файла
        file_ext = (''.join(reversed(item[:-5:-1])))
        if file_ext == '.txt' and item != 'final.txt':
            # Читаем содержимое файла в словарь формата {длина_списка_строк : [имя файла, [список строк]]}
            # Также заполняем список final_list значениями длины списка строк
            with open(f'{path}/{item}', 'r') as read_file:
                file_content = read_file.readlines()
                content_size = len(file_content)
                final_dict[content_size] = [item, file_content]
                final_list.append(content_size)

    # обратная сортировка списка длин строк
    final_list.sort(reverse=True)
    # Пишем в файл final.txt - идем по списку длин списка строк, это значением соответствует ключу в словаре с данными, то есть именем файла и списком строк
    with open(f'{path}/final.txt', 'w') as final_file:
        for list_num in final_list:
            final_file.write(f'Файл: {final_dict[list_num][0]}\n')
            final_file.write(f'Число строк: {list_num}\n')
            final_file.writelines(final_dict[list_num][1])
            final_file.write('\n')
    return 'Файлы прочитаны и записаны в test_files/final.txt'


def file_sorter_main():
    print(
        'Путь к файлам вводите без символа / в конце. Либо нажмите Enter, чтобы оставить папку по умолчанию, "test_files"')
    file_path = input('Введите путь: ')
    print()
    if not file_path:
        file_path = 'test_files'
    print(file_content_sorter(file_path))

# file_sorter_main()