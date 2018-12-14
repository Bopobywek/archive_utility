import shutil
import os
import sys
from PyQt5.QtWidgets import QInputDialog, QFileDialog, \
    QMessageBox, QAction, qApp
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QFileSystemModel, QToolTip, QDialog
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QFont
from archive_d import Ui_MainWindow
from archive_content_d import Ui_Dialog
import uuid


# noinspection PyCallByClass, PyBroadException, PyTypeChecker, PyArgumentList, PyArgumentList
class Archive(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        try:
            QToolTip.setFont(QFont('SansSerif', 10))
        except Exception:
            pass
        self.pushButton.clicked.connect(self.button_first_clicked)
        self.pushButton.setToolTip("create <b>archive</b>\nfrom <b>folder</b>")
        self.pushButton_2.clicked.connect(self.button_third_clicked)
        self.pushButton_2.setToolTip("<b>archive</b> unpacking")
        self.pushButton_5.clicked.connect(self.button_second_clicked)
        self.pushButton_5.setToolTip("create <b>archive</b>\nfrom <b>file</b>")
        self.pushButton_3.setToolTip("Delete files and folders")
        self.pushButton_3.clicked.connect(self.delete_clicked)
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
        view_action = QAction("&View archive content", self)
        view_action.setShortcut("Ctrl+Shift+A")
        view_action.setStatusTip("Shows the contents of the archive")
        view_action.triggered.connect(self.view_archive)
        archive_menu = self.menubar.addMenu('&Archive')
        archive_menu.addAction(view_action)
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Shift+E")
        exit_action.setStatusTip("Exit from app")
        exit_action.triggered.connect(qApp.exit)
        archive_menu.addAction(exit_action)

    def update_recent_arcs(self):
        self.listWidget.clear()
        self.show_recent_arcs()

    def show_recent_arcs(self):
        if os.path.exists(os.path.join(os.getcwd(), "arcs.txt")):
            with open("arcs.txt", encoding="utf-8") as filein:
                output = filein.readlines()
        else:
            with open("arcs.txt", mode="w", encoding="utf-8"):
                output = []
        for i in output:
            self.listWidget.addItem(i)

    def button_first_clicked(self):
        """'Add folder' button click handler."""
        try:
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
        except Exception as e:
            self.show_report_msgbox(e)

    def button_second_clicked(self):
        """'Add file' button click handler."""
        try:
            if self.file != "" and os.path.isfile(self.file) and not self.check_is_file_arc(self.file):
                directory = "{}_{}".format(self.file[self.file.rfind("/") + 1:], uuid.uuid4().hex)
                if not os.path.exists(directory):
                    new_path = "{}/{}/{}".format(self.file[:self.file.rfind("/")], directory,
                                                 self.file[self.file.rfind("/") + 1:])
                    os.mkdir("{}/{}".format(self.file[:self.file.rfind("/")], directory))
                    os.rename(self.file, new_path)
                    self.user_interface_creating_arc("{}/{}".format(self.file[:self.file.rfind("/")],
                                                                    directory))
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
        except Exception as e:
            self.show_report_msgbox(e)

    def button_third_clicked(self):
        """'Extarct all' button click handler."""
        try:
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
        except Exception as e:
            self.show_report_msgbox(e)
            
    def delete_clicked(self):
        try:
            file = self.model.filePath(self.treeView.currentIndex())
            if file and os.path.isdir(file):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.resize(300, 300)
                msg.move(self.x() + 300, self.y() + 350)
                msg.setText("Вы уверены, что хотите удалить папку?")
                msg.setWindowTitle("Удаление файла")
                msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
                msg.buttonClicked.connect(lambda x:
                                          shutil.rmtree(file)
                                          if "Yes" in x.text() else msg.close())
                msg.exec_()

            elif file and os.path.isfile(file):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.resize(300, 300)
                msg.move(self.x() + 300, self.y() + 350)
                msg.setText("Вы уверены, что хотите удалить файл?")
                msg.setWindowTitle("Удаление файла")
                msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
                msg.buttonClicked.connect(lambda x:
                                          os.remove(file)
                                          if "Yes" in x.text() else msg.close())
                msg.exec_()

            else:
                self.show_report_msgbox("Chose the folder or file to delete")

        except Exception:
            pass

    @staticmethod
    def check_is_file_arc(name_arc):
        """By file name returns information on whether it is a valid archive or not."""
        for name, format_of_arc in dict([(x[0], x[1]) for x in shutil.get_unpack_formats()]).items():
            for el in format_of_arc:
                if el in name_arc:
                    return True
        else:
            return False

    def arc_once_clicked(self, index):
        """The single click handler for an item in treeView."""
        self.file = self.model.filePath(index)

    def arc_double_clicked(self, index):
        """The double click handler for an item in treeView."""
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
                                      self.user_interface_creating_arc(file)
                                      if "Yes" in x.text() else msg.close())
            msg.exec_()
        elif os.path.isfile(file) and self.check_is_file_arc(file[file.rfind("/") + 1:]):
            msg.setIcon(QMessageBox.Question)
            msg.resize(300, 300)
            msg.move(self.x() + 300, self.y() + 350)
            msg.setText("Вы хотите разархивировать этот архив?")
            msg.setWindowTitle("Разархивирование")
            msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
            msg.buttonClicked.connect(lambda x:
                                      self.user_interface_extarct_arc(file)
                                      if "Yes" in x.text() else msg.close())
            msg.exec_()

    def user_interface_creating_arc(self, dir_name_out):
        """Calls the user interface.
        dir_name_out - argument with the path to the folder to be archived.
        """
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
                        result, message = ArchiveFunctional().create_arhcive(name_arc, result_type,
                                                                             dir_name_out, dir_name_in)
                        if not result:
                            self.show_report_msgbox(message)
                        else:
                            self.show_success_msgbox("Archiving", "Success creating!")

    def user_interface_extarct_arc(self, name_arc):
        """Calls the user interface.
        name_arc - archive name to unpack.
        """
        if name_arc:
            try:
                if self.check_is_file_arc(name_arc):
                    dir_name_in = QFileDialog.getExistingDirectory(self,
                                                                   'Select directory for extarct all files')
                    if dir_name_in:
                        result, message = ArchiveFunctional().extract_arhcive(name_arc, dir_name_in)
                        if not result:
                            self.show_report_msgbox(message)
                        else:
                            self.show_success_msgbox("Extracting", "Success extracting!")
                else:
                    report = QMessageBox()
                    report.setIcon(QMessageBox.Critical)
                    report.resize(300, 300)
                    report.move(self.x() + 300, self.y() + 350)
                    report.setText("Bad file type!")
                    report.setWindowTitle("File Type")
                    report.setDetailedText("The details are as follows:\n BadType fo archive. "
                                           "Указан тип архива, который не поддерживается программой")
                    report.setStandardButtons(QMessageBox.Cancel)
                    report.exec_()
            except Exception as e:
                self.show_report_msgbox(e)

    def view_archive(self):
        try:
            file = self.model.filePath(self.treeView.currentIndex())
            if file and self.check_is_file_arc(file):
                name_of_directory = str(uuid.uuid4().hex)
                os.mkdir(os.path.join(os.getcwd(), name_of_directory))
                result, message = ArchiveFunctional().extract_arhcive(file,
                                                                      os.path.join(os.getcwd(), name_of_directory))
                if not result:
                    self.show_report_msgbox(message)
                else:
                    DialogView(os.path.join(os.getcwd(), name_of_directory)).exec_()
                    shutil.rmtree(os.path.join(os.getcwd(), name_of_directory))
            else:
                self.show_report_msgbox("Archive is not selected, or unsupported archive is selected.")
        except Exception as e:
            self.show_report_msgbox(e)

    def show_report_msgbox(self, message):
        report = QMessageBox()
        report.setIcon(QMessageBox.Critical)
        report.resize(300, 300)
        report.move(self.x() + 300, self.y() + 350)
        report.setText("Error!")
        report.setWindowTitle("Error!")
        report.setDetailedText("The details are as follows:\n {}".format(message))
        report.setStandardButtons(QMessageBox.Cancel)
        report.exec_()

    def show_success_msgbox(self, title, message):
        success = QMessageBox()
        success.setIcon(QMessageBox.Information)
        success.resize(300, 300)
        success.move(self.x() + 300, self.y() + 350)
        success.setText(message)
        success.setWindowTitle(title)
        success.setStandardButtons(QMessageBox.Ok)
        success.exec_()


class ArchiveFunctional(object):

    def __init__(self):
        super().__init__()

    @staticmethod
    def create_arhcive(name_arc, result_type,
                       dir_name_out, dir_name_in):
        try:
            res = shutil.make_archive(os.path.join(dir_name_in, name_arc), format=result_type,
                                      root_dir=dir_name_out)
            if os.path.exists(os.path.join(os.getcwd(), "arcs.txt")):
                with open("arcs.txt", mode="a", encoding="utf-8") as info_out:
                    info_out.write("{}{}\n".format(dir_name_in, res[res.rfind("/"):]))
            else:
                with open("arcs.txt", mode="w", encoding="utf-8") as info_out:
                    info_out.write("{}{}\n".format(dir_name_in, res[res.rfind("/"):]))
        except Exception as e:
            return False, e
        else:
            return True, "ok"

    @staticmethod
    def extract_arhcive(name_arc, dir_name_out):
        try:
            for name, format_of_arc in dict([(x[0], x[1]) for x in shutil.get_unpack_formats()]).items():
                for el in format_of_arc:
                    if el in name_arc:
                        shutil.unpack_archive(name_arc, dir_name_out, name)
        except Exception as e:
            return False, e
        else:
            return True, "ok"


class DialogView(QDialog, Ui_Dialog):

    def __init__(self, path):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)
        self.return_btn.clicked.connect(self.back)
        self.start_path = path
        self.path = path
        self.show_files()
        self.listWidget.doubleClicked.connect(self.show_folder)

    def show_files(self):
        self.listWidget.clear()
        if os.path.isdir(self.path):
            for el in os.listdir(self.path):
                self.listWidget.addItem(el)

    def show_folder(self, item):
        file = self.listWidget.itemFromIndex(item).text()
        if os.path.isdir(os.path.join(self.path, file)):
            self.path = os.path.join(self.path, file)
            self.show_files()

    def back(self):
        if self.path != self.start_path:
            self.path = self.path[:self.path.rfind("/")]
            self.show_files()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    arc = Archive()
    arc.show()
    sys.exit(app.exec_())
