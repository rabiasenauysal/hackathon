import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QGraphicsDropShadowEffect, QStackedWidget, QScrollArea
)
from PyQt5.QtGui import QFont, QMovie, QPainter, QLinearGradient, QColor, QPen
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect, QParallelAnimationGroup

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        
        # Hover animasyonu için
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #667eea, stop: 1 #764ba2);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 600;
                padding: 12px 20px;
                text-align: left;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #7c94f4, stop: 1 #8b5fbf);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #5a6fd8, stop: 1 #6b4c93);
            }
        """)

class ModernSidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(280)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2c3e50, stop: 1 #34495e);
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }
        """)
        
        # Gölge efekti
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(3)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setSpacing(20)
        
        # Logo/Başlık alanı
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 10);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 20);
            }
        """)
        
        header_layout = QVBoxLayout(header)
        
        title = QLabel("SınavTakvim")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: white; background: none; border: none;")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Profesyonel Sınav Planlama")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #bdc3c7; background: none; border: none;")
        subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)
        
        # Ana menü bölümü
        menu_label = QLabel("ANA MENÜ")
        menu_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        menu_label.setStyleSheet("color: #95a5a6; background: none; border: none; margin-top: 10px;")
        layout.addWidget(menu_label)
        
        # Ana menü butonları
        self.main_buttons = [
            ("🎯 Sınav Takvimi Oluştur", "Ana özellik - Excel dosyası yükleyerek otomatik sınav takvimi oluşturun"),
            ("📊 Müfredatı Görüntüle", "Yüklenmiş müfredat bilgilerini inceleyin"),
            ("📅 Haftalık Program", "Haftalık ders programını görüntüleyin"),
        ]
        
        for text, tooltip in self.main_buttons:
            btn = AnimatedButton(text)
            btn.setToolTip(tooltip)
            layout.addWidget(btn)
        
        # Yardımcı araçlar bölümü
        tools_label = QLabel("YARDIMCI ARAÇLAR")
        tools_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        tools_label.setStyleSheet("color: #95a5a6; background: none; border: none; margin-top: 20px;")
        layout.addWidget(tools_label)
        
        self.tool_buttons = [
            ("👨‍🏫 Öğretim Görevlileri", "Öğretim görevlisi listesini görüntüleyin"),
            ("📚 Ders Listesi", "Tüm dersleri listeleyin"),
            ("🏛️ Sınıf Kapasiteleri", "Sınıf kapasitelerini kontrol edin"),
            ("👥 Öğrenci Listeleri", "Ders bazlı öğrenci listelerini görün"),
        ]
        
        for text, tooltip in self.tool_buttons:
            btn = AnimatedButton(text)
            btn.setToolTip(tooltip)
            btn.setStyleSheet(btn.styleSheet().replace("667eea", "95a5a6").replace("764ba2", "7f8c8d"))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Alt bilgi
        info_frame = QFrame()
        info_frame.setFixedHeight(60)
        info_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 5);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 10);
            }
        """)
        
        info_layout = QVBoxLayout(info_frame)
        version = QLabel("v2.0 - Modern UI")
        version.setFont(QFont("Segoe UI", 8))
        version.setStyleSheet("color: #7f8c8d; background: none; border: none;")
        version.setAlignment(Qt.AlignCenter)
        
        author = QLabel("© 2024 SınavTakvim")
        author.setFont(QFont("Segoe UI", 8))
        author.setStyleSheet("color: #7f8c8d; background: none; border: none;")
        author.setAlignment(Qt.AlignCenter)
        
        info_layout.addWidget(version)
        info_layout.addWidget(author)
        
        layout.addWidget(info_frame)

class WelcomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # Hoş geldin başlığı
        welcome_frame = QFrame()
        welcome_frame.setFixedHeight(120)
        welcome_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #667eea, stop: 1 #764ba2);
                border-radius: 20px;
            }
        """)
        
        welcome_layout = QVBoxLayout(welcome_frame)
        
        title = QLabel("Hoş Geldiniz! 👋")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet("color: white; background: none;")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Profesyonel sınav takvimi oluşturma sistemi")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 180); background: none;")
        subtitle.setAlignment(Qt.AlignCenter)
        
        welcome_layout.addWidget(title)
        welcome_layout.addWidget(subtitle)
        
        layout.addWidget(welcome_frame)
        
        # Özellikler kartları
        features_layout = QHBoxLayout()
        
        features = [
            ("🎯", "Otomatik Planlama", "Excel dosyanızı yükleyin, sistem otomatik olarak en uygun sınav takvimini oluştursun"),
            ("⚡", "Hızlı İşlem", "Karmaşık algoritmalarla saniyeler içinde optimum sonuç alın"),
            ("📊", "Detaylı Analiz", "Sınav dağılımları, çakışma analizi ve kapsamlı raporlar")
        ]
        
        for icon, title, desc in features:
            card = self.create_feature_card(icon, title, desc)
            features_layout.addWidget(card)
        
        layout.addLayout(features_layout)
        
        # Başlama butonu
        start_button = QPushButton("🚀 Sınav Takvimi Oluşturmaya Başla")
        start_button.setFixedHeight(60)
        start_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        start_button.setCursor(Qt.PointingHandCursor)
        start_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #ff6b6b, stop: 1 #ee5a24);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #ff7979, stop: 1 #fd79a8);
            }
        """)
        
        layout.addWidget(start_button)
        layout.addStretch()
        
    def create_feature_card(self, icon, title, description):
        card = QFrame()
        card.setFixedHeight(180)
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                border: 1px solid #e0e6ed;
            }
            QFrame:hover {
                border: 1px solid #667eea;
            }
        """)
        
        # Gölge efekti
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 30))
        card.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI", 32))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("background: none; border: none;")
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; background: none; border: none;")
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 10))
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #7f8c8d; background: none; border: none; line-height: 1.4;")
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        
        return card

class ModernDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SınavTakvim - Profesyonel Sınav Planlama Sistemi")
        self.setGeometry(100, 100, 1400, 800)
        self.setMinimumSize(1200, 700)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #f8f9fa, stop: 1 #e9ecef);
            }
        """)
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.sidebar = ModernSidebar()
        main_layout.addWidget(self.sidebar)
        
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet("background: transparent; border: none;")
        self.welcome_page = WelcomeWidget()
        self.content_area.addWidget(self.welcome_page)
        main_layout.addWidget(self.content_area)
        
    def connect_signals(self):
        sidebar_buttons = self.sidebar.findChildren(AnimatedButton)
        if len(sidebar_buttons) >= 1:
            sidebar_buttons[0].clicked.connect(self.open_exam_scheduler)
        if len(sidebar_buttons) >= 2:
            sidebar_buttons[1].clicked.connect(self.open_syllabus_viewer)
        if len(sidebar_buttons) >= 3:
            sidebar_buttons[2].clicked.connect(self.show_weekly_schedule)
        
        start_buttons = self.welcome_page.findChildren(QPushButton)
        if start_buttons:
            start_buttons[0].clicked.connect(self.open_exam_scheduler)
    
    def open_exam_scheduler(self):
        from b import ModernUploadPage  # Dosya ismi doğrudan belirtiliyor
        self.upload_page = ModernUploadPage()
        self.upload_page.show()

        
    def open_syllabus_viewer(self):
        from syllabus_viewer import SyllabusViewer
        self.syllabus_window = SyllabusViewer()
        self.syllabus_window.show()
        
    def show_weekly_schedule(self):
        print("Haftalık program açılıyor...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = ModernDashboard()
    dashboard.show()
    sys.exit(app.exec_())
