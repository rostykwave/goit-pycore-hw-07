from collections import UserDict
import re
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
          if not value:
                raise ValueError("Name cannot be empty")
          super().__init__(value)

class Phone(Field):
    def __init__(self, value):
          if not re.match(r"^\d{10}$", value):
        # another variant:
        # if not re.fullmatch(r"\d{10}", value): 
                raise ValueError("Phone number must be 10 digits")
          super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
        if Birthday.is_future_date(parsed_date):
            raise ValueError("Birthday is in the future")
        
        self.value = parsed_date
    
    
    @staticmethod
    def is_future_date(date):
        return date > datetime.today().date()
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
         self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
         self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = Phone(new_phone).value
                return
        raise ValueError("Phone number not found")

    def find_phone(self, phone_number):
        return next((phone for phone in self.phones if phone.value == phone_number), None)
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "Not set"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
         self.data[record.name.value] = record
    
    def find(self, name):
         return self.data.get(name, None)
    
    def delete(self, name):
         if name in self.data:
              del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                if today <= birthday_this_year <= next_week:
                    # Find next Monday
                    if birthday_this_year.weekday() in (5, 6):  # Saturday = 5, Sunday = 6
                        days_to_monday = 7 - birthday_this_year.weekday()
                        congratulation_date = birthday_this_year + timedelta(days=days_to_monday)
                    else:
                        congratulation_date = birthday_this_year
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })
        return upcoming_birthdays
       

if __name__ == "__main__":
# Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("18.03.1995")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("20.03.1993")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)
        
    #Upcoming Birthdays:
    print("\nUpcoming Birthdays:")
    for entry in book.get_upcoming_birthdays():
        print(f"{entry['name']}: {entry['congratulation_date']}")

    print("\nEditing and deleting info:")
    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
