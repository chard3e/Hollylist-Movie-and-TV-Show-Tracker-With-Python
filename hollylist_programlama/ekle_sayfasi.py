from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QIcon, QIntValidator
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton,
    QCheckBox, QLineEdit, QTextEdit, QComboBox, QFileDialog, QMessageBox
)
import os
import csv

from veritabani import turleri_oku_csv, kayit_ekle, kayit_var_mi


class StarRatingWidget(QWidget):
    ratingChanged = pyqtSignal(int)

    def __init__(self, parent=None, initial=0):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background: transparent;")

        self.maxStars = 5
        self.currentRating = initial

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.starLabels = []
        for i in range(self.maxStars):
            lbl = QLabel()
            lbl.setStyleSheet("background: transparent;")
            lbl.setPixmap(QPixmap("iconlar/star_off.png").scaled(
                24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
            lbl.mousePressEvent = lambda event, idx=i: self.handleStarClick(idx + 1)
            layout.addWidget(lbl)
            self.starLabels.append(lbl)

        self.updateStars()

    def handleStarClick(self, rating):
        if self.currentRating == rating:
            self.setRating(0)
        else:
            self.setRating(rating)

    def setRating(self, rating):
        if self.currentRating != rating:
            self.currentRating = rating
            self.updateStars()
            self.ratingChanged.emit(self.currentRating)

    def updateStars(self):
        for i, lbl in enumerate(self.starLabels):
            if i < self.currentRating:
                lbl.setPixmap(QPixmap("iconlar/star_on.png").scaled(
                    24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation
                ))
            else:
                lbl.setPixmap(QPixmap("iconlar/star_off.png").scaled(
                    24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation
                ))

    def getRating(self):
        return self.currentRating

    def setStarRating(self, rating):
        self.setRating(rating)


class EkleSayfasi(QWidget):
    kayitEklendi = pyqtSignal()

    def __init__(self, kullaniciAdi="Kullanıcı"):
        super().__init__()
        self.kullaniciAdi = kullaniciAdi

        self.setStyleSheet("""
            EkleSayfasi {
                background: qradialgradient(
                    cx:0.5, cy:0.5, radius: 1,
                    fx:0.2, fy:0.3,
                    stop:0 #0C0C38,
                    stop:1 #050516
                );
            }
        """)

        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(15)

        self.leftPanel = self.buildLeftPanel()
        mainLayout.addWidget(self.leftPanel, 2)

        self.rightPanel = self.buildRightPanel()
        mainLayout.addWidget(self.rightPanel, 1)

        self.loadTurCSV()

    def buildLeftPanel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #39405e;
                border-radius: 8px;
            }
        """)
        panel.setMinimumWidth(400)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Dizi / Film
        rowDF = QHBoxLayout()
        lblDF = QLabel("Dizi/Film:")
        lblDF.setStyleSheet("font-size: 16px; font-weight: bold; color: white; background: transparent;")
        self.chkDizi = QCheckBox("Dizi")
        self.chkFilm = QCheckBox("Film")
        for c in [self.chkDizi, self.chkFilm]:
            c.setStyleSheet("color: white; font-size: 16px; background: transparent;")
        rowDF.addWidget(lblDF)
        rowDF.addWidget(self.chkDizi)
        rowDF.addWidget(self.chkFilm)
        rowDF.addStretch()
        layout.addLayout(rowDF)

        self.chkDizi.stateChanged.connect(self.onDFChanged)
        self.chkFilm.stateChanged.connect(self.onDFChanged)

        # Ad
        lblAd = QLabel("Ad:")
        lblAd.setStyleSheet("font-size: 16px; font-weight: bold; color: white; background: transparent;")
        self.lineAd = QLineEdit()
        self.lineAd.setPlaceholderText("Ad giriniz...")
        self.lineAd.setStyleSheet("""
            QLineEdit {
                background: white;
                color: black;
                border: 1px solid #ccc;
                font-size: 14px;
                border-radius: 3px;
                padding: 4px;
            }
            QLineEdit:focus {
                border: 2px solid #fa3c4c;
            }
        """)
        layout.addWidget(lblAd)
        layout.addWidget(self.lineAd)

        # Tür
        rowTur = QHBoxLayout()
        lblTur = QLabel("Tür:")
        lblTur.setStyleSheet("font-size: 16px; font-weight: bold; color: white; background: transparent;")

        self.cmbTur = QComboBox()
        self.cmbTur.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                font-size: 14px;
                border-radius: 3px;
                padding: 3px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
            }
        """)

        self.btnTurEkle = QPushButton("+")
        self.btnTurEkle.setFixedWidth(30)
        self.btnTurEkle.setStyleSheet("""
            QPushButton {
                background-color: #39405e; 
                color: white;
                font-size: 16px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4A5170;
            }
        """)
        self.btnTurEkle.clicked.connect(self.turEkleClicked)

        rowTur.addWidget(lblTur)
        rowTur.addWidget(self.cmbTur)
        rowTur.addWidget(self.btnTurEkle)
        rowTur.addStretch()
        layout.addLayout(rowTur)

        self.selectedTurler = []
        self.lblSelectedTur = QLabel("Seçilen türler: -")
        self.lblSelectedTur.setStyleSheet("font-size: 14px; color: white; background: transparent;")
        layout.addWidget(self.lblSelectedTur)

        # İlerleme
        rowIler = QHBoxLayout()
        lblIler = QLabel("İlerleme:")
        lblIler.setStyleSheet("font-size: 16px; font-weight: bold; color: white; background: transparent;")

        self.lineIler1 = QLineEdit()
        self.lineIler2 = QLineEdit()
        for l in [self.lineIler1, self.lineIler2]:
            l.setFixedWidth(40)
            l.setStyleSheet("""
                QLineEdit {
                    background: white;
                    color: black;
                    border: 1px solid #ccc;
                    font-size: 14px;
                    padding: 2px;
                    border-radius: 3px;
                }
                QLineEdit:focus {
                    border: 2px solid #fa3c4c;
                }
            """)

        # Apply QIntValidator to ensure only integers are entered
        int_validator = QIntValidator(0, 1000, self)  # Adjust the upper limit as needed
        self.lineIler1.setValidator(int_validator)
        self.lineIler2.setValidator(int_validator)

        # Connect textChanged signals to validation slot
        self.lineIler1.textChanged.connect(self.validateIlerleme)
        self.lineIler2.textChanged.connect(self.validateIlerleme)

        slashLabel = QLabel("/")
        slashLabel.setStyleSheet("font-size: 20px; color: white; background: transparent;")

        rowIler.addWidget(lblIler)
        rowIler.addWidget(self.lineIler1)
        rowIler.addWidget(slashLabel)
        rowIler.addWidget(self.lineIler2)
        rowIler.addStretch()
        layout.addLayout(rowIler)

        # Puan
        rowPuan = QHBoxLayout()
        lblPuan = QLabel("Puan:")
        lblPuan.setStyleSheet("font-size: 16px; font-weight: bold; color: white; background: transparent;")

        self.starWidget = StarRatingWidget()

        rowPuan.addWidget(lblPuan)
        rowPuan.addWidget(self.starWidget)
        rowPuan.addStretch()
        layout.addLayout(rowPuan)

        # Not
        lblNot = QLabel("Not:")
        lblNot.setStyleSheet("font-size: 16px; font-weight: bold; color: white; background: transparent;")
        layout.addWidget(lblNot)

        self.txtNot = QTextEdit()
        self.txtNot.setFixedHeight(120)
        self.txtNot.setPlaceholderText("Notunuzu yazın...")
        self.txtNot.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: black;
                font-size: 14px;
                border-radius: 3px;
            }
            QTextEdit:focus {
                border: 2px solid #fa3c4c;
            }
        """)
        layout.addWidget(self.txtNot)

        # Durum
        rowDurum = QHBoxLayout()
        lblDurum = QLabel("Durum:")
        lblDurum.setStyleSheet("font-size: 16px; font-weight: bold; color: white; background: transparent;")

        self.chkIzlendi = QCheckBox("İzlendi")
        self.chkIzleniyor = QCheckBox("İzleniyor")
        self.chkIzlenecek = QCheckBox("İzlenecek")
        for c in [self.chkIzlendi, self.chkIzleniyor, self.chkIzlenecek]:
            c.setStyleSheet("color: white; font-size: 16px; background: transparent;")

        rowDurum.addWidget(lblDurum)
        rowDurum.addWidget(self.chkIzlendi)
        rowDurum.addWidget(self.chkIzleniyor)
        rowDurum.addWidget(self.chkIzlenecek)
        rowDurum.addStretch()
        layout.addLayout(rowDurum)

        self.chkIzlendi.stateChanged.connect(self.onDurumChanged)
        self.chkIzleniyor.stateChanged.connect(self.onDurumChanged)
        self.chkIzlenecek.stateChanged.connect(self.onDurumChanged)

        # Kaydet
        self.btnKaydet = QPushButton("KAYDET")
        self.btnKaydet.setStyleSheet("""
            QPushButton {
                background-color: #fa3c4c;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: 12px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #f72b3c;
            }
        """)
        self.btnKaydet.clicked.connect(self.kaydetTiklandi)
        layout.addWidget(self.btnKaydet, alignment=Qt.AlignRight)

        return panel

    def buildRightPanel(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #1E1E3C; 
                border-radius: 8px;
            }
        """)
        frame.setFixedSize(450, 600)

        vbox = QVBoxLayout(frame)
        vbox.setContentsMargins(20, 20, 20, 20)
        vbox.setSpacing(15)

        self.selectedImagePath = "afisler/default.jpg"

        self.lblAfis = QLabel()
        self.lblAfis.setStyleSheet("background: #444; border-radius: 5px;")
        self.lblAfis.setFixedSize(410, 520)
        self.lblAfis.setScaledContents(True)

        if os.path.exists(self.selectedImagePath):
            pix = QPixmap(self.selectedImagePath)
            self.lblAfis.setPixmap(pix)

        vbox.addWidget(self.lblAfis, alignment=Qt.AlignCenter)

        self.btnFotoSec = QPushButton()
        self.btnFotoSec.setIcon(QIcon("iconlar/ekle_icon.png"))
        self.btnFotoSec.setIconSize(QSize(24, 24))
        self.btnFotoSec.setFixedSize(60, 40)
        self.btnFotoSec.setStyleSheet("""
            QPushButton {
                background-color: #39405e;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #4A5170;
            }
        """)
        self.btnFotoSec.clicked.connect(self.fotoSecClicked)
        vbox.addWidget(self.btnFotoSec, alignment=Qt.AlignCenter)

        return frame

    def loadTurCSV(self):
        turler = turleri_oku_csv("tur.csv")
        self.cmbTur.clear()
        if turler:
            self.cmbTur.addItems(turler)

    def turEkleClicked(self):
        t = self.cmbTur.currentText().strip()
        if t and t not in self.selectedTurler:
            self.selectedTurler.append(t)
            self.lblSelectedTur.setText("Seçilen türler: " + "/".join(self.selectedTurler))
        else:
            QMessageBox.information(self, "Bilgi", "Tür zaten seçili veya boş!")

    def fotoSecClicked(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Fotoğraf Seç", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if filePath:
            self.selectedImagePath = filePath
            pix = QPixmap(filePath)
            self.lblAfis.setPixmap(pix)

    def kaydetTiklandi(self):
        if self.chkDizi.isChecked() and not self.chkFilm.isChecked():
            diziFilm = "Dizi"
        elif self.chkFilm.isChecked() and not self.chkDizi.isChecked():
            diziFilm = "Film"
        else:
            diziFilm = "Film"

        turStr = "/".join(self.selectedTurler)
        ad = self.lineAd.text().strip()
        if not ad:
            self.showWarning("Uyarı", "Ad boş olamaz!")
            return

        i1 = self.lineIler1.text().strip() or "0"
        i2 = self.lineIler2.text().strip() or "1"

        if not i1.isdigit() or not i2.isdigit():
            self.showWarning("Uyarı", "İlerleme alanlarına sadece sayısal değerler giriniz.")
            return

        iler = f"{i1}/{i2}"
        puan = self.starWidget.getRating()
        note = self.txtNot.toPlainText().strip()

        if self.chkIzlendi.isChecked():
            durum = "İzlendi"
        elif self.chkIzleniyor.isChecked():
            durum = "İzleniyor"
        elif self.chkIzlenecek.isChecked():
            durum = "İzlenecek"
        else:
            durum = "İzlendi"

        afis = self.selectedImagePath if hasattr(self, 'selectedImagePath') else "afisler/default.jpg"

        if os.path.isabs(afis):
            afis = os.path.relpath(afis, os.path.dirname(__file__)).replace("\\", "/")

        yeni_kayit = {
            "kullaniciAdi": self.kullaniciAdi,
            "Dizi/Film": diziFilm,
            "Tür": turStr,
            "Ad": ad,
            "İlerleme": iler,
            "Puan": puan,
            "Not": note,
            "Durum": durum,
            "Afiş": afis
        }

        if kayit_var_mi(self.kullaniciAdi, ad):
            self.showWarning("Uyarı", f"{ad} adında bir içerik zaten eklenmiş.")
            return

        try:
            kayit_ekle(yeni_kayit)
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Başarılı")
            msgBox.setText("Kayıt eklendi.")
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
            self.kayitEklendi.emit()
            self.resetForm()
        except Exception as e:
            self.showCritical("Hata", f"Kayıt eklenirken bir hata oluştu:\n{str(e)}")

    def resetForm(self):
        self.chkDizi.setChecked(False)
        self.chkFilm.setChecked(False)
        self.selectedTurler.clear()
        self.lblSelectedTur.setText("Seçilen türler: -")
        self.lineAd.clear()
        self.lineIler1.setText("0")
        self.lineIler2.setText("1")
        self.starWidget.setRating(0)
        self.txtNot.clear()
        self.chkIzlendi.setChecked(False)
        self.chkIzleniyor.setChecked(False)
        self.chkIzlenecek.setChecked(False)
        self.selectedImagePath = "afisler/default.jpg"
        if os.path.exists(self.selectedImagePath):
            pix = QPixmap(self.selectedImagePath)
            self.lblAfis.setPixmap(pix)
        else:
            self.lblAfis.clear()

    def onDFChanged(self, state):
        sender = self.sender()
        if sender == self.chkDizi and state == Qt.Checked:
            self.chkFilm.setChecked(False)
        elif sender == self.chkFilm and state == Qt.Checked:
            self.chkDizi.setChecked(False)

    def onDurumChanged(self, state):
        sender = self.sender()
        if state == Qt.Checked:
            if sender == self.chkIzlendi:
                self.chkIzleniyor.setChecked(False)
                self.chkIzlenecek.setChecked(False)
            elif sender == self.chkIzleniyor:
                self.chkIzlendi.setChecked(False)
                self.chkIzlenecek.setChecked(False)
            elif sender == self.chkIzlenecek:
                self.chkIzlendi.setChecked(False)
                self.chkIzleniyor.setChecked(False)

    def showWarning(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2c3e50;
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #fa3c4c;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #f72b3c;
            }
        """)
        msg.exec_()

    def showCritical(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2c3e50;
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #fa3c4c;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #f72b3c;
            }
        """)
        msg.exec_()

    def validateIlerleme(self):
        state1 = self.lineIler1.validator().validate(self.lineIler1.text(), 0)[0]
        if state1 == QIntValidator.Acceptable or not self.lineIler1.text():
            self.lineIler1.setStyleSheet("""
                QLineEdit {
                    background: white;
                    color: black;
                    border: 1px solid #ccc;
                    font-size: 14px;
                    padding: 2px;
                    border-radius: 3px;
                }
                QLineEdit:focus {
                    border: 2px solid #fa3c4c;
                }
            """)
        else:
            self.lineIler1.setStyleSheet("""
                QLineEdit {
                    background: #ffe6e6; /* Light red background for error */
                    color: black;
                    border: 1px solid #fa3c4c;
                    font-size: 14px;
                    padding: 2px;
                    border-radius: 3px;
                }
                QLineEdit:focus {
                    border: 2px solid #fa3c4c;
                }
            """)


        state2 = self.lineIler2.validator().validate(self.lineIler2.text(), 0)[0]
        if state2 == QIntValidator.Acceptable or not self.lineIler2.text():
            self.lineIler2.setStyleSheet("""
                QLineEdit {
                    background: white;
                    color: black;
                    border: 1px solid #ccc;
                    font-size: 14px;
                    padding: 2px;
                    border-radius: 3px;
                }
                QLineEdit:focus {
                    border: 2px solid #fa3c4c;
                }
            """)
        else:
            self.lineIler2.setStyleSheet("""
                QLineEdit {
                    background: #ffe6e6; /* Light red background for error */
                    color: black;
                    border: 1px solid #fa3c4c;
                    font-size: 14px;
                    padding: 2px;
                    border-radius: 3px;
                }
                QLineEdit:focus {
                    border: 2px solid #fa3c4c;
                }
            """)
