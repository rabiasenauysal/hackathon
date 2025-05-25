from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import Qt, QSize

# YENİ: ExamUploadPage ve ExamScheduleOptionsPage'yi ekliyoruz
from exam_schedule_page import ExamUploadPage, ExamScheduleOptionsPage
from upload_page import UploadPage

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sınav Sistemi Paneli")
        self.setGeometry(100, 100, 960, 540)
        self.setFixedSize(960, 540)

        # 🎞️ Arka plan gif
        self.bg_label = QLabel(self)
        self.bg_movie = QMovie(r"C:\Users\uysal\OneDrive\Desktop\projects\sinavtakvim\src\starfall-night-sky-mountains-aesthetic-gif-preview-desktop-wallpaper.gif")
        self.bg_movie.setScaledSize(QSize(960, 540))
        self.bg_label.setMovie(self.bg_movie)
        self.bg_label.resize(960, 540)
        self.bg_movie.start()

        # 🧊 Başlık çerçevesi
        self.title_frame = QLabel(self)
        self.title_frame.setGeometry(180, 30, 600, 70)
        self.title_frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 100);
            border: 2px solid white;
            border-radius: 15px;
        """)

        # ✨ Başlık yazısı (gradyan)
        self.title_label = QLabel("Sınav Sistemi Ana Panel", self.title_frame)
        self.title_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.title_label.setGeometry(0, 0, 600, 70)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                background: none;
                color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a64bf4, stop:1 #45aaff
                );
                border: none;
            }
        """)

        # 🔘 Butonlar
        self.buttons = [
            ("Sınav Takvimi Oluştur", self.open_schedule_creator),
            ("Müfredatı Görüntüle", self.open_syllabus),
            ("Ders Programını Görüntüle", self.open_weekly_schedule),
            ("Hocaları Listele", self.open_instructors),
            ("Dersleri Listele", self.open_courses),
            ("Sınıf Kapasitelerini Görüntüle", self.open_classrooms),
            ("Ders Bazlı Öğrenci Listesi", self.open_students_per_course),
            ("Ortak Ders ve Saatlerini Görüntüle", self.open_common_courses),
        ]

        self.button_widgets = []
        start_y = 120
        for i, (label, action) in enumerate(self.buttons):
            btn = QPushButton(label, self)
            btn.setGeometry(300, start_y + i * 45, 360, 35)
            btn.setFont(QFont("Segoe UI", 11))
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(
                        spread:pad, x1:0, y1:0, x2:1, y2:0,
                        stop:0 #a64bf4, stop:1 #45aaff
                    );
                    color: white;
                    border: 2px solid white;
                    font-size: 14pt;
                    font-weight: bold;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background: qlineargradient(
                        spread:pad, x1:0, y1:0, x2:1, y2:0,
                        stop:0 #b574ff, stop:1 #62c0ff
                    );
                }
            """)
            btn.clicked.connect(action)
            self.button_widgets.append(btn)

    # --- Burası en önemli değişiklik ---
    def open_schedule_creator(self):
        self.upload_page = UploadPage()
        self.upload_page.show()
        self.close()



    def open_exam_options_page(self, file_path):
        gif_path = r"C:\Users\uysal\OneDrive\Desktop\projects\sinavtakvim\src\starfall-night-sky-mountains-aesthetic-gif-preview-desktop-wallpaper.gif"
        self.exam_options_page = ExamScheduleOptionsPage(file_path, gif_path)
        self.exam_options_page.show()
        # Geri tuşları için ExamScheduleOptionsPage içinde bir geri fonksiyonu yazabilirsin
    # --- Diğer fonksiyonlar aynı kalıyor ---
    def open_syllabus(self):
        from syllabus_viewer import SyllabusViewer
        self.syllabus_window = SyllabusViewer()
        self.syllabus_window.show()

    def open_weekly_schedule(self):
        QMessageBox.information(self, "Yönlendirme", "Haftalık Ders Programı açılıyor...")

    def open_instructors(self):
        QMessageBox.information(self, "Yönlendirme", "Hocalar listeleniyor...")

    def open_courses(self):
        QMessageBox.information(self, "Yönlendirme", "Dersler listeleniyor...")

    def open_classrooms(self):
        QMessageBox.information(self, "Yönlendirme", "Sınıf ve kapasiteler gösteriliyor...")

    def open_students_per_course(self):
        QMessageBox.information(self, "Yönlendirme", "Ders bazlı öğrenci listesi yükleniyor...")

    def open_common_courses(self):
        QMessageBox.information(self, "Yönlendirme", "Ortak ders programı açılıyor...")
