import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

  def button1_clicked(self):
    # TODO: insert here parsed text
    self.plain_text_area.clear()
    http_url = self.url_line.text()
    self.plain_text_area.insertPlainText('Parsed {}'.format(http_url))

  def button2_clicked(self):
    self.text_area_rules.clear()
    for i in range(5):
      self.text_area_rules.insertPlainText('Rule {} \n'.format(i + 1))


  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    self.setWindowTitle("Edami projekt")
    vbox = QVBoxLayout()

    url_label_one = QLabel("Wikipedia URL")
    vbox.addWidget(url_label_one)

    self.url_line = QLineEdit()
    vbox.addWidget(self.url_line)

    url_label = QLabel("Parsed text")
    vbox.addWidget(url_label)


    self.plain_text_area = QPlainTextEdit()
    self.plain_text_area.insertPlainText("Here parsed text will be presented")
    vbox.addWidget(self.plain_text_area)

    button1 = QPushButton()
    button1.setText("Parse text")
    button1.clicked.connect(self.button1_clicked)
    vbox.addWidget(button1)

    # Sequential pattern section

    sp_label = QLabel("Find sequential patterns")
    vbox.addWidget(sp_label)

    self.text_area_rules = QPlainTextEdit()
    self.text_area_rules.insertPlainText("Found rules")
    vbox.addWidget(self.text_area_rules)

    button2 = QPushButton()
    button2.setText("Run GSP")
    button2.clicked.connect(self.button2_clicked)
    vbox.addWidget(button2)

  


    # Set the geometry and the layout for the main window
    self.setGeometry(300, 300, 500, 500)
    wid = QWidget(self)
    self.setCentralWidget(wid)
    wid.setLayout(vbox)


def main():
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec_()

if __name__ == '__main__':
  main()


