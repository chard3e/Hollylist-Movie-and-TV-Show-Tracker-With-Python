
from tablo_page import TabloPage

class IzlenecekPage(TabloPage):

    def __init__(self, kullaniciAdi, parent=None):
        super().__init__(kullaniciAdi, "İzlenecek", puanFiltre=False, parent=parent)
