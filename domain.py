from collections import UserDict
from datetime import datetime, timedelta
import pickle


DATE_FORMAT: str = "%d.%m.%Y"


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str) -> None:
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    def __eq__(self, other):
        return self.value == other.value

    @staticmethod
    def is_valid_phone(value: str) -> bool:
        return len(str(value)) == 10 and value.isdigit()


class Birthday(Field):
    def __init__(self, value: str) -> None:
        super().__init__(datetime.strptime(value, DATE_FORMAT).date())

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.value.strftime(DATE_FORMAT)


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        phone = Phone(phone)
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        old_phone = Phone(old_phone)
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = Phone(new_phone)
            return

        raise ValueError(
            f"phone {old_phone} wasn't found in record {self.name}")

    def find_phone(self, phone: str) -> Phone:
        phone = Phone(phone)
        for p in self.phones:
            if p == phone:
                return p
        raise ValueError(f"phone {phone} not found")

    def add_birthday(self, date: str) -> None:
        self.birthday = Birthday(date)

    def __str__(self):
        phone_str = "; ".join(str(p) for p in self.phones)
        result = f"Contact name: {self.name}, phones: {phone_str}"

        return result


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        if not isinstance(record, Record):
            raise ValueError("record must be an instance of the Record class")
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def __get_users_with_birthdays(self) -> list[dict[str, datetime.date]]:
        users = []
        for record in self.data.values():
            birthday = record.birthday
            if birthday:
                users.append({"name": record.name.value,
                             "birthday": record.birthday.value})

        return users

    def get_birthdays_per_week(self) -> dict[str, list[str]]:
        users = self.__get_users_with_birthdays()

        today = datetime.today().date()

        users_to_congratulate: dict[str, list[str]] = {}

        for user in users:
            birthday_this_year = user["birthday"].replace(year=today.year)

            days_to_period_start, days_to_period_end = 0, 7
            if today.strftime("%A") == "Monday":
                days_to_period_start, days_to_period_end = -2, 5
            elif today.strftime("%A") == "Sunday":
                days_to_period_start, days_to_period_end = -1, 6

            delta_days = (birthday_this_year - today).days

            if days_to_period_start <= delta_days < days_to_period_end:
                day_name = birthday_this_year.strftime("%A")

                if day_name in ("Saturday", "Sunday"):
                    day_name = "Monday"

                if day_name not in users_to_congratulate:
                    users_to_congratulate[day_name] = []

                users_to_congratulate[day_name].append(user["name"])

        birthday_days = list(users_to_congratulate.keys())
        sorted_days = [(datetime.today()+timedelta(days=i)).
                       strftime("%A") for i in range(7)]
        sorted_days = list(filter(
            lambda day: day in birthday_days, sorted_days))

        dayly_sorted_users_to_congratulate: dict[str, list] = {}

        for day in sorted_days:
            names = ", ".join(users_to_congratulate[day])
            dayly_sorted_users_to_congratulate[day] = names

        return dayly_sorted_users_to_congratulate

    def save_to_file(self, path: str) -> None:
        with open(path, "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self, path: str) -> None:
        with open(path, "ab+") as file:
            file.seek(0)
            content = pickle.load(file)
            self.data = content

    def __len__(self):
        return len(self.data)

    def __str__(self):
        result = ""
        for record in self.data.values():
            result += str(record) + "\n"

        return result.rstrip()


if __name__ == "__main__":
    # task reqirements test script
    print("Task reqirements test script:")

    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")

    # additional test script
    print("\nAdditional test script:")

    john_record.remove_phone("5555555555")
    print(john_record)

    try:
        john_record.add_phone("1112223333")
    except ValueError as ve:
        print(f"error: {ve}")

    try:
        john_record.add_phone("11122233334")
    except ValueError as ve:
        print(f"error: {ve}")

    try:
        john_record.add_phone("111222333")
    except ValueError as ve:
        print(f"error: {ve}")

    try:
        john_record.edit_phone("5555555555", "6666666666")
    except ValueError as ve:
        print(f"error: {ve}")

    book.add_record(jane_record)
    jane_record.add_phone("0975554862")

    print(book.find("Alex"))

    print(str(book))
