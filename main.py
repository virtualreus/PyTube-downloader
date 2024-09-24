import sys
from urllib import request
from pytube import YouTube
import validators
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(880, 700)
        uic.loadUi("design.ui", self)
        self.setWindowTitle("YouTube Downloader")

        self.dir_list = ""
        self.link_to_video = ""

        self.pushButton.clicked.connect(self.download_by_link)
        self.selectFolder.clicked.connect(self.get_directory)
        self.lineEdit.textChanged.connect(self.get_data_by_link)

        self.centralwidget.setStyleSheet("background-color: white;")

        self.lineEdit.setStyleSheet("display: block;"
                                    "width: 100%;"
                                    "padding: 0 20px;"
                                    "margin-bottom: 10px;"
                                    "background: #E9EFF6;"
                                    "line-height: 40px;"
                                    "border-width: 0;"
                                    "border-radius: 20px;"
                                    "font-family: Roboto, sans-serif;"
                                    "font-size: 17px;")

        self.pushButton.setStyleSheet("color: white;"
                                      "letter-spacing: 1px;"
                                      "text-transform: uppercase;"
                                      "border-radius: 10px;"
                                      "background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #49c2ff, stop:1 "
                                      "#6a27d2); "
                                      "padding: 15px 34px;"
                                      "font-family: Verdana, sans-serif;"
                                      "font-size: 17px;")

        self.selectFolder.setStyleSheet("color: white;"
                                        "letter-spacing: 1px;"
                                        "text-transform: uppercase;"
                                        "border-radius: 10px;"
                                        "background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #49c2ff, stop:1 "
                                        "#6a27d2); "
                                        "padding: 2px 4px;"
                                        "font-family: Verdana, sans-serif;"
                                        "font-size: 12px")

        self.label.setStyleSheet("font-size: 25px;"
                                 "font-family: Verdana")

        self.video_name.setStyleSheet("font-size: 22px;"
                                      "font-family: Verdana")

        self.label_2.setStyleSheet("font-size: 15px;"
                                   "font-family: Verdana")

    # Этот метод вызывает окно с уведомлением

    @classmethod
    def show_success_message(cls, desc):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(desc)
        msg.setWindowTitle("Уведомление")
        msg.exec_()

    # Этот метод вызывает окно с ошибкой и ее описанием

    @classmethod
    def show_err_message(cls, desc):
        msg = QMessageBox()
        msg.resize(400, 800)
        msg.setIcon(QMessageBox.Critical)
        msg.setText(desc)
        msg.setWindowTitle("Ошибка")
        msg.exec_()

    # Метод переводит секунды в часы:минуты:секунды

    @classmethod
    def sec_to_hours(cls, seconds):
        a = str(seconds // 3600)
        b = str((seconds % 3600) // 60)
        if len(b) == 1:
            b = "0" + b
        c = str((seconds % 3600) % 60)
        if len(c) == 1:
            c = "0" + c

        if seconds < 3600:
            d = ("{}:{}".format(b, c))
        else:
            d = ("{}:{}:{}".format(a, b, c))
        return d

    # Метод, который проверяет, есть ли такое видео или нет.

    @classmethod
    def check_link_validity(cls, link):
        is_correct = False
        try:
            video_check = YouTube(link)
            video_check_title = video_check.title
            is_correct = True
        except:
            is_correct = False
        return is_correct

    # Метод проверяет содержимое ссылки, и в случае валидной ссылки выводит всю информацию о видео.

    def get_data_by_link(self):
        self.video_name.setWordWrap(True)
        self.link_to_video = self.lineEdit.text()

        if self.check_link_validity(self.link_to_video):
            self.video_params = YouTube(self.link_to_video)
            self.video_name.setText(self.video_params.title)

            self.video_thumbnail_data = request.urlopen(self.video_params.thumbnail_url).read()
            self.video_image_url = QPixmap()

            self.video_image_url.loadFromData(self.video_thumbnail_data)
            self.video_image_url = self.video_image_url.scaled(230, 180)
            self.video_image.setPixmap(self.video_image_url)

            self.video_author.setText(f"Автор: {self.video_params.author}")
            self.video_length.setText(f"Длинна: {self.sec_to_hours(self.video_params.length)}")

        else:
            self.video_thumbnail_data = request.urlopen("https://media.istockphoto.com/vectors/document-error-icon-in"
                                                        "-flat-style-broken-report-vector-illustration-vector"
                                                        "-id1187109567?k=20&m=1187109567&s=170667a&w=0&h"
                                                        "=NkQaHu7aGojenPyoXJPjfiayi_IPvTXRe_3qx4BpW4Y=").read()
            self.video_image_url = QPixmap()

            self.video_image_url.loadFromData(self.video_thumbnail_data)
            self.video_image_url = self.video_image_url.scaled(230, 180)
            self.video_image.setPixmap(self.video_image_url)
            self.video_author.setText("")
            self.video_length.setText("")
            self.video_name.setText("Такого видео не существует, либо оно недоступно.")

    # Метод открывает окно выбора директории

    def get_directory(self):
        self.dir_list = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.label_2.setText(f"Путь для установки: \n{self.dir_list}")

    def download_by_link(self):
        self.link_to_video = self.lineEdit.text()
        if self.link_to_video:
            if validators.url(self.link_to_video) is True:
                try:
                    if self.dir_list:
                        self.video = YouTube(self.link_to_video)
                        if self.video.length >= 600:
                            self.show_success_message(f"Внимание! Видео длится более 10 минут."
                                                      f" Скачивание видео может занять некоторое время.")
                        if self.radioButton.isChecked():
                            if self.radioButton_4.isChecked():
                                self.streams = self.video.streams
                                self.video_480 = self.streams.filter(progressive=True).desc().first()
                                self.video_480.download(self.dir_list)

                            if self.radioButton_3.isChecked():
                                self.streams = self.video.streams
                                self.video_best = self.streams.order_by('resolution').filter(
                                    progressive=True).desc().first()
                                self.video_best.download(self.dir_list)

                        elif self.radioButton_2.isChecked():
                            self.streams = self.video.streams
                            self.audio = self.streams.filter(only_audio=True).desc().first()
                            self.audio.download(self.dir_list)

                        self.show_success_message(f"Файл успешно скачалось в директорию {self.dir_list}!")
                    else:
                        self.show_err_message(f"Укажите папку.")

                except OSError:
                    self.show_err_message("Произошла ошибка.")
                except:
                    self.show_err_message("Такого видео не существует, либо оно удалено или недоступно")

            else:
                self.show_err_message('Ввведена некорректная ссылка.')
        else:
            self.show_err_message("Введите ссылку")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
