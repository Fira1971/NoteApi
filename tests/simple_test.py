import pytest


def test_simple():
    mylist = [1, 2, 3, 4, 5]

    assert 1 in mylist


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def set_age(self, new_age: int):
        if type(new_age) == int:
            self.age = new_age
            return
        raise ValueError

    def __str__(self):
        return f'Person{self.name, self.age}'


@pytest.fixture
def people():
    person = Person("Ivan", 30)
    return person

# Фикстура(функция people) отрабатывает и результаты
# ее работы будут доступны в функции test_func_name


def test_create_person(people):
    person = people
    assert person.name == "Ivan"
    assert person.age == 30


def test_set_age(people):
    assert people.age == 30
    people.set_age(50)
    assert people.age == 50
