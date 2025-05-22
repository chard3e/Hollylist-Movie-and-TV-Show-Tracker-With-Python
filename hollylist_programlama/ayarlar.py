from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from veritabani import kullanici_bilgilerini_oku, kullanici_bilgilerini_guncelle, kullanici_sil, \
    kullaniciadi_mevcut_mu, eposta_mevcut_mu, eposta_gecerli_mi, sifre_uygun_mu

class Ayarlar(QDialog):
    def __init__(self, kullaniciAdi, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayarlar")
        self.setFixedSize(400, 400)
        self.kullaniciAdi = kullaniciAdi

        self.setStyleSheet("""
            QDialog {
                background-color: #0C0C38;
                color: white;
                font-family: Arial;
            }
            QLabel {
                font-size: 14px;
                color: white;
            }
            QLineEdit {
                background-color: white;
                color: black;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #28a745;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton.delete {
                background-color: #dc3545;
            }
            QPushButton.delete:hover {
                background-color: #c82333;
            }
        """)

        self.setupUI()
        self.loadUserData()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Başlık
        title = QLabel("Hesap Bilgileriniz", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Form Alanları
        self.fields = {}
        self.addField(layout, "Ad Soyad:", "adSoyad")
        self.addField(layout, "Kullanıcı Adı:", "kullaniciAdi")
        self.addField(layout, "E-posta:", "email")
        self.addField(layout, "Şifre:", "sifre", echo_mode=True)

        # Butonlar
        btnLayout = QHBoxLayout()
        self.btnGuncelle = QPushButton("Bilgileri Güncelle", self)
        self.btnGuncelle.clicked.connect(self.updateUserInfo)
        btnLayout.addWidget(self.btnGuncelle)

        self.btnHesapSil = QPushButton("Hesabı Sil", self)
        self.btnHesapSil.setProperty("class", "delete")
        self.btnHesapSil.clicked.connect(self.deleteAccount)
        btnLayout.addWidget(self.btnHesapSil)

        layout.addLayout(btnLayout)

    def addField(self, parentLayout, label_text, field_key, echo_mode=False):
        fieldLayout = QVBoxLayout()
        label = QLabel(label_text, self)
        field = QLineEdit(self)
        if echo_mode:
            field.setEchoMode(QLineEdit.Password)
        field.setPlaceholderText(label_text)
        fieldLayout.addWidget(label)
        fieldLayout.addWidget(field)
        parentLayout.addLayout(fieldLayout)
        self.fields[field_key] = field

    def loadUserData(self):
        user_data = kullanici_bilgilerini_oku(self.kullaniciAdi)


        if user_data:
            adSoyad = user_data.get("adSoyad", "")
            kullaniciAdi = user_data.get("kullaniciAdi", "")
            email = user_data.get("email", "")
            sifre = user_data.get("sifre", "")

            self.fields["adSoyad"].setText(adSoyad)
            self.fields["kullaniciAdi"].setText(kullaniciAdi)
            self.fields["email"].setText(email)
            self.fields["sifre"].setText(sifre)
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı bilgileri yüklenemedi.", QMessageBox.Ok)

    def updateUserInfo(self):
        yeni_bilgiler = {
            "adSoyad": self.fields["adSoyad"].text().strip(),
            "kullaniciAdi": self.fields["kullaniciAdi"].text().strip(),
            "email": self.fields["email"].text().strip(),
            "sifre": self.fields["sifre"].text().strip()
        }

        for key, value in yeni_bilgiler.items():
            if not value:
                QMessageBox.warning(self, "Hata", f"{key} alanı boş bırakılamaz.", QMessageBox.Ok)
                return

        if not eposta_gecerli_mi(yeni_bilgiler["email"]):
            QMessageBox.warning(self, "Hata", "Geçerli bir e-posta adresi giriniz.", QMessageBox.Ok)
            return

        if not sifre_uygun_mu(yeni_bilgiler["sifre"]):
            QMessageBox.warning(self, "Hata", "Şifre 8 ile 12 karakter arasında olmalıdır.", QMessageBox.Ok)
            return

        if yeni_bilgiler["kullaniciAdi"] != self.kullaniciAdi:
            if kullaniciadi_mevcut_mu(yeni_bilgiler["kullaniciAdi"]):
                QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten kullanılıyor.", QMessageBox.Ok)
                return

        if yeni_bilgiler["email"] != self.fields["email"].text().strip():
            if eposta_mevcut_mu(yeni_bilgiler["email"]):
                QMessageBox.warning(self, "Hata", "Bu e-posta adresi zaten kullanılıyor.", QMessageBox.Ok)
                return

        if kullanici_bilgilerini_guncelle(self.kullaniciAdi, yeni_bilgiler):
            QMessageBox.information(self, "Başarılı", "Bilgiler başarıyla güncellendi!", QMessageBox.Ok)
            self.kullaniciAdi = yeni_bilgiler["kullaniciAdi"]  # Kullanıcı adı değiştiyse güncelle
        else:
            QMessageBox.warning(self, "Hata", "Bilgiler güncellenirken bir hata oluştu.", QMessageBox.Ok)

    def deleteAccount(self):
        confirm = QMessageBox.question(self, "Emin misiniz?", "Hesabınızı silmek istediğinize emin misiniz?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            if kullanici_sil(self.kullaniciAdi):
                QMessageBox.information(self, "Başarılı", "Hesabınız başarıyla silindi.", QMessageBox.Ok)
                self.accept()
            else:
                QMessageBox.warning(self, "Hata", "Hesap silinirken bir hata oluştu.", QMessageBox.Ok)
