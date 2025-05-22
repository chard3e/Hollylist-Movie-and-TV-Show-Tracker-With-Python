import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QFrame
)

from veritabani import kayitlari_oku

class AnaSayfa(QWidget):
    def __init__(self, kullaniciAdi):
        super().__init__()
        self.kullaniciAdi = kullaniciAdi

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

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        centerWidget = QWidget()
        centerLayout = QHBoxLayout(centerWidget)
        centerLayout.setContentsMargins(20, 20, 20, 20)
        centerLayout.setSpacing(15)

        # Sol alan: Son eklenen filmler/diziler
        self.leftArea = self.buildLeftArea()
        centerLayout.addWidget(self.leftArea, 3)

        # Sağ istatistik paneli
        self.rightStats = self.buildRightStats()
        centerLayout.addWidget(self.rightStats, 1)

        mainLayout.addWidget(centerWidget, 1)

        self.loadDataFromCSV()

    def buildLeftArea(self):
        container = QWidget()
        vbox = QVBoxLayout(container)
        vbox.setSpacing(5)
        vbox.setContentsMargins(0, 0, 0, 0)


        lblFilmler = QLabel("Son eklenen filmler")
        lblFilmler.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        vbox.addWidget(lblFilmler, alignment=Qt.AlignLeft)

        # Filmler kutusu
        self.filmlerFrame = QFrame()
        self.filmlerFrame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 #b4342f, stop:1 #620c0c
                );
                border-radius: 15px;
            }
        """)
        self.filmlerFrame.setMinimumHeight(250)

        filmLayout = QHBoxLayout(self.filmlerFrame)
        filmLayout.setContentsMargins(10, 10, 10, 10)
        filmLayout.setSpacing(8)
        self.filmsLayout = filmLayout
        vbox.addWidget(self.filmlerFrame)

        lblDiziler = QLabel("Son eklenen diziler")
        lblDiziler.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        vbox.addWidget(lblDiziler, alignment=Qt.AlignLeft)

        # Diziler kutusu
        self.dizilerFrame = QFrame()
        self.dizilerFrame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 #b4342f, stop:1 #620c0c
                );
                border-radius: 15px;
            }
        """)
        self.dizilerFrame.setMinimumHeight(250)

        diziLayout = QHBoxLayout(self.dizilerFrame)
        diziLayout.setContentsMargins(10, 10, 10, 10)
        diziLayout.setSpacing(8)
        self.seriesLayout = diziLayout
        vbox.addWidget(self.dizilerFrame)

        vbox.addStretch()
        return container

    def buildRightStats(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 #b4342f, 
                    stop:1 #620c0c
                );
                border-radius: 20px;
            }
        """)
        frame.setMinimumWidth(250)

        vbox = QVBoxLayout(frame)
        vbox.setContentsMargins(15, 15, 15, 15)
        vbox.setSpacing(10)

        # İstatistik label'ları
        styleStats = "color: white; font-size: 16px; background: transparent;"
        self.lblEnSonBitDizi = QLabel("En son bitirdiğin dizi: -")
        self.lblEnSonBitDizi.setStyleSheet(styleStats)
        self.lblEnSonBitDizi.setWordWrap(True)

        self.lblEnSonBitFilm = QLabel("En son bitirdiğin film: -")
        self.lblEnSonBitFilm.setStyleSheet(styleStats)
        self.lblEnSonBitFilm.setWordWrap(True)

        self.lblYuksekPuanDizi = QLabel("En yüksek puanlı dizin: -")
        self.lblYuksekPuanDizi.setStyleSheet(styleStats)
        self.lblYuksekPuanDizi.setWordWrap(True)

        self.lblYuksekPuanFilm = QLabel("En yüksek puanlı filmin: -")
        self.lblYuksekPuanFilm.setStyleSheet(styleStats)
        self.lblYuksekPuanFilm.setWordWrap(True)

        self.lblDusukPuanDizi = QLabel("En düşük puanlı dizin: -")
        self.lblDusukPuanDizi.setStyleSheet(styleStats)
        self.lblDusukPuanDizi.setWordWrap(True)

        self.lblDusukPuanFilm = QLabel("En düşük puanlı filmin: -")
        self.lblDusukPuanFilm.setStyleSheet(styleStats)
        self.lblDusukPuanFilm.setWordWrap(True)

        self.lblToplamDiziSayisi = QLabel("Toplam dizi sayısı: 0")
        self.lblToplamDiziSayisi.setStyleSheet(styleStats)

        self.lblToplamFilmSayisi = QLabel("Toplam film sayısı: 0")
        self.lblToplamFilmSayisi.setStyleSheet(styleStats)

        self.lblToplamBolum = QLabel("İzlediğin toplam bölüm: 0")
        self.lblToplamBolum.setStyleSheet(styleStats)

        self.lblEnCokIzlenenTur = QLabel("En çok izlenen tür: -")
        self.lblEnCokIzlenenTur.setStyleSheet(styleStats)

        stats = [
            self.lblEnSonBitDizi,
            self.lblEnSonBitFilm,
            self.lblYuksekPuanDizi,
            self.lblYuksekPuanFilm,
            self.lblDusukPuanDizi,
            self.lblDusukPuanFilm,
            self.lblToplamDiziSayisi,
            self.lblToplamFilmSayisi,
            self.lblToplamBolum,
            self.lblEnCokIzlenenTur
        ]
        for lab in stats:
            vbox.addWidget(lab)

        vbox.addStretch()

        self.btnEkle = QPushButton("EKLE")
        self.btnEkle.setStyleSheet("""
            QPushButton {
                background-color: #fa3c4c;
                color: white;
                font-weight: bold;
                font-size: 15px;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #f72b3c;
            }
        """)
        vbox.addWidget(self.btnEkle, alignment=Qt.AlignCenter)

        return frame

    def loadDataFromCSV(self):
        kayitlar = kayitlari_oku(self.kullaniciAdi)
        filmler = [k for k in kayitlar if k["Dizi/Film"].lower() == "film"]
        diziler = [k for k in kayitlar if k["Dizi/Film"].lower() == "dizi"]


        while self.filmsLayout.count():
            item = self.filmsLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        while self.seriesLayout.count():
            item = self.seriesLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()


        lastFilms = filmler[-5:]
        lastDiziler = diziler[-5:]

        # Posterler
        for film in lastFilms:
            w = self.createPosterWidget(film["Ad"], film["Durum"], film["Afiş"])
            self.filmsLayout.addWidget(w)

        for dizi in lastDiziler:
            w = self.createPosterWidget(dizi["Ad"], dizi["Durum"], dizi["Afiş"])
            self.seriesLayout.addWidget(w)

        self.calculateStats(filmler, diziler)

    def createPosterWidget(self, ad, durum, afisPath):
        container = QFrame()
        container.setFixedSize(130, 250)
        container.setStyleSheet("QFrame { background: transparent; border-radius: 10px; }")

        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(4,4,4,4)
        vbox.setSpacing(4)

        lblAfis = QLabel()
        lblAfis.setFixedSize(120, 180)
        lblAfis.setStyleSheet("background: transparent")
        lblAfis.setAlignment(Qt.AlignCenter)

        if os.path.exists(afisPath):
            pix = QPixmap(afisPath)
            scaled = pix.scaled(
                lblAfis.width(),
                lblAfis.height(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            lblAfis.setPixmap(scaled)
        else:
            lblAfis.setText("No Image")

        vbox.addWidget(lblAfis, alignment=Qt.AlignCenter)

        lblInfo = QLabel(f"{ad}\n({durum})")
        lblInfo.setStyleSheet("color: white; font-size: 12px; background: transparent;")
        lblInfo.setAlignment(Qt.AlignCenter)
        vbox.addWidget(lblInfo)

        return container

    def calculateStats(self, filmler, diziler):
        izlendiFilmler = [f for f in filmler if f["Durum"] == "İzlendi"]
        izlendiDiziler = [d for d in diziler if d["Durum"] == "İzlendi"]

        if izlendiFilmler:
            self.lblEnSonBitFilm.setText(f"En son bitirdiğin film: {izlendiFilmler[-1]['Ad']}")
        else:
            self.lblEnSonBitFilm.setText("En son bitirdiğin film: -")

        if izlendiDiziler:
            self.lblEnSonBitDizi.setText(f"En son bitirdiğin dizi: {izlendiDiziler[-1]['Ad']}")
        else:
            self.lblEnSonBitDizi.setText("En son bitirdiğin dizi: -")

        if izlendiFilmler:
            bestF = max(izlendiFilmler, key=lambda x: x["Puan"] if isinstance(x["Puan"], int) else 0)
            worstF = min(izlendiFilmler, key=lambda x: x["Puan"] if isinstance(x["Puan"], int) else 0)
            self.lblYuksekPuanFilm.setText(
                f"En yüksek puanlı filmin: {bestF['Ad']} (puan={bestF['Puan']})"
            )
            self.lblDusukPuanFilm.setText(
                f"En düşük puanlı filmin: {worstF['Ad']} (puan={worstF['Puan']})"
            )
        else:
            self.lblYuksekPuanFilm.setText("En yüksek puanlı filmin: -")
            self.lblDusukPuanFilm.setText("En düşük puanlı filmin: -")

        if izlendiDiziler:
            bestD = max(izlendiDiziler, key=lambda x: x["Puan"] if isinstance(x["Puan"], int) else 0)
            worstD = min(izlendiDiziler, key=lambda x: x["Puan"] if isinstance(x["Puan"], int) else 0)
            self.lblYuksekPuanDizi.setText(
                f"En yüksek puanlı dizin: {bestD['Ad']} (puan={bestD['Puan']})"
            )
            self.lblDusukPuanDizi.setText(
                f"En düşük puanlı dizin: {worstD['Ad']} (puan={worstD['Puan']})"
            )
        else:
            self.lblYuksekPuanDizi.setText("En yüksek puanlı dizin: -")
            self.lblDusukPuanDizi.setText("En düşük puanlı dizin: -")


        self.lblToplamFilmSayisi.setText(f"Toplam film sayısı: {len(filmler)}")
        self.lblToplamDiziSayisi.setText(f"Toplam dizi sayısı: {len(diziler)}")


        toplamBolum = 0
        for d in diziler:
            iler = d["İlerleme"]
            parts = iler.split("/")
            if len(parts) == 2:
                try:
                    x = int(parts[0])
                    toplamBolum += x
                except:
                    pass
        self.lblToplamBolum.setText(f"İzlediğin toplam bölüm: {toplamBolum}")


        izlendiHepsi = izlendiFilmler + izlendiDiziler
        turSayac = {}
        for item in izlendiHepsi:
            turStr = item["Tür"]
            altTurler = turStr.split("/")
            for t in altTurler:
                t = t.strip().title()
                if t:
                    turSayac[t] = turSayac.get(t, 0) + 1

        if turSayac:
            enCok = max(turSayac, key=turSayac.get)
            self.lblEnCokIzlenenTur.setText(f"En çok izlenen tür: {enCok} ({turSayac[enCok]})")
        else:
            self.lblEnCokIzlenenTur.setText("En çok izlenen tür: -")

