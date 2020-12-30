import sys
from PyQt5.QtWidgets import *
from googletrans import Translator
import server

class TranslateWindow(QWidget):
    def __init__(self):
        super().__init__()

        # self.s = server.ServerSocket(self)
        self.lbl1 = QLabel('한국어:', self)
        self.lbl2 = QLabel('영어:', self)
        self.le = QLineEdit(self)
        self.te = QTextEdit(self)
        self.trans_btn = QPushButton('번역하기', self)
        self.translator = Translator()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('서버')

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl1)
        vbox.addWidget(self.le)
        vbox.addWidget(self.lbl2)
        vbox.addWidget(self.te)
        vbox.addWidget(self.trans_btn)
        self.setLayout(vbox)

        self.trans_btn.clicked.connect(self.translate_kor)
        self.le.editingFinished.connect(self.translate_kor)

        self.setWindowTitle('Google Translator')
        self.setGeometry(200, 200, 400, 300)
        # self.show()

    def translate_kor(self):
        text_kor = self.le.text()
        # self.translator.translate(text_kor, src='ko', dest='en').le.text()
        # text_en = self.translator.translate(text_kor, src='ko', dest='en').text
        text_en = self.translator.translate(text_kor).text
        self.te.setText(text_en)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TranslateWindow()
    sys.exit(app.exec_())

