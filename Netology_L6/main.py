"""Нетология - д/з по ООП - Урок 6"""


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def set_lecturer_rate(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and (
                course in self.courses_in_progress or course in self.finished_courses):
            # проверка на наличие имени курса как ключа в словаре.
            # Закомментированные строки в методе позволяют следить, кому из лекторов какие давались оценки
            # и за какой курс
            if course not in lecturer.grades_for_lecturer.keys():
                # print(f'{course} not in the list. Adding.')
                lecturer.grades_for_lecturer[course] = [grade]
                # print('Added new grade to Lecturer dictionary of lists')
            else:
                # print('Adding another grade to Lecturer dictionary of lists')
                my_list = list(lecturer.grades_for_lecturer[course])
                my_list.append(grade)
                lecturer.grades_for_lecturer[course] = my_list

            # можно отследить, какому лектору за какой курс какая был присвоена оценка
            # print('Лектор, курс и новая оценка:', lecturer.name + " " + lecturer.surname, course, grade)
        else:
            print(
                f'Ошибка. Не существует лектор {lecturer.name + " " + lecturer.surname}, либо у лектора нет этого '
                f'языка ({course}), либо некорретно введена оценка ({grade})')


    def mean_grade(self, student_grades):
        temp_list = []
        for my_key in student_grades.keys():
            temp_list += student_grades.get(my_key)
        if len(temp_list) == 0:
            return 'Оценок нет'
        else:
            return str(round(sum(temp_list) / len(temp_list), 1))

    def __eq__(self, other):
        if self.mean_grade(self.grades) == 'Оценок нет' or other.mean_grade(other.grades) == 'Оценок нет':
            return 'Сравнение невозможно'
        else:
            return self.mean_grade(self.grades) == other.mean_grade(other.grades)

    def __gt__(self, other):
        if self.mean_grade(self.grades) == 'Оценок нет' or other.mean_grade(other.grades) == 'Оценок нет':
            return 'Сравнение невозможно'
        else:
            return self.mean_grade(self.grades) > other.mean_grade(other.grades)

    def __lt__(self, other):
        if self.mean_grade(self.grades) == 'Оценок нет' or other.mean_grade(other.grades) == 'Оценок нет':
            return 'Сравнение невозможно'
        else:
            return self.mean_grade(self.grades) < other.mean_grade(other.grades)

    def __str__(self):
        name = f'Имя: {self.name} \n'
        surname = f'Фамилия: {self.surname}\n'
        mean_hw_grade = f'Средняя оценка за д.з.: {self.mean_grade(self.grades)}\n'
        studied_courses = f'Курсы в процессе изучения: {str(self.courses_in_progress).strip("[]")}\n'
        finished_courses = f'Законченные курсы: {str(self.finished_courses).strip("[]")}\n'
        return 'Студент\n' + name + surname + mean_hw_grade + studied_courses + finished_courses


class Mentor:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades_for_lecturer = dict()

    def lecturer_rate(self, course):
        return self.grades_for_lecturer[course]

    def mean_grade(self, lecturer_grades):
        temp_list = []
        for my_key in lecturer_grades.keys():
            temp_list += lecturer_grades.get(my_key)
        if len(temp_list) == 0:
            return 'Оценок нет'
        else:
            return str(round(sum(temp_list) / len(temp_list), 1))

    def __eq__(self, other):
        if self.mean_grade(self.grades_for_lecturer) == 'Оценок нет' or other.mean_grade(
                other.grades_for_lecturer) == 'Оценок нет':
            return 'Сравнение невозможно'
        else:
            return self.mean_grade(self.grades_for_lecturer) == other.mean_grade(other.grades_for_lecturer)

    def __gt__(self, other):
        if self.mean_grade(self.grades_for_lecturer) == 'Оценок нет' or other.mean_grade(
                other.grades_for_lecturer) == 'Оценок нет':
            return 'Сравнение невозможно'
        else:
            return self.mean_grade(self.grades_for_lecturer) > other.mean_grade(other.grades_for_lecturer)

    def __lt__(self, other):
        if self.mean_grade(self.grades_for_lecturer) == 'Оценок нет' or other.mean_grade(
                other.grades_for_lecturer) == 'Оценок нет':
            return 'Сравнение невозможно'
        else:
            return self.mean_grade(self.grades_for_lecturer) < other.mean_grade(other.grades_for_lecturer)

    def __str__(self):
        name = f'Имя: {self.name} \n'
        surname = f'Фамилия: {self.surname}\n'
        mean_grade = f'Средняя оценка за лекции: {self.mean_grade(self.grades_for_lecturer)}\n'
        return 'Лектор\n' + name + surname + mean_grade


class Reviewer(Mentor):

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and (
                course in student.courses_in_progress or course in student.finished_courses):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        name = f'Имя: {self.name} \n'
        surname = f'Фамилия: {self.surname}\n'
        return 'Проверяющий\n' + name + surname


# Классы студентов - best_student и best_student1

best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']
best_student1 = Student('Ben', 'Roy', 'your_gender')
best_student1.courses_in_progress += ['Python']
best_student.finished_courses += ['Java']

# Классы проверяющих экспертов - cool_reviewer и cool_reviewer1
# Сразу выставляем оценки студентам по предметам

cool_reviewer = Reviewer('Some', 'Buddy')
cool_reviewer.courses_attached += ['Python']

cool_reviewer.rate_hw(best_student, 'Python', 10)
cool_reviewer.rate_hw(best_student, 'Python', 10)
cool_reviewer.rate_hw(best_student, 'Python', 10)

cool_reviewer.rate_hw(best_student1, 'Python', 10)
cool_reviewer.rate_hw(best_student1, 'Python', 7)
cool_reviewer.rate_hw(best_student1, 'Python', 8)

cool_reviewer1 = Reviewer('Another', 'Buddy')
cool_reviewer1.courses_attached += ['Java']

cool_reviewer1.rate_hw(best_student, 'Java', 10)
cool_reviewer1.rate_hw(best_student, 'Java', 10)
cool_reviewer1.rate_hw(best_student, 'Java', 10)

cool_reviewer1.rate_hw(best_student1, 'Java', 10)
cool_reviewer1.rate_hw(best_student1, 'Java', 7)
cool_reviewer1.rate_hw(best_student1, 'Java', 8)

# Классы лекторов - code_expert и code_expert1

code_expert = Lecturer('Ivan', 'Ivanov')
code_expert.courses_attached += ['Python']
code_expert.courses_attached += ['Java']

code_expert1 = Lecturer('Peter', 'Petrov')
code_expert1.courses_attached += ['Python']
code_expert1.courses_attached += ['Java']

# можно посмотреть на срабатывание ошибки, если вместо Питона (закомментировать строки 200 и 201) поставить лектору С++
# code_expert1.courses_attached += ['C++']
# print(code_expert1.courses_attached)

# Метод выставления оценок лекторам студентами
best_student.set_lecturer_rate(code_expert, 'Python', 10)
best_student1.set_lecturer_rate(code_expert, 'Python', 9)
best_student.set_lecturer_rate(code_expert, 'Java', 8)

# Для второго лектора вылетает ошибка, если он читает курс по С++
best_student.set_lecturer_rate(code_expert1, 'Python', 5)
best_student1.set_lecturer_rate(code_expert1, 'Python', 6)
best_student.set_lecturer_rate(code_expert1, 'Java', 4)

# Раскомментируйте строки печати для вывода соответствующей информации
# Исходно срабабывает запуск методов по выводу средней оценки преподавателей и студентов по определенному курсу

# Выводим на печать информацию по перегруженному __str__
# print(code_expert)
# print(code_expert1)
# print(best_student)
# print(best_student1)
# print(cool_reviewer)
# print(cool_reviewer1)

# Сравниваем средние оценки студентов

# print(best_student > best_student1)
# print(best_student < best_student1)
# print(best_student == best_student1)

# Сравниваем средние оценки лекторов

# print(code_expert > code_expert1)
# print(code_expert < code_expert1)
# print(code_expert == code_expert1)

# Два метода - средние оценки за курс для лекторов и для студентов

lecturer_list = [code_expert, code_expert1]

def count_all_lecturer_grades(lecturers_list, course):
    if len(lecturers_list) == 0:
        return 'Список лекторов не заполнен'
    temp_list = []
    for i in range(len(lecturers_list)):
        if course in lecturers_list[i].grades_for_lecturer.keys():
            temp_list += lecturers_list[i].grades_for_lecturer.get(course)
    if len(temp_list) == 0:
        return f'Оценок оп курсу {course} нет'
    else:
        return f'Средняя оценка всех лекторов по курсу {course}: {str(round(sum(temp_list) / len(temp_list), 1))}'


student_list = [best_student, best_student1]
# student_list.clear()

def count_all_student_grades(student_list, course):
    if len(student_list) == 0:
        return 'Список студентов не заполнен'
    temp_list = []
    for i in range(len(student_list)):
        if course in student_list[i].grades.keys():
            temp_list += student_list[i].grades.get(course)
    if len(temp_list) == 0:
        return f'Оценок оп курсу {course} нет'
    else:
        return f'Средняя оценка всех студентов по курсу {course}: {str(round(sum(temp_list) / len(temp_list), 1))}'


print(count_all_student_grades(student_list, 'Python'))
print(count_all_lecturer_grades(lecturer_list, 'Python'))

# EOF