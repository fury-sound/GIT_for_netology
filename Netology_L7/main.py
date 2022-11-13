# Для проверки заданий 1 и 2 раскомментируйте строку 112 main() и запустите файл на исполнение :-) По заданию 3 - для
# вызова функции чтения и записи отсортированного содержимого файлов раскомментируйте строку 161, file_content_sorter()

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
        return cook_book

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
    print(len(dish_list))
    for dish_number in range(len(dish_list)):
        if dish_list[dish_number] not in my_cook_book.keys():
            return (
                f"Блюда '{dish_list[dish_number]}' в книге рецептов нет. Введите блюда из текущей книги рецептов '{recipes}'")
        else:
            for elem in my_cook_book[dish_list[dish_number]]:
                elements_list = dict()
                elements_list['quantity'] = int(elem['quantity']) * int(person_count)
                elements_list['measure'] = elem['measure'].strip()
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
            if os.path.exists(cook_book):  # True
                print(f'Новая книга рецептов - файл {cook_book}')
            else:
                print(f'Файл {cook_book} не существует')
                cook_book = 'recipes.txt'

        elif user_input == 's':
            dish_name = input('Введите блюдо для списка покупок: ')
            person_number = input('Введите число персон: ')
            print(dish_name, person_number)
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
# Для вызова функции чтения и записи отсортированного содержимого файлов раскомментируйте строку 161, file_content_sorter()
def file_content_sorter():
    try:
        # Считываем содержимое 3 файлов
        file_1 = open('test_files/file_1.txt')
        file_2 = open('test_files/file_2.txt')
        file_3 = open('test_files/file_3.txt')
        # Записываем в три списка
        list_1 = file_1.readlines()
        list_2 = file_2.readlines()
        list_3 = file_3.readlines()
        # Определяем длину списка
        list_1_size = len(list_1)
        list_2_size = len(list_2)
        list_3_size = len(list_3)
        # Список для сортировки имени и содержимого файлов по числу строк
        # Далее по этому списку в цикле записываем содержимое в конечный файл
        sorted_list = []
        if list_1_size > list_2_size:
            sorted_list.insert(0, ['file_1.txt', list_1])
            sorted_list.insert(1, ['file_2.txt', list_2])
        else:
            sorted_list.insert(1, ['file_1.txt', list_1])
            sorted_list.insert(0, ['file_2.txt', list_2])
        if (list_3_size > list_1_size) and (list_3_size > list_2_size):
            sorted_list.insert(0, ['file_3.txt', list_3])
        elif list_3_size < list_1_size and list_3_size < list_2_size:
            sorted_list.append(['file_3.txt', list_3])
        else:
            sorted_list.insert(1, ['file_3.txt', list_3])

        with open('test_files/final.txt', 'w') as final_file:
            for item in range(len(sorted_list)):
                final_file.write(f'Файл: {sorted_list[item][0]}\n')
                final_file.write(f'Число строк: {len(sorted_list[item][1])}\n')
                final_file.writelines(sorted_list[item][1])
                final_file.write('\n')
        return 'Файлы прочитаны и записаны в test_files/final.txt'

    except FileNotFoundError:
        return ('Файл не найден')
    except:
        return 'Ой. Какая-то ошибка'
    finally:
        file_1.close()
        file_2.close()
        file_3.close()

print(file_content_sorter())

