import os
import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog, QLineEdit, QVBoxLayout,
    QHBoxLayout, QFrame, QProgressBar, QGraphicsDropShadowEffect,
    QCheckBox, QSpinBox
)
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class FileProcessor(QThread):
    """Dosya işleme thread'i"""
    progress_updated = pyqtSignal(int)
    processing_finished = pyqtSignal(bool, str)
    
    def __init__(self, file_path, allow_weekend, max_parallel):
        super().__init__()
        self.file_path = file_path
        self.allow_weekend = allow_weekend
        self.max_parallel = max_parallel
        
    def run(self):
        try:
            # Basit simülasyon: ilerlemeyi güncelle
            for pct in (20, 50, 80):
                self.progress_updated.emit(pct)
                self.msleep(300)
            
            if not os.path.exists(self.file_path):
                self.processing_finished.emit(False, "Dosya bulunamadı!")
                return
            
            df = pd.read_excel(self.file_path)
            self.progress_updated.emit(90)
            self.msleep(300)
            
            if df.empty:
                self.processing_finished.emit(False, "Excel dosyası boş!")
                return
            
            # Burada asıl takvim oluşturma kodunuz çalışır
            # Örneğin: scheduler.create_schedule(df, allow_weekend, max_parallel)
            
            self.progress_updated.emit(100)
            self.msleep(200)
            self.processing_finished.emit(True, f"Başarıyla işlendi: {len(df)} satır")
            
        except Exception as e:
            self.processing_finished.emit(False, f"Hata: {str(e)}")

class DragDropArea(QFrame):
    """Sürükle bırak alanı"""
    file_dropped = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFixedHeight(180)
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                border: 3px dashed #bdc3c7;
                border-radius: 12px;
                background: rgba(248, 249, 250, 0.5);
            }
        """)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        lbl = QLabel("📁 Excel (*.xlsx, *.xls)\nSürükle-Bırak veya \"Dosya Seç\"")
        lbl.setFont(QFont("Segoe UI", 12))
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("color: #2c3e50;")
        layout.addWidget(lbl)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            path = event.mimeData().urls()[0].toLocalFile()
            if path.lower().endswith(('.xlsx', '.xls')):
                event.acceptProposedAction()
                self.setStyleSheet(self.styleSheet().replace("#bdc3c7", "#667eea"))
                
    def dragLeaveEvent(self, event):
        self.setStyleSheet(self.styleSheet().replace("#667eea", "#bdc3c7"))
        
    def dropEvent(self, event: QDropEvent):
        path = event.mimeData().urls()[0].toLocalFile()
        self.file_dropped.emit(path)
        self.setStyleSheet(self.styleSheet().replace("#667eea", "#bdc3c7"))

class ModernUploadPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SınavTakvim – Dosya Yükle")
        self.setGeometry(200, 150, 1000, 700)
        self.setMinimumSize(900, 600)
        self.selected_file = ""
        
        self.setStyleSheet("""
            QWidget { background: qlineargradient(
                x1:0,y1:0,x2:1,y2:1,
                stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """)
        
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(40, 30, 40, 30)
        main.setSpacing(20)
        
        # Header: Geri Butonu
        hdr = QHBoxLayout()
        self.back_btn = QPushButton("← Ana Menü")
        self.back_btn.setFixedSize(120, 40)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background:white; color:#6c757d;
                border:2px solid #dee2e6; border-radius:8px;
            }
            QPushButton:hover { color:#667eea; border-color:#667eea; }
        """)
        hdr.addWidget(self.back_btn)
        hdr.addStretch()
        main.addLayout(hdr)
        
        # Content card
        card = QFrame()
        card.setStyleSheet("QFrame{background:white; border-radius:15px;}")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25); shadow.setYOffset(5)
        card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(20)
        
        # Başlık
        title = QLabel("📊 Excel Dosyası Yükle")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        
        sub = QLabel("Öğrenci bilgilerinizi içeren Excel dosyasını seçin ve işleme başlayın")
        sub.setFont(QFont("Segoe UI", 12))
        sub.setAlignment(Qt.AlignCenter)
        sub.setWordWrap(True)
        card_layout.addWidget(sub)
        
        # Drag & Drop alanı
        self.drop_area = DragDropArea()
        card_layout.addWidget(self.drop_area)
        
        # Dosya yol input + buton
        row = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setReadOnly(True)
        self.file_input.setPlaceholderText("Seçilen dosya yolu...")
        self.file_input.setFixedHeight(40)
        row.addWidget(self.file_input)
        self.browse_btn = QPushButton("Dosya Seç")
        self.browse_btn.setFixedSize(120, 40)
        row.addWidget(self.browse_btn)
        card_layout.addLayout(row)
        
        # İlerleme çubuğu ve durum etiketi
        self.progress = QProgressBar()
        self.progress.setFixedHeight(8)
        self.progress.hide()
        card_layout.addWidget(self.progress)
        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.status)
        
        # Ayarlar
        settings = QHBoxLayout()
        self.chk_weekend = QCheckBox("Hafta sonu dahil et")
        self.chk_weekend.setChecked(False)
        settings.addWidget(self.chk_weekend)
        settings.addStretch()
        self.spin_parallel = QSpinBox()
        self.spin_parallel.setRange(1, 16)
        self.spin_parallel.setValue(4)
        self.spin_parallel.setSuffix(" paralel iş")
        settings.addWidget(self.spin_parallel)
        card_layout.addLayout(settings)
        
        # İşlem başlat butonu
        self.start_btn = QPushButton("🛠 İşlem Başlat")
        self.start_btn.setFixedHeight(50)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0,y1:0,x2:1,y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color:white; border:none; border-radius:12px;
                font-size:14px; font-weight:600;
            }
            QPushButton:hover { background: qlineargradient(
                x1:0,y1:0,x2:1,y2:0,
                stop:0 #7c94f4, stop:1 #8b5fbf);
            }
        """)
        card_layout.addWidget(self.start_btn)
        
        main.addWidget(card)
        
    def connect_signals(self):
        self.back_btn.clicked.connect(self.close)
        self.browse_btn.clicked.connect(self.on_browse)
        self.drop_area.file_dropped.connect(self.set_file)
        self.start_btn.clicked.connect(self.on_start)
        
    def on_browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Excel Dosyası Seç", "", "Excel Files (*.xlsx *.xls)"
        )
        if path:
            self.set_file(path)
        
    def set_file(self, path):
        self.selected_file = path
        self.file_input.setText(path)
        self.status.clear()
        
    def on_start(self):
        if not self.selected_file:
            self.status.setText("Lütfen önce dosya seçin.")
            return
        # Thread ile işlemi başlat
        self.progress.show()
        self.progress.setValue(0)
        self.status.setText("İşlem başlatılıyor...")
        
        self.worker = FileProcessor(
            self.selected_file,
            allow_weekend=self.chk_weekend.isChecked(),
            max_parallel=self.spin_parallel.value()
        )
        self.worker.progress_updated.connect(self.progress.setValue)
        self.worker.processing_finished.connect(self.on_finished)
        self.worker.start()
        
    def on_finished(self, success: bool, msg: str):
        self.status.setText(msg)
        if success:
            self.progress.setValue(100)
        else:
            self.progress.hide()

# Eğer bu dosyayı doğrudan çalıştırırsanız, test için açılır:
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = ModernUploadPage()
    win.show()
    sys.exit(app.exec_())
