# star_rating_widget.py

import os
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QSize

class StarRatingWidget(QWidget):
    ratingChanged = pyqtSignal(int)

    def __init__(self, initial=0, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.stars = []
        self.currentRating = initial

        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_dir = os.path.join(script_dir, "icons")

        star_on_path = os.path.join(icon_dir, "star_on.png")
        star_off_path = os.path.join(icon_dir, "star_off.png")

        if not os.path.exists(star_on_path):
            print(f"İkon bulunamadı: {star_on_path}")
        if not os.path.exists(star_off_path):
            print(f"İkon bulunamadı: {star_off_path}")

        for i in range(1, 6):
            star = QPushButton()
            star.setFixedSize(40, 40)
            star.setFlat(True)
            star.setStyleSheet("background: transparent; border: none;")

            if i <= self.currentRating:
                if os.path.exists(star_on_path):
                    icon = QIcon(star_on_path)
                    star.setIcon(icon)
                    print(f"Dolu yıldız yüklendi: {star_on_path}")  # Debug
                else:
                    star.setText("★")
                    print(f"Dolu yıldız ikonu bulunamadı, metin kullanılıyor.")  # Debug
            else:
                if os.path.exists(star_off_path):
                    icon = QIcon(star_off_path)
                    star.setIcon(icon)
                    print(f"Boş yıldız yüklendi: {star_off_path}")  # Debug
                else:
                    star.setText("☆")
                    print(f"Boş yıldız ikonu bulunamadı, metin kullanılıyor.")  # Debug

            star.setIconSize(QSize(32, 32))
            star.clicked.connect(lambda checked, x=i: self.setRating(x))
            self.stars.append(star)
            self.layout.addWidget(star)

        self.updateStars()

    def setRating(self, rating):
        if rating < 0:
            rating = 0
        elif rating > 5:
            rating = 5
        self.currentRating = rating
        self.updateStars()
        self.ratingChanged.emit(self.currentRating)
        print(f"Puan güncellendi: {self.currentRating}")  # Debug

    def getRating(self):
        return self.currentRating

    def setStarRating(self, rating):
        self.setRating(rating)

    def updateStars(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_dir = os.path.join(script_dir, "iconlar")
        star_on_path = os.path.join(icon_dir, "star_on.png")
        star_off_path = os.path.join(icon_dir, "star_off.png")

        for i, star in enumerate(self.stars, 1):
            if i <= self.currentRating:
                if os.path.exists(star_on_path):
                    star.setIcon(QIcon(star_on_path))
                    star.setText("")
                    print(f"Dolu yıldız yüklendi: {star_on_path}")  # Debug
                else:
                    star.setText("★")
                    print(f"Dolu yıldız ikonu bulunamadı, metin kullanılıyor: {star_on_path}")  # Debug
            else:
                if os.path.exists(star_off_path):
                    star.setIcon(QIcon(star_off_path))
                    star.setText("")
                    print(f"Boş yıldız yüklendi: {star_off_path}")  # Debug
                else:
                    star.setText("☆")
                    print(f"Boş yıldız ikonu bulunamadı, metin kullanılıyor: {star_off_path}")  # Debug
