from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AuthDialog(object):
    def setupUi(self, AuthDialog):
        AuthDialog.setObjectName("AuthDialog")
        AuthDialog.resize(350, 175)
        AuthDialog.setMinimumSize(QtCore.QSize(350, 0))
        AuthDialog.setMaximumSize(QtCore.QSize(9999997, 16777215))
        AuthDialog.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        AuthDialog.setWindowIcon(QtGui.QIcon('cipher.ico'))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(AuthDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.auth_vertical_layout_2 = QtWidgets.QVBoxLayout()
        self.auth_vertical_layout_2.setObjectName("auth_vertical_layout_2")
        self.login_input = QtWidgets.QLineEdit(AuthDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.login_input.setFont(font)
        self.login_input.setObjectName("login_input")
        self.auth_vertical_layout_2.addWidget(self.login_input)
        self.pass_input = QtWidgets.QLineEdit(AuthDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pass_input.setFont(font)
        self.pass_input.setObjectName("pass_input")
        self.pass_input.setEchoMode(2)
        self.auth_vertical_layout_2.addWidget(self.pass_input)
        self.btn_sing_up = QtWidgets.QPushButton(AuthDialog)
        self.btn_sing_up.setObjectName("btn_sing_up")
        self.auth_vertical_layout_2.addWidget(self.btn_sing_up)
        self.btn_sing_in = QtWidgets.QPushButton(AuthDialog)
        self.btn_sing_in.setObjectName("btn_sing_in")
        self.auth_vertical_layout_2.addWidget(self.btn_sing_in)
        self.pass_mode = QtWidgets.QRadioButton(AuthDialog)
        self.pass_mode.setObjectName("pass_mode")
        self.auth_vertical_layout_2.addWidget(self.pass_mode)
        self.verticalLayout_3.addLayout(self.auth_vertical_layout_2)
        AuthDialog.setLayout(self.verticalLayout_3)

        self.retranslateUi(AuthDialog)
        QtCore.QMetaObject.connectSlotsByName(AuthDialog)

    def retranslateUi(self, AuthDialog):
        _translate = QtCore.QCoreApplication.translate
        AuthDialog.setWindowTitle(_translate("AuthDialog", "Авторизация"))
        self.login_input.setPlaceholderText(_translate("AuthDialog", "Login"))
        self.pass_input.setPlaceholderText(_translate("AuthDialog", "Password"))
        self.btn_sing_up.setText(_translate("AuthDialog", "Регистрация"))
        self.btn_sing_in.setText(_translate("AuthDialog", "Войти"))
        self.pass_mode.setText(_translate("AuthDialog", "Показывать пароль"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AuthDialog = QtWidgets.QDialog()
    ui = Ui_AuthDialog()
    ui.setupUi(AuthDialog)
    AuthDialog.show()
    sys.exit(app.exec_())
