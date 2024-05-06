import os
from datetime import datetime


class FinancialWallet:
    def __init__(self, data_file='wallet_data.txt'):
        """
        Конструктор класса FinancialWallet.

        Parameters:
        - data_file (str): Путь к файлу данных кошелька.

        Attributes:
        - data_file (str): Путь к файлу данных кошелька.
        - data (list): Список словарей, содержащих записи о доходах и расходах.
        """
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        """
        Метод для загрузки данных из файла.

        Returns:
        - list: Список словарей, содержащих записи о доходах и расходах.
        """
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                lines = file.readlines()
                data = []
                entry = {}
                for line in lines:
                    if line.strip():
                        key, value = line.strip().split(': ')
                        entry[key] = value
                    else:
                        data.append(entry)
                        entry = {}
                if entry:
                    data.append(entry)
            return data
        else:
            return []

    def save_data(self):
        """
        Метод для сохранения данных в файл.
        """
        with open(self.data_file, 'w') as file:
            for entry in self.data:
                for key, value in entry.items():
                    file.write(f'{key}: {value}\n')
                file.write('\n')

    @staticmethod
    def validate_entry(entry):
        """
        Метод для валидации записи.

        Parameters:
        - entry (dict): Словарь с данными записи.

        Returns:
        - bool: True, если запись корректна, False в противном случае.
        """
        if not all(key in entry for key in ['Дата', 'Категория', 'Сумма', 'Описание']):
            return False
        try:
            datetime.strptime(entry['Дата'], '%Y-%m-%d')
            int(entry['Сумма'])
            if entry['Категория'] not in ['Доход', 'Расход']:
                raise ValueError
        except ValueError:
            return False
        return True

    def add_entry(self, date, category, amount, description):
        """
        Метод для добавления новой записи о доходе или расходе.

        Parameters:
        - date (str): Дата в формате 'ГГГГ-ММ-ДД'.
        - category (str): Категория (Доход или Расход).
        - amount (str): Сумма.
        - description (str): Описание.
        """
        new_entry = {
            'Дата': date,
            'Категория': category,
            'Сумма': amount,
            'Описание': description
        }
        if self.validate_entry(new_entry):
            self.data.append(new_entry)
            self.save_data()
            print('\nДобавленная запись:')
            print(new_entry)
            print('\nЗапись успешно добавлена.')
        else:
            print('\nНекорректный формат записи. Пожалуйста, проверьте введенные данные.')

    def edit_entry(self, index, date=None, category=None, amount=None, description=None):
        """
        Метод для редактирования существующей записи.

        Parameters:
        - index (int): Индекс записи в списке данных.
        - date (str): Новая дата.
        - category (str): Новая категория.
        - amount (str): Новая сумма.
        - description (str): Новое описание.
        """
        if 0 <= index < len(self.data):
            entry = self.data[index]
            if date:
                entry['Дата'] = date
            if category:
                entry['Категория'] = category
            if amount:
                entry['Сумма'] = amount
            if description:
                entry['Описание'] = description
            if self.validate_entry(entry):
                self.save_data()
                print('\nИзмененная запись:')
                print(self.data[index])
                print('\nЗапись успешно изменена.')
            else:
                print('\nНекорректные данные. Пожалуйста, проверьте введенные данные.')
        else:
            print('\nНеверный индекс записи.')

    def delete_entry(self, index):
        """
        Метод для удаления записи.

        Parameters:
        - index (int): Индекс записи в списке данных.
        """
        if 0 <= index < len(self.data):
            print('\nУдаленная запись:')
            print(self.data[index])
            del self.data[index]
            self.save_data()
            print('\nЗапись успешно удалена.')
        else:
            print('\nНеверный индекс записи.')

    def search_entries(self, category=None, date=None, amount=None):
        """
        Метод для поиска записей по заданным параметрам.

        Parameters:
        - category (str): Категория (Доход или Расход).
        - date (str): Дата в формате 'ГГГГ-ММ-ДД'.
        - amount (str): Сумма.

        Returns:
        - list: Список записей, удовлетворяющих заданным параметрам.
        """
        results = []
        for entry in self.data:
            if (not category or entry.get('Категория') == category) and \
                    (not date or entry.get('Дата') == date) and \
                    (not amount or entry.get('Сумма') == amount):
                results.append(entry)
        return results

    def get_balance(self):
        """
        Метод для вычисления баланса кошелька.

        Returns:
        - tuple: Кортеж с тремя значениями: баланс, доходы, расходы.
        """
        income = sum(int(entry['Сумма']) for entry in self.data if entry.get('Категория') == 'Доход')
        expenses = sum(int(entry['Сумма']) for entry in self.data if entry.get('Категория') == 'Расход')
        balance = income - expenses
        return balance, income, expenses


def main():
    """
    Главная функция программы.
    """
    wallet = FinancialWallet()

    while True:
        print('\nВыберите действие:')
        print('1. Вывести баланс')
        print('2. Добавить запись')
        print('3. Редактировать запись')
        print('4. Удалить запись')
        print('5. Поиск по записям')
        print('6. Выйти')

        choice = input('Введите номер действия: ')

        if choice == '1':
            balance, income, expenses = wallet.get_balance()
            print(f'\nБаланс: {balance}, Доходы: {income}, Расходы: {expenses}')
        elif choice == '2':
            date = input('Введите дату (формат ввода Y-m-d): ')
            category = input('Введите категорию (Доход/Расход): ')
            amount = input('Введите сумму: ')
            description = input('Введите описание: ')
            wallet.add_entry(date, category, amount, description)
        elif choice == '3':
            index = int(input('Введите индекс записи для редактирования: '))
            if 0 <= index < len(wallet.data):
                print('Редактируемая запись:')
                print(wallet.data[index])
                date = input('Введите новую дату (оставьте пустым если хотите оставить без изменения): ')
                category = input('Введите новую категорию (оставьте пустым если хотите оставить без изменения): ')
                amount = input('Введите новую сумму (оставьте пустым если хотите оставить без изменения): ')
                description = input('Введите новое описание (оставьте пустым если хотите оставить без изменения): ')
                wallet.edit_entry(index, date, category, amount, description)
            else:
                print('\nЗаписи с указанным индексом не существует.')
        elif choice == '4':
            index = int(input('Введите индекс записи для удаления: '))
            wallet.delete_entry(index)
        elif choice == '5':
            category = input('Введите категорию (оставьте пустым если хотите без фильтрации по этому параметру): ')
            date = input('Введите дату (оставьте пустым если хотите без фильтрации по этому параметру): ')
            amount = input('Введите сумму (оставьте пустым если хотите без фильтрации по этому параметру): ')
            results = wallet.search_entries(category, date, amount)
            if results:
                for idx, entry in enumerate(results):
                    print(f'\nЗапись {idx + 1}:')
                    print(entry)
            else:
                print('Записи не найдены.')
        elif choice == '6':
            print('Выход из программы.')
            break
        else:
            print('Некорректный ввод. Пожалуйста, выберите действие из списка.')


if __name__ == '__main__':
    main()
