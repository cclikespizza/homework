# -*- coding=utf-8 -*-

__author__ = 'elmira'


class NoSuchYear(Exception):

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message


class Student:
    """
    Attributes:
        name
        surname
        year: "1 бак", "2 бак", "3 бак", "4 бак", "1 маг" или "2 маг"
        department

    Methods:
        next_year
            переводит студента на следующий курс. Если студент был успешно переведён, next_year возвращает True,
            а если он учился на последнем курсе магистратуры и его некуда переводить, то False.
        comparison methods  - то a < b, если a учится на более младшем курсе, чем b
    """

    years = [u"1бак", u"2бак", u"3бак", u"4бак", u"1маг", u"2маг"]

    def __init__(self, name, surname, department, year):
        self.name = name
        self.surname = surname
        self.year = self.define_year(year)
        self.department = department

    def define_year(self, year):
        if year in self.years:
            return year
        else:
            raise NoSuchYear('Year "' + year + '" is not in possible values. Possible values are: ' +
                             ', '.join(self.years))

    def next_year(self):
        index = self.years.index(self.year)
        if index == len(self.years) - 1:
            return False
        self.year = self.years[index + 1]
        return True

    def __lt__(self, other):
        if self.years.index(self.year) < self.years.index(other.year):
            return True
        return False

    def __gt__(self, other):
        if self.years.index(self.year) > self.years.index(other.year):
            return True
        return False

    def __eq__(self, other):
        if self.years.index(self.year) == self.years.index(other.year):
            return True
        return False

    def __ne__(self, other):
        if self.years.index(self.year) != self.years.index(other.year):
            return True
        return False

    def __le__(self, other):
        if self == other or self < other:
            return True
        return False

    def __ge__(self, other):
        if self == other or self > other:
            return True
        return False


class University:
    """
    хранит информацию о всех студентах университета - Student objects

    Methods:
    add_student с аргументами name, surname, department -- зачислить студента на 1 курс бакалавриата
    end_year -- функция, вызываемая в конце каждого учебного года:
        она переводит всех имеющихся студентов на следующий курс, а тех, кто закончил обучение, удаляет из списков

    """
    def __init__(self):
        self.students = []

    def add_student(self, name, surname, department, year=''):
        if year == '':
            new_year = u"1бак"
        else:
            new_year = year
        new_student = Student(name, surname, department, new_year)
        self.students.append(new_student)

    def end_year(self):
        graduated = []
        for studNum in range(len(self.students)):
            if not self.students[studNum].next_year():
                graduated.append(self.students[studNum])
        for grad in graduated:
            self.students.remove(grad)

    def __iter__(self):
        return iter(self.students)

    def show(self):
        for student in self:
            print(student.name, student.surname, student.department, student.year)


class ChatBot(object):
    def __init__(self):
        self.uni = University()
        print("Hello, I'a a ChatBot of this University! ")
        self.intro()
        user_command = input()
        while user_command != '':
            self.parse(user_command)
            self.intro()
            user_command = input()

    def intro(self):
        print("""Here's the list of commands:
        /add name surname department - to enroll a student to the 1st year
        /add name surname department year - to enroll a student to a defined year
        /end_year - upgrade students""")

    def parse(self, command):
        if command.startswith('/'):
            if command.startswith('/add'):
                c = command.split(' ')[1:]
                if len(c) < 3:
                    print('Please, add name, surname and department.')
                elif len(c) == 3:
                    self.uni.add_student(c[0], c[1], c[2])
                elif len(c) == 4:
                    try:
                        self.uni.add_student(c[0], c[1], c[2], c[3])
                    except NoSuchYear as e:
                        print(e.message)
                else:
                    pass
                self.uni.show()
            elif command == '/end_year':
                self.uni.end_year()
                self.uni.show()
            else:
                print('No such command.')
        else:
            print('Please, print slash at the beginning of a command')


if __name__ == "__main__":
    r = ChatBot()