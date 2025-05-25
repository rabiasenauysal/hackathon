from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QFileDialog, QFrame, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer  # QTimer eklendi!
import pandas as pd
import os

class SyllabusViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Müfredat Görüntüleyici")
        self.setStyleSheet("background-color: #f8fafd;")
        self.resize(1300, 800)
        self._first_show = True
        self.initUI()

        default_path = r"C:\Users\uysal\OneDrive\Desktop\projects\sinavtakvim\data\raw\müfredat.xlsx"
        self.load_syllabus(default_path)

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

        info_row = QHBoxLayout()
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
        info_row.addWidget(self.back_button)
        info_row.addSpacing(5)

        self.info_box = QFrame()
        self.info_box.setFixedHeight(52)
        self.info_box.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a0d8ef, stop:1 #cbb4f6
                );
                border-radius: 12px;
                border: 2px solid #7d57c5;
            }
        """)
        info_layout = QHBoxLayout(self.info_box)
        info_layout.setContentsMargins(15, 0, 0, 0)
        icon = QLabel()
        icon.setPixmap(QPixmap("icons/info.png").scaled(28, 28, Qt.KeepAspectRatio))
        info_layout.addWidget(icon)
        self.info_label = QLabel("")
        self.info_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.info_label.setStyleSheet("color: #333; margin-left: 14px;")
        info_layout.addWidget(self.info_label)
        info_layout.addStretch(1)
        info_row.addWidget(self.info_box)

        self.upload_button = QPushButton("Yeni Müfredat Yükle ↓")
        self.upload_button.setFixedWidth(210)
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #6c47c7;
                color: white;
                border-radius: 9px;
                font-weight: bold;
                font-size: 10.5pt;
                padding: 7px 12px 7px 12px;
            }
            QPushButton:hover {
                background-color: #a987e6;
            }
        """)
        self.upload_button.clicked.connect(self.select_new_file)
        info_row.addWidget(self.upload_button)
        info_row.addStretch(1)
        self.layout.addLayout(info_row)

        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

    def go_back(self):
        self.close()

    def load_syllabus(self, file_path):
        if not os.path.exists(file_path):
            self.info_label.setText("Müfredat dosyası bulunamadı.")
            return

        try:
            df_raw = pd.read_excel(file_path, header=None)
            final_rows = []
            kodu_indices = df_raw[df_raw.apply(
                lambda row: row.astype(str).str.contains("Kodu", case=False).any(), axis=1)].index

            if len(kodu_indices) == 0:
                self.info_label.setText("Geçerli başlık (Kodu...) bulunamadı.")
                return

            for idx in kodu_indices:
                yarıyıl_label = "Bilinmeyen"
                for i in range(1, 6):
                    if idx - i >= 0:
                        cell = str(df_raw.iloc[idx - i, 0]).strip().upper()
                        if "YARIYIL" in cell:
                            yarıyıl_label = cell.title()
                            break

                headers = [str(h).strip() for h in df_raw.iloc[idx].tolist()]
                next_idx = kodu_indices[kodu_indices.get_loc(idx) + 1] if kodu_indices.get_loc(idx) + 1 < len(kodu_indices) else len(df_raw)

                for i in range(idx + 1, next_idx):
                    row = df_raw.iloc[i].tolist()
                    if not any(pd.notna(x) for x in row):
                        continue
                    if isinstance(row[0], str) and any(keyword in row[0].upper() for keyword in ["YIL", "YARIYIL", "TOPLAM", "KODU"]):
                        continue

                    row_dict = {headers[j]: row[j] for j in range(len(headers)) if j < len(row)}
                    row_dict["Yarıyıl"] = yarıyıl_label
                    final_rows.append(row_dict)

            if not final_rows:
                self.info_label.setText("Hiçbir uygun veri satırı bulunamadı.")
                return

            df = pd.DataFrame(final_rows)
            df.dropna(how="all", inplace=True)
            df.dropna(axis=1, how="all", inplace=True)
            df = df.loc[:, [str(c).lower() != 'nan' for c in df.columns]]

            if "Yarıyıl" in df.columns:
                cols = list(df.columns)
                cols.remove("Yarıyıl")
                cols.append("Yarıyıl")
                df = df[cols]

            self.update_table(df)
            filename = os.path.basename(file_path)
            self.info_label.setText(
                f"<b>{filename}</b> müfredatı görüntüleniyor.<br>Farklı dosya için <b>'Yeni Müfredat Yükle'</b> butonunu kullanabilirsin."
            )
        except Exception as e:
            self.info_label.setText(f"Hata: {str(e)}")

    def update_table(self, df):
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
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
        QTimer.singleShot(0, self.adjust_table_columns)  # <- En garanti yol!

    def adjust_table_columns(self):
        if self.table.columnCount() > 0:
            w = self.table.viewport().width()
            col_width = int(w / self.table.columnCount()) - 2
            for i in range(self.table.columnCount()):
                self.table.setColumnWidth(i, col_width)

    def select_new_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Yeni Müfredat Seç", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.load_syllabus(file_path)
            self.showMaximized()
            QTimer.singleShot(0, self.adjust_table_columns)
