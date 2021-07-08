import sys
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import numpy as np
import os
from PIL import Image 
from matplotlib import pyplot as plt

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        widget = QtWidgets.QWidget()

        v_box = QtWidgets.QVBoxLayout()
        h1_box = QtWidgets.QHBoxLayout()
        v2_box = QtWidgets.QVBoxLayout()
        h3_box = QtWidgets.QHBoxLayout()
        
        self.onislem_label = QtWidgets.QLabel("Ön İşleme",self)
        self.onislem_label.move(35,60)
        self.onislem_combo = QtWidgets.QComboBox(self)
        self.onislem_combo.move(10,90)
        self.onislem_combo.addItem("Seçiniz",self)
        self.onislem_combo.addItem("Gri Seviye",self)
        self.onislem_combo.addItem("ROI",self)
        self.onislem_combo.addItem("Histogram",self)
        
        self.durum_label = QtWidgets.QLabel("----------",self)
        self.onislem_label.move(480,480)
        

        
        self.filtreleme_label = QtWidgets.QLabel("Filtreleme",self)
        self.filtreleme_label.move(125,60)
        self.filtreleme_combo = QtWidgets.QComboBox(self)
        self.filtreleme_combo.move(125,90)
        self.filtreleme_combo.addItem("Seçiniz",self)
        self.filtreleme_combo.addItem("Bulanıklaştırma",self)
        self.filtreleme_combo.addItem("Keskinleştirme",self)
        self.filtreleme_combo.addItem("Kenar Bulma",self)      
        
        self.morfolojik_label = QtWidgets.QLabel("Morfolojik İşlem",self)
        self.morfolojik_label.move(240,60)
        self.morfolojik_combo = QtWidgets.QComboBox(self)
        self.morfolojik_combo.move(240,90)
        self.morfolojik_combo.addItem("Seçiniz",self)
        self.morfolojik_combo.addItem("Genişletme",self)
        self.morfolojik_combo.addItem("Erozyon",self)

        self.segmentasyon_label = QtWidgets.QLabel("Segmentasyon",self)
        self.segmentasyon_label.move(360,60)
        self.segmentasyon_combo = QtWidgets.QComboBox(self)
        self.segmentasyon_combo.move(360,90)
        self.segmentasyon_combo.addItem("Seçiniz",self)
        self.segmentasyon_combo.addItem("4'lü Komşu ile Nesne",self)
        self.segmentasyon_combo.addItem("Gri Seviyede Nesne",self)
        self.segmentasyon_combo.addItem("Renkli Görselde Nesne",self)
        
        self.kaydet_label = QtWidgets.QLabel("Dosya Uzantısı",self)
        self.kaydet_label.move(480,480)
        self.kaydet_combo = QtWidgets.QComboBox(self)
        self.kaydet_combo.move(480,510)
        self.kaydet_combo.addItem("Seçiniz",self)
        self.kaydet_combo.addItem(".jpg",self)
        self.kaydet_combo.addItem(".bmp",self)
        self.kaydet_combo.addItem(".png",self) 
        


        
        self.gorselYukleButton = QtWidgets.QPushButton("Resim Seçin")
        h1_box.addWidget(self.gorselYukleButton)
        h1_box.addWidget(self.onislem_label)
        h1_box.addWidget(self.onislem_combo)
        h1_box.addWidget(self.filtreleme_label)
        h1_box.addWidget(self.filtreleme_combo)
        h1_box.addWidget(self.morfolojik_label)
        h1_box.addWidget(self.morfolojik_combo)
        h1_box.addWidget(self.segmentasyon_label)
        h1_box.addWidget(self.segmentasyon_combo)
        h1_box.addWidget(self.kaydet_label)
        h1_box.addWidget(self.kaydet_combo)  
        h1_box.addWidget(self.durum_label)
        h1_box.addStretch()

        self.label = QtWidgets.QLabel()
        v2_box.addWidget(self.label)
        self.label.setAlignment(Qt.AlignCenter)

        self.imageDownloadButton = QtWidgets.QPushButton("KAYDET")
        h3_box.addStretch()
        h3_box.addWidget(self.imageDownloadButton)

        v_box.addLayout(h1_box)
        v_box.addStretch()
        v_box.addLayout(v2_box)
        v_box.addStretch()
        v_box.addLayout(h3_box)

        self.gorselYukleButton.clicked.connect(self.gorselYukle)
        self.onislem_combo.currentTextChanged.connect(self.onIsleme)
        self.filtreleme_combo.currentTextChanged.connect(self.filtreleme)
        self.morfolojik_combo.currentTextChanged.connect(self.morfolojik)
        self.kaydet_combo.currentTextChanged.connect(self.kaydet)
        
        widget.setLayout(v_box)
        self.setCentralWidget(widget)
        self.setGeometry(100,100,300,100)
        self.setWindowTitle('151220103 || Sayısal Görüntü İşleme Dersi Paket Program')
        self.show()
        
        self.flag=0
        self.redPix = 0
        self.greenPix = 0
        self.bluePix = 0
        
    def gorselYukle(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Dosya seçiniz', 
            'd:\\',"Image files (*.jpg *.gif *.png)")
        self.image = fname[0]
        self.img_deneme = fname[0]
        if len(fname[0]) > 0:
            self.label.setPixmap(QPixmap(fname[0]))


    def onIsleme(self):
        if self.onislem_combo.currentText() == "Gri Seviye":
            img =cv2.imread(self.img_deneme)
            h,w = img.shape[:2]
            img2 = np.zeros((h,w,1), np.uint8)
            
            for i in range(h):
                for j in range(w):
                    img2[i,j]= int(((img[i,j][0]*0.2989)+(img[i,j][1]*0.5870)+(img[i,j][2]*0.1140)))
                    
            cv2.imwrite('cikti.png',img2)
            self.image=img2
            self.label.setPixmap(QPixmap('cikti.png'))
            self.flag=1
            self.durum_label.setText("Gri Seviye")
        
        if self.onislem_combo.currentText() == "ROI":
            img = cv2.imread('cikti.png')
            roi = cv2.selectROI("Alan secip ESC'ye basiniz.",img,False)
            imCrop = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
            cv2.imshow("Goruntu", imCrop)
            cv2.imwrite("cikti.png",imCrop)
            img_kirpik = cv2.imread("cikti.png")
            self.image=img_kirpik
            self.label.setPixmap(QPixmap('cikti.png'))
            self.flag=2
            self.durum_label.setText("ROI")
       
        
        if self.onislem_combo.currentText() == "Histogram":
            if self.flag == 0:
                img2 = cv2.imread(self.img_deneme)
            if self.flag == 1:
                img2 = cv2.imread('cikti.png')
            if self.flag == 2:
                img2 = cv2.imread('cikti.png')    
            h,w = img2.shape[:2] # img is a grayscale image
            y = np.zeros((256), np.uint8)
            for i in range(0,h):
               for j in range(0,w):
                  y[img2[i,j]] += 1
            x = np.arange(0,256)
            plt.bar(x,y,align="center")
            plt.savefig('histogram.png')
            img2 = cv2.imread("histogram.png")
            self.image=img2
            self.label.setPixmap(QPixmap('histogram.png'))
            self.durum_label.setText("Histogram")
    
    
    def filtreleme(self):
        def average(img,x,y,blurfactor):
            rtotal = gtotal = btotal = 0
            for x2 in range(x-blurfactor,x+blurfactor+1):
                for y2 in range(y-blurfactor,y+blurfactor+1):
                    r,g,b = img.getpixel((x2,y2))
                    rtotal = rtotal + r
                    gtotal = gtotal + g
                    btotal = btotal + b
            rtotal = rtotal // ((blurfactor * 2 +1)**2)
            gtotal = gtotal // ((blurfactor * 2 +1)**2)
            btotal = btotal // ((blurfactor * 2 +1)**2)
            return (rtotal, gtotal, btotal)
    
        if self.filtreleme_combo.currentText() == "Bulanıklaştırma":
            img = Image.open("cikti.png")
            w = img.size[0]
            h = img.size[1]
            img2 = Image.new("RGB",(w,h),(0,0,0))
            
            for x in range(5,w-5):
                for y in range(5,h-5):
                    r,g,b = img.getpixel((x,y))
                    r2,g2,b2 = average(img,x,y,5)
                    img2.putpixel((x,y),(r2,g2,b2))
                    
            img2 = img2.save("cikti.png")
            img2 = cv2.imread("cikti.png")
            self.image = img2
            self.label.setPixmap(QPixmap('cikti.png'))
            self.durum_label.setText("Bulanıklaştırma")
            
    def morfolojik(self):
        if self.morfolojik_combo.currentText() == "Genişletme":
            img1= cv2.imread('cikti.png',0)
            m,n= img1.shape
            k=5
            SE= np.ones((k,k), dtype=np.uint8)
            constant= (k-1)//2
            imgErode= np.zeros((m,n), dtype=np.uint8)
            for i in range(constant, m-constant):
              for j in range(constant,n-constant):
                temp= img1[i-constant:i+constant+1, j-constant:j+constant+1]
                product= temp*SE
                imgErode[i,j]= np.min(product)
            cv2.imwrite("cikti.png", imgErode)
            img2 = cv2.imread("cikti.png")
            self.image = img2
            self.label.setPixmap(QPixmap('cikti.png'))
            self.durum_label.setText("Genişletme")
        
        if self.morfolojik_combo.currentText() == "Erozyon":
            img2= cv2.imread('cikti.png',0)
            p,q= img2.shape
            imgDilate= np.zeros((p,q), dtype=np.uint8)
            SED= np.array([[0,1,0], [1,1,1],[0,1,0]])
            constant1=1
            for i in range(constant1, p-constant1):
              for j in range(constant1,q-constant1):
                temp= img2[i-constant1:i+constant1+1, j-constant1:j+constant1+1]
                product= temp*SED
                imgDilate[i,j]= np.max(product)
            cv2.imwrite("cikti.png", imgDilate)
            img2 = cv2.imread("cikti.png")
            self.image = img2
            self.label.setPixmap(QPixmap('cikti.png'))
            self.durum_label.setText("Erozyon")
            
    def kaydet(self):
        if self.kaydet_combo.currentText() == ".jpg":
            img = cv2.imread('cikti.png',0)
            dosyaAdi = "sonuc.jpg"
            cv2.imwrite(dosyaAdi,img)
        
        if self.kaydet_combo.currentText() == ".bmp":
            img = cv2.imread('cikti.png',0)
            dosyaAdi = "sonuc.bmp"
            cv2.imwrite(dosyaAdi,img)
        
        if self.kaydet_combo.currentText() == ".png":
            img = cv2.imread('cikti.png',0)
            dosyaAdi = "sonuc.png"
            cv2.imwrite(dosyaAdi,img)  
        os.remove("cikti.png")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()