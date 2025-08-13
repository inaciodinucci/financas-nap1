import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget, QMessageBox
from PyQt5.QtGui import QPalette, QColor

from .core.db import DatabaseManager
from .ui.login import LoginWindow
from .ui.signup import SignupWindow
from .ui.dashboard import DashboardWindow


class MainApplication:
    """Aplicação principal"""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.db_manager = DatabaseManager()

        self.app.setStyle('Fusion')
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(248, 249, 250))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(51, 51, 51))
        self.app.setPalette(palette)

        self.stacked_widget = QStackedWidget()

        self.login_window = LoginWindow(self.db_manager)
        self.signup_window = SignupWindow(self.db_manager)

        self.login_window.show_signup.connect(self.mostrar_signup)
        self.login_window.login_successful.connect(self.abrir_dashboard)
        self.signup_window.show_login.connect(self.mostrar_login)
        self.signup_window.signup_successful.connect(self.mostrar_login)

        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.signup_window)
        self.stacked_widget.show()

    def mostrar_signup(self):
        self.stacked_widget.setCurrentIndex(1)

    def mostrar_login(self):
        self.stacked_widget.setCurrentIndex(0)
        self.signup_window.nome_input.clear()
        self.signup_window.email_input.clear()
        self.signup_window.senha_input.clear()
        self.signup_window.confirmar_senha_input.clear()

    def abrir_dashboard(self, user_id, nome):
        try:
            self.stacked_widget.hide()
            self.dashboard_window = DashboardWindow(user_id, nome, self.db_manager)
            self.dashboard_window.show()
        except Exception:
            QMessageBox.critical(self.login_window, "Erro", "Erro ao abrir dashboard!")

    def run(self):
        return self.app.exec()


def main():
    try:
        app = MainApplication()
        return app.run()
    except Exception as e:
        print(f"Erro fatal na aplicação: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())


