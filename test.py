import unittest
from main import FinancialWallet


class TestFinancialWallet(unittest.TestCase):
    def setUp(self):
        self.test_data_file = 'test_wallet_data.txt'
        self.clear_data_file()
        self.wallet = FinancialWallet(data_file=self.test_data_file)

    def clear_data_file(self):
        with open(self.test_data_file, 'w') as file:
            file.truncate(0)

    def test_add_entry(self):
        self.wallet.add_entry('2024-05-01', 'Доход', '5000', 'Зарплата')
        self.assertEqual(len(self.wallet.data), 1)
        self.wallet.add_entry('2024-05-02', 'Расход', '1500', 'Покупка продуктов')
        self.assertEqual(len(self.wallet.data), 2)

    def test_edit_entry(self):
        self.wallet.add_entry('2024-05-01', 'Доход', '5000', 'Зарплата')
        self.wallet.edit_entry(0, category='Расход', amount='1500', description='Покупка продуктов')
        edited_entry = self.wallet.data[0]
        self.assertEqual(edited_entry['Категория'], 'Расход')
        self.assertEqual(edited_entry['Сумма'], '1500')
        self.assertEqual(edited_entry['Описание'], 'Покупка продуктов')

    def test_delete_entry(self):
        self.wallet.add_entry('2024-05-01', 'Доход', '5000', 'Зарплата')
        self.wallet.add_entry('2024-05-02', 'Расход', '1500', 'Покупка продуктов')
        self.wallet.delete_entry(1)
        self.assertEqual(len(self.wallet.data), 1)

    def test_search_entries(self):
        self.wallet.add_entry('2024-05-01', 'Доход', '5000', 'Зарплата')
        self.wallet.add_entry('2024-05-02', 'Расход', '1500', 'Покупка продуктов')
        results = self.wallet.search_entries(category='Доход')
        self.assertEqual(len(results), 1)
        results = self.wallet.search_entries(date='2024-05-02')
        self.assertEqual(len(results), 1)
        results = self.wallet.search_entries(amount='1500')
        self.assertEqual(len(results), 1)

    def test_get_balance(self):
        self.wallet.add_entry('2024-05-01', 'Доход', '5000', 'Зарплата')
        self.wallet.add_entry('2024-05-02', 'Расход', '1500', 'Покупка продуктов')
        balance, income, expenses = self.wallet.get_balance()
        self.assertEqual(balance, 3500)
        self.assertEqual(income, 5000)
        self.assertEqual(expenses, 1500)


if __name__ == '__main__':
    unittest.main()
