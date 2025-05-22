import os
import csv
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QCheckBox, QComboBox, QHeaderView,
    QMessageBox, QDialog
)
from PyQt5.QtGui import QIcon

from detay_duzenle_dialog import DetayDuzenleDialog
from veritabani import kayitlari_oku, turleri_oku_csv

class TabloPage(QWidget):
    kayitGuncellendi = pyqtSignal()

    def __init__(self, kullaniciAdi, durum, puanFiltre=True, parent=None):
        super().__init__(parent)
        self.kullaniciAdi = kullaniciAdi
        self.durum = durum
        self.puanFiltre = puanFiltre
        self.allData = []

        self.setStyleSheet("""
            QWidget {
                background: qradialgradient(
                    cx:0.5, cy:0.5, radius:1,
                    fx:0.2, fy:0.3,
                    stop:0 #0C0C38,
                    stop:1 #050516
                );
            }
        """)

        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Dizi/Film", "Tür", "Ad", "İlerleme", "Puan", "Not", "Detay/Düzenle"])
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSortingEnabled(False)
        self.table.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table.setStyleSheet("""
            QTableWidget {
                color: white;
                font-size: 14px;
                background: transparent;
            }
            QHeaderView::section {
                background-color: #b4342f;
                color: white;
                font-size: 15px;
                font-weight: bold;
                border: none;
            }
            QPushButton {
                background: transparent;
                border: none;
            }
        """)

        mainLayout.addWidget(self.table, 3)

        # Filtre Paneli
        self.filterWidget = self.buildFilterPanel()
        mainLayout.addWidget(self.filterWidget, 1)

        self.loadData()

    def buildFilterPanel(self):

        panel = QWidget()
        panel.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 #b4342f,
                    stop:1 #620c0c
                );
                border-radius: 20px;
            }
        """)
        vLayout = QVBoxLayout(panel)
        vLayout.setContentsMargins(10, 10, 10, 10)
        vLayout.setSpacing(8)

        # İsme göre arama
        lblArama = QLabel("İsme göre arama")
        lblArama.setStyleSheet("color:white; font-size:14px; background:transparent")
        self.lineSearch = QLineEdit()
        self.lineSearch.setPlaceholderText("Arama...")
        self.lineSearch.setStyleSheet("background:white; color:black; border-radius:6px; padding:4px;")
        self.lineSearch.textChanged.connect(self.applyFilter)
        vLayout.addWidget(lblArama)
        vLayout.addWidget(self.lineSearch)

        # Dizi/Film Checkbox
        self.chkDizi = QCheckBox("Dizi")
        self.chkFilm = QCheckBox("Film")
        for chk in [self.chkDizi, self.chkFilm]:
            chk.setStyleSheet("color:white; font-size:14px; background:transparent")
            chk.stateChanged.connect(self.applyFilter)
        vLayout.addWidget(self.chkDizi)
        vLayout.addWidget(self.chkFilm)

        # Tür Combobox
        lblTur = QLabel("Tür...")
        lblTur.setStyleSheet("color:white; font-size:14px; background:transparent")
        self.cmbTur = QComboBox()
        self.cmbTur.setStyleSheet("background:white; color:black; border-radius:6px; padding:4px;")
        self.cmbTur.addItem("Hepsi")
        for tur in turleri_oku_csv():
            self.cmbTur.addItem(tur)
        self.cmbTur.currentIndexChanged.connect(self.applyFilter)
        vLayout.addWidget(lblTur)
        vLayout.addWidget(self.cmbTur)

        # Puan Combobox (isteğe bağlı)
        if self.puanFiltre:
            lblPuan = QLabel("Puana göre")
            lblPuan.setStyleSheet("color:white; font-size:14px; background:transparent")
            self.cmbPuan = QComboBox()
            self.cmbPuan.setStyleSheet("background:white; color:black; border-radius:6px; padding:4px;")
            self.cmbPuan.addItem("Hepsi")
            self.cmbPuan.addItem("1+ (>=1)")
            self.cmbPuan.addItem("2+ (>=2)")
            self.cmbPuan.addItem("3+ (>=3)")
            self.cmbPuan.addItem("4+ (>=4)")
            self.cmbPuan.addItem("5 (==5)")
            self.cmbPuan.currentIndexChanged.connect(self.applyFilter)
            vLayout.addWidget(lblPuan)
            vLayout.addWidget(self.cmbPuan)

        # Bölüm sayısı SpinBox
        lblBolum = QLabel("Bölüm sayısına göre (x/y)")
        lblBolum.setStyleSheet("color:white; font-size:14px; background:transparent")
        self.lineBolum = QLineEdit()
        self.lineBolum.setPlaceholderText("Bölüm sayısı...")
        self.lineBolum.setStyleSheet("background:white; color:black; border-radius:6px; padding:4px;")
        self.lineBolum.textChanged.connect(self.applyFilter)
        vLayout.addWidget(lblBolum)
        vLayout.addWidget(self.lineBolum)

        # Eklenme sırasına göre
        self.chkEklenme = QCheckBox("Eklenme sırasına göre")
        self.chkEklenme.setStyleSheet("color:white; font-size:14px; background:transparent")
        self.chkEklenme.stateChanged.connect(self.applyFilter)
        vLayout.addWidget(self.chkEklenme)

        vLayout.addStretch()
        return panel

    def loadData(self):
        self.allData = kayitlari_oku(self.kullaniciAdi, durum=self.durum)
        self.applyFilter()

    def applyFilter(self):

        textS = self.lineSearch.text().lower().strip()
        diziC = self.chkDizi.isChecked()
        filmC = self.chkFilm.isChecked()
        turSec = self.cmbTur.currentText()
        puanSec = self.cmbPuan.currentText() if self.puanFiltre else None
        bolumVal = self.lineBolum.text().strip()
        eklenmeC = self.chkEklenme.isChecked()

        filtered = []
        for row in self.allData:
            # Filtre 1: İsme göre arama
            if textS and textS not in row["Ad"].lower():
                continue

            # Filtre 2: Dizi/Film
            df = row["Dizi/Film"].lower()
            if diziC and filmC:
                pass
            elif diziC and not filmC:
                if df != "dizi":
                    continue
            elif filmC and not diziC:
                if df != "film":
                    continue

            # Filtre 3: Tür
            if turSec != "Hepsi":
                if turSec.lower() not in row["Tür"].lower():
                    continue

            # Filtre 4: Puan
            if self.puanFiltre and puanSec != "Hepsi":
                p = row["Puan"]
                try:
                    p = int(p)
                except:
                    p = 0
                if puanSec.startswith("1+"):
                    if p < 1:
                        continue
                elif puanSec.startswith("2+"):
                    if p < 2:
                        continue
                elif puanSec.startswith("3+"):
                    if p < 3:
                        continue
                elif puanSec.startswith("4+"):
                    if p < 4:
                        continue
                elif puanSec.startswith("5"):
                    if p != 5:
                        continue

            # Filtre 5: Bölüm sayısı
            if bolumVal:
                try:
                    bolum = int(bolumVal)
                    ilerleme = row["İlerleme"]
                    parts = ilerleme.split("/")
                    if len(parts) == 2:
                        x = int(parts[0])
                        y = int(parts[1])
                        if y != bolum:
                            continue
                except:
                    pass

            filtered.append(row)

        # Eklenme sırasına göre
        if eklenmeC:
            filtered = filtered[::-1]

        self.populateTable(filtered)

    def populateTable(self, data):

        self.table.setRowCount(len(data))
        for rowIndex, row in enumerate(data):
            # Sütun 0: Dizi/Film
            itemDf = QTableWidgetItem(row["Dizi/Film"])
            itemDf.setTextAlignment(Qt.AlignCenter)
            itemDf.setFlags(itemDf.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(rowIndex, 0, itemDf)

            # Sütun 1: Tür
            itemTur = QTableWidgetItem(row["Tür"])
            itemTur.setFlags(itemTur.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(rowIndex, 1, itemTur)

            # Sütun 2: Ad
            itemAd = QTableWidgetItem(row["Ad"])
            itemAd.setFlags(itemAd.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(rowIndex, 2, itemAd)

            # Sütun 3: İlerleme
            itemIler = QTableWidgetItem(row["İlerleme"])
            itemIler.setTextAlignment(Qt.AlignCenter)
            itemIler.setFlags(itemIler.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(rowIndex, 3, itemIler)

            # Sütun 4: Puan
            try:
                p = int(row["Puan"])
            except:
                p = 0
            stars = "★" * p + "☆" * (5 - p)
            itemPuan = QTableWidgetItem(stars)
            itemPuan.setTextAlignment(Qt.AlignCenter)
            itemPuan.setFlags(itemPuan.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(rowIndex, 4, itemPuan)

            # Sütun 5: Not
            noteShort = row["Not"]
            if len(noteShort) > 30:
                noteShort = noteShort[:30] + "..."
            itemNot = QTableWidgetItem(noteShort)
            itemNot.setFlags(itemNot.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(rowIndex, 5, itemNot)

            # Sütun 6: Detay/Düzenle
            btnDetay = QPushButton()
            btnDetay.setIcon(QIcon("iconlar/edit_icon.png"))
            btnDetay.setStyleSheet("background: transparent; border: none;")
            btnDetay.clicked.connect(lambda checked, r=row: self.openDetay(r))
            self.table.setCellWidget(rowIndex, 6, btnDetay)

        self.table.resizeColumnsToContents()

    def openDetay(self, kayit):
        dlg = DetayDuzenleDialog(kayit, self)
        dlg.kayitGuncellendi.connect(self.kayitGuncellendi.emit)
        if dlg.exec_() == QDialog.Accepted:
            self.loadData()

    def onHeaderClicked(self, logicalIndex):
        currentOrder = self.table.horizontalHeader().sortIndicatorOrder()
        if currentOrder == Qt.AscendingOrder:
            newOrder = Qt.DescendingOrder
        else:
            newOrder = Qt.AscendingOrder
        self.table.sortItems(logicalIndex, newOrder)
