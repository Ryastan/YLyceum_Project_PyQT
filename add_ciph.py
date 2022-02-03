from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddCiphDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 316)
        Dialog.setWindowIcon(QtGui.QIcon('cipher.ico'))
        self.row = 3 #Количество строк
        self.column = 11 #Количество колонн
        self.list_lineEdit_rus_letters = []
        self.list_lineEdit_eng_letters = []
        self.ru_alphabet = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й',
                             'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
                              'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
        self.eng_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        
        self.numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.addciph_layout = QtWidgets.QVBoxLayout()
        self.addciph_layout.setObjectName("addciph_layout")
        self.rus_alphabet_text = QtWidgets.QLabel(Dialog)
        self.rus_alphabet_text.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.rus_alphabet_text.setFont(font)
        self.rus_alphabet_text.setAlignment(QtCore.Qt.AlignCenter)
        self.rus_alphabet_text.setObjectName("rus_alphabet_text")
        self.addciph_layout.addWidget(self.rus_alphabet_text)
        self.rus_alphabet_layout = QtWidgets.QGridLayout()
        self.rus_alphabet_layout.setObjectName("rus_alphabet")

        self.count = 0
        for r in range(self.row): #Цикл с добавлением LineEdit для Русского алфавита
            for c in range(self.column):
                lineEdit = QtWidgets.QLineEdit()
                lineEdit.setPlaceholderText(self.ru_alphabet[self.count])
                self.count += 1
                self.list_lineEdit_rus_letters.append(lineEdit)
                self.rus_alphabet_layout.addWidget(lineEdit, r, c)

        self.addciph_layout.addLayout(self.rus_alphabet_layout)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.addciph_layout.addWidget(self.line)
        self.eng_alphabet_text = QtWidgets.QLabel(Dialog)
        self.eng_alphabet_text.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.eng_alphabet_text.setFont(font)
        self.eng_alphabet_text.setAlignment(QtCore.Qt.AlignCenter)
        self.eng_alphabet_text.setObjectName("eng_alphabet_text")
        self.addciph_layout.addWidget(self.eng_alphabet_text)
        self.eng_alphabet_layout = QtWidgets.QGridLayout()
        self.eng_alphabet_layout.setObjectName("eng_alphabet")

        self.count = 0
        for r in range(self.row): #Цикл с добавлением LineEdit для Английского алфавита
            for c in range(self.column):
                lineEdit = QtWidgets.QLineEdit()
                if self.count < 26:
                    lineEdit.setPlaceholderText(self.eng_alphabet[self.count])
                    self.count += 1
                    self.list_lineEdit_eng_letters.append(lineEdit)
                    self.eng_alphabet_layout.addWidget(lineEdit, r, c)

        self.addciph_layout.addLayout(self.eng_alphabet_layout)
        self.name_ciph = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.name_ciph.setFont(font)
        self.name_ciph.setObjectName("name_ciph")
        self.addciph_layout.addWidget(self.name_ciph)
        self.btn_add_ciph = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_add_ciph.setFont(font)
        self.btn_add_ciph.setObjectName("btn_add_ciph")
        self.addciph_layout.addWidget(self.btn_add_ciph)
        self.verticalLayout_2.addLayout(self.addciph_layout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Добавление шифра"))
        self.rus_alphabet_text.setText(_translate("Dialog", "Русский алфавит"))
        self.eng_alphabet_text.setText(_translate("Dialog", "Английский алфавит"))
        self.name_ciph.setPlaceholderText(_translate("Dialog", "Название шифра"))
        self.btn_add_ciph.setText(_translate("Dialog", "Добавить шифр"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_AddCiphDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
