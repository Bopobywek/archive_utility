class Archive(QMainWindow, Ui_MainWindow):

    def __init__(self):
        self.pushButton_3.setToolTip("Delete files")
        self.pushButton_3.clicked.connect(self.delete_clicked)


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
