from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import Qt, QSize
from exam_scheduler import read_input_files, assign_exams, save_schedule

class ExamOperationsPage(QWidget):
    def __init__(self, file_path):
        super().__init__()
        self.setWindowTitle("Sınav Takvimi: İşlemler")
        self.setGeometry(100, 100, 960, 540)
        self.setFixedSize(960, 540)
        self.file_path = file_path

        # Arka plan GIF (isteğe bağlı)
        self.bg_label = QLabel(self)
        self.bg_movie = QMovie(r"C:\Users\uysal\OneDrive\Desktop\projects\sinavtakvim\src\starfall-night-sky-mountains-aesthetic-gif-preview-desktop-wallpaper.gif")
        self.bg_movie.setScaledSize(QSize(960, 540))
        self.bg_label.setMovie(self.bg_movie)
        self.bg_label.resize(960, 540)
        self.bg_movie.start()

        # Başlık
        self.title = QLabel("Devam Etmek İçin Bir İşlem Seçin", self)
        self.title.setFont(QFont("Georgia", 20, QFont.Bold))
        self.title.setStyleSheet("color: white; background: rgba(80,80,80,0.7); border-radius: 16px;")
        self.title.setGeometry(200, 45, 560, 50)
        self.title.setAlignment(Qt.AlignCenter)

        # --- Butonlar ---
        btn_y = 140
        btn_gap = 65

        # 1. Dosya görüntüle
        self.view_btn = QPushButton("Yüklenen Dosyayı Görüntüle", self)
        self.view_btn.setGeometry(300, btn_y, 360, 50)
        self.view_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.view_btn.setStyleSheet("""
            QPushButton {
                background-color: #a987e6;
                color: white;
                border-radius: 10px;
                font-size: 14pt;
                border: 2px solid #6c47c7;
            }
            QPushButton:hover { background-color: #6c47c7; }
        """)
        self.view_btn.clicked.connect(self.open_data_viewer)

        # 2. Sınav Takvimi Oluştur
        self.schedule_btn = QPushButton("Sınav Takvimi Oluştur", self)
        self.schedule_btn.setGeometry(300, btn_y + btn_gap, 360, 50)
        self.schedule_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.schedule_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a987e6, stop:1 #6c47c7
                );
                color: white;
                border-radius: 12px;
                font-size: 15pt;
                border: 2px solid #fff;
            }
            QPushButton:hover {
                background: #dfc8fc;
                color: #6c47c7;
                border: 2px solid #6c47c7;
            }
        """)
        self.schedule_btn.clicked.connect(self.create_schedule)

        # 3. (Opsiyonel) Ana Menüye Dön
        self.back_btn = QPushButton("Ana Menüye Dön", self)
        self.back_btn.setGeometry(300, btn_y + 2*btn_gap, 360, 45)
        self.back_btn.setFont(QFont("Segoe UI", 12))
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #fff;
                color: #a987e6;
                border-radius: 9px;
                font-size: 13pt;
                border: 2px solid #a987e6;
            }
            QPushButton:hover { background-color: #f8fafd; color: #6c47c7; }
        """)
        self.back_btn.clicked.connect(self.go_dashboard)

    def open_data_viewer(self):
        from data_viewer import DataViewer
        self.viewer = DataViewer(self.file_path)
        self.viewer.show()

    def create_schedule(self):
        # Burada kendi sınav takvimi algoritma arayüzüne yönlendirebilirsin
        print("Sınav Takvimi Oluşturuluyor...")  # Placeholder

    def go_dashboard(self):
        from dashboard_page import DashboardPage
        self.dashboard = DashboardPage()
        self.dashboard.show()
        self.close()

    def create_schedule(self):
        ogrenci_file = self.file_path
        salon_file = r"C:\Users\uysal\OneDrive\Desktop\projects\sinavtakvim\data\raw\a.docx"
        ogrenci_df, salon_df = read_input_files(ogrenci_file, salon_file)
        takvim_df = assign_exams(
            ogrenci_df, salon_df,
            start_date="2025-06-01",
            end_date="2025-06-14",
            slot_hours=[9, 12, 15],
            max_daily_exams=2,
            include_weekends=True
        )
        save_schedule(takvim_df)
        # Sonra kullanıcıya bilgi mesajı: sınav_takvimi.xlsx kaydedildi!
