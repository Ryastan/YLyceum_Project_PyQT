from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget, QDialog
from auth import Ui_AuthDialog
from cipher import Ui_CipherWindow
from add_ciph import Ui_AddCiphDialog
import sqlite3 as sq
import sys

#Классы ошибок
class IncorrectPassword(Exception): #Неверный пароль
    pass


class IncorrectLogin(Exception): #Неверный логин
    pass


class EmptyFields(Exception): #Пустые поля
    pass


class IncorrectNameCiph(Exception): #Некоректное название шифра
    pass

#Классы окон
class Cipher(QMainWindow, Ui_CipherWindow): #Класс с главным окном
    def __init__(self):
        super(Cipher, self).__init__()
        self.setupUi(self)


class AuthDialog(QWidget, Ui_AuthDialog): #Класс с окном авторизации
    def __init__(self):
        super(AuthDialog, self).__init__()
        self.setupUi(self)

        self.pass_mode.toggled.connect(self.echo_mode)
    
    def echo_mode(self): #Функция для изменения показа пароля в строке PASSWORD
        if self.pass_mode.isChecked():
            self.pass_input.setEchoMode(0)
        else:
            self.pass_input.setEchoMode(2)


class AddCiphDialog(QWidget, Ui_AddCiphDialog): #Класс с окном для добавления шифра
    def __init__(self):
        super(AddCiphDialog, self).__init__()
        self.setupUi(self)


class MainWindow(): #Класс полного приложения
    def __init__(self):
        self.cipher = Cipher()
        self.cipher.show()
        self.add_ciph_dialog = AddCiphDialog()
        self.auth_dialog = AuthDialog()

        self.cipher.btn_login.clicked.connect(self.authorization)
        self.cipher.btn_logout.clicked.connect(self.logout)
        self.cipher.btn_add_cipher.clicked.connect(self.start_add_ciph)
        self.cipher.btn_ciph_text.clicked.connect(self.ciph_text)

    def error_message(self, title, text, detailed_text=''): #Функция для создания QMessageBox.error
        error = QMessageBox()
        error.setText(text)
        error.setWindowTitle(title)
        error.setStandardButtons(QMessageBox.Ok)
        error.setIcon(QMessageBox.Warning)
        if detailed_text != '':
            error.setDetailedText(detailed_text)
        error.exec_()

    def authorization(self): #Запуск класса с диалоговым окном авторизации
        self.auth_dialog = AuthDialog()
        self.auth_dialog.show()

        self.auth_dialog.btn_sing_in.clicked.connect(self.sing_in)
        self.auth_dialog.btn_sing_up.clicked.connect(self.sing_up)

    def start_add_ciph(self): #Запуск класса с добавление шифра
        self.add_ciph_dialog = AddCiphDialog()
        if self.cipher.btn_login.visibleRegion().isEmpty():
            self.add_ciph_dialog.show()
        else:
            self.error_message('Ошибка', 'Для добавление шифра необходимо войти в аккаунт')

        self.add_ciph_dialog.btn_add_ciph.clicked.connect(self.add_ciph)

    def sing_in(self): #Функция авторизации
        login = self.auth_dialog.login_input.text()
        password = self.auth_dialog.pass_input.text()
        self.succesful = False

        #Подклчение Базы данных
        con = sq.connect("dataBase\ciphers.db")
        cur = con.cursor()

        #Если не существует таблицы создаём, во избежании обшибки
        cur.execute("""CREATE TABLE IF NOT EXISTS "users" (
	                "id"	INTEGER,
	                "login"	TEXT,
	                "password"	TEXT,
	                PRIMARY KEY("id" AUTOINCREMENT)
                    );""")

        #Проверяем на наличие пользователя
        cur.execute(f'SELECT * FROM users WHERE login="{login}";')
        value = cur.fetchall()

        try:
            if login == '' or password == '':
                raise EmptyFields
            if value == []:
                raise IncorrectLogin
            if value[0][2] != password:
                raise IncorrectPassword

            succesful = QMessageBox()
            succesful.setText('Вы успешно авторизованны!')
            succesful.setWindowTitle('Успешно')
            succesful.setStandardButtons(QMessageBox.Ok)
            succesful.exec_()

            self.cipher.name_user.setText(login)
            self.cipher.btn_login.hide()
            self.cipher.btn_logout.show()
            self.auth_dialog.close()
            self.update_comboBox()
        except EmptyFields:
            self.error_message('Ошибка', 'Поля LOGIN и PASSWORD обязательны для заполнения')
        except IncorrectLogin:
            self.error_message('Ошибка', 'Пользователя с таким логином не обнаруженно')
        except IncorrectPassword:
            self.error_message('Ошибка', 'Пароль неверный')

    def logout(self): #Функция выхода из аккаунта
        self.cipher.name_user.setText('Guest')
        self.cipher.btn_logout.hide()
        self.cipher.btn_login.show()
        self.cipher.ciph.clear()
        self.cipher.ciph.addItem('Шифр Морзе')
        self.cipher.ciph.addItem('Шифр Цезаря')

    def sing_up(self): #Функция регистрации
        login = self.auth_dialog.login_input.text()
        password = self.auth_dialog.pass_input.text()

        #Подключение базы данных
        con = sq.connect("dataBase\ciphers.db")
        cur = con.cursor()

        #Если не существует таблицы создаём, во избежании обшибки
        cur.execute("""CREATE TABLE IF NOT EXISTS "users" (
	                "id"	INTEGER,
	                "login"	TEXT,
	                "password"	TEXT,
	                PRIMARY KEY("id" AUTOINCREMENT)
                    );""")

        cur.execute(f'SELECT * FROM users WHERE login="{login}";')
        value = cur.fetchall()

        try:
            if login == '' or password == '':
                raise EmptyFields
            
            if value != []:
                raise IncorrectLogin
            
            if not self.check_password(self.auth_dialog.pass_input.text()):
                raise IncorrectPassword

            cur.execute(f"INSERT INTO users(login, password, ciphers) VALUES('{login}', '{password}', '')")
            con.commit()
            succesful = QMessageBox()
            succesful.setText('Вы успешно зарегестрированы!')
            succesful.setWindowTitle('Успешно')
            succesful.setStandardButtons(QMessageBox.Ok)
            succesful.exec_()
        except EmptyFields:
            self.error_message('Ошибка', 'Поля LOGIN и PASSWORD обязательны для заполнения')
        except IncorrectPassword:
            self.error_message('Ошибка', 'Пароль несоотвествует требованиям безопастности',
                          '1)Длина пароля больше 8 символов.\n'
                          '2)В нем должны присутствовать большие и маленькие буквы любого алфавита.\n'
                          '3)В нем имеется хотя бы одна цифра.')
        except IncorrectLogin:
            self.error_message('Ошибка', 'Такой логин уже занят!')
        con.close()

    def check_password(self, password): #Функция для проверки пароля

        def check_symbols(string, number): #Функция проверки на наличие большой\заглавной буквы и цифры в пароле
            if number == 1:
                for i in string:
                    if not i.isdigit():
                        if not i.isupper():
                            return True
                return False
            if number == 2:
                for i in string:
                    if not i.isdigit():
                        if i.isupper():
                            return True
                return False
            if number == 3:
                for i in string:
                    if i.isdigit():
                        return True
                return False

        if len(password) > 8:
            if check_symbols(password, 1):
                if check_symbols(password, 2):
                    if check_symbols(password, 3):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def add_ciph(self): #Функция добавления шифра
        with sq.connect('dataBase\ciphers.db') as con:
            try:
                if self.add_ciph_dialog.name_ciph.text() == '':
                    raise IncorrectNameCiph

                cur = con.cursor()
                cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.add_ciph_dialog.name_ciph.text()}'")
                if cur.fetchall() == []:
                    name_ciph = self.add_ciph_dialog.name_ciph.text()
                else:
                    name_ciph_for_change = cur.fetchall()
                    name_ciph = name_ciph_for_change[0] + str((int(name_ciph_for_change[1]) + 1))

                #Добаление в БД таблицу для шифра с названием name_ciph
                cur.execute(f"""CREATE TABLE "{name_ciph}" ( 
                                "letter"    TEXT,
                                "ciph_letter"	TEXT
                            );""")

                count = 0
                
                for letter_lineEdit in self.add_ciph_dialog.list_lineEdit_rus_letters: #Добавление в БД шифр для русских букв
                    if letter_lineEdit.text() == '':
                        raise EmptyFields
                    cur.execute(f"""INSERT INTO "{name_ciph}"(letter, ciph_letter) VALUES(
                        '{self.add_ciph_dialog.ru_alphabet[count]}',
                        '{letter_lineEdit.text()}'
                        )""")
                    count += 1
                
                count = 0
                for letter_lineEdit in self.add_ciph_dialog.list_lineEdit_eng_letters: #Добавление в БД шифр для английский букв
                    if letter_lineEdit.text() == '':
                        raise EmptyFields
                    cur.execute(f"""INSERT INTO "{name_ciph}"(letter, ciph_letter) VALUES(
                        '{self.add_ciph_dialog.eng_alphabet[count]}',
                        '{letter_lineEdit.text()}'
                        )""")
                    count += 1

                cur.execute(f"SELECT ciphers FROM 'users' WHERE login='{self.cipher.name_user.text()}'")
                value_ciphers = cur.fetchone()
                if value_ciphers[0] != 'all':
                    if value_ciphers[0] != '':
                        cur.execute(f"""UPDATE users SET ciphers='{value_ciphers[0] + ', ' + self.add_ciph_dialog.name_ciph.text()}'
                                    WHERE login='{self.cipher.name_user.text()}'
                                    """)
                    else:
                        cur.execute(f"""UPDATE users SET ciphers='{self.add_ciph_dialog.name_ciph.text()}'
                                    WHERE login='{self.cipher.name_user.text()}'""")

                succesful = QMessageBox()
                succesful.setText('Шифр успешно добавлен!')
                succesful.setWindowTitle('Успешно')
                succesful.setStandardButtons(QMessageBox.Ok)
                succesful.exec_()

                self.cipher.ciph.addItem(self.add_ciph_dialog.name_ciph.text())

                self.add_ciph_dialog.close()
            except EmptyFields:
                cur.execute(f"DROP TABLE IF EXISTS '{name_ciph}'")
                self.error_message('Ошибка', 'Необхобимо ввести значения во всех полях')
            except IncorrectNameCiph:
                self.error_message('Ошибка', 'Необходимо ввести название шифра')

    def update_comboBox(self): #Функция для обновления имеющихся шифров
        with sq.connect('dataBase\ciphers.db') as con:
            cur = con.cursor()

            cur.execute(f"SELECT ciphers FROM users WHERE login='{self.cipher.name_user.text()}'")
            value_ciphers = cur.fetchone()

            if value_ciphers[0] == 'all':
                self.cipher.ciph.clear()
                cur.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
                tables = cur.fetchall()
                for table in tables:
                    if table[0] != 'users' and table[0] != 'sqlite_sequence':
                        self.cipher.ciph.addItem(table[0])
            elif value_ciphers[0] != '':
                cur.execute(f"SELECT ciphers FROM users WHERE login='{self.cipher.name_user.text()}'")
                values_ciphers = cur.fetchone()
                for name_ciph in values_ciphers[0].split(', '):
                    self.cipher.ciph.addItem(name_ciph)

    def ciph_text(self): #Функция для шифрования текста выбранным шифром
        name_ciph = self.cipher.ciph.currentText()
        ciph_text = ''
        with sq.connect('dataBase\ciphers.db') as con:
            cur = con.cursor()

            for letter in self.cipher.text_input.toPlainText():
                cur.execute(f"SELECT ciph_letter FROM '{name_ciph}' WHERE letter='{letter.upper()}'")
                ciph_letter = cur.fetchone()

                if ciph_letter != None:
                    ciph_text += ciph_letter[0]
                elif ciph_letter == None:
                    ciph_text += letter
           
            self.cipher.text_output.clear()
            self.cipher.text_output.setText(ciph_text)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())