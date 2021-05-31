import sys
from PyQt5.QtWidgets import QApplication, QBoxLayout, QLabel, QMainWindow, QRadioButton, QVBoxLayout, QHBoxLayout, QWidget, QPlainTextEdit, QPushButton, QLineEdit, QErrorMessage
from PyQt5.QtCore import Qt
from generate_data import get_text_wiki, text_to_code, create_seq_list, create_new_candidates, calculate_support, GSP, translate_to_words, create_graph, SPADE
from datetime import datetime




# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

  def button1_clicked(self):
    # TODO: insert here parsed text
    self.plain_text_area.clear()
    http_url = self.url_line.text()
    try:
      text = get_text_wiki(http_url)
      self.plain_text_area.insertPlainText(format(text))
    except:
      error_dialog = QErrorMessage()
      error_dialog.showMessage('Wrong URL')
      self.exec_()



  def button2_clicked(self):
    self.text_area_rules.clear()
    try:
      max_len = int(self.max_len_text.text())
      min_sup = int(self.min_sup_text.text())
    except:
      error_dialog = QErrorMessage()
      error_dialog.showMessage('Maximal length and minimal support must be integers greater than 0')
      self.exec_()   
  
    if max_len > 0 and min_sup > 0:
      text = self.plain_text_area.toPlainText()

      start = datetime.now()
      if self.radioSPADE.isChecked():
        page_code, word_list, number_list = text_to_code(text)
        candidates = GSP(page_code, number_list, min_sup, max_len)
        candidates_translated = translate_to_words(candidates, word_list)
      elif self.radioGSP.isChecked():
        candidates_translated = SPADE(text, min_sup, max_len)

      time = int((datetime.now() - start).total_seconds() * 1000)      
      separator=' '


      self.text_area_rules.insertPlainText('Algorithm excecution time: ' + str(time) + ' ms' + '\n')
      for cand in candidates_translated:
        cand_string = separator.join(cand)
        self.text_area_rules.insertPlainText(cand_string+'\n')

      create_graph(candidates_translated)

   

    else:
      error_dialog = QErrorMessage()
      error_dialog.showMessage('Maximal length and minimal support must be integers greater than 0')
      self.exec_()         




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


    labels_horiz = QHBoxLayout()
    min_sup_label = QLabel("Minimal support")
    labels_horiz.addWidget(min_sup_label)
    max_len_label = QLabel("Maximal sequence length")
    labels_horiz.addWidget(max_len_label)
    vbox.addLayout(labels_horiz)


    text_horiz = QHBoxLayout()
    self.min_sup_text = QLineEdit()
    text_horiz.addWidget(self.min_sup_text)
    self.max_len_text = QLineEdit()
    text_horiz.addWidget(self.max_len_text)
    vbox.addLayout(text_horiz)

    radio_horiz = QHBoxLayout()
    self.radioGSP = QRadioButton("GSP")
    self.radioGSP.setChecked(True)
    radio_horiz.addWidget(self.radioGSP)
    self.radioSPADE = QRadioButton("SPADE")
    self.radioSPADE.setChecked(False)
    radio_horiz.addWidget(self.radioSPADE)
    vbox.addLayout(radio_horiz)

    button2 = QPushButton()
    button2.setText("Run Algorithm")
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


