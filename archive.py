import shutil
import os
import sys
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel
from PyQt5.QtCore import QDir, QFileInfo, QLibraryInfo
from archive_d import Ui_MainWindow


# noinspection PyCallByClass
class Archive(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button_first_clicked)
        self.pushButton_2.clicked.connect(self.button_second_clicked)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.treeView.setModel(self.model)
        self.treeView.setAnimated(True)
        self.treeView.setRootIndex(self.model.index(QDir.homePath()))
        self.treeView.clicked.connect(self.arc_once_clicked)
        self.treeView.doubleClicked.connect(self.arc_double_clicked)
        self.file = ""

    def button_first_clicked(self):
        if self.file != "" and os.path.isdir(self.file):
            self.user_interface_creating_arc(self.file)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.resize(300, 300)
            msg.move(self.x() + 350, self.y() + 350)
            if self.file == "":
                msg.setText("Укажите папку для архивирования")
                msg.setWindowTitle("Ошибка!")
            elif not os.path.isdir(self.file):
                msg.setText("Укажите ПАПКУ для архивирования")
                msg.setWindowTitle("Ошибка!")
            msg.setStandardButtons(QMessageBox.Cancel)
            msg.exec_()

    def button_second_clicked(self):
        if self.file != "" and os.path.isfile(self.file) and self.check_is_file_arc(self.file):
            self.user_interface_extarct_arc(self.file)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.resize(300, 300)
            msg.move(self.x() + 350, self.y() + 350)
            if self.file == "":
                msg.setText("Укажите архив для распаковки")
                msg.setWindowTitle("Ошибка!")
            elif not os.path.isfile(self.file) or not self.check_is_file_arc(self.file):
                msg.setText("Укажите АРХИВ для распаковки")
                msg.setWindowTitle("Ошибка!")
            msg.setStandardButtons(QMessageBox.Cancel)
            msg.exec_()

    def check_is_file_arc(self, name_arc):
        for name, format_of_arc in dict([(x[0], x[1]) for x in shutil.get_unpack_formats()]).items():
            for el in format_of_arc:
                if el in name_arc:
                    return True
        else:
            return False

    def arc_once_clicked(self, index):
        self.file = self.model.filePath(index)

    def arc_double_clicked(self, index):
        msg = QMessageBox()
        file = self.model.filePath(index)
        if os.path.isdir(file):
            msg.setIcon(QMessageBox.Question)
            msg.resize(300, 300)
            msg.move(self.x() + 350, self.y() + 350)
            msg.setText("Вы хотите создать архив этой папкой?")
            msg.setWindowTitle("Создание архива")
            msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
            msg.buttonClicked.connect(lambda x:
                                      self.user_interface_creating_arc(file) if "Yes" in x.text() else msg.close())
            msg.exec_()
        elif os.path.isfile(file) and self.check_is_file_arc(file[file.rfind("/") + 1:]):
            msg.setIcon(QMessageBox.Question)
            msg.resize(300, 300)
            msg.move(self.x() + 350, self.y() + 350)
            msg.setText("Вы хотите разархивировать этот архив?")
            msg.setWindowTitle("Разархивирование")
            msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
            msg.buttonClicked.connect(lambda x:
                                      self.user_interface_extarct_arc(file) if "Yes" in x.text() else msg.close())
            msg.exec_()

    def create_arhcive(self, name_arc, result_type,
                       dir_name_out, dir_name_in):
        res = shutil.make_archive(name_arc, result_type, dir_name_out, dir_name_in)
        if dir_name_in != os.getcwd():
            shutil.move(res[res.rfind("/") + 1:], dir_name_in)
            with open("arcs.config", mode="w") as info_out:
                info_out.write("{}{}\n".format(dir_name_in, res[res.rfind("/"):]))
            QMessageBox.about(self, "Archive status", "Successfull!")

    def user_interface_creating_arc(self, dir_name_out):
        if dir_name_out:
            result_type, state_type = QInputDialog.getItem(
                self,
                "Выбор типа",
                "Выберите тип архива:",
                tuple(x[0] for x in shutil.get_archive_formats()),
                1,
                True)
            if state_type:
                name_arc, state_arc = QInputDialog.getText(self, "Укажите название",
                                                           "Укажите название архива\t(без указания типа)")
                if state_arc:
                    dir_name_in = QFileDialog.getExistingDirectory(self, 'Select directory')
                    if dir_name_in:
                        self.create_arhcive(name_arc, result_type, dir_name_out, dir_name_in)

    def extract_arhcive(self, name_arc, dir_name_out):
        for name, format_of_arc in dict([(x[0], x[1]) for x in shutil.get_unpack_formats()]).items():
            for el in format_of_arc:
                if el in name_arc:
                    shutil.unpack_archive(name_arc, dir_name_out, name)
                    QMessageBox.about(self, "Extarct status", "Successfull!")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.resize(300, 300)
            msg.move(self.x() + 350, self.y() + 350)
            msg.setText("Failed!")
            msg.setWindowTitle("Extarct status")
            msg.setDetailedText("The details are as follows:\n BadType fo archive. "
                                "Не поддерживается данный формат архива")
            msg.setStandardButtons(QMessageBox.Cancel)
            msg.exec_()

    def user_interface_extarct_arc(self, name_arc):
        if name_arc:
            for name, format_of_arc in dict([(x[0], x[1]) for x in shutil.get_unpack_formats()]).items():
                for el in format_of_arc:
                    if el in name_arc:
                            dir_name_in = QFileDialog.getExistingDirectory(self,
                                                                           'Select directory for extarct all files')
                            if dir_name_in:
                                self.extract_arhcive(name_arc, dir_name_in)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.resize(300, 300)
                msg.move(self.x() + 350, self.y() + 350)
                msg.setText("Bad file type!")
                msg.setWindowTitle("File Type")
                msg.setDetailedText("The details are as follows:\n BadType fo archive. "
                                    "Указан тип архива, который не поддерживается программой")
                msg.setStandardButtons(QMessageBox.Cancel)
                msg.exec_()

    def delete(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    arc = Archive()
    arc.show()
    sys.exit(app.exec_())
