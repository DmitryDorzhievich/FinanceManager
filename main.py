import os
import datetime

class Record:
    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

class FinanceManager:
    def __init__(self, filename="records.txt"):
        self.filename = filename
        self.create_file_if_not_exists()

    def create_file_if_not_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w"):
                pass

    def add_record(self, record):
        """Добавляет новую запись о доходе или расходе."""
        with open(self.filename, "a") as file:
            file.write("Дата: {}\n".format(record.date))
            file.write("Категория: {}\n".format(record.category))
            file.write("Сумма: {}\n".format(record.amount))
            file.write("Описание: {}\n".format(record.description))
            file.write("\n")

    def get_balance(self) -> tuple[float, float, float]:
        """Возвращает текущий баланс, общие доходы и расходы."""
        incomes = 0
        expenses = 0
        with open(self.filename, "r") as file:
            lines = file.readlines()
            for i in range(len(lines)):
                if "Категория: Доход" in lines[i]:
                    try:
                        amount = float(lines[i+1].split(": ")[1])
                        incomes += amount
                    except (ValueError, IndexError):
                        print("Ошибка: Невозможно получить сумму дохода из файла.")
                elif "Категория: Расход" in lines[i]:
                    try:
                        amount = float(lines[i+1].split(": ")[1])
                        expenses += amount
                    except (ValueError, IndexError):
                        print("Ошибка: Невозможно получить сумму расхода из файла.")
        balance = incomes - expenses
        return balance, incomes, expenses

    def search_records(self, category=None, start_date=None, end_date=None, min_amount=None, max_amount=None):
        """Ищет записи по заданным критериям и возвращает список найденных записей."""
        results = []
        with open(self.filename, "r") as file:
            record = {}
            for line in file:
                if line.strip():
                    key, value = line.split(": ")
                    record[key.strip()] = value.strip()
                else:
                    if self._filter_record(record, category, start_date, end_date, min_amount, max_amount):
                        results.append(record.copy())
                    record.clear()
            if self._filter_record(record, category, start_date, end_date, min_amount, max_amount):
                results.append(record.copy())
        return results

    def _filter_record(self, record, category, start_date, end_date, min_amount, max_amount):
        """Фильтрует записи по заданным критериям."""
        if category and record.get("Категория") != category:
            return False
        record_date_str = record.get("Дата")
        if start_date and record_date_str and datetime.datetime.strptime(record_date_str, "%Y-%m-%d") < start_date:
            return False
        if end_date and record_date_str and datetime.datetime.strptime(record_date_str, "%Y-%m-%d") > end_date:
            return False
        if min_amount and float(record.get("Сумма")) < min_amount:
            return False
        if max_amount and float(record.get("Сумма")) > max_amount:
            return False
        return True
    
    def edit_record(self, old_record: Record, new_record: Record) -> bool:
        """Редактирует существующую запись."""
        try:
            edited = False
            with open(self.filename, "r") as file:
                lines = file.readlines()
            with open(self.filename, "w") as file:
                i = 0
                while i < len(lines):
                    if old_record.date in lines[i] and old_record.category in lines[i + 1] and str(old_record.amount) in lines[i + 2] and old_record.description in lines[i + 3]:
                        file.write(f"Дата: {new_record.date}\n")
                        file.write(f"Категория: {new_record.category}\n")
                        file.write(f"Сумма: {new_record.amount}\n")
                        file.write(f"Описание: {new_record.description}\n\n")
                        edited = True
                        i += 4  # Пропускаем строки с предыдущей записью
                    else:
                        file.write(lines[i])
                        i += 1
            return edited
        except Exception as e:
            print(f"Ошибка при редактировании записи: {e}")
            return False

if __name__ == "__main__":
    manager = FinanceManager()

    while True:
        print("\nВыберите действие:")
        print("1. Вывод баланса")
        print("2. Добавление записи")
        print("3. Редактирование записи")
        print("4. Поиск записей")
        print("5. Выход")
        choice = input("Введите номер действия: ")

        if choice == "1":
            balance, incomes, expenses = manager.get_balance()
            print("Текущий баланс: {:.2f}".format(balance))
            print("Доходы: {:.2f}".format(incomes))
            print("Расходы: {:.2f}".format(expenses))
        elif choice == "2":
            date = input("Введите дату (ГГГГ-ММ-ДД): ")
            category = input("Введите категорию (Доход/Расход): ")
            amount = float(input("Введите сумму: "))
            description = input("Введите описание: ")
            record = Record(date, category, amount, description)
            manager.add_record(record)
            print("Запись успешно добавлена!")
        elif choice == "3":
            old_date = input("Введите дату записи для редактирования (ГГГГ-ММ-ДД): ")
            old_category = input("Введите категорию записи для редактирования (Доход/Расход): ")
            old_amount = float(input("Введите сумму записи для редактирования: "))
            old_description = input("Введите описание записи для редактирования: ")

            new_date = input("Введите новую дату (ГГГГ-ММ-ДД): ")
            new_category = input("Введите новую категорию (Доход/Расход): ")
            new_amount = float(input("Введите новую сумму: "))
            new_description = input("Введите новое описание: ")

            old_record = Record(old_date, old_category, old_amount, old_description)
            new_record = Record(new_date, new_category, new_amount, new_description)
            if manager.edit_record(old_record, new_record):
                print("Запись успешно отредактирована!")
            else:
                print("Запись не найдена или произошла ошибка при редактировании.")
        elif choice == "4":
            category = input("Введите категорию (Доход/Расход), или оставьте пустым: ")
            start_date = input("Введите начальную дату (ГГГГ-ММ-ДД), или оставьте пустым: ")
            end_date = input("Введите конечную дату (ГГГГ-ММ-ДД), или оставьте пустым: ")
            min_amount = input("Введите минимальную сумму, или оставьте пустым: ")
            max_amount = input("Введите максимальную сумму, или оставьте пустым: ")

            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
            min_amount = float(min_amount) if min_amount else None
            max_amount = float(max_amount) if max_amount else None

            results = manager.search_records(category, start_date, end_date, min_amount, max_amount)
            if results:
                print("Результаты поиска:")
                for result in results:
                    print(result)
            else:
                print("Ничего не найдено.")
        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")