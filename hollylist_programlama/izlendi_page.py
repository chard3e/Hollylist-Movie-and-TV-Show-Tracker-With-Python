
from tablo_page import *

class IzlendiPage(TabloPage):
    def __init__(self, kullaniciAdi, parent=None):
        super().__init__(kullaniciAdi, "İzlendi", puanFiltre=True, parent=parent)
