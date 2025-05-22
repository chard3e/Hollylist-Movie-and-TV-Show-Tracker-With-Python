

from tablo_page import *

class IzleniyorPage(TabloPage):

    def __init__(self, kullaniciAdi, parent=None):
        super().__init__(kullaniciAdi, "İzleniyor", puanFiltre=True, parent=parent)
