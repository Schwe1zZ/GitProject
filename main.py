import sqlite3
import os
import sys
from PIL import Image
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QPixmap
from des import Ui_MainWindow


def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def write_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
        file.close()
    print("Данный из blob сохранены в: ", filename, "\n")

class FoundWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.foundButton.clicked.connect(self.found)
        self.pushButton_2.clicked.connect(self.upload)
        self.pushButton.clicked.connect(self.delete)
        self.pixmap = QPixmap()

    def delete(self):
        con = sqlite3.connect('Project.db')
        cur = con.cursor()
        item_place = self.placeText.toPlainText()
        item_year = self.yearPhoto.value()
        print("Подключен к SQLite")

        cur.execute("DELETE FROM items WHERE Place=? AND Year=?",(item_place, item_year))
        con.commit()
        self.textEdit.setText("Запись успешно удалена")
        cur.close()

    def found(self):
        item_place = self.placeText.toPlainText()
        item_year = self.yearPhoto.value()
        con = sqlite3.connect('C:\\Users\\user\\Desktop\\pythonProject\\Project.db')
        cur = con.cursor()

        res = cur.execute("SELECT * FROM items WHERE Place=? AND Year=?", (item_place, item_year)).fetchall()
        self.textEdit.setText('Фотографии найдены)')


        for row in res:
            name = row[1] + str(row[2])
            photo = row[3]

            photo_path = os.path.join("db_data", name + ".jpg")
            directory = os.path.dirname(photo_path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            write_to_file(photo, photo_path)

            image = Image.open(photo_path)
            image.show()
        con.close()

    def upload(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать Фото', '',
            'Все файлы (*.*);;Изображение (*.png, *.jpg);')[0]

        fname = convert_to_binary_data(fname)

        item_place = self.placeText.toPlainText()
        item_year = self.yearPhoto.value()
        con = sqlite3.connect('C:\\Users\\user\\Desktop\\pythonProject\\Project.db')
        cur = con.cursor()

        cur.execute("INSERT INTO items (Place, Year, Photo) VALUES(?, ?, ?)", (item_place, item_year, fname))
        con.commit()
        self.textEdit.setText('Фотография загружена')
        con.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FoundWin()
    ex.show()
    sys.exit(app.exec())
