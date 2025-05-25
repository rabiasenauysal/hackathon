# main_ui.py (ya da mevcut main.py içindeki MainWindow sınıfınızı aşağıdakilerle değiştirin)
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QFrame, QPushButton, QStackedWidget,
    QHBoxLayout, QVBoxLayout, QLabel
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QIcon, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sınav Sistemi")
        self.setGeometry(100, 100, 1200, 700)

        # --- Merkezi widget ve layout ---
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0,0,0,0)

        # --- Sidebar Frame ---
        self.sidebar = QFrame()
        self.sidebar.setMaximumWidth(200)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #2f2f2f;
            }
        """)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0,0,0,0)
        sidebar_layout.setSpacing(10)

        # Hamburger (toggle) butonu
        self.btn_toggle = QPushButton("☰")
        self.btn_toggle.setFixedSize(40, 40)
        self.btn_toggle.setStyleSheet("""
            QPushButton {
                color: white; background: transparent; font-size: 20pt;
                border: none;
            }
            QPushButton:hover { color: #00aced; }
        """)
        self.btn_toggle.clicked.connect(self.toggle_sidebar)
        sidebar_layout.addWidget(self.btn_toggle, alignment=Qt.AlignLeft)

        # Menü butonları
        self.menu_buttons = []
        pages = [
            ("Ana Panel", "icons/dashboard.png"),
            ("Excel Yükle", "icons/upload.png"),
            ("Veri Görüntüle", "icons/table.png"),
            ("Müfredat", "icons/syllabus.png"),
            ("Sınav Ayarları", "icons/settings.png"),
        ]
        for idx, (text, icon_path) in enumerate(pages):
            btn = QPushButton(f"  {text}")
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(24,24))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    color: white; background: transparent;
                    text-align: left; padding-left: 10px;
                    border: none; font-size: 11pt;
                }
                QPushButton:hover { background-color: #3c3c3c; }
                QPushButton:pressed { background-color: #505050; }
            """)
            btn.clicked.connect(lambda checked, i=idx: self.stack.setCurrentIndex(i))
            sidebar_layout.addWidget(btn)
            self.menu_buttons.append(btn)

        sidebar_layout.addStretch(1)  # en alta esneklik

        # --- Stacked Widget (sayfalar) ---
        self.stack = QStackedWidget()
        # Sayfa örnekleri; gerçek widget’larınızı buraya aktarın:
        for name in ["DashboardPage", "UploadPage", "DataViewer", "SyllabusViewer", "ExamScheduleOptionsPage"]:
            w = QLabel(f"<h2>{name}</h2>", alignment=Qt.AlignCenter)
            self.stack.addWidget(w)

        # --- Ana layout’a ekle ---
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack, stretch=1)

    def toggle_sidebar(self):
        """Sidebar’ı aç/kapat animasyonuyla."""
        new_width = 50 if self.sidebar.maximumWidth() > 100 else 200
        anim = QPropertyAnimation(self.sidebar, b"maximumWidth")
        anim.setDuration(300)
        anim.setStartValue(self.sidebar.maximumWidth())
        anim.setEndValue(new_width)
        anim.setEasingCurve(QEasingCurve.InOutQuart)
        anim.start()
        # Animasyon objesinin scope’a takılmaması için referansı saklıyoruz:
        self._sidebar_anim = anim
