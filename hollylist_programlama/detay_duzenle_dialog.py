import os
import csv
from PyQt5.QtCore import Qt, pyqtSignal, QRegularExpression
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QComboBox, QWidget, QCheckBox, QMessageBox, QScrollArea, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QIcon, QRegularExpressionValidator

from star_rating_widget import StarRatingWidget
from veritabani import kayit_guncelle, turleri_oku_csv


class DetayDuzenleDialog(QDialog):
    kayitGuncellendi = pyqtSignal()

    def __init__(self, kayit, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detay / Düzenle")
        self.setFixedSize(620, 975)

        self.kayit = dict(kayit)
        self.originalDurum = kayit["Durum"]
        self.originalDf = kayit["Dizi/Film"]

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Afiş
        self.lblAfis = QLabel()
        self.lblAfis.setFixedSize(150, 220)
        self.lblAfis.setStyleSheet("background: #333; border-radius:5px;")
        if os.path.exists(self.kayit["Afiş"]):
            pix = QPixmap(self.kayit["Afiş"]).scaled(
                self.lblAfis.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.lblAfis.setPixmap(pix)
        self.layout.addWidget(self.lblAfis, alignment=Qt.AlignCenter)

        # Form Alanları
        formLayout = QVBoxLayout()

        lblAd = QLabel("Ad:")
        lblAd.setStyleSheet("color:white; font-size:16px;")
        self.lineAd = QLineEdit(self.kayit["Ad"])
        self.lineAd.setStyleSheet("""
            QLineEdit {
                background: white;
                color: black;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #fa3c4c;
            }
        """)
        formLayout.addWidget(lblAd)
        formLayout.addWidget(self.lineAd)

        lblTur = QLabel("Tür:")
        lblTur.setStyleSheet("color:white; font-size:16px;")
        self.turScrollArea = QScrollArea()
        self.turScrollArea.setWidgetResizable(True)
        self.turScrollArea.setFixedHeight(100)
        self.turContainer = QWidget()
        self.turLayout = QHBoxLayout(self.turContainer)
        self.turLayout.setContentsMargins(5, 5, 5, 5)
        self.turLayout.setSpacing(5)
        self.turScrollArea.setWidget(self.turContainer)
        formLayout.addWidget(lblTur)
        formLayout.addWidget(self.turScrollArea)

        # Mevcut türleri ekle
        self.currentTurler = []
        splitted = self.kayit["Tür"].replace(",", "/").split("/")
        for t in splitted:
            t = t.strip()
            if t:
                self.currentTurler.append(t)
                self.addTurChip(t)

        # Tür ekleme butonu
        turAddLayout = QHBoxLayout()
        self.cmbTur = QComboBox()
        self.cmbTur.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
            }
        """)
        for tur in turleri_oku_csv():
            self.cmbTur.addItem(tur)
        self.btnTurEkle = QPushButton("+")
        self.btnTurEkle.setFixedSize(30, 30)
        self.btnTurEkle.setStyleSheet("""
            QPushButton {
                background-color: #39405e;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4A5170;
            }
        """)
        self.btnTurEkle.clicked.connect(self.addTurFromCombo)
        turAddLayout.addWidget(self.cmbTur)
        turAddLayout.addWidget(self.btnTurEkle)
        formLayout.addLayout(turAddLayout)

        # İlerleme
        lblIler = QLabel("İlerleme (x/y):")
        lblIler.setStyleSheet("color:white; font-size:16px;")
        self.lineIler = QLineEdit(self.kayit["İlerleme"])
        self.lineIler.setStyleSheet("""
            QLineEdit {
                background: white;
                color: black;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #fa3c4c;
            }
        """)

        # validator
        regex = QRegularExpression(r'^\d+/\d+$')
        validator = QRegularExpressionValidator(regex, self.lineIler)
        self.lineIler.setValidator(validator)
        self.lineIler.textChanged.connect(self.validateIlerleme)

        formLayout.addWidget(lblIler)
        formLayout.addWidget(self.lineIler)

        # Puan
        lblPuan = QLabel("Puan (1-5):")
        lblPuan.setStyleSheet("color:white; font-size:16px;")
        self.starWidget = StarRatingWidget(initial=self.kayit["Puan"])
        formLayout.addWidget(lblPuan)
        formLayout.addWidget(self.starWidget)

        # Dizi/Film (Checkbox'lar)
        lblDf = QLabel("Dizi/Film:")
        lblDf.setStyleSheet("color:white; font-size:16px;")
        dfLayout = QHBoxLayout()
        self.chkDizi = QCheckBox("Dizi")
        self.chkFilm = QCheckBox("Film")
        for chk in [self.chkDizi, self.chkFilm]:
            chk.setStyleSheet("color:white; font-size:14px;")
            chk.stateChanged.connect(self._diziFilmChecked)
        dfLayout.addWidget(self.chkDizi)
        dfLayout.addWidget(self.chkFilm)
        dfLayout.addStretch()
        formLayout.addWidget(lblDf)
        formLayout.addLayout(dfLayout)

        # Durum (Checkbox'lar)
        lblDurum = QLabel("Durum:")
        lblDurum.setStyleSheet("color:white; font-size:16px;")
        durumLayout = QHBoxLayout()
        self.chkIzlendi = QCheckBox("İzlendi")
        self.chkIzleniyor = QCheckBox("İzleniyor")
        self.chkIzlenecek = QCheckBox("İzlenecek")
        for chk in [self.chkIzlendi, self.chkIzleniyor, self.chkIzlenecek]:
            chk.setStyleSheet("color:white; font-size:14px;")
            chk.stateChanged.connect(self._durumChecked)
        durumLayout.addWidget(self.chkIzlendi)
        durumLayout.addWidget(self.chkIzleniyor)
        durumLayout.addWidget(self.chkIzlenecek)
        durumLayout.addStretch()
        formLayout.addWidget(lblDurum)
        formLayout.addLayout(durumLayout)

        # Not
        lblNot = QLabel("Not:")
        lblNot.setStyleSheet("color:white; font-size:16px;")
        self.txtNot = QTextEdit(self.kayit["Not"])
        self.txtNot.setStyleSheet("""
            QTextEdit {
                background: white;
                color: black;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
            QTextEdit:focus {
                border: 2px solid #fa3c4c;
            }
        """)
        formLayout.addWidget(lblNot)
        formLayout.addWidget(self.txtNot)

        self.layout.addLayout(formLayout)

        # Kaydet / İptal Butonları
        btnLayout = QHBoxLayout()
        self.btnKaydet = QPushButton("Kaydet")
        self.btnKaydet.setStyleSheet("""
            QPushButton {
                background-color: #fa3c4c;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #f72b3c;
            }
        """)
        self.btnKaydet.clicked.connect(self.kaydetTiklandi)
        self.btnIptal = QPushButton("İptal")
        self.btnIptal.setStyleSheet("""
            QPushButton {
                background-color: #39405e;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #4A5170;
            }
        """)
        self.btnIptal.clicked.connect(self.reject)
        btnLayout.addWidget(self.btnKaydet)
        btnLayout.addWidget(self.btnIptal)
        self.layout.addLayout(btnLayout)

        self.initCheckBoxes()

    def initCheckBoxes(self):
        # Dizi/Film
        if self.kayit["Dizi/Film"] == "Dizi":
            self.chkDizi.setChecked(True)
        elif self.kayit["Dizi/Film"] == "Film":
            self.chkFilm.setChecked(True)
        else:
            self.chkFilm.setChecked(True)

        # Durum
        if self.kayit["Durum"] == "İzlendi":
            self.chkIzlendi.setChecked(True)
        elif self.kayit["Durum"] == "İzleniyor":
            self.chkIzleniyor.setChecked(True)
        elif self.kayit["Durum"] == "İzlenecek":
            self.chkIzlenecek.setChecked(True)
        else:
            self.chkIzlendi.setChecked(True)

    def _diziFilmChecked(self, state):
        sender = self.sender()
        if sender == self.chkDizi and state == Qt.Checked:
            self.chkFilm.setChecked(False)
        elif sender == self.chkFilm and state == Qt.Checked:
            self.chkDizi.setChecked(False)

    def _durumChecked(self, state):
        sender = self.sender()
        if sender == self.chkIzlendi and state == Qt.Checked:
            self.chkIzleniyor.setChecked(False)
            self.chkIzlenecek.setChecked(False)
        elif sender == self.chkIzleniyor and state == Qt.Checked:
            self.chkIzlendi.setChecked(False)
            self.chkIzlenecek.setChecked(False)
        elif sender == self.chkIzlenecek and state == Qt.Checked:
            self.chkIzlendi.setChecked(False)
            self.chkIzleniyor.setChecked(False)

    def addTurChip(self, turStr):
        from PyQt5.QtWidgets import QFrame, QHBoxLayout

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #39405e;
                border-radius: 6px;
            }
        """)
        hLayout = QHBoxLayout(frame)
        hLayout.setContentsMargins(5, 3, 5, 3)
        hLayout.setSpacing(5)

        lblTur = QLabel(turStr)
        lblTur.setStyleSheet("color:white;")
        btnSil = QPushButton("-")
        btnSil.setFixedSize(20, 20)
        btnSil.setStyleSheet("""
            QPushButton {
                background-color: #fa3c4c;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #f72b3c;
            }
        """)
        btnSil.clicked.connect(lambda: self.removeTurChip(frame, turStr))

        hLayout.addWidget(lblTur)
        hLayout.addWidget(btnSil)
        self.turLayout.addWidget(frame)

    def removeTurChip(self, frame, turStr):
        self.turLayout.removeWidget(frame)
        frame.deleteLater()
        if turStr in self.currentTurler:
            self.currentTurler.remove(turStr)

    def addTurFromCombo(self):
        selTur = self.cmbTur.currentText().strip()
        if selTur and selTur not in self.currentTurler:
            self.currentTurler.append(selTur)
            self.addTurChip(selTur)

    def validateIlerleme(self):
        text = self.lineIler.text()
        state = self.lineIler.validator().validate(text, 0)[0]

        if state == QRegularExpressionValidator.Acceptable:
            # Input is valid
            self.lineIler.setStyleSheet("""
                QLineEdit {
                    background: white;
                    color: black;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 5px;
                }
                QLineEdit:focus {
                    border: 2px solid #fa3c4c;
                }
            """)
        else:
            self.lineIler.setStyleSheet("""
                QLineEdit {
                    background: #ffe6e6; /* Light red background for error */
                    color: black;
                    border: 1px solid #fa3c4c;
                    border-radius: 4px;
                    padding: 5px;
                }
                QLineEdit:focus {
                    border: 2px solid #fa3c4c;
                }
            """)

    def kaydetTiklandi(self):
        oldDurum = self.originalDurum
        newDurum = "İzlendi"
        if self.chkIzleniyor.isChecked():
            newDurum = "İzleniyor"
        elif self.chkIzlenecek.isChecked():
            newDurum = "İzlenecek"

        if oldDurum == "İzlendi" and newDurum == "İzlenecek":
            self.starWidget.setStarRating(0)
            self.txtNot.setText("")
            ilerStr = self.lineIler.text().strip()
            parts = ilerStr.split("/")
            if len(parts) == 2:
                parts[0] = "0"
                ilerStr = "/".join(parts)
                self.lineIler.setText(ilerStr)

        # Dizi/Film seçimi
        diziFilm = "Film"
        if self.chkDizi.isChecked() and not self.chkFilm.isChecked():
            diziFilm = "Dizi"

        # Türler
        turStr = "/".join(self.currentTurler)

        # Formdan verileri al
        adVal = self.lineAd.text().strip()
        ilerVal = self.lineIler.text().strip()
        puanVal = self.starWidget.getRating()
        notVal = self.txtNot.toPlainText().strip()

        # Validasyon: Ad alanı boş mu?
        if not adVal:
            self.showCustomWarning("Ad alanı boş bırakılamaz.")
            return

        # Validasyon: İlerleme alanı boş mu?
        if not ilerVal:
            self.showCustomWarning("İlerleme alanı boş bırakılamaz.")
            return

        # Validasyon: İlerleme formatı "x/y" mu ve x ile y sayısal mı?
        iler_parts = ilerVal.split('/')
        if len(iler_parts) != 2:
            self.showCustomWarning("İlerleme formatı hatalı. Lütfen 'x/y' şeklinde giriniz.")
            return

        try:
            x = int(iler_parts[0])
            y = int(iler_parts[1])
            if x < 0 or y < 0:
                self.showCustomWarning("İlerleme değerleri negatif olamaz.")
                return
        except ValueError:
            self.showCustomWarning("İlerleme kısmına sadece sayısal değerler giriniz.")
            return

        # Kaydı güncelle
        updatedKayit = {
            "kullaniciAdi": self.kayit["kullaniciAdi"],
            "Dizi/Film": diziFilm,
            "Tür": turStr,
            "Ad": adVal,
            "İlerleme": ilerVal,
            "Puan": puanVal,
            "Not": notVal,
            "Durum": newDurum,
            "Afiş": self.kayit["Afiş"]
        }

        kayit_guncelle(updatedKayit)

        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Başarılı")
        msgBox.setText("Kayıt güncellendi.")

        msgBox.setStyleSheet("""
               QMessageBox {
                   background-color: #2E2E2E; /* Koyu arka plan */
                   color: white; /* Genel metin rengi beyaz */
               }
               QMessageBox QLabel {
                   color: white; /* QLabel içindeki metin rengi beyaz */
                   font-size: 14px;
               }
               QMessageBox QPushButton {
                   background-color: #fa3c4c;
                   color: white;
                   border: none;
                   padding: 5px 15px;
                   border-radius: 5px;
               }
               QMessageBox QPushButton:hover {
                   background-color: #f72b3c;
               }
           """)

        msgBox.exec_()

        self.kayitGuncellendi.emit()
        self.accept()

    def showCustomWarning(self, message):
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("Uyarı")
        msgBox.setText(message)
        msgBox.setStyleSheet("""
               QMessageBox {
                   background-color: #2E2E2E; /* Koyu arka plan */
                   color: white; /* Genel metin rengi beyaz */
               }
               QMessageBox QLabel {
                   color: white; /* QLabel içindeki metin rengi beyaz */
                   font-size: 14px;
               }
               QMessageBox QPushButton {
                   background-color: #fa3c4c;
                   color: white;
                   border: none;
                   padding: 5px 15px;
                   border-radius: 5px;
               }
               QMessageBox QPushButton:hover {
                   background-color: #f72b3c;
               }
           """)
        msgBox.exec_()
