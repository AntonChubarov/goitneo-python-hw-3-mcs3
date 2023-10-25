import argparse
import json
import signal
import sys

from domain import AddressBook, Record


book_file_name: str = ""
book: AddressBook = AddressBook()


def handle_system_signal(sig, frame):
    _, _ = sig, frame
    print("\nTermination signal received. Shutting down...")
    shutdown()


def load_book():
    if not book_file_name:
        raise ValueError("file name is not specified (empty)")

    if not book_file_name.endswith(".dat"):
        raise ValueError(f"file {book_file_name} is not a DAT file")

    global book

    try:
        book.read_from_file(book_file_name)
    except EOFError:
        pass


def save_book():
    if not book_file_name:
        raise ValueError("file name was not specified (empty)")

    if len(book) == 0:
        return

    book.save_to_file(book_file_name)


def greet() -> str:
    return "How can I help you?"


def get_help() -> str:
    return "Commands:\n" \
        "hello: show greeting\n" \
        "add: add new phone, example: add John 0685554689\n" \
        "change: change phone, example: change John 0685554689 0505557899\n" \
        "phone: show phones, example: phone John\n" \
        "all: show entire address book\n" \
        "add-birthday: example: add-birthday John 17.10.1989\n" \
        "show-birthday: example: show-birthday John\n" \
        "birthdays: show who shulld be congratulated this week"


def add_contact(name: str, phone: str) -> str:
    record = book.find(name)

    if not record:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return f"{name} was added to your book"

    record.add_phone(phone)
    return f"New phone was added to {name}'s record"


def change_contact(name: str, old_phone: str, new_phone: str) -> str:
    record = book.find(name)

    if not record:
        raise ValueError(f"no name {name} in address book")

    record.edit_phone(old_phone, new_phone)
    return f"{name}'s contact was updated"


def show_phone(name: str) -> str:
    record = book.find(name)

    if not record:
        raise ValueError(f"no name {name} in address book")

    return str(record)


def get_all() -> str:
    return str(book)


def add_birthday(name: str, date: str) -> str:
    book.find(name).add_birthday(date)
    return f"added birth date for {name}"


def get_birthday(name: str) -> str:
    birthday = book.find(name).birthday

    if not birthday:
        return f"no saved birthday for {name}"

    return str(birthday)


def get_birthdays_per_week() -> str:
    birthdays = book.get_birthdays_per_week()
    result = ""
    for day, names in birthdays.items():
        result += f"{day}: {names}\n"

    return result.rstrip()


def critical_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except json.JSONDecodeError as jde:
            print(f"json decode error: {jde}")
            sys.exit(1)
        except ValueError as ve:
            print(f"critical value error: {ve}")
            sys.exit(1)
        except FileNotFoundError as fnfe:
            print(f"file not found error: {fnfe}")
            sys.exit(1)
        except KeyError as ke:
            print(f"key error: {ke}")
            sys.exit(1)
        except PermissionError as pe:
            print(f"permission error: {pe}")
            sys.exit(1)
        except argparse.ArgumentError as ape:
            print(f"argument parse error: {ape}")
            sys.exit(1)
        except Exception as e:
            print(f"unexpected critical error: {type(e)}: {e}")
            sys.exit(1)

    return inner


@critical_error
def shutdown():
    save_book()
    sys.exit()


@critical_error
def init():
    signal.signal(signal.SIGINT, handle_system_signal)
    signal.signal(signal.SIGTERM, handle_system_signal)

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str,
                        help="Path to the json file with saved book",
                        default="./data/book.dat")

    args = parser.parse_args()

    global book_file_name
    book_file_name = args.file

    load_book()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return f"value error: {ve}"
        except KeyError as ke:
            return f"key error: {ke}"
        except IndexError as ie:
            return f"index error: {ie}"
        except AttributeError as ae:
            return f"attribute error: {ae}"
        except Exception as e:
            return f"unexpected error: {type(e)}: {e}"

    return inner


@input_error
def handle_command(cmd: str, args: list[str]) -> str:
    if cmd == "hello":
        return greet()
    if cmd == "help":
        return get_help()
    if cmd == "add":
        name, phone = args
        return add_contact(name, phone)
    if cmd == "change":
        name, old_phone, new_phone = args
        return change_contact(name, old_phone, new_phone)
    if cmd == "phone":
        name, = args
        return show_phone(name)
    if cmd == "all":
        return get_all()
    if cmd == "add-birthday":
        name, birthday = args
        return add_birthday(name, birthday)
    if cmd == "show-birthday":
        name, = args
        return get_birthday(name)
    if cmd == "birthdays":
        return get_birthdays_per_week()

    raise ValueError(f"invalid command: {cmd}")


def parse_command(user_input: str) -> (str, list[str]):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    init()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("console bot >>> ")
        cmd, *args = parse_command(user_input)
        if cmd is None or cmd == "":
            print("No command was entered. Try again")
        elif cmd in ("exit", "q", "quit", "close", "good bye"):
            break
        message = handle_command(cmd, args)
        if message:
            print(message)

    print("Good bye!")
    shutdown()


if __name__ == "__main__":
    main()
