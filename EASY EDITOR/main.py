#создай тут фоторедактор Easy Editor!
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import BLUR, CONTOUR, DETAIL, SMOOTH, SHARPEN

app = QApplication([])
win = QWidget()
win.resize(900,800)
win.setWindowTitle('Easy Editor')

lb_image = QLabel("КАРТИНКИ")
btn_dir = QPushButton("Папка")
lw_files = QListWidget()

left = QPushButton("Лево")
Right = QPushButton("Право")
flip = QPushButton("Зеркало")
REZ = QPushButton("Резкость")
bw = QPushButton("Ч/Б")

row = QHBoxLayout() #основная строка
col1 = QVBoxLayout()
col2 = QVBoxLayout()
row_tools = QHBoxLayout() 

col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)

row_tools.addWidget(left)
row_tools.addWidget(Right)
row_tools.addWidget(flip)
row_tools.addWidget(REZ)
row_tools.addWidget(bw)

col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)

win.show()

workdir = ''

def filter(files, extencions):
    result=[]
    for filename in files:
        for ext in extencions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkDir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg', '.png', '.gif', '.bmp', '.jpeg']
    chooseWorkDir()
    filenames = filter(os.listdir(workdir), extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def do_left(self):
            self.image = self.image.transpose(Image.ROTATE_90)
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
           self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
           self.saveImage()
           image_path = os.path.join(workdir, self.save_dir, self.filename)
           self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()


def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProcessor()

lw_files.currentRowChanged.connect(showChosenImage)
left.clicked.connect(workimage.do_left)
Right.clicked.connect(workimage.do_right)
REZ.clicked.connect(workimage.do_sharpen)
bw.clicked.connect(workimage.do_bw)
flip.clicked.connect(workimage.do_flip)


app.exec_()