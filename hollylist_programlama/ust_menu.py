from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QPushButton, QMenu, QAction
)

class UstMenu(QFrame):
    menuSecildi = pyqtSignal(str)
    kullaniciMenuSecildi = pyqtSignal(str)

    def __init__(self, kullaniciAdi="Kullanıcı", parent=None):
        super().__init__(parent)
        self.kullaniciAdi = kullaniciAdi
        self.activeMenu = "anasayfa"
        self.setFixedHeight(80)


        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #b4342f,
                    stop:1 #620c0c
                );
                border-bottom-left-radius: 30px;
                border-bottom-right-radius: 30px;
            }
        """)

        self.buildUI()

    def buildUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(20)

        # Menü butonları
        self.btnAnasayfa = self.createMenuButton("Anasayfa", "iconlar/home_icon.png", "anasayfa")
        self.btnIzlendi = self.createMenuButton("İzlendi", "iconlar/izlendi_icon.png", "izlendi")
        self.btnIzleniyor = self.createMenuButton("İzleniyor", "iconlar/izleniyor_icon.png", "izleniyor")
        self.btnIzlenecek = self.createMenuButton("İzlenecek", "iconlar/izlenecek_icon.png", "izlenecek")

        layout.addWidget(self.btnAnasayfa)
        layout.addWidget(self.btnIzlendi)
        layout.addWidget(self.btnIzleniyor)
        layout.addWidget(self.btnIzlenecek)
        layout.addStretch()

        # Kullanıcı butonu
        self.userButton = QPushButton(self.kullaniciAdi)
        self.userButton.setIcon(QIcon("iconlar/user_icon.png"))
        self.userButton.setIconSize(QSize(20, 20))
        self.userButton.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                border: 2px solid rgba(255,255,255,0.2);
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.1);
            }
        """)
        self.userButton.clicked.connect(self.showUserMenu)
        layout.addWidget(self.userButton)

        self.updateActiveMenu("anasayfa")

    def createMenuButton(self, text, iconPath, menuName):
        btn = QPushButton(text)
        btn.setIcon(QIcon(iconPath))
        btn.setIconSize(QSize(24, 24))
        btn.setProperty("menuName", menuName)
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 20px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.2);
            }
            QPushButton[active="true"] {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #b4342f,
                    stop:1 #620c0c
                );
                border: 2px solid #fff;
                color: white;
                font-weight: bold;
            }
        """)
        btn.clicked.connect(lambda: self.navigateToPage(menuName))
        return btn

    def updateActiveMenu(self, menuName):
        for btn in [self.btnAnasayfa, self.btnIzlendi, self.btnIzleniyor, self.btnIzlenecek]:
            if btn.property("menuName") == menuName:
                btn.setProperty("active", "true")
            else:
                btn.setProperty("active", "false")
            btn.setStyle(btn.style())  # Güncelle

        self.activeMenu = menuName

    def navigateToPage(self, menuName):
        self.updateActiveMenu(menuName)
        self.menuSecildi.emit(menuName)

    def showUserMenu(self):
        menu = QMenu()
        actAyarlar = QAction("Ayarlar", self)
        actCikis = QAction("Çıkış yap", self)

        actAyarlar.triggered.connect(lambda: self.kullaniciMenuSecildi.emit("ayarlar"))
        actCikis.triggered.connect(lambda: self.kullaniciMenuSecildi.emit("cikis"))

        menu.addAction(actAyarlar)
        menu.addAction(actCikis)
        menu.exec_(self.userButton.mapToGlobal(self.userButton.rect().bottomLeft()))