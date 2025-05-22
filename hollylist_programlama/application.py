import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt

from ust_menu import UstMenu
from anasayfa import AnaSayfa
from izlendi_page import IzlendiPage
from izleniyor_page import IzleniyorPage
from izlenecek_page import IzlenecekPage
from ekle_sayfasi import EkleSayfasi
from ayarlar import Ayarlar


class MainWindow(QMainWindow):
    def __init__(self, kullaniciAdi):
        super().__init__()
        self.kullaniciAdi = kullaniciAdi
        self.setObjectName("MainWindow")

        self.setFixedSize(1200, 700)
        self.setWindowTitle("Hollylist - MainWindow")

        self.setStyleSheet("""
            #MainWindow {
                background: qradialgradient(
                    cx:0.5, cy:0.5, radius: 1,
                    fx:0.3, fy:0.3,
                    stop:0 #0C0C38,
                    stop:1 #050516
                );
            }
        """)

        central = QWidget()
        central.setObjectName("CentralWidget")
        self.setCentralWidget(central)

        mainLayout = QVBoxLayout(central)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # Üst menü
        self.ustMenu = UstMenu(kullaniciAdi=self.kullaniciAdi)
        self.ustMenu.menuSecildi.connect(self.handleMenuSecildi)
        self.ustMenu.kullaniciMenuSecildi.connect(self.handleUserMenuSecildi)
        mainLayout.addWidget(self.ustMenu, 0)

        # QStackedWidget
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.setStyleSheet("background: transparent;")
        mainLayout.addWidget(self.stackedWidget, 1)

        # 1) Anasayfa
        self.pageAnaSayfa = AnaSayfa(kullaniciAdi=self.kullaniciAdi)
        self.pageAnaSayfa.btnEkle.clicked.connect(lambda: self.navigateTo("ekle"))

        # 2) Diğer sayfalar
        self.pageIzlendi = IzlendiPage(self.kullaniciAdi)
        self.pageIzleniyor = IzleniyorPage(self.kullaniciAdi)
        self.pageIzlenecek = IzlenecekPage(self.kullaniciAdi)

        # 3) Ekle sayfası
        self.pageEkle = EkleSayfasi(self.kullaniciAdi)
        self.pageEkle.kayitEklendi.connect(self._onKayitEklendi)

        # 4) StackedWidget'e ekle
        self.stackedWidget.addWidget(self.pageAnaSayfa)   # index 0
        self.stackedWidget.addWidget(self.pageIzlendi)    # index 1
        self.stackedWidget.addWidget(self.pageIzleniyor)  # index 2
        self.stackedWidget.addWidget(self.pageIzlenecek)  # index 3
        self.stackedWidget.addWidget(self.pageEkle)       # index 4

        # 5) TabloPage Sinyallerini Bağlama
        self.pageIzlendi.kayitGuncellendi.connect(self.refreshPages)
        self.pageIzleniyor.kayitGuncellendi.connect(self.refreshPages)
        self.pageIzlenecek.kayitGuncellendi.connect(self.refreshPages)

        self.refreshCounter = 0

        self.stackedWidget.setCurrentIndex(0)

    def handleMenuSecildi(self, secim):
        if secim == "anasayfa":
            self.ustMenu.updateActiveMenu("anasayfa")
            self.stackedWidget.setCurrentIndex(0)

        elif secim == "izlendi":
            self.ustMenu.updateActiveMenu("izlendi")
            self.stackedWidget.setCurrentIndex(1)

        elif secim == "izleniyor":
            self.ustMenu.updateActiveMenu("izleniyor")
            self.stackedWidget.setCurrentIndex(2)

        elif secim == "izlenecek":
            self.ustMenu.updateActiveMenu("izlenecek")
            self.stackedWidget.setCurrentIndex(3)

    def handleUserMenuSecildi(self, secim):
        if secim == "ayarlar":
            try:
                ayarlarDialog = Ayarlar(self.kullaniciAdi, self)
                ayarlarDialog.exec_()
            except Exception as e:
                print(f"Ayarlar penceresi açılırken hata oluştu: {e}")
                QMessageBox.critical(self, "Hata", f"Ayarlar penceresi açılamadı: {e}")
        elif secim == "cikis":
            self.logout()

    def navigateTo(self, pageName):
        if pageName == "ekle":
            self.ustMenu.updateActiveMenu(None)
            self.stackedWidget.setCurrentIndex(4)

    def _onKayitEklendi(self):
        self.refreshPages()
        self.stackedWidget.setCurrentIndex(0)

    def refreshPages(self):
        self.refreshCounter += 1
        print(f"refreshPages çağrıldı. Sayaç: {self.refreshCounter}")  # Debug

        if self.refreshCounter > 10:
            print("refreshPages çok fazla çağrıldı. Muhtemel döngü.")
            QMessageBox.critical(self, "Hata", "Uygulama beklenmedik şekilde çöktü.")
            self.close()
            return

        try:
            self.pageAnaSayfa.loadDataFromCSV()
            self.pageIzlendi.loadData()
            self.pageIzleniyor.loadData()
            self.pageIzlenecek.loadData()
            print("refreshPages tamamlandı.")  # Debug
        except Exception as e:
            print(f"refreshPages sırasında hata oluştu: {e}")
            QMessageBox.critical(self, "Hata", f"Veriler yenilenirken bir hata oluştu: {e}")

    def logout(self):
        self.hide()
        print("Çıkış yapıldı.")
        QApplication.quit()


def main():
    import faulthandler
    faulthandler.enable()
    app = QApplication(sys.argv)
    kullaniciAdi = "exampleuser"
    window = MainWindow(kullaniciAdi)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
