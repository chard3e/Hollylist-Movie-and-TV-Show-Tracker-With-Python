
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QRect
from veritabani import (
    eposta_mevcut_mu,
    kullaniciadi_mevcut_mu,
    eposta_gecerli_mi,
    sifre_uygun_mu,
    kullanici_ekle
)


class KayitEkrani(QWidget):

    geriClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        self._setupUI()
        for w in [self.adSoyadLine, self.kullaniciLine, self.epostaLine,
                  self.parolaLine, self.kayitButon, self.geriButon]:
            w.setWindowOpacity(0.0)

    def _setupUI(self):
        # Ad Soyad
        self.adSoyadLine = QLineEdit(self)
        self.adSoyadLine.setPlaceholderText("Ad Soyad")
        self._styleLine(self.adSoyadLine)

        # Kullanıcı Adı
        self.kullaniciLine = QLineEdit(self)
        self.kullaniciLine.setPlaceholderText("Kullanıcı Adı")
        self._styleLine(self.kullaniciLine)

        # E-posta
        self.epostaLine = QLineEdit(self)
        self.epostaLine.setPlaceholderText("E-posta adresi")
        self._styleLine(self.epostaLine)

        # Parola
        self.parolaLine = QLineEdit(self)
        self.parolaLine.setPlaceholderText("Parola")
        self.parolaLine.setEchoMode(QLineEdit.Password)
        self._styleLine(self.parolaLine)

        # Kayıt Ol butonu
        self.kayitButon = QPushButton("Kayıt Ol", self)
        self.kayitButon.setStyleSheet("""
            QPushButton {
                background-color: #fa3c4c;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f72b3c;
            }
        """)
        self.kayitButon.clicked.connect(self._kayitOlTiklandi)

        # Geri butonu
        self.geriButon = QPushButton("Geri", self)
        self.geriButon.setStyleSheet("""
            QPushButton {
                background-color: #242b48;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #39405e;
            }
        """)
        self.geriButon.clicked.connect(self.geriClicked.emit)


        self.lblAdSoyadHata = QLabel("", self)
        self.lblAdSoyadHata.setStyleSheet("color: red; font-size: 12px; background: transparent;")

        self.lblKullaniciHata = QLabel("", self)
        self.lblKullaniciHata.setStyleSheet("color: red; font-size: 12px; background: transparent;")

        self.lblEpostaHata = QLabel("", self)
        self.lblEpostaHata.setStyleSheet("color: red; font-size: 12px; background: transparent;")

        self.lblSifreHata = QLabel("", self)
        self.lblSifreHata.setStyleSheet("color: red; font-size: 12px; background: transparent;")

        self.adSoyadLine.textChanged.connect(lambda: self._stilNormal(self.adSoyadLine, self.lblAdSoyadHata))
        self.kullaniciLine.textChanged.connect(lambda: self._stilNormal(self.kullaniciLine, self.lblKullaniciHata))
        self.epostaLine.textChanged.connect(lambda: self._stilNormal(self.epostaLine, self.lblEpostaHata))
        self.parolaLine.textChanged.connect(lambda: self._stilNormal(self.parolaLine, self.lblSifreHata))

    def _styleLine(self, line):

        line.setStyleSheet("""
            QLineEdit {
                height: 36px;
                border-radius: 6px;
                padding: 6px;
                background-color: #242b48;
                color: white;
                border: 1px solid #39405e;
            }
        """)

    def resizeEvent(self, event):

        super().resizeEvent(event)
        w = self.width()
        h = self.height()
        form_width = 400
        x_center = (w - form_width) // 2
        y_start = int(h * 0.4)
        gap = 60

        # Ad Soyad
        self.adSoyadLine.setGeometry(x_center, y_start, form_width, 36)
        self.lblAdSoyadHata.setGeometry(x_center, y_start - 20, form_width, 20)

        # Kullanıcı Adı
        self.kullaniciLine.setGeometry(x_center, y_start + gap, form_width, 36)
        self.lblKullaniciHata.setGeometry(x_center, (y_start + gap) - 20, form_width, 20)

        # E-posta
        self.epostaLine.setGeometry(x_center, y_start + gap * 2, form_width, 36)
        self.lblEpostaHata.setGeometry(x_center, (y_start + gap * 2) - 20, form_width, 20)

        # Parola
        self.parolaLine.setGeometry(x_center, y_start + gap * 3, form_width, 36)
        self.lblSifreHata.setGeometry(x_center, (y_start + gap * 3) - 20, form_width, 20)

        # Butonlar
        self.kayitButon.setGeometry(x_center + 50, y_start + gap * 4 + 10, 140, 40)
        self.geriButon.setGeometry(x_center + 210, y_start + gap * 4 + 10, 140, 40)

    def _stilNormal(self, lineEdit, hataLabel):

        self._styleLine(lineEdit)
        hataLabel.setText("")

    def _stilKirmizi(self, lineEdit):

        lineEdit.setStyleSheet("""
            QLineEdit {
                height: 36px;
                border-radius: 6px;
                padding: 6px;
                background-color: #242b48;
                color: white;
                border: 2px solid red;
            }
        """)

    def _temizleHatalar(self):

        self.lblAdSoyadHata.setText("")
        self.lblKullaniciHata.setText("")
        self.lblEpostaHata.setText("")
        self.lblSifreHata.setText("")

        self._stilNormal(self.adSoyadLine, self.lblAdSoyadHata)
        self._stilNormal(self.kullaniciLine, self.lblKullaniciHata)
        self._stilNormal(self.epostaLine, self.lblEpostaHata)
        self._stilNormal(self.parolaLine, self.lblSifreHata)

    def animateIn(self):

        self._temizleHatalar()
        self.adSoyadLine.setText("")
        self.kullaniciLine.setText("")
        self.epostaLine.setText("")
        self.parolaLine.setText("")

        group = QParallelAnimationGroup(self)
        for w in [self.adSoyadLine, self.kullaniciLine, self.epostaLine,
                  self.parolaLine, self.kayitButon, self.geriButon]:
            w.setWindowOpacity(0.0)
            anim = QPropertyAnimation(w, b"windowOpacity")
            anim.setDuration(300)
            anim.setStartValue(0.0)
            anim.setEndValue(1.0)
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            group.addAnimation(anim)

        group.start()

    def animateOut(self, finishedCallback=None):

        group = QParallelAnimationGroup(self)
        widgets = [self.adSoyadLine, self.kullaniciLine, self.epostaLine,
                   self.parolaLine, self.kayitButon, self.geriButon]
        for w in widgets:
            anim = QPropertyAnimation(w, b"windowOpacity")
            anim.setDuration(300)
            anim.setStartValue(w.windowOpacity())
            anim.setEndValue(0.0)
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            group.addAnimation(anim)

        if finishedCallback:
            group.finished.connect(finishedCallback)
        group.start()

    def _kayitOlTiklandi(self):

        self._temizleHatalar()

        adSoyad = self.adSoyadLine.text().strip()
        kullaniciAdi = self.kullaniciLine.text().strip()
        email = self.epostaLine.text().strip()
        sifre = self.parolaLine.text()

        # Boş alan kontrolü
        bosVarMi = False
        if not adSoyad:
            self.lblAdSoyadHata.setText("Ad Soyad boş bırakılamaz")
            self._stilKirmizi(self.adSoyadLine)
            bosVarMi = True
        if not kullaniciAdi:
            self.lblKullaniciHata.setText("Kullanıcı Adı boş bırakılamaz")
            self._stilKirmizi(self.kullaniciLine)
            bosVarMi = True
        if not email:
            self.lblEpostaHata.setText("E-posta boş bırakılamaz")
            self._stilKirmizi(self.epostaLine)
            bosVarMi = True
        if not sifre:
            self.lblSifreHata.setText("Şifre boş bırakılamaz")
            self._stilKirmizi(self.parolaLine)
            bosVarMi = True

        if bosVarMi:
            self._popupUyari("Boş alanlar var.")
            return

        # E-posta formatı kontrolü
        if not eposta_gecerli_mi(email):
            self.lblEpostaHata.setText("Geçerli bir e-posta giriniz")
            self._stilKirmizi(self.epostaLine)
            self._popupUyari("E-posta formatı hatalı.")
            return

        # Şifre uzunluğu
        if not sifre_uygun_mu(sifre):
            self.lblSifreHata.setText("Şifre 8-12 karakter olmalı")
            self._stilKirmizi(self.parolaLine)
            self._popupUyari("Şifre uzunluğu hatalı.")
            return

        # E-posta mevcut mu
        if eposta_mevcut_mu(email):
            self.lblEpostaHata.setText("Bu e-posta zaten kayıtlı")
            self._stilKirmizi(self.epostaLine)
            self._popupUyari("E-posta mevcut.")
            return

        # Kullanıcı adı mevcut mu
        if kullaniciadi_mevcut_mu(kullaniciAdi):
            self.lblKullaniciHata.setText("Bu kullanıcı adı kullanımda")
            self._stilKirmizi(self.kullaniciLine)
            self._popupUyari("Kullanıcı adı kullanımda.")
            return

        # Kayıt işlemi
        kullanici_ekle(adSoyad, kullaniciAdi, email, sifre)

        self._popupBilgi("Kayıt başarılı!")


    def _popupUyari(self, mesaj):
        mbox = QMessageBox(self)
        mbox.setStyleSheet("""
            QMessageBox {
                background-color: #1C1C33; 
            }
            QMessageBox QLabel {
                background: transparent;
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2E2E4B;
                color: white;
                padding: 6px 12px;
                border: 1px solid #444466;
            }
            QPushButton:hover {
                background-color: #3C3C5A;
            }
        """)
        mbox.setIcon(QMessageBox.Warning)
        mbox.setWindowTitle("Uyarı")
        tamMetin = f"{mesaj}\n\nLütfen alanları tekrar kontrol ediniz."
        mbox.setText(tamMetin)
        mbox.exec_()

    def _popupBilgi(self, mesaj):
        mbox = QMessageBox(self)
        mbox.setStyleSheet("""
            QMessageBox {
                background-color: #1C1C33;
            }
            QMessageBox QLabel {
                background: transparent;
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2E2E4B;
                color: white;
                padding: 6px 12px;
                border: 1px solid #444466;
            }
            QPushButton:hover {
                background-color: #3C3C5A;
            }
        """)
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Bilgi")
        mbox.setText(mesaj)

        def afterClose():
            self.geriClicked.emit()

        mbox.finished.connect(afterClose)
        mbox.exec_()
