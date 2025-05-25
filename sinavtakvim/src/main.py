import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import Qt, QSize
from dashboard_page import DashboardPage  # ✅ Ana menüyü çağırmak için

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sınav Sistemi")
        self.setGeometry(100, 100, 960, 540)
        self.setFixedSize(960, 540)

        # 🎞️ Arka plan gif (isteğe bağlı)
        self.bg_label = QLabel(self)
        self.bg_movie = QMovie(r"C:\Users\uysal\OneDrive\Desktop\projects\sinavtakvim\src\giphy.gif")
        self.bg_movie.setScaledSize(QSize(960, 540))
        self.bg_label.setMovie(self.bg_movie)
        self.bg_label.resize(960, 540)
        self.bg_movie.start()

        # Başlık
        self.title = QLabel("SINAV SİSTEMİ", self)
        self.title.setFont(QFont("Georgia", 36, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setGeometry(0, 120, 960, 100)

        # Başla butonu
        self.start_button = QPushButton("BAŞLA", self)
        self.start_button.setGeometry(405, 320, 150, 50)
        self.start_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(0, 0, 0, 0);
                border: 2px solid white;
                font-size: 18pt;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.start_button.clicked.connect(self.go_to_dashboard)

    def go_to_dashboard(self):
        self.dashboard = DashboardPage()
        self.dashboard.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
