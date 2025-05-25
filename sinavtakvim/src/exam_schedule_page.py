from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog, QLineEdit, QCheckBox, QSpinBox, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import Qt, QSize
import pandas as pd
import os

class ExamUploadPage(QWidget):
    def __init__(self, next_callback, gif_path=None):
        super().__init__()
        self.setWindowTitle("Sınav Takvimi Dosya Yükle")
        self.setGeometry(200, 200, 960, 540)
        self.setFixedSize(960, 540)
        self.next_callback = next_callback

        # GIF arka plan
        if gif_path:
            self.bg_label = QLabel(self)
            self.bg_movie = QMovie(gif_path)
            self.bg_movie.setScaledSize(QSize(960, 540))
            self.bg_label.setMovie(self.bg_movie)
            self.bg_label.resize(960, 540)
            self.bg_movie.start()

        # Başlık
        self.title = QLabel("Sınav Takvimi için Excel (.xlsx) dosyanızı seçin", self)
        self.title.setFont(QFont("Georgia", 17, QFont.Bold))
        self.title.setStyleSheet("color: white; background: rgba(80,80,80,0.6); border-radius: 12px;")
        self.title.setGeometry(180, 60, 600, 48)
        self.title.setAlignment(Qt.AlignCenter)

        # Dosya seçme alanı
        self.file_input = QLineEdit(self)
        self.file_input.setGeometry(260, 180, 340, 40)
        self.file_input.setPlaceholderText("Dosya yolu...")
        self.file_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255,255,255,0.95);
                border-radius: 8px;
                font-size: 13pt;
            }
        """)
        self.browse_button = QPushButton("Gözat", self)
        self.browse_button.setGeometry(610, 180, 90, 40)
        self.browse_button.setStyleSheet("""
            QPushButton {
                background: #a987e6;
                color: white;
                border-radius: 8px;
                font-size: 13pt;
            }
            QPushButton:hover { background: #6c47c7; }
        """)
        self.browse_button.clicked.connect(self.select_file)

        # Yükle butonu
        self.upload_button = QPushButton("Yükle", self)
        self.upload_button.setGeometry(380, 250, 200, 50)
        self.upload_button.setStyleSheet("""
            QPushButton {
                background: #6c47c7;
                color: white;
                border-radius: 10px;
                font-size: 16pt;
                font-weight: bold;
            }
            QPushButton:hover { background: #a987e6; }
        """)
        self.upload_button.clicked.connect(self.on_upload)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Excel Dosyası Seç", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.file_input.setText(file_path)

    def on_upload(self):
        path = self.file_input.text()
        if os.path.exists(path):
            self.next_callback(path)
        else:
            self.title.setText("Lütfen geçerli bir dosya seçin!")

class ExamScheduleOptionsPage(QWidget):
    def __init__(self, file_path, gif_path=None):
        super().__init__()
        self.setWindowTitle("Sınav Takvimi Oluştur")
        self.setGeometry(180, 120, 1080, 600)
        self.setFixedSize(1080, 600)

        # Arka plan GIF
        if gif_path:
            self.bg_label = QLabel(self)
            self.bg_movie = QMovie(gif_path)
            self.bg_movie.setScaledSize(QSize(1080, 600))
            self.bg_label.setMovie(self.bg_movie)
            self.bg_label.resize(1080, 600)
            self.bg_movie.start()

        # Başlık
        self.title = QLabel("Sınav Takvimi Ayarları", self)
        self.title.setFont(QFont("Georgia", 20, QFont.Bold))
        self.title.setStyleSheet("color: white; background: rgba(90,50,150,0.7); border-radius: 15px;")
        self.title.setGeometry(300, 30, 480, 55)
        self.title.setAlignment(Qt.AlignCenter)

        # Hafta sonu kutusu
        self.weekend_checkbox = QCheckBox("Hafta sonu sınav yapılsın mı?", self)
        self.weekend_checkbox.setFont(QFont("Segoe UI", 14))
        self.weekend_checkbox.setStyleSheet("color: white; background: rgba(60,60,80,0.4); border-radius: 8px;")
        self.weekend_checkbox.setGeometry(340, 110, 400, 44)

        # Maksimum günlük sınav sayısı
        self.max_exam_label = QLabel("Bir öğrencinin girebileceği maksimum günlük sınav:", self)
        self.max_exam_label.setFont(QFont("Segoe UI", 13))
        self.max_exam_label.setStyleSheet("color: white; background: rgba(60,60,80,0.2); border-radius: 7px;")
        self.max_exam_label.setGeometry(290, 170, 500, 40)
        self.max_exam_spinbox = QSpinBox(self)
        self.max_exam_spinbox.setGeometry(800, 170, 70, 40)
        self.max_exam_spinbox.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.max_exam_spinbox.setMinimum(1)
        self.max_exam_spinbox.setMaximum(6)
        self.max_exam_spinbox.setValue(2)

        # Tabloda göster butonu
        self.show_table_button = QPushButton("Yüklenen Dosyayı Tablo Olarak Gör", self)
        self.show_table_button.setGeometry(370, 230, 340, 44)
        self.show_table_button.setStyleSheet("""
            QPushButton {
                background: #f5f3fc;
                color: #5b2cb5;
                border-radius: 8px;
                font-size: 13pt;
                font-weight: bold;
                border: 2px solid #6c47c7;
            }
            QPushButton:hover { background: #e1dbfa; }
        """)
        self.show_table_button.clicked.connect(self.show_table)

        # Kocaman "Sınav Takvimi Oluştur" butonu
        self.create_button = QPushButton("SINAV TAKVİMİ OLUŞTUR", self)
        self.create_button.setGeometry(220, 330, 620, 70)
        self.create_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a987e6, stop:1 #6c47c7
                );
                color: white;
                border-radius: 18px;
                font-size: 27pt;
                font-weight: bold;
                border: 4px solid #fff;
                box-shadow: 0 8px 28px #333;
            }
            QPushButton:hover {
                background: #dfc8fc;
                color: #6c47c7;
                border: 4px solid #6c47c7;
            }
        """)
        self.create_button.clicked.connect(self.create_schedule)

        # Tablo önizleme widget'ı (saklı)
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(90, 430, 900, 120)
        self.table_widget.hide()
        self.loaded_file_path = file_path

    def show_table(self):
        try:
            df = pd.read_excel(self.loaded_file_path)
            self.table_widget.setRowCount(len(df))
            self.table_widget.setColumnCount(len(df.columns))
            self.table_widget.setHorizontalHeaderLabels(df.columns)
            for i in range(len(df)):
                for j in range(len(df.columns)):
                    value = df.iloc[i, j]
                    self.table_widget.setItem(i, j, QTableWidgetItem("" if pd.isna(value) else str(value)))
            self.table_widget.show()
        except Exception as e:
            self.table_widget.hide()

    def create_schedule(self):
        # Burada parametreleri al, algoritmaya gönder (örnek):
        weekend = self.weekend_checkbox.isChecked()
        max_daily = self.max_exam_spinbox.value()
        print("Sınav Takvimi Oluşturuluyor!\nHafta sonu:", weekend, "Max günlük sınav:", max_daily)
        # ... algoritma kısmına bağla ...
