from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, qApp


class UserNameDialog(QDialog):
    """Стартовый диалог с выбором имени пользователя"""
    def __init__(self):
        super().__init__()

        self.ok_pressed = False

        self.setWindowTitle('Регистрация')
        self.setFixedSize(250, 100)

        self.label = QLabel('Логин:', self)
        self.label.move(10, 12)
        self.label.setFixedSize(150, 10)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(154, 20)
        self.client_name.move(70, 10)

        self.label = QLabel('Пароль:', self)
        self.label.move(10, 44)
        self.label.setFixedSize(150, 10)

        self.client_password = QLineEdit(self)
        self.client_password.setFixedSize(154, 20)
        self.client_password.move(70, 40)

        self.btn_ok = QPushButton('Начать', self)
        self.btn_ok.move(10, 70)
        self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(90, 70)
        self.btn_cancel.clicked.connect(qApp.exit)

        self.show()

    def click(self):
        """Обработчик кнопки ОК, если поле вводе не пустое,
        ставим флаг и завершаем приложение."""
        if self.client_name.text():
            self.ok_pressed = True
            qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = UserNameDialog()
    app.exec_()
