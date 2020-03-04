import sys

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import _sqlite3

conn = _sqlite3.connect("kutuphane.db")
kalem = conn.cursor()

ButtonFontu = QFont("Century Gothic",24)
LabelFontu = QFont("Century Gothic",30)
YaziFontu = QFont("Century Gothic",16)
CloseFontu = QFont()

def Window(defaultWindow):

    backwardButton = QPushButton("<",defaultWindow)
    backwardButton.setFont(LabelFontu)
    backwardButton.setGeometry(20,20,50,50)
    backwardButton.clicked.connect(defaultWindow.geriDon)

    closeButton = QPushButton("X", defaultWindow)
    closeButton.setFont(CloseFontu)
    closeButton.setGeometry(1300, 20, 50, 50)
    closeButton.clicked.connect(Pencere.Close)

class Intro(QWidget):
    def __init__(self):
        super().__init__()

        yatay = QHBoxLayout()

        self.intro = QLabel("Kütüphane Sistemi")

        yatay.addStretch()
        yatay.addWidget(self.intro)
        yatay.addStretch()

        self.intro.setFont(ButtonFontu)
        self.setLayout(yatay)
class kitapListesi(QWidget):

    def __init__(self):
        super().__init__()

        Window(self)

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        baslık = QLabel("Kitap Listesi")
        baslık.setFont(LabelFontu)
        aciklama = QLabel("Durumunu görmek istediğiniz kitabın üzerine tıklayınız")

        liste = QListWidget()


        newAdd = QPushButton("Yeni Kitap Ekle")
        newAdd.setFont(ButtonFontu)
        newAdd.clicked.connect(self.yeniEkle)

        kitaplar = kalem.execute("Select *from Kitaplar")

        for i in kitaplar.fetchall():
            liste.addItem(i[1])

        liste.itemClicked.connect(self.kitapBilgi)

        dikey.addWidget(baslık)
        dikey.addWidget(aciklama)
        dikey.addWidget(liste)
        dikey.addWidget(newAdd)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)
    def kitapBilgi(self,item):
        kitapismi = item.text()
        kontrol = kalem.execute("Select *from Kitaplar Where kitap_ad=?",(kitapismi,))
        durum = kontrol.fetchall()[0][2]
        if(durum==0):
            QMessageBox.information(self,"Kitap Bilgisi",kitapismi+" isimli kitap şuan boştadır")
        else:
            kimde = kalem.execute("Select *from Odunc Where kitap_ad=?",(kitapismi,))
            ogrenci = kimde.fetchall()[0][1]
            QMessageBox.information(self,"Kitap Bilgisi",kitapismi + " isimli kitap şuanda " + ogrenci + " adlı öğrencide")
    def yeniEkle(self):
        self.yeni = yenikitapEkle()
        self.yeni.show()
    def geriDon(self):
        self.close()
class yenikitapEkle(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yeni Kitap Ekle")

        self.dikey = QVBoxLayout()

        baslik = QLabel("Yeni Kitap Ekle")
        baslik.setFont(ButtonFontu)

        self.kitapismi = QLineEdit()
        self.kitapismi.setPlaceholderText("Kitap ismini giriniz")

        kaydet = QPushButton("Kaydet")
        kaydet.clicked.connect(self.kaydet)

        self.dikey.addWidget(baslik)
        self.dikey.addWidget(self.kitapismi)
        self.dikey.addWidget(kaydet)

        self.setLayout(self.dikey)
    def kaydet(self):
        bilgi = QLabel("Kaydediliyor ... Lütfen bekleyiniz")
        self.dikey.addWidget(bilgi)
        QTest.qWait(750)

        isim = self.kitapismi.text()
        kalem.execute("Insert Into Kitaplar (kitap_ad) Values(?)",(isim,))
        conn.commit()

        bilgi.setText("Kayıt Başarılı")
        QTest.qWait(500)
        self.close()
class yeniOgrenci(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yeni Öğrenci İsmi Ekle")

        self.dikey = QVBoxLayout()

        baslik = QLabel("Yeni Öğrenci Ekle")
        baslik.setFont(ButtonFontu)

        self.ogrenciismi = QLineEdit()
        self.ogrenciismi.setPlaceholderText("Öğrenci ismini giriniz")

        kaydet = QPushButton("Kaydet")
        kaydet.clicked.connect(self.kaydet)

        self.dikey.addWidget(baslik)
        self.dikey.addWidget(self.ogrenciismi)
        self.dikey.addWidget(kaydet)

        self.setLayout(self.dikey)
    def kaydet(self):
        bilgi = QLabel("Kaydediliyor ... Lütfen bekleyiniz")
        self.dikey.addWidget(bilgi)
        QTest.qWait(750)

        isim = self.ogrenciismi.text()
        kalem.execute("Insert Into Ogrenciler (ogrenci_ad) Values(?)",(isim,))
        conn.commit()

        bilgi.setText("Kayıt Başarılı")
        QTest.qWait(500)
        self.close()
class yeniOdunc(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yeni Ödünç Alma İşlemi Ekle")

        self.dikey = QVBoxLayout()

        baslik = QLabel("Yeni Ödünç Alma İşlemi Ekle")
        baslik.setFont(ButtonFontu)

        self.ogrenciismi = QLineEdit()
        self.ogrenciismi.setPlaceholderText("Öğrenci ismini giriniz")

        self.kitapismi = QLineEdit()
        self.kitapismi.setPlaceholderText("Kitabın ismini giriniz")

        kaydet = QPushButton("Kaydet")
        kaydet.clicked.connect(self.kaydet)

        self.dikey.addWidget(baslik)
        self.dikey.addWidget(self.ogrenciismi)
        self.dikey.addWidget(self.kitapismi)
        self.dikey.addWidget(kaydet)

        self.setLayout(self.dikey)
    def kaydet(self):
        bilgi = QLabel("Kaydediliyor ... Lütfen bekleyiniz")
        self.dikey.addWidget(bilgi)
        QTest.qWait(750)

        ogrencismi = self.ogrenciismi.text()
        kitapismi = self.kitapismi.text()
        kalem.execute("Insert Into Odunc (ogrenci_ad,kitap_ad) Values(?,?)",(ogrencismi,kitapismi))
        conn.commit()

        bilgi.setText("Kayıt Başarılı")
        QTest.qWait(500)
        self.close()
class yeniIade(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yeni İade İşlemi Ekle")

        self.dikey = QVBoxLayout()

        baslik = QLabel("Yeni İade İşlemi Ekle")
        baslik.setFont(ButtonFontu)

        self.ogrenciismi = QLineEdit()
        self.ogrenciismi.setPlaceholderText("Öğrenci ismini giriniz")

        self.kitapismi = QLineEdit()
        self.kitapismi.setPlaceholderText("Kitabın ismini giriniz")

        kaydet = QPushButton("Kaydet")
        kaydet.clicked.connect(self.kaydet)

        self.dikey.addWidget(baslik)
        self.dikey.addWidget(self.ogrenciismi)
        self.dikey.addWidget(self.kitapismi)
        self.dikey.addWidget(kaydet)

        self.setLayout(self.dikey)
    def kaydet(self):
        bilgi = QLabel("Kaydediliyor ... Lütfen bekleyiniz")
        self.dikey.addWidget(bilgi)
        QTest.qWait(750)

        ogrencismi = self.ogrenciismi.text()
        kitapismi = self.kitapismi.text()
        kalem.execute("Delete from Odunc Where ogrenci_ad=? And kitap_ad=?",(ogrencismi,kitapismi))
        conn.commit()

        bilgi.setText("Kayıt Başarılı")
        QTest.qWait(500)
        self.close()
class ogrenciListesi(QWidget):
    def __init__(self):
        super().__init__()

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        Window(self)

        baslık = QLabel("Öğrenci Listesi")
        baslık.setFont(LabelFontu)
        aciklama = QLabel("Kitapların durumunu öğrenmek için öğrencilere tıklayınız")

        liste = QListWidget()

        newAdd = QPushButton("Yeni Öğrenci Ekle")
        newAdd.setFont(ButtonFontu)
        newAdd.clicked.connect(self.yeniEkle)

        ogrenciler = kalem.execute("Select *from Ogrenciler")

        for i in ogrenciler.fetchall():
            liste.addItem(i[1])

        liste.itemClicked.connect(self.ogrenciBilgi())

        dikey.addWidget(baslık)
        dikey.addWidget(aciklama)
        dikey.addWidget(liste)
        dikey.addWidget(newAdd)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)

    def ogrenciBilgi(self, item):
        ogrenciismi = item.text()
        kontrol = kalem.execute("Select *from Odunc Where ogrenci_ad=?", (ogrenciismi,))
        say = len(kontrol.fetchall())
        if (say == 0):
            QMessageBox.information(self, "Öğrenci Bilgisi", ogrenciismi + " isimli öğrencinin elinde şuan hiç kitap yok")
        else:
            hangi = kalem.execute("Select *from Odunc Where ogrenci_ad=?", (ogrenciismi,))
            kitap = hangi.fetchall()[0][2]
            QMessageBox.information(self, "Öğrenci Bilgisi",
                                    ogrenciismi + " isimli öğrencinin elinde şuan bu kitap var: " + kitap)


    def geriDon(self):
        self.close()
    def yeniEkle(self):
        self.yeni = yeniOgrenci()
        self.yeni.show()
class oduncListesi(QWidget):
    def __init__(self):
        super().__init__()

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        Window(self)

        baslık = QLabel("Ödünç  İşlemleri Listesi")
        baslık.setFont(LabelFontu)

        liste = QListWidget()

        newAdd = QPushButton("Yeni Ödünç Alma İşlemi Ekle")
        iadeAdd = QPushButton("Yeni İade Alma İşlemi Ekle")
        newAdd.setFont(ButtonFontu)
        iadeAdd.setFont(ButtonFontu)
        newAdd.clicked.connect(self.yeniEkle)
        iadeAdd.clicked.connect(self.iadeEkle)


        oduncler = kalem.execute("Select *From Odunc")

        for i in oduncler.fetchall():
            eklenecek = i[1] + " - " + i[2]
            liste.addItem(eklenecek)

        dikey.addWidget(baslık)
        dikey.addWidget(liste)
        dikey.addWidget(iadeAdd)
        dikey.addWidget(newAdd)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)

    def geriDon(self):
        self.close()
    def yeniEkle(self):
        self.yeni = yeniOdunc()
        self.yeni.show()
    def iadeEkle(self):
        self.yeni = yeniIade()
        self.yeni.show()
class yardimHakkimizda(QWidget):
    def __init__(self):
        super().__init__()

        Window(self)

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        baslik = QLabel("Yardım - Hakkımızda")
        baslik.setFont(ButtonFontu)
        yazi = QLabel("Bu Projede Python programlama dili ve DB Browser veritabanı kullanılarak kütüphane sistemi yazılmıştır.\n"
                      "Projede classlar ve fonksiyonlar kullanılmıştır.")
        yazi.setFont(YaziFontu)

        dikey.addWidget(baslik)
        dikey.addStretch()
        dikey.addWidget(yazi)
        dikey.addStretch()

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)

    def geriDon(self):
        self.close()
class Pencere(QWidget):

    def __init__(self):
        super().__init__()
        
        self.intro = Intro()
        self.intro.showFullScreen()
        QTest.qWait(5000)


        closeButton = QPushButton("X", self)
        closeButton.setFont(CloseFontu)
        closeButton.setGeometry(1300, 20, 50, 50)
        closeButton.clicked.connect(self.Close)


        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        baslik = QLabel("Kütüphane Otomasyonu")
        baslik.setFont(LabelFontu)

        bookButton = QPushButton("Kitap Listesi")
        bookButton.setFont(ButtonFontu)
        studentButton=QPushButton("Öğrenci Listesi")
        studentButton.setFont(ButtonFontu)
        processButton = QPushButton("Ödünç Listesi")
        processButton.setFont(ButtonFontu)
        helpButton = QPushButton("Yardım - Hakkımızda")
        helpButton.setFont(ButtonFontu)

        bookButton.clicked.connect(self.kitapAc)
        studentButton.clicked.connect(self.ogrenciAc)
        processButton.clicked.connect(self.islemAc)
        helpButton.clicked.connect(self.yardimAc)

        dikey.addWidget(baslik)
        dikey.addStretch()
        dikey.addWidget(bookButton)
        dikey.addStretch()
        dikey.addWidget(studentButton)
        dikey.addStretch()
        dikey.addWidget(processButton)
        dikey.addStretch()
        dikey.addWidget(helpButton)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)
        self.showFullScreen()

    def islemAc(self):
        self.islem = oduncListesi()
        self.islem.showFullScreen()
    def kitapAc(self):
        self.kitap = kitapListesi()
        self.kitap.showFullScreen()
    def ogrenciAc(self):
        self.ogrenci = ogrenciListesi()
        self.ogrenci.showFullScreen()
    def yardimAc(self):
        self.yardim = yardimHakkimizda()
        self.yardim.showFullScreen()
    def Close(self):
        qApp.quit()

uygulama = QApplication(sys.argv)
pencere= Pencere()
sys.exit(uygulama.exec_())

