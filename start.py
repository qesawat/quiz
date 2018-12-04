import json
import os
import sys
from datetime import datetime

from PyQt5.QtCore import QEvent, QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QCursor, QFont, QFontDatabase, QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QFormLayout, QFrame,
                             QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                             QMessageBox, QProgressBar, QPushButton,
                             QRadioButton, QScrollArea, QStackedWidget,
                             QStatusBar, QTextEdit, QVBoxLayout, QWidget, qApp)

with open("style.css","r") as file:
    stil = file.read()

class Window(QMainWindow):
    def __init__(self,parent=None):
        
        super(Window,self).__init__(parent)
        
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint ) #title bar hide
        
        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont("font/Handlee.ttf")
        families = font_db.applicationFontFamilies(font_id)
        self.my_ttf_font = QFont("Handlee")
        
        self.setWindowIcon(QIcon("./icon/icon.png"))

        self.setWindowTitle("Testler")
        self.bas = Baslangic(self)
        self.cenWid = QStackedWidget()
        self.setCentralWidget(self.cenWid)
        self.cenWid.addWidget(self.bas)
        
        self.setStyleSheet(stil)
        
        
        self.initUi()
    
        
    def initUi(self):
        
        
        
        self.setMinimumSize(750,550)
        
        self.v = QStatusBar()
        self.setStatusBar(self.v)
        self.myBar = MyBar(self)
        self.setMenuWidget(self.myBar)
        
        self.myBar.maximize.mousePressEvent = lambda even:  self.maximizeDef() 
        self.myBar.minimize.mousePressEvent = lambda even:  self.showMinimized()
        self.myBar.fullscreen.mousePressEvent = lambda even: self.fullEkran()
        self.myBar.newMenu.mousePressEvent = lambda event: self.selected_ac(self,pr="Baslangic")
        

        
        
    
    def fullEkran(self):
        if self.windowState():
            self.showNormal()
        else:
            self.showFullScreen()
    def maximizeDef(self):
        
        if self.windowState():
            self.showNormal()
            
        else:
            self.showMaximized()   
        
    def selected_ac(self,q,pr="",baslik=""):
        if pr == "Ana":
            widgetl = IcerikWidget(self,name=str(baslik))
            self.cenWid.addWidget(widgetl)
            self.cenWid.setCurrentWidget(widgetl)
        elif pr =="Baslangic":
            c = Baslangic(self)
            self.cenWid.addWidget(c)
            self.cenWid.setCurrentWidget(c)
        elif pr =="Duzenle":
            duzen = Duzenle(self,baslik=baslik)
            self.cenWid.addWidget(duzen)
            self.cenWid.setCurrentWidget(duzen)
        else:
            if q.text() == "Exit":
                qApp.quit()
            elif q.text() == "Baslangic":
                bas = Baslangic(self)
                self.cenWid.addWidget(bas)
                self.cenWid.setCurrentWidget(bas)
            elif q.text() == "Duzenle":
                duzen = Duzenle(self)
                self.cenWid.addWidget(duzen)
                self.cenWid.setCurrentWidget(duzen)
            

class MyBar(QPushButton):
    def __init__(self,parent):
        super(MyBar,self).__init__(parent)
        self.setStyleSheet("background-color:rgb(20, 20, 20);border:none")
        self.parent = parent
        self.toplistButtonBox = QHBoxLayout(self)
        self.toplistButtonBox.setContentsMargins(0,0,0,0)
        
        self.fullscreen = QLabel("")
        self.fullscreen.setPixmap(QPixmap("icon/scale-screen.png"))
        self.minimize = QLabel("")
        self.minimize.setPixmap(QPixmap("icon/minimize.png"))
        self.maximize = QLabel("")
        self.maximize.setPixmap(QPixmap("icon/maximize.png"))
        self.shoutdown = QLabel("")
        self.shoutdown.setPixmap(QPixmap("icon/er.png"))
        
        self.title = QLabel("MyWorkPlace")
        self.newMenu = QLabel("Baslangic")
        self.newMenu.setObjectName("anaMenu")
        self.newMenu.setMinimumWidth(30)
        self.newMenu.setCursor(Qt.PointingHandCursor)
        
       
        
        
        self.title.setStyleSheet("background-color:rgb(20, 20, 20);color:#fff;margin:0px;padding:2px")
        self.fullscreen.setStyleSheet("background-color:rgb(20, 20, 20);color:#fff;margin:0px;padding:1px")
        self.minimize.setStyleSheet("background-color:rgb(20, 20, 20);color:#fff;margin:0px;padding:1px")
        self.maximize.setStyleSheet("background-color:rgb(20, 20, 20);color:#fff;margin:0px;padding:1px")
        self.shoutdown.setStyleSheet("background-color:rgb(20, 20, 20);color:#fff;margin:0px;padding:1px")
        
        
        self.title.setFixedHeight(34)
        self.title.setAlignment(Qt.AlignCenter)
        
        self.toplistButtonBox.addWidget(self.newMenu)
        self.toplistButtonBox.addStretch()
        self.toplistButtonBox.addWidget(self.title)
        self.toplistButtonBox.addStretch()
        self.toplistButtonBox.addWidget(self.fullscreen)
        self.toplistButtonBox.addWidget(self.minimize)
        self.toplistButtonBox.addWidget(self.maximize)
        self.toplistButtonBox.addWidget(self.shoutdown)
        

 
        self.shoutdown.mousePressEvent = lambda even: qApp.quit()
        

       

    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True
        
    

    def mouseMoveEvent(self, event):
        
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

class IcerikWidget(QWidget):
    def __init__(self,parent=None,name=""):
        super(IcerikWidget,self).__init__(parent)
        
        self.parent =parent
        self.name = "icerik/"+name+".json"
        self.init_ui()

    def init_ui(self):
        
        
        with open(self.name,"r") as file:
            self.json_veri =file.read()
        self.json_veriq = json.loads(self.json_veri)
        self.aktifSoru =0
        self.area = QScrollArea()
        self.area.setAlignment(Qt.AlignCenter)
        self.area.setWidgetResizable(True)
        self.area.setMaximumHeight(300)
        self.area.setMinimumHeight(150)
        
        

        self.metin =QLabel(self.json_veriq["sorular"][self.aktifSoru]["metin"])
        self.metin.setWordWrap(True)
        
        self.metin.setAlignment(Qt.AlignVCenter)
        self.metin.setObjectName("metin_icerik")
        self.metin.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        self.metin.setFont(QFont("Handlee",16))
        self.area.setWidget(self.metin)
        
        
        
        self.soru = QLabel(self.json_veriq["sorular"][self.aktifSoru]["soru"])
        self.soru.setObjectName("soru")
        self.soru.setAlignment(Qt.AlignCenter )
        self.soru.setTextInteractionFlags(Qt.TextSelectableByMouse);
        

        
       
        self.form = QFormLayout()
        self.sik_0 = QRadioButton(self.json_veriq["sorular"][self.aktifSoru]["siklar"][0])
        self.sik_0.setObjectName("0")
        self.sik_1 = QRadioButton(self.json_veriq["sorular"][self.aktifSoru]["siklar"][1])
        self.sik_1.setObjectName("1")
        self.sik_2 = QRadioButton(self.json_veriq["sorular"][self.aktifSoru]["siklar"][2])
        self.sik_2.setObjectName("2")
        self.sik_3 = QRadioButton(self.json_veriq["sorular"][self.aktifSoru]["siklar"][3])
        self.sik_3.setObjectName("3")

        self.form.addRow(self.sik_0)
        self.form.addRow(self.sik_1)
        self.form.addRow(self.sik_2)
        self.form.addRow(self.sik_3)
        
        


        self.next = QPushButton("İleri")
        self.next.setIcon(QIcon("icon/next.png"))
        self.back = QPushButton("Geri")
        self.back.setIcon(QIcon("icon/back.png"))

        self.progres = QProgressBar()
        self.progres.setMaximum(len(self.json_veriq["sorular"] )-1)
        self.progres.setMinimum(0)
        self.progres.setValue(self.aktifSoru)

        self.hb = QHBoxLayout()
        self.hb.addWidget(self.back)
        self.hb.addStretch()
        self.hb.addWidget(self.next)

        self.sonuc = QLabel("başarısız oldu")
        self.sonuc.setObjectName("sonuc")
        
        self.sonuc.setPixmap(QPixmap("icon/locked.png"))
        self.sonuc.setAlignment(Qt.AlignCenter)

        
       
        
        
        
        self.v_box1 = QVBoxLayout()
        
        self.v_box1.addWidget(self.area)
        self.v_box1.addStretch()
        self.v_box1.addWidget(self.soru)
        self.v_box1.addStretch()
        self.v_box1.addLayout(self.form)
        self.v_box1.addWidget(self.sonuc)
        
        

        self.l_vBox = QVBoxLayout()
        self.l_vBox.addLayout(self.v_box1)
        self.l_vBox.addStretch()
        self.l_vBox.addLayout(self.hb)
        self.l_vBox.addWidget(self.progres)

        self.setLayout(self.l_vBox)


        self.next.clicked.connect(self.ileri)
        self.back.clicked.connect(self.geri)
        self.sik_0.clicked.connect(self.secildi)
        self.sik_1.clicked.connect(self.secildi)
        self.sik_2.clicked.connect(self.secildi)
        self.sik_3.clicked.connect(self.secildi)
        
    
    
    def ileri(self):
        
        if self.aktifSoru < len(self.json_veriq["sorular"] )-1:
            
            self.aktifSoru += 1  
            
            self.metin.setText(self.json_veriq["sorular"][self.aktifSoru]["metin"])
            self.soru.setText(self.json_veriq["sorular"][self.aktifSoru]["soru"])
            self.sik_0.setText(self.json_veriq["sorular"][self.aktifSoru]["siklar"][0])
            self.sik_1.setText(self.json_veriq["sorular"][self.aktifSoru]["siklar"][1])
            self.sik_2.setText(self.json_veriq["sorular"][self.aktifSoru]["siklar"][2])
            self.sik_3.setText(self.json_veriq["sorular"][self.aktifSoru]["siklar"][3])
            self.sifirla()
            self.progres.setValue(self.aktifSoru)
            
    def geri(self):
        
        if not self.aktifSoru == 0:
            
            self.aktifSoru -= 1  
            
            self.metin.setText(self.json_veriq["sorular"][self.aktifSoru]["metin"])
            self.soru.setText(self.json_veriq["sorular"][self.aktifSoru]["soru"])
            self.sik_0.setText(self.json_veriq["sorular"][self.aktifSoru]["siklar"][0])
            
            self.sik_1.setText(self.json_veriq["sorular"][self.aktifSoru]["siklar"][1])
            self.sik_2.setText(self.json_veriq["sorular"][self.aktifSoru]["siklar"][2])
            self.sik_3.setText(self.json_veriq["sorular"][self.aktifSoru]["siklar"][3])
           
            self.sifirla()
            self.progres.setValue(self.aktifSoru)
                    
    def secildi(self):
        self.secilen = self.sender().objectName()

        self.dogru_sik =self.json_veriq["sorular"][self.aktifSoru]["dogruindex"]
        if self.secilen == self.dogru_sik:
            self.sonuc.setPixmap(QPixmap("icon/success.png"))
            self.sender().setStyleSheet("background-color:rgba(27, 58, 27, 0.658)")
            self.metin.setStyleSheet("background-color:rgba(27, 58, 27, 0.658)")
        else:
            self.sonuc.setPixmap(QPixmap("icon/error.png"))
            self.sender().setStyleSheet("background-color: rgba(58, 27, 27, 0.658)")
            self.metin.setStyleSheet("background-color: rgba(58, 27, 27, 0.658)")

    def sifirla(self):
        self.sik_0.setCheckable(False)
        self.sik_0.setCheckable(True)
        self.sik_0.setStyleSheet("outline: none; color: #212222; margin-bottom: 2px;border: 2px solid rgba(0, 0, 0, 0.2); color: rgb(255, 255, 255);")
        self.sik_1.setCheckable(False)
        self.sik_1.setCheckable(True)
        self.sik_1.setStyleSheet("outline: none; color: #212222; margin-bottom: 2px;border: 2px solid rgba(0, 0, 0, 0.2); color: rgb(255, 255, 255);")
        self.sik_2.setCheckable(False)
        self.sik_2.setCheckable(True)
        self.sik_2.setStyleSheet("outline: none; color: #212222; margin-bottom: 2px;border: 2px solid rgba(0, 0, 0, 0.2); color: rgb(255, 255, 255);")
        self.sik_3.setCheckable(False)
        self.sik_3.setCheckable(True)
        self.sik_3.setStyleSheet("outline: none; color: #212222; margin-bottom: 2px;border: 2px solid rgba(0, 0, 0, 0.2); color: rgb(255, 255, 255);")
        self.sonuc.setPixmap(QPixmap("icon/locked.png"))
        self.metin.setStyleSheet("background-color: rgb(29, 29, 29);")

class Baslangic(QWidget):
    def __init__(self,parent=None):
        super(Baslangic,self).__init__(parent)
        self.parent =parent
        self.init_ui()
    def init_ui(self):

        ar = QScrollArea()
        
        self.soruForm = QFormLayout()
        f = QFrame()
        f.setLayout(self.soruForm)
        ar.setWidget(f)
        ar.setWidgetResizable(True)
        self.hBox = QHBoxLayout()
        st = "padding:25px; border:1px solid #000;background-color:rgb(20,20,20)"
        self.testSayi = QLabel("0")
        self.testSayi.setStyleSheet(st)
        self.toplamSoru = QLabel("0")
        self.toplamSoru.setStyleSheet(st)
        self.vb = QVBoxLayout()
        self.b = QHBoxLayout()
        bl = QLabel("Toplam Test :")
        bl.setStyleSheet(st)
        self.b.addWidget(bl)
        self.b.addWidget(self.testSayi)
        self.c = QHBoxLayout()
        cl = QLabel("Toplam Soru:")
        cl.setStyleSheet(st)
        self.c.addWidget(cl)
        self.c.addWidget(self.toplamSoru)

        self.yeniTestEkleBtn = QPushButton("Yeni Test Ekle")

        self.vb.addLayout(self.b)
        self.vb.addLayout(self.c)
        self.vb.addWidget(self.yeniTestEkleBtn)
        self.vb.addStretch()

        self.hBox.addLayout(self.vb)
        self.hBox.addWidget(ar)


        if os.path.exists("icerik/"):
            dosyalar = os.listdir("icerik/")
            ds = []
            for item in dosyalar:
                d = os.stat("icerik/"+item)
                c = d.st_mtime
                ds .append([c,item])
                
            ds.sort(reverse=True)
            self.testSayi.setText(str(len(ds)))
            tops = 0
            for i in ds:
                with open("icerik/"+i[1],"r") as file:
                    self.json_ver =file.read()
                self.json_verim = json.loads(self.json_ver)
                uzunluk = len(self.json_verim["sorular"])
                isim = self.json_verim["isim"]
                tarih=os.stat("icerik/"+i[1]).st_mtime
                
                self.baslikEkle(isim,uzunluk,tarih)
                
                tops += len(self.json_verim["sorular"])

            self.toplamSoru.setText(str(tops))
        self.yeniTestEkleBtn.clicked.connect(self.yeniTestEkleFonk)
        self.setLayout(self.hBox)
        
    def yeniTestEkleFonk(self):
        dialog = QDialog()
        dialog.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint)
        dialog.setStyleSheet(stil)
        dialog.setFixedSize(400,150)
        isim = QLineEdit()
        isim.setPlaceholderText("Test başlığını giriniz ")
        isim.setStyleSheet("padding:15px;")
        iptal = QPushButton("İptal")
        kaydet = QPushButton("Kaydet")

        hbl = QHBoxLayout()
        hbl.addStretch()
        hbl.addWidget(iptal)
        hbl.addWidget(kaydet)

        vbl = QVBoxLayout()
        vbl.addWidget(isim)
        vbl.addStretch()
        vbl.addLayout(hbl)
        dialog.setLayout(vbl)
        
        iptal.clicked.connect(lambda x: dialog.close())
        kaydet.clicked.connect(lambda x: self.yeniTestDosya(dialog,isim))
        dialog.exec()
    def yeniTestDosya(self,dialog,isim):
        if isim.text() == "" or isim.text().isspace():
            QMessageBox.warning(self,"Hata","İsim belirtmediniz ! \n\nLütfen İsim belirtiniz ",QMessageBox.Yes)
        else:
            veri = isim.text()
            veri = veri.lower()
            veri = self.replaceVeri(veri)
            if os.path.exists("icerik/"+veri+".json"):
                QMessageBox.warning(self,"Hata","Aynı isimde Test mevcut \n\nLütfen Farklı isim deneyiniz  ",QMessageBox.Yes)
            else:
                deger =   {"isim": veri,"sorular": [{"metin": "Burası sizin yeni Testinizin ilk sorusu \nBuraya metin yada sorunuzu ekleyin","soru": "Burası soru ekleyebilirsiniz ","siklar": ["Şık 1","Şık 2","Şık 3","Şık 4"],"dogruindex": "0"}]}

                son = json.dumps(deger,indent=7)
                
                with open("icerik/"+veri+".json","w") as file:
                    file.write(son)
                dialog.close()
                ic = Duzenle(baslik=veri)
                self.parent.cenWid.addWidget(ic)
                self.parent.cenWid.setCurrentWidget(ic)
                QMessageBox.information(self,"Test Başarıyla oluştu","Test Başarıyla oluştu.\nBaşlangıç için bir test sorusu oluşturuldu.\nGüncelleyebilir ve Yeni sorular Ekleyebilirsiniz",QMessageBox.Yes)
            

    def replaceVeri(self,asil):
        sonuc =""
        for i in asil:
            i = i.replace("ı","i")
            i = i.replace("ö","o")
            i = i.replace("ğ","g")
            i = i.replace("ü","u")
            i = i.replace("ş","s")
            i = i.replace("ç","c")
            i = i.replace(".","")
            i = i.replace(",","")
            i = i.replace("_","-")
            i = i.replace(" ","-")
            i = i.replace("'","")
            i = i.replace("\\","-")
            i = i.replace("/","-")
            i = i.replace("\n","")
            sonuc += i
        return sonuc
            


    def baslikEkle(self,isim,uzunluk,tarih):
        testBaslik = QLabel(isim[:25])
        testSoruSayisi = QLabel(str(uzunluk)+" : Soru")
        testTarih = QLabel(str(datetime.strftime(datetime.fromtimestamp(tarih), '%d/%m/%Y  %H:%M')))
        testBaslik.setStyleSheet("background-color:rgba(0,0,0,0.0);font:14px ;font-weight: bold;")
        testBaslik.setMinimumWidth(300)
        testSoruSayisi.setMinimumWidth(100)
        testSoruSayisi.setStyleSheet("background-color:rgba(0,0,0,0.0)")
        testTarih.setStyleSheet("background-color:rgba(0,0,0,0.0);font-size:9px")
        self.delete =QPushButton(QIcon("icon/x-mark.png"),"")
        self.edit = QPushButton(QIcon("icon/edit.png"),"")
        h_box = QHBoxLayout()
        h_box.addWidget(testBaslik)
        h_box.addWidget(testSoruSayisi)
        h_box.addWidget(testTarih)
        
        h_box.addStretch()
        h_box.addWidget(self.delete)
        h_box.addWidget(self.edit)
        


        
        h_box.setContentsMargins(4,4,4,4)
        self.fr = QPushButton()
        self.fr.setLayout(h_box)
        self.fr.setMinimumWidth(300)
        
        self.fr.setObjectName("fr")
        self.fr.setCursor(Qt.PointingHandCursor)
        self.baslik = isim
        self.soruForm.addRow(self.fr)
        self.fr.mousePressEvent = lambda event:self.parent.selected_ac(self,pr="Ana",baslik=isim)
        self.delete.mousePressEvent = lambda event: self.deleteTest(isim,uzunluk,tarih,self.parent)
        self.edit.mousePressEvent = lambda event: self.parent.selected_ac(self,pr="Duzenle",baslik=isim)

    def deleteTest(self,isim,uzunluk,tarih,pre):
        
        gelen = QMessageBox.question(self,"Eminmisiniz",isim+" Testi simlmek istediğinize emin misiniz ?",QMessageBox.No,QMessageBox.Yes)
        
        if gelen == QMessageBox.Yes:
            a = os.remove("icerik/"+isim+".json")
            self.parent.selected_ac(self.parent,pr="Baslangic") 
        
        
        
class Duzenle(QWidget):
    def __init__(self,parent=None,baslik=""):
        super(Duzenle,self).__init__(parent)
        self.baslik = baslik
        self.init__ui()
    def init__ui(self):
  
        
        self.disBox = QHBoxLayout()
        self.anaBox = QVBoxLayout()
        self.foruml = QFormLayout()
        
        
        self.are = QScrollArea()
        self.are.setStyleSheet("")
        
        
        
        with open("icerik/"+self.baslik+".json","r")as file:
            self.json_veri =file.read()
        self.json_veriq = json.loads(self.json_veri)
        self.isim = QLabel(self.json_veriq["isim"])
        self.isim.setStyleSheet("background-color: rgb(15, 79, 90); border-radius: 1px;padding: 5px;color: rgb(202, 199, 199) ;font-weight: bold;font-size: 15px  ;border-radius:2px      ")
       
        self.anaBox.addWidget(self.isim)
        self.f = QFrame()
        self.f.setLayout(self.foruml)
        self.are.setWidget(self.f)
        self.anaBox.addWidget(self.are)
        
        self.are.setWidgetResizable(True)
        self.sonucDeger = {
                "isim":self.json_veriq["isim"],
                "sorular":[]
                }
        soru_sayi = 1
        self.framelist = []
        
        
        self.a = {}
        self.b ={}
        k = 0
        for i in self.json_veriq["sorular"]:
            key = str(k)
            self.sonucDeger["sorular"].append(i)
            value = QPushButton(str(k))
            self.a[key] = value 
            
            
            self.a[key].setObjectName("duzen")
            
           
            
            self.a[key].setMinimumHeight(500)
            
            self.sorubas = QLabel(str(soru_sayi)+" Soru ")
            self.sorubas.setAlignment(Qt.AlignCenter)
            self.sorubas.setStyleSheet("background-color: rgb(7, 7, 7); border-radius: 1px;padding: 5px;color: rgb(202, 199, 199) ;font-weight: bold;font-size: 15px  ;border-radius:2px      ")
            self.soruColumDelete = QLabel(str(soru_sayi))
            self.b[key] =self.soruColumDelete
            self.sirala(i["metin"],i["soru"],i["siklar"],i["dogruindex"],self.sorubas,self.b[key],k)
            self.a[key].clicked.connect(self.getir)
            
            
            
            
            self.soruColumDelete.setMaximumWidth(25)
            self.soruColumDelete.setStyleSheet("background-color:#771010;padding:5px;border-radius: 2px;    ")
            self.soruColumDelete.setPixmap(QPixmap("icon/x-mark.png"))
            self.soruColumDelete.setToolTip("Soruyu Sil")
            
            
            k += 1
            soru_sayi+=1

            self.framelist.append(self.a[key])

        self.yeniSoruEkle = QPushButton("Yeni Soru Ekle")
        self.guncelle = QPushButton("Güncelle")
        self.guncelle.clicked.connect(self.guncelleDef)

        self.yeniSoruEkle.clicked.connect(self.yeniSoruEkran) 
        self.rowInsert()
        
        self.solsikbox = QVBoxLayout()
        self.solsikbox.addWidget(self.yeniSoruEkle)
        self.solsikbox.addWidget(self.guncelle)
        self.solsikbox.addStretch()

        self.disBox.addLayout(self.solsikbox)
        self.disBox.addLayout(self.anaBox)
        self.setLayout(self.disBox)

        
        
    def guncelleDef(self):
        
        
        veri = json.dumps(self.sonucDeger,indent=5)


        with open("icerik/"+self.sonucDeger["isim"]+".json","w") as file:
            sonuc =file.write(veri)
            if sonuc:
                QMessageBox.about(self,"Soru Güncelleme Bilgilendirmesi","Başarı ile Gündellendi !")
        
    def yeniSoruEkran(self):
        dialog = QDialog()
        dialog.setStyleSheet(stil)
        dialog.setMinimumSize(400,500)
        dialog.setWindowTitle("Yeni Soru Ekleme Penceresi")
        metin = QTextEdit()
        metin.setPlaceholderText("Metin içerik")
        soru = QLineEdit()
        soru.setPlaceholderText("Soru içerik")

        dVBox = QVBoxLayout()
        dVBox.addWidget(metin)
        dVBox.addWidget(soru)

        sik1 = QLineEdit()
        sik1.setPlaceholderText("Şık İçerik")
        sik2 = QLineEdit()
        sik2.setPlaceholderText("Şık İçerik")
        sik3 = QLineEdit()
        sik3.setPlaceholderText("Şık İçerik")
        sik4 = QLineEdit()
        sik4.setPlaceholderText("Şık İçerik")

        r1 = QRadioButton()
        r2 = QRadioButton()
        r3 = QRadioButton()
        r4 = QRadioButton()

        iptal = QPushButton("İptal")
        ekle = QPushButton("Ekle")
        
        fl = QFormLayout()
        fl.setWidget(0,QFormLayout.LabelRole,r1)
        fl.setWidget(0,QFormLayout.FieldRole,sik1)
        fl.setWidget(1,QFormLayout.LabelRole,r2)
        fl.setWidget(1,QFormLayout.FieldRole,sik2)
        fl.setWidget(2,QFormLayout.LabelRole,r3)
        fl.setWidget(2,QFormLayout.FieldRole,sik3)
        fl.setWidget(3,QFormLayout.LabelRole,r4)
        fl.setWidget(3,QFormLayout.FieldRole,sik4)
        
        hb = QHBoxLayout()
        hb.addStretch()
        hb.addWidget(iptal)
        hb.addWidget(ekle)
        dVBox.addLayout(fl)
        dVBox.addLayout(hb)

        dialog.setLayout(dVBox)
        
        
        iptal.clicked.connect(lambda x: dialog.close())
        ekle.clicked.connect(lambda x: self.sorularaYenisiniEkle(dialog,metin.toPlainText(),soru.text().replace("\n"," "),[r1,r2,r3,r4],[sik1.text().replace("\n"," "),sik2.text().replace("\n"," "),sik3.text().replace("\n"," "),sik4.text().replace("\n"," ")]))

        dialog.exec()
    def sorularaYenisiniEkle(self,dialog,metin,soru,rsecili,siklar):
        
        if rsecili[0].isChecked():
            self.soru_ek(dialog,metin,soru,"0",siklar)
        elif rsecili[1].isChecked():
            self.soru_ek(dialog,metin,soru,"1",siklar)
        elif rsecili[2].isChecked():
            self.soru_ek(dialog,metin,soru,"2",siklar)
        elif rsecili[3].isChecked():
            self.soru_ek(dialog,metin,soru,"3",siklar)
        else:
            QMessageBox.warning(self,"Bilgilendirme","Herhangi bir doğru şık seçmediniz ! \n Lutfen Bir şık işaretleyip tekrar deneyiniz",QMessageBox.Ok)
        
    def soru_ek(self,dialog,metin,soru,dogruIndex,siklar):
        aSonind = len(self.a)
        
        self.a[str(aSonind)] = QPushButton(str(aSonind))
        self.a[str(aSonind)].setObjectName("duzen")
        self.a[str(aSonind)].setMinimumHeight(500)
        self.a[str(aSonind)].clicked.connect(self.getir)
        self.b[str(aSonind)] = QLabel(str(aSonind+1))
        self.b[str(aSonind)].setToolTip("Soruyu Sil")
        self.b[str(aSonind)].setMaximumWidth(25)
        self.b[str(aSonind)].setPixmap(QPixmap("icon/x-mark.png"))
        self.b[str(aSonind)].setStyleSheet("background-color:#771010;padding:5px;border-radius: 2px;    ")
        sorub =QLabel(str(aSonind+1)+" Soru ")
        sorub.setAlignment(Qt.AlignCenter)
        sorub.setStyleSheet("background-color: rgb(7, 7, 7); border-radius: 1px;padding: 5px;color: rgb(202, 199, 199) ;font-weight: bold;font-size: 15px  ;border-radius:2px      ")
        
        self.sirala(metin,soru,siklar,dogruIndex,sorub,self.b[str(aSonind)],aSonind)
        self.framelist.append(self.a[str(aSonind)] )

        ek={"metin":metin,
            "soru":soru,
            "siklar":[siklar[0],siklar[1],siklar[2],siklar[3]],
            "dogruindex":dogruIndex}
        self.sonucDeger["sorular"].append(ek)
        self.rowInsert()
        dialog.close()
        ff =self.are.verticalScrollBar().size()
       
        self.are.verticalScrollBar().setValue((ff.height()*(len(self.a)*8)))
    def getir(self,q):

        a =self.sender().text()
        soruSayi = int(a)+1
        if self.b[a].underMouse()== True:

            son =QMessageBox.question(self,"Silinsin mi ?",str(soruSayi)+" Nolu soruyu silmek istediğinize eminmisiniz ?",QMessageBox.Yes,QMessageBox.No)

            if son == QMessageBox.Yes :
                self.sender().setParent(None)
                del self.sonucDeger["sorular"][int(a)]
                del self.framelist[int(a)]
                del self.a[a]
                
            
    def rowInsert(self):
        for i in self.framelist:
            self.foruml.addRow(i)


    def sirala(self,metin,soru,siklar,dogruindex,sorubaslik,sil,soru_sayi):
        self.metinD = {}
        metinVal = QTextEdit(metin)
        self.metinD[soru_sayi]=metinVal
        self.metinD[soru_sayi].setObjectName(str(soru_sayi))
        self.metinD[soru_sayi].textChanged.connect(self.metinIcerikDegis)

        self.soruD = {}
        soruVal= QLineEdit(soru)
        
        self.soruD[soru_sayi] = soruVal
        self.soruD[soru_sayi].setObjectName(str(soru_sayi))
        self.soruD[soru_sayi].textChanged.connect(self.soruIcerikDegis)
        self.vBox = QVBoxLayout()
        self.vBox.setAlignment(Qt.AlignRight)
        hb = QHBoxLayout()
        hb.addWidget(sorubaslik)
        hb.addWidget(sil)
        self.vBox.addLayout(hb)
        self.vBox.setObjectName(str(soru_sayi))
        
        self.formlayout = QFormLayout()
        self.vBox.addWidget(self.metinD[soru_sayi])
        self.vBox.addWidget(self.soruD[soru_sayi])
        self.vBox.addLayout(self.formlayout)
        
        inde = 0
        self.siklari = {}
        self.sikIcerik = {}
        for i in siklar:
            key= str(inde)
            value = QRadioButton(str(inde)+sorubaslik.text()[0:-6])
            self.siklari[key] = value
            self.siklari[key].setStyleSheet(" color: transparent;")
            icerikValue = QLineEdit(i)

            self.sikIcerik[key] = icerikValue
            self.sikIcerik[key].setObjectName(str(inde)+sorubaslik.text()[0:-6])

            
            self.sikIcerik[key].setMinimumHeight(23)
           
            self.formlayout.setWidget(int(inde),QFormLayout.LabelRole,self.siklari[key])
            self.formlayout.setWidget(int(inde),QFormLayout.FieldRole,self.sikIcerik[key])
            
            
            if inde == int(dogruindex):
               self.siklari[key].setChecked(True)
            
            
            self.sikIcerik[key].textChanged.connect(self.sikIcerikDegis)
            self.siklari[key].toggled.connect(self.sikSecim)
            inde +=1
        self.a[str(soru_sayi)].setLayout(self.vBox)
    def sikSecim(self):
        sender = self.sender().text()
        
        self.sonucDeger["sorular"][int(sender[1:])-1]["dogruindex"]=sender[0:1]
    def sikIcerikDegis(self):
        sender = self.sender().objectName()
        icerik = self.sender().text().replace("\n"," ")
        soruno = int(sender[1:])-1
        sorusik = int(sender[:1])
        self.sonucDeger["sorular"][soruno]["siklar"][sorusik]=icerik
        

    def metinIcerikDegis(self):
        value = self.sender().toPlainText()
        soruSayi = int(self.sender().objectName())

        self.sonucDeger["sorular"][soruSayi]["metin"] = value


    def soruIcerikDegis(self):
        value = self.sender().text().replace("\n"," ")
        soruSayi = int(self.sender().objectName())
        
        self.sonucDeger["sorular"][soruSayi]["soru"] = value

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    
    window.show()
    sys.exit(app.exec_())
