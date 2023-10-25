# Console bot
Console Bot is a command-line interface application for managing, updating, and
viewing phone numbers and birthdays. The app saves the current contacts to a file
at the end of each session.

To run the Console Bot, go to the 'goitneo-python-hw-3-mcs3' folder and execute
the following command:
```console
python3 console_bot.py --file ./data/book.dat
```
In case when specified file doesn't exist, it will be created.

You can also run the application with the default file as follows:
```console
python3 console_bot.py
```
In this case, the tool will use the default './data/book.dat' file.

### Improvements added to previous version from [goitneo-python-hw-2-mcs3](https://github.com/AntonChubarov/goitneo-python-hw-2-mcs3) repository:

1. dictionary, that stored contacts was changed to the AddressBook class
