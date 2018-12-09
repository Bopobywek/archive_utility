import shutil
import os
import sys
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QDialogButtonBox
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QDialog
from PyQt5.QtCore import QDir, QFileInfo, QLibraryInfo, Qt, QModelIndex
from archive_d import Ui_MainWindow
from exit_dialog_d import Ui_Dialog
import uuid


# noinspection PyCallByClass
class Archive(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button_first_clicked)
        self.pushButton_2.clicked.connect(self.button_third_clicked)
        self.pushButton_5.clicked.connect(self.button_second_clicked)
        self.pushButton_4.clicked.connect(self.update_recent_arcs)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, 200)
        self.treeView.setAnimated(True)
        self.treeView.setRootIndex(self.model.index(QDir.homePath()))
        self.treeView.clicked.connect(self.arc_once_clicked)
        self.treeView.doubleClicked.connect(self.arc_double_clicked)
        self.file = ""
        self.show_recent_arcs()

    def update_recent_arcs(self):
        self.listWidget.clear()
        self.show_recent_arcs()

    def show_recent_arcs(self):
        with open("arcs.txt", encoding="utf-8") as filein:
            output = filein.readlines()
        for i in output:
            self.listWidget.addItem(i)

    def create_arhcive(self, name_arc, result_type,
                       dir_name_out, dir_name_in):
        try:
            res = shutil.make_archive(name_arc, result_type, root_dir=QDir.rootPath(),
                                      base_dir=dir_name_out[dir_name_out.rfind("/") + 1:])
            if dir_name_in != os.getcwd():
                shutil.move(res[res.rfind("/") + 1:], dir_name_in)
            with open("arcs.txt", mode="a", encoding="utf-8") as info_out:
                info_out.write("{}{}\n".format(dir_name_in, res[res.rfind("/"):]))
            QMessageBox.about(self, "Archive status", "Successfull!")
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.resize(300, 300)
            msg.move(self.x() + 300, self.y() + 350)
            msg.setText("Failed!")
            msg.setWindowTitle("Extarct status")
            msg.setDetailedText("The details are as follows:\n "
                                "{}".format(e))
            msg.setStandardButtons(QMessageBox.Cancel)
            msg.exec_()

    def extract_arhcive(self, name_arc, dir_name_out):
        for name, format_of_arc in dict([(x[0], x[1]) for x in shutil.get_unpack_formats()]).items():
            for el in format_of_arc:
                if el in name_arc:
                    shutil.unpack_archive(name_arc, dir_name_out, name)
                    QMessageBox.about(self, "Extarct status", "Successfull!")

    def button_first_clicked(self):
        if self.file != "" and os.path.isdir(self.file):
            self.user_interface_creating_arc(self.file)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.resize(300, 300)
            msg.move(self.x() + 300, self.y() + 350)
            if self.file == "":
                msg.setText("Укажите папку для архивирования")
                msg.setWindowTitle("Ошибка!")
            elif not os.path.isdir(self.file):
                msg.setText("Укажите ПАПКУ для архивирования")
                msg.setWindowTitle("Ошибка!")
            msg.setStandardButtons(QMessageBox.Cancel)
            msg.exec_()

    def button_third_clicked(self):
        if self.file != "" and os.path.isfile(self.file) and self.check_is_file_arc(self.file):
            self.user_interface_extarct_arc(self.file)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.resize(300, 300)
            msg.move(self.x() + 300, self.y() + 350)
            if self.file == "":
                msg.setText("Укажите архив для распаковки")
                msg.setWindowTitle("Ошибка!")
            elif not os.path.isfile(self.file) or not self.check_is_file_arc(self.file):
                msg.setText("Укажите АРХИВ для распаковки")
                msg.setWindowTitle("Ошибка!")
            msg.setStandardButtons(QMessageBox.Cancel)
            msg.exec_()

    def button_second_clicked(self):
        if self.file != "" and os.path.isfile(self.file) and not self.check_is_file_arc(self.file):
            directory = "{}_{}".format(self.file[self.file.rfind("/") + 1:], uuid.uuid4().hex)
            if not os.path.exists(directory):
                print(self.file[:self.file.rfind("/")])
                new_path = "{}/{}/{}".format(self.file[:self.file.rfind("/")], directory,
                                             self.file[self.file.rfind("/") + 1:])
                os.mkdir("{}/{}".format(self.file[:self.file.rfind("/")], directory))
                os.rename(self.file, new_path)
                self.user_interface_creating_arc("{}/{}".format(self.file[:self.file.rfind("/")], directory))
                os.rename(new_path, self.file)
                os.removedirs("{}/{}".format(self.file[:self.file.rfind("/")], directory))

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.resize(300, 300)
            msg.move(self.x() + 300, self.y() + 350)
            if self.file == "":
                msg.setText("Укажите файл для архивации, который не является архивом")
                msg.setWindowTitle("Ошибка!")
            elif not os.path.isfile(self.file) or self.check_is_file_arc(self.file):
                msg.setText("Укажите файл для архивации, который не является архивом")
                msg.setWindowTitle("Ошибка!")
            msg.setStandardButtons(QMessageBox.Cancel)
            msg.exec_()

    @staticmethod
    def check_is_file_arc(name_arc):
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
            msg.move(self.x() + 300, self.y() + 350)
            msg.setText("Вы хотите создать архив этой папкой?")
            msg.setWindowTitle("Создание архива")
            msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
            msg.buttonClicked.connect(lambda x:
                                      self.user_interface_creating_arc(file) if "Yes" in x.text() else msg.close())
            msg.exec_()
        elif os.path.isfile(file) and self.check_is_file_arc(file[file.rfind("/") + 1:]):
            msg.setIcon(QMessageBox.Question)
            msg.resize(300, 300)
            msg.move(self.x() + 300, self.y() + 350)
            msg.setText("Вы хотите разархивировать этот архив?")
            msg.setWindowTitle("Разархивирование")
            msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
            msg.buttonClicked.connect(lambda x:
                                      self.user_interface_extarct_arc(file) if "Yes" in x.text() else msg.close())
            msg.exec_()

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

    def user_interface_extarct_arc(self, name_arc):
        if name_arc:
            if self.check_is_file_arc(name_arc):
                dir_name_in = QFileDialog.getExistingDirectory(self,
                                                               'Select directory for extarct all files')
                if dir_name_in:
                    self.extract_arhcive(name_arc, dir_name_in)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.resize(300, 300)
                msg.move(self.x() + 300, self.y() + 350)
                msg.setText("Bad file type!")
                msg.setWindowTitle("File Type")
                msg.setDetailedText("The details are as follows:\n BadType fo archive. "
                                    "Указан тип архива, который не поддерживается программой")
                msg.setStandardButtons(QMessageBox.Cancel)
                msg.exec_()

    def delete(self):
        pass


class Dialogs(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.clicked.connect(self.get_button_value)

    def get_button_value(self):
        self.close()
        if "No" in self.buttonBox.sender().text():
            return False
        else:
            return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    arc = Archive()
    arc.show()
    sys.exit(app.exec_())
