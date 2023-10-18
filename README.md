# Console bot
Console Bot is a command-line interface application for managing, updating, and
viewing phone numbers. The app saves the current list of contacts to a file at
the end of each session.

To run the Console Bot, go to the 'goitneo-python-hw-2-mcs3' folder and execute
the following command:
```console
python3 console_bot.py --file ./data/contacts.json
```
Ensure that the specified JSON file is formatted as a dictionary, where keys
represent names, and values are phone numbers (strings).

You can also run the application with the default file as follows:
```console
python3 console_bot.py
```
In this case, the tool will use the default './data/contacts.json' file.

### Improvements added to previous version from [goitneo-python-hw-2-mcs3](https://github.com/AntonChubarov/goitneo-python-hw-2-mcs3) repository:

1. Added errors handling using decorators
2. Developed classes for future refactoring
