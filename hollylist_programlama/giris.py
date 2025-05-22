import sys
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QFont, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QParallelAnimationGroup

from kayit import KayitEkrani
from veritabani import giris_kontrol

from application import MainWindow


class AsymmetricImageWidget(QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(image_path)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        rect = self.rect()

        path = QPainterPath()
        path.moveTo(rect.topLeft())
        path.lineTo(rect.x() + rect.width() * 0.7, rect.y())
        path.quadTo(rect.right(), rect.center().y(),
                    rect.x() + rect.width() * 0.7, rect.bottom())
        path.lineTo(rect.bottomLeft())
        path.closeSubpath()

        painter.setClipPath(path)

        scaledPixmap = self.pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        x = (rect.width() - scaledPixmap.width()) // 2
        y = (rect.height() - scaledPixmap.height()) // 2
        painter.drawPixmap(x, y, scaledPixmap)

        painter.setClipping(False)
        borderPath = QPainterPath()
        borderPath.moveTo(rect.x() + rect.width() * 0.7, rect.y())
        borderPath.quadTo(rect.right(), rect.center().y(),
                          rect.x() + rect.width() * 0.7, rect.bottom())

        pen = QPen(Qt.white, 10)
        painter.setPen(pen)
        painter.drawPath(borderPath)


class GirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hollylist")
        self.setStyleSheet("""
            QWidget {
                background: qradialgradient(
                    cx:0.5, cy:0.5, radius: 1,
                    fx:0.2, fy:0.3,
                    stop:0 #0C0C38,
                    stop:1 #050516
                );
            }
        """)

        self.asymmetricWidget = AsymmetricImageWidget("girisfoto.jpg", self)

        self.logoLabel = QLabel(self)
        self.logoPixmap = QPixmap("logo.png")
        self.logoLabel.setPixmap(self.logoPixmap)
        self.logoLabel.setStyleSheet("background: transparent;")

        self.aciklamaLabel = QLabel("FİLM VE DİZİ DÜNYANA YÖN VER.", self)
        self.aciklamaLabel.setFont(QFont("Arial", 14))
        self.aciklamaLabel.setStyleSheet("color: #bbbbbb; background: transparent;")

        self.epostaLine = QLineEdit(self)
        self.epostaLine.setPlaceholderText("Kullanıcı Adı")
        self._styleLineDefault(self.epostaLine)

        self.parolaLine = QLineEdit(self)
        self.parolaLine.setPlaceholderText("Parola")
        self.parolaLine.setEchoMode(QLineEdit.Password)
        self._styleLineDefault(self.parolaLine)

        self.girisButon = QPushButton("Giriş", self)
        self.girisButon.setStyleSheet("""
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
        self.girisButon.clicked.connect(self._girisTiklandi)

        self.sifremiUnuttumLabel = QLabel("<a href='#' style='color: #FFFFFF;'>Şifremi unuttum.</a>", self)
        self.sifremiUnuttumLabel.setStyleSheet("color: #FFFFFF; font-size: 12px; background: transparent;")

        self.kayitOlLabel1 = QLabel("Hesabın mı yok?", self)
        self.kayitOlLabel1.setStyleSheet("color: #FFFFFF; font-size: 12px; background: transparent;")

        self.kayitOlLabel = QLabel("<a href='kayit' style='color: #FFFFFF;'>Kayıt ol.</a>", self)
        self.kayitOlLabel.setStyleSheet("color: #FFFFFF; font-size: 12px; background: transparent;")
        self.kayitOlLabel.setOpenExternalLinks(False)
        self.kayitOlLabel.linkActivated.connect(self.animasyonlaKayitEkraninaGec)

        self.resize(1200, 700)
        self.setMinimumSize(800, 600)

        self.kayitEkrani = KayitEkrani(self)
        self.kayitEkrani.hide()
        self.kayitEkrani.geriClicked.connect(self.animasyonlaGirisDon)


        self.mainWindow = None

        self.epostaLine.textChanged.connect(lambda: self._styleLineDefault(self.epostaLine))
        self.parolaLine.textChanged.connect(lambda: self._styleLineDefault(self.parolaLine))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.width()
        h = self.height()

        self.asymmetricWidget.setGeometry(0, 0, int(w * 0.6), h)
        cx = int(w * 0.65)
        lw = self.logoPixmap.width()
        lh = self.logoPixmap.height()
        self.logoLabel.setGeometry(cx - 70, int(h * 0.24), lw, lh)
        self.aciklamaLabel.move(cx - 10, int(h * 0.36))

        self.epostaLine.setGeometry(cx - 60, int(h * 0.43), 400, 50)
        self.parolaLine.setGeometry(cx - 60, int(h * 0.53), 400, 50)
        self.girisButon.setGeometry(cx - 10, int(h * 0.65), 300, 40)

        self.sifremiUnuttumLabel.move(cx, int(h * 0.75))
        self.kayitOlLabel1.move(cx + 140, int(h * 0.75))
        self.kayitOlLabel.move(cx + 233, int(h * 0.75))

        self.kayitEkrani.setGeometry(0, 0, w, h)

    def animasyonlaKayitEkraninaGec(self, link_str=None):
        w = self.width()
        items = [
            self.asymmetricWidget,
            self.aciklamaLabel,
            self.epostaLine,
            self.parolaLine,
            self.girisButon,
            self.sifremiUnuttumLabel,
            self.kayitOlLabel1,
            self.kayitOlLabel
        ]
        group = QParallelAnimationGroup(self)
        for widget in items:
            anim = QPropertyAnimation(widget, b"geometry")
            anim.setDuration(400)
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            anim.setStartValue(widget.geometry())
            endRect = widget.geometry()
            endRect.moveLeft(-w)
            anim.setEndValue(endRect)
            group.addAnimation(anim)

        logoGeo = self.logoLabel.geometry()
        logoAnim = QPropertyAnimation(self.logoLabel, b"geometry")
        logoAnim.setDuration(400)
        logoAnim.setEasingCurve(QEasingCurve.InOutQuad)
        logoAnim.setStartValue(logoGeo)
        newX = (self.width() - logoGeo.width()) // 2
        newY = logoGeo.y()
        logoAnim.setEndValue(QRect(newX, newY, logoGeo.width(), logoGeo.height()))
        group.addAnimation(logoAnim)

        def afterFinished():
            self.kayitEkrani.show()
            self.kayitEkrani.animateIn()

        group.finished.connect(afterFinished)
        group.start()

    def animasyonlaGirisDon(self):
        def afterKayitOut():
            self.kayitEkrani.hide()
            self._showGirisElemanlari()

        self.kayitEkrani.animateOut(finishedCallback=afterKayitOut)

    def _showGirisElemanlari(self):
        w = self.width()
        items = [
            self.asymmetricWidget,
            self.aciklamaLabel,
            self.epostaLine,
            self.parolaLine,
            self.girisButon,
            self.sifremiUnuttumLabel,
            self.kayitOlLabel1,
            self.kayitOlLabel
        ]
        group = QParallelAnimationGroup(self)
        for widget in items:
            anim = QPropertyAnimation(widget, b"geometry")
            anim.setDuration(400)
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            anim.setStartValue(widget.geometry())
            endRect = self._getOriginalGeometry(widget)
            anim.setEndValue(endRect)
            group.addAnimation(anim)

        logoGeo = self.logoLabel.geometry()
        logoAnim = QPropertyAnimation(self.logoLabel, b"geometry")
        logoAnim.setDuration(400)
        logoAnim.setEasingCurve(QEasingCurve.InOutQuad)
        logoAnim.setStartValue(logoGeo)
        logoAnim.setEndValue(self._getOriginalLogoRect())
        group.addAnimation(logoAnim)

        def afterFinished():
            self._resetGirisForm()

        group.finished.connect(afterFinished)
        group.start()

    def _getOriginalGeometry(self, widget):
        w = self.width()
        h = self.height()
        cx = int(w * 0.65)

        if widget == self.asymmetricWidget:
            return QRect(0, 0, int(w * 0.6), h)
        elif widget == self.aciklamaLabel:
            return QRect(cx - 10, int(h * 0.36), widget.width(), widget.height())
        elif widget == self.epostaLine:
            return QRect(cx - 60, int(h * 0.43), widget.width(), widget.height())
        elif widget == self.parolaLine:
            return QRect(cx - 60, int(h * 0.53), widget.width(), widget.height())
        elif widget == self.girisButon:
            return QRect(cx - 10, int(h * 0.65), widget.width(), widget.height())
        elif widget == self.sifremiUnuttumLabel:
            return QRect(cx, int(h * 0.75), widget.width(), widget.height())
        elif widget == self.kayitOlLabel1:
            return QRect(cx + 140, int(h * 0.75), widget.width(), widget.height())
        elif widget == self.kayitOlLabel:
            return QRect(cx + 233, int(h * 0.75), widget.width(), widget.height())
        return widget.geometry()

    def _getOriginalLogoRect(self):
        w = self.width()
        h = self.height()
        cx = int(w * 0.65)
        lw = self.logoPixmap.width()
        lh = self.logoPixmap.height()
        return QRect(cx - 70, int(h * 0.24), lw, lh)

    def _resetGirisForm(self):
        self.epostaLine.setText("")
        self.parolaLine.setText("")
        self._styleLineDefault(self.epostaLine)
        self._styleLineDefault(self.parolaLine)

    def _girisTiklandi(self):
        kullaniciAdi = self.epostaLine.text().strip()
        sifre = self.parolaLine.text()

        sonuc = giris_kontrol(kullaniciAdi, sifre)
        if sonuc == "BULUNAMADI":
            self._stilKirmizi(self.epostaLine)
            self._popupUyari("Kullanıcı bulunamadı!")
        elif sonuc == "HATALI_SIFRE":
            self._stilKirmizi(self.parolaLine)
            self._popupUyari("Hatalı şifre!")
        else:
            self._girisBasariliAnim(kullaniciAdi)

    def _girisBasariliAnim(self, kullaniciAdi):
        w = self.width()
        items = [
            self.asymmetricWidget,
            self.aciklamaLabel,
            self.epostaLine,
            self.parolaLine,
            self.girisButon,
            self.sifremiUnuttumLabel,
            self.kayitOlLabel1,
            self.kayitOlLabel
        ]
        group = QParallelAnimationGroup(self)
        for widget in items:
            anim = QPropertyAnimation(widget, b"geometry")
            anim.setDuration(400)
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            anim.setStartValue(widget.geometry())
            endRect = widget.geometry()
            endRect.moveLeft(-w)
            anim.setEndValue(endRect)
            group.addAnimation(anim)

        logoGeo = self.logoLabel.geometry()
        logoAnim = QPropertyAnimation(self.logoLabel, b"geometry")
        logoAnim.setDuration(400)
        logoAnim.setEasingCurve(QEasingCurve.InOutQuad)
        logoAnim.setStartValue(logoGeo)
        logoAnim.setEndValue(QRect(-w, logoGeo.y(), logoGeo.width(), logoGeo.height()))
        group.addAnimation(logoAnim)

        def afterFinished():
            self.hide()
            self.mainWindow = MainWindow(kullaniciAdi)
            self.mainWindow.show()

        group.finished.connect(afterFinished)
        group.start()

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
        tamMetin = f"{mesaj}\n\nLütfen tekrar deneyiniz."
        mbox.setText(tamMetin)
        mbox.exec_()

    def _styleLineDefault(self, lineEdit):
        lineEdit.setStyleSheet("""
            QLineEdit {
                height: 32px;
                border-radius: 6px;
                padding: 6px;
                background-color: #242b48;
                color: white;
                border: 1px solid #39405e;
            }
        """)

    def _stilKirmizi(self, lineEdit):
        lineEdit.setStyleSheet("""
            QLineEdit {
                height: 32px;
                border-radius: 6px;
                padding: 6px;
                background-color: #242b48;
                color: white;
                border: 2px solid red;
            }
        """)


def main():
    app = QApplication(sys.argv)
    pencere = GirisEkrani()
    pencere.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()