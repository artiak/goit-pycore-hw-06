import re
from typing import List, Tuple, Dict
from collections import UserDict


class Field:
    
    def __init__(self, value: str):
        self._value = value

    def get_value(self) -> str:
        return self._value

    def __eq__(self, other):
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)

    def __str__(self):
        return str(self._value)


class Name(Field):
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Name):
            return False

        return super().__eq__(other)


class Phone(Field):
    
    def __init__(self, value: str):
        if not _is_phone(value):
            raise PhoneException

        self._value = value

    def set_value(self, value: str) -> None:
        self._value = value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Phone):
            return False

        return super().__eq__(other)


def _is_phone(input: str) -> bool:
    """
    Defines if input corresponds to 10 digit formats, e.g.:
        (XXX)-XXX-XXXX
         XXX-XXX-XXXX
        (XXX)XXXXXXX
         XXXXXXXXXX
    """
    pattern = r"\b\(?\d{3}\)?-?\d{3}-?\d{4}\b"
    return bool(re.match(pattern, input))


class PhoneException(Exception):
    
    def __init__(self):
        super().__init__("Invalid phone number. It must be a 10-digit number.")


class Record:
    
    def __init__(self, name: str):
        self.__name: Name = Name(name)
        self.__phones: List[Phone] = []

    def get_name(self) -> Name:
        return self.__name

    def add_phone(self, str_phone: str) -> None:
        self.__phones.append(Phone(str_phone))

    def find_phone(self, str_phone: str) -> Phone:
        for phone in self.__phones:
            if phone.get_value() == str_phone:
                return phone

    def edit_phone(self, orig_str_phone: str, upd_str_phone: str) -> None:
        if not _is_phone(upd_str_phone):
            raise PhoneException

        phone: Phone = self.find_phone(orig_str_phone)

        if not Phone:
            return

        phone.set_value(upd_str_phone)

    def get_phones(self) -> Tuple[Phone]:
        return tuple(self.__phones)

    def __str__(self):
        return f"""Contact name: {self.__name.get_value()},
        phones: {'; '.join(p.get_value() for p in self.__phones)}"""


class AddressBook(UserDict):
    
    def find(self, name: str) -> Record:
        data: Dict[str, Record] = self.data
        for key in data.keys():
            if key == name:
                return data[key]

        return None

    def add_record(self, record: Record) -> None:
        self.data[record.get_name().get_value()] = record
        
    def delete(self, name: str) -> None:
        del self.data[name]


# testing


# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")

# Створення нової адресної книги
book = AddressBook()

# Додавання запису John до адресної книги
book.add_record(john_record)
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
found_john_record = book.find("John")
found_john_record.edit_phone("1234567890", "1112223333")

# Виведення: Contact name: John, phones: 1112223333; 5555555555
print(found_john_record)

# Пошук конкретного телефону у записі John
found_phone = found_john_record.find_phone("5555555555")

# Виведення: 5555555555
print(f"{found_john_record.get_name()}: {found_phone}")

# Видалення запису Jane
book.delete("Jane")

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)