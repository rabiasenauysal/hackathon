from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
import pandas as pd
import os

class DataViewer(QWidget):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.setWindowTitle("Excel Verisi")
        self.setStyleSheet("background-color: #f8fafd;")
        self.resize(1300, 800)
        self._first_show = True
        self.initUI()

    def showEvent(self, event):
        super().showEvent(event)
        if self._first_show:
            self._first_show = False
            self.showNormal()
            self.showMaximized()
            QTimer.singleShot(0, self.adjust_table_columns)

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 18, 24, 24)
        self.layout.setSpacing(14)

        # Üst satır: Geri ve başlık
        top_row = QHBoxLayout()
        self.back_button = QPushButton("← Geri")
        self.back_button.setFixedWidth(85)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #e1dbfa;
                color: #5b2cb5;
                border-radius: 7px;
                font-weight: bold;
                font-size: 10.2pt;
            }
            QPushButton:hover {
                background-color: #d1c4e9;
            }
        """)
        self.back_button.clicked.connect(self.go_back)
        top_row.addWidget(self.back_button)
        top_row.addSpacing(10)

        self.title = QLabel("Excel Verisi Görüntüleme")
        self.title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.title.setStyleSheet("color: #333;")
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        top_row.addWidget(self.title)
        top_row.addStretch(1)
        self.layout.addLayout(top_row)

        # Dataframe okuma ve doldurma
        try:
            df = pd.read_excel(self.file_path)
            # Sınıf sütunundaki nan değerlerini yukarıdan doldur (forward fill)
            if "Sınıf" in df.columns:
                df["Sınıf"] = df["Sınıf"].fillna(method="ffill")
            # Başka bir sütunda da forward fill istersen benzer şekilde ekle
        except Exception as e:
            self.error_label = QLabel(f"Hata: {str(e)}", self)
            self.error_label.setStyleSheet("color: red; font-size: 12pt;")
            self.layout.addWidget(self.error_label)
            return

        # Tablo widget'ı
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df))
        self.table.setHorizontalHeaderLabels([str(c) for c in df.columns])
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #f5f3fc;
                background-color: white;
                font-size: 11pt;
                border: 1.5px solid #a987e6;
            }
            QHeaderView::section {
                background-color: #6c47c7;
                color: white;
                font-weight: bold;
                font-size: 11pt;
                padding: 4px;
            }
        """)

        for i in range(len(df)):
            for j in range(len(df.columns)):
                value = df.iloc[i, j]
                self.table.setItem(i, j, QTableWidgetItem("" if pd.isna(value) else str(value)))

        QTimer.singleShot(0, self.adjust_table_columns)

    def adjust_table_columns(self):
        if self.table.columnCount() > 0:
            w = self.table.viewport().width()
            col_width = int(w / self.table.columnCount()) - 2
            for i in range(self.table.columnCount()):
                self.table.setColumnWidth(i, col_width)

    def go_back(self):
        from upload_page import UploadPage
        self.back = UploadPage()
        self.back.show()
        self.close()
