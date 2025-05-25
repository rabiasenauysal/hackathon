from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QLineEdit
from PyQt5.QtGui import QFont, QMovie, QPixmap
from PyQt5.QtCore import Qt, QSize
from data_viewer import DataViewer  # ✅ Yeni sayfayı çağırmak için
import os

class UploadPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel Yükleme Sayfası")
        self.setGeometry(100, 100, 960, 540)
        self.setFixedSize(960, 540)
        self.selected_file = ""

        # 🎞️ Arka plan gif
        self.bg_label = QLabel(self)
        self.bg_movie = QMovie(r"C:\Users\uysal\OneDrive\Desktop\projects\sinavtakvim\src\agif1opt.gif")
        self.bg_movie.setScaledSize(QSize(960, 540))
        self.bg_label.setMovie(self.bg_movie)
        self.bg_label.resize(960, 540)
        self.bg_movie.start()

        # Başlık çerçevesi
        self.title_box = QLabel(self)
        self.title_box.setGeometry(180, 40, 600, 60)
        self.title_box.setStyleSheet("""
            background-color: rgba(0, 0, 0, 100);
            border: 2px solid white;
            border-radius: 12px;
        """)

        self.title = QLabel("Excel (.xlsx) dosyanızı yükleyin.", self.title_box)
        self.title.setFont(QFont("Georgia", 16, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setGeometry(0, 0, 600, 60)

        # İkon
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(QPixmap(r"C:\Users\uysal\OneDrive\Desktop\projects\sinavtakvim\src\images.png"))
        self.icon_label.setScaledContents(True)
        self.icon_label.setGeometry((960 - 100) // 2, 225, 100, 100)

        # Gözat + Çubuk
        input_width = 320
        button_width = 80
        spacing = 10
        total_width = input_width + spacing + button_width
        start_x = (960 - total_width) // 2
        input_y = 420

        self.file_input = QLineEdit(self)
        self.file_input.setGeometry(start_x, input_y, input_width, 35)
        self.file_input.setPlaceholderText("Dosya yolu...")
        self.file_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 150);
                border-radius: 8px;
                padding-left: 10px;
                color: black;
            }
        """)

        self.browse_button = QPushButton("Gözat", self)
        self.browse_button.setGeometry(start_x + input_width + spacing, input_y, button_width, 35)
        self.browse_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 150);
                border: 1px solid #999;
                border-radius: 8px;
                color: black;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 200);
            }
        """)
        self.browse_button.clicked.connect(self.select_file)

        # ✅ Yükle butonu
        self.upload_button = QPushButton("YÜKLE", self)
        self.upload_button.setGeometry((960 - 100) // 2, input_y + 60, 100, 40)
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 150, 255, 180);
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 150, 255, 230);
            }
        """)
        self.upload_button.clicked.connect(self.upload_file)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Excel Dosyası Seç", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.selected_file = file_path
            self.file_input.setText(file_path)

    def upload_file(self):
        if os.path.exists(self.selected_file):
            from exam_operations_page import ExamOperationsPage
            self.operations = ExamOperationsPage(self.selected_file)
            self.operations.show()
            self.close()

