import sys
import pytesseract#goruntuyu texte cevirmek icin kullanacagımız kutuphane
import cv2 #opencv kütüphanesi
import numpy as np #np ile numpy kütüphanesine kısaltmada bulunduk
import numpy #maskeleme islemleri icindir
import imutils #Goruntuyu uzerinde islem yapmak icin gerekli kütüphane
from PyQt5.QtGui import QImage, QPixmap #Qt'de bulunan resim yukleme fonk. icin import ettik
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout,QHBoxLayout, QPushButton, QFileDialog #
from PyQt5.QtCore import Qt #Qt fonksiyonlarını kullanabilmek icin import ettik


class Example(QWidget):
    def __init__(self): #kodumuzun main de calisacak olan fonksiyonu
        super().__init__() 
        self.image = None #resim icin atadıgımız degiskendir, baslangicta ici bostur
        self.label = QLabel() #label icin atadıgımız degiskendir
        self.pencere() #ekrana cikacak window icin yazdigimiz fonk.

    
    def pencere(self):
        self.label.setText('İşlenecek Araba Resmi') #label icine yazilacak text atandi
        self.label.setAlignment(Qt.AlignCenter) #labelin ortali durmasi saglandi
        self.label.setStyleSheet('border: gray; border-style:solid; border-width: 1px;') #html kodlari ile textin yazi stili belirlendi

        btn_open = QPushButton('Görseli buradan yükleyiniz') #resim yuklemek icin buton atandi ustune islevi yazildi
        btn_open.clicked.connect(self.resimYukle) #bu buton tiklaninca resimYukle fonksiyonunu cagirir
        
        btn_procesar_gray = QPushButton('Griye Çevir') #resmi griye cevirmek icin buton atandi ustune islevi yazildi
        btn_procesar_filtele = QPushButton('Filtre') #resmi filtrelemek icin buton atandi ustune islevi yazildi
        btn_procesar_kenar = QPushButton('Kenarlama')#resmi kenarlandirmak icin buton atandi ustune islevi yazildi
        btn_procesar_mask = QPushButton('Maskeleme')#resmi maskelemek icin buton atandi ustune islevi yazildi
        btn_procesar_plaka = QPushButton('Plaka')  #plakayı goruntulemek icin buton atandi ustune islevi yazildi   
        btn_procesar_gray.clicked.connect(self.resmiGrile)#bu buton tiklaninca resmiGrile fonksiyonunu cagirir
        btn_procesar_filtele.clicked.connect(self.resmiFiltrele)#bu buton tiklaninca resmiFiltrele fonksiyonunu cagirir
        btn_procesar_kenar.clicked.connect(self.resmiKenarla)#bu buton tiklaninca resmiKenarla fonksiyonunu cagirir
        btn_procesar_mask.clicked.connect(self.resmiMask)#bu buton tiklaninca resmiMask fonksiyonunu cagirir
        btn_procesar_plaka.clicked.connect(self.resmiPlaka)#bu buton tiklaninca resmiPlaka fonksiyonunu cagirir     
        

        top_bar = QHBoxLayout() #ust menu belirledik h.layout olarak (yatay)
        top_bar.addWidget(btn_open)#ust menu ıcersine btn_open butonu eklendi
        top_bar.addWidget(btn_procesar_gray)#ust menu ıcersine btn_procesar_gray butonu eklendi
        top_bar.addWidget(btn_procesar_filtele)#ust menu ıcersine btn_procesar_filtele butonu eklendi
        top_bar.addWidget(btn_procesar_kenar)#ust menu ıcersine btn_procesar_kenar butonu eklendi
        top_bar.addWidget(btn_procesar_mask)#ust menu ıcersine btn_procesar_mask butonu eklendi
        top_bar.addWidget(btn_procesar_plaka)#ust menu ıcersine btn_procesar_plaka butonu eklendi
        
        root = QVBoxLayout(self) #virtualBox Layout belirledik
        root.addLayout(top_bar) #icersine ust menu eklendi
        root.addWidget(self.label)#icersine label eklendi

        self.resize(540, 574) #window boyutlari belirlendi
        self.setWindowTitle('Dicle İNCELER && Kader ARSLAN' ) #window basligini belirledik
        

        
    def resimYukle(self): #resim yuklemek icin yazdigimiz fonk.
        filename, _ = QFileDialog.getOpenFileName(None, 'Resim Ara', '.', 'Image Files (*.png *.jpg *.jpeg *.bmp)')#resim belgesi uzantili belgelerde arama yaptik
        if filename:
            with open(filename, "rb") as file: #dosya ikilik sistemde okuma yapiliyorsa
                data = numpy.array(bytearray(file.read())) #görsel okunarak numpy turunde data icersine atanir
                self.image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED) #opencv fonk. ile data okunur ve self.image icine atanır. arttik gorsel sistemdedir.
                self.goruntule()#goruntulenir
                

    def resmiGrile(self): #resmi grilemek için yazdigimiz fonk.  
        if self.image is not None: #eger resim bos degilse devam eder
             gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY) #opencvde hazir bulunan fonk ile RGB deger griye cevrildi
             self.image = gray #griye donen resim degiskene atanir
             self.goruntule() #güncel resim goruntulenir
             
             
    def resmiFiltrele(self):#resmi filtrelemek için yazdigimiz fonk.
        if self.image is not None:#eger resim bos degilse devam eder
             gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)#opencvde hazir bulunan fonk ile RGB deger griye cevrildi
             filtered = cv2.bilateralFilter(gray,6,250,250)#opencvde hazir bulunan fonk filtreleme islemi yapildi ve gurultuden arindirildi 
             self.image = filtered#filtrelenmis resim degiskene atanir
             self.goruntule()#güncel resim goruntulenir
             
    def resmiKenarla(self):#resmi kenarlamak için yazdigimiz fonk.
        if self.image is not None:#eger resim bos degilse devam eder
             gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)#opencvde hazir bulunan fonk ile RGB deger griye cevrildi
             filtered = cv2.bilateralFilter(gray,6,250,250)#opencvde hazir bulunan fonk filtreleme islemi yapildi ve gurultuden arindirildi
             edged = cv2.Canny(filtered,30,200)#opencvde hazir bulunan fonk gurultuden arindirilmis gorselin kenarlarini belirginlestirir 
             self.image = edged#kenarlanmis resim degiskene atanir
             self.goruntule()#güncel resim goruntulenir
             
    def resmiMask(self):#resmi maskelemek için yazdigimiz fonk.
        if self.image is not None:#eger resim bos degilse devam eder
             gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)#opencvde hazir bulunan fonk ile RGB deger griye cevrildi
             filtered = cv2.bilateralFilter(gray,6,250,250)#opencvde hazir bulunan fonk filtreleme islemi yapildi ve gurultuden arindirildi
             edged = cv2.Canny(filtered,30,200)#opencvde hazir bulunan fonk gurultuden arindirilmis gorselin kenarlarini belirginlestirir 
             contours = cv2.findContours(edged,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#opencv'de bulunan fonk ile görseldeki konturlar bulundu
             cnts = imutils.grab_contours(contours) #konturları yakalamaya yariyor
             cnts = sorted(cnts, key=cv2.contourArea,reverse=True)[:10] #pespese gelen aynı renkten olusan dikdortgeni belirledik, alana gore sıralama yaptık
             screen=None #ekran tanımladık,oncelikle ici bostur

             for c in cnts: #bulunan konturlar duzgun hale getirilmeye calisiliyor
                epsilon = 0.018*cv2.arcLength(c,True) #bu yaklasim daha once denenip ınaylanmistir, oradan hazir olarak aldik, epsilon bizim icin bir katsayidir
                approx = cv2.approxPolyDP(c,epsilon,True) #yaklasim hesaplanir, kontura daha da yaklasilir. Girintili cikintili sekillerde hatayi aza indirir
                if len(approx) == 4: #yaklasilmis hal 4 tane ise bu dikdortgendir diyebiliyoruz
                   screen = approx #ici bos olan ekrana artik dortgen atanir
                   break             
             mask = np.zeros(gray.shape,np.uint8) #gri resmin boyutlari kadar deger tutulur, o boyutta siyah ekran gelir. Siyah maske.
             mask = cv2.drawContours(mask,[screen],0,(255,255,255),-1) #plaka bolgesi beyaz olur, kalan bolge mask olarak siyah kalir.
             self.image = mask #maskelenmis ve plakanın beyazlasmis hali degiskene atanir
             self.goruntule()   #görsel görüntülenir 
             
    def resmiPlaka(self):#plakayi gostermek için yazdigimiz fonk
        if self.image is not None:#eger resim bos degilse devam eder
             gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)#opencvde hazir bulunan fonk ile RGB deger griye cevrildi
             filtered = cv2.bilateralFilter(gray,6,250,250)#opencvde hazir bulunan fonk filtreleme islemi yapildi ve gurultuden arindirildi
             edged = cv2.Canny(filtered,30,200)#opencvde hazir bulunan fonk gurultuden arindirilmis gorselin kenarlarini belirginlestirir 
             contours = cv2.findContours(edged,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#opencv'de bulunan fonk ile görseldeki konturlar bulundu
             cnts = imutils.grab_contours(contours)#konturları yakalamaya yariyor
             cnts = sorted(cnts, key=cv2.contourArea,reverse=True)[:10]#pespese gelen aynı renkten olusan dikdortgeni belirledik, alana gore
             screen=None #ekran tanımladık,oncelikle ici bostur

             for c in cnts:#bulunan konturlar duzgun hale getirilmeye calisiliyor
                epsilon = 0.018*cv2.arcLength(c,True)#bu yaklasim daha once denenip ınaylanmistir, oradan hazir olarak aldik, epsilon bizim icin bir katsayidir
                approx = cv2.approxPolyDP(c,epsilon,True)#yaklasim hesaplanir, kontura daha da yaklasilir.Girintili cikintili sekillerde hatayi aza indirir
                if len(approx) == 4:#yaklasilmis hal 4 tane ise bu dikdortgendir diyebiliyoruz
                   screen = approx #ici bos olan ekrana artik dortgen atanir
                   break
    
             mask = np.zeros(gray.shape,np.uint8)  #gri resmin boyutlari kadar deger tutulur, o boyutta siyah ekran gelir. Siyah maske.
             plaka = cv2.drawContours(mask,[screen],0,(255,255,255),-1) #plaka bolgesi beyaz olur, kalan bolge mask olarak siyah kalir.
             plaka = cv2.bitwise_and(self.image,self.image,mask=mask) #belirlenen plaka alanina plakanin asli yerlestirilir.

             self.image = plaka  #maskelenmis ve plakanin belirgin hali degiskene atanir
             self.goruntule()    #görsel görüntülenir   
             
             (x,y) = np.where(mask ==255) #beyaz bolgelerinin koordinatlari x ve y icine atanir
             (topx,topy) = (np.min(x),np.min(y)) #en yuksek x ve y koordinatlarina ulasiriz
             (bottomx, bottomy) = (np.max(x), np.max(y)) #en alcak x ve y koordinatlarina ulasilir
             cropped = gray[topx:bottomx +1, topy:bottomy + 1] #en yuksekten en alcak degerlere kadar olan yerleri aliriz. hem x hem de y icin.
             
             text = pytesseract.image_to_string(cropped, lang="eng") #elde ettigimiz bu bolgedeki karakterleri görselnden algılayarak texte ceviririz.
             print("* * * * * * * * * * * * * * * * *" +"\n")
             print(" ARACIN PLAKASI : ", text )
             print("\n"+"* * * * * * * * * * * * * * * * *" +"\n")
             
    def goruntule(self): #goruntunun goruntulenemsini saglayan fonk.
        size = self.image.shape #goruntunun boyutunu aldik
        step = self.image.size / size[0] #adim sayisini belirledik
        qformat = QImage.Format_Indexed8 #gorselin formati 8bitlik olarak ayarlanir

        if len(size) == 3: #formatlar yani boyut uygun degilse cevrim islemleri gerceklesir
            if size[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(self.image, size[1], size[0], step, qformat) #gorsel QImage icersinde gerekli parametreler girilerek uygun hale getirilir
        img = img.rgbSwapped() #Tüm piksellerin RGB değerlerinin değiştirildiği ve RGB görüntüsünü etkili bir şekilde BGR görüntüsüne dönüştüren fonk.

        self.label.setPixmap(QPixmap.fromImage(img)) #label icersinde gorselin goruntulenmesini saglar
        self.resize(self.label.pixmap().size())#labelin boyutları da gorselin  boyutuna gore sekillenir
        

if __name__ == '__main__': #kodun calistigi ana fonk.
    app = QApplication(sys.argv)
    win = Example() #tum kodların bulundugu class cagırılır
    win.show() #pencere goruntulenir
    sys.exit(app.exec_()) #kod dongusunun bitmesini saglar