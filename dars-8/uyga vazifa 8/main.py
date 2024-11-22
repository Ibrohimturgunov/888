from PyQt5.QtWidgets import *
from Moduls import *



class Loyiha(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(350,150)

        # self.registr=QHBoxLayout()
        # self.regis_label=QLabel("Registratsiya")
        # self.regis_label.setStyleSheet("text-align: center;")
        # self.registr.addWidget(self.regis_label)

        self.login_box=QHBoxLayout()
        self.login=QLabel("Login       ")
        self.login_edit=QLineEdit()
        self.login_box.addWidget(self.login)
        self.login_box.addWidget(self.login_edit)

        self.pass_box=QHBoxLayout()
        self.password=QLabel("Password")
        self.pass_edit=QLineEdit()
        self.pass_box.addWidget(self.password)
        self.pass_box.addWidget(self.pass_edit)

        self.btn_box=QHBoxLayout()
        self.btn=QPushButton("Ok")
        self.btn_box.addWidget(self.btn)

        self.allwidget=QVBoxLayout()
        # self.allwidget.addLayout(self.registr)
        self.allwidget.addLayout(self.login_box)
        self.allwidget.addLayout(self.pass_box)
        self.allwidget.addLayout(self.btn_box)

        self.setLayout(self.allwidget)

        self.btn.clicked.connect(self.baza)

    
    def baza(self):
        global login, message
        login=self.login_edit.text()
        parol=self.pass_edit.text()
        tekshir=data.search_info('telegram', 'watsapp',f'login = "{login}"')

        if tekshir[0][1]==parol:
            message=tekshir[0][3]
            self.hide()
            self.main=Main()
            self.main.show()

        else:
            QMessageBox.warning(None, "Xabarnoma", "Login yoki Parol xato", QMessageBox.Ok)
            # self.login_edit.clear()
            # self.pass_edit.clear()

data=Database()
data.createdatabase('telegram')
data.createtable('telegram', 'watsapp','login varchar(50) primary key, parol varchar(50), inchat text, outchat text')
data.insertinto('telegram','watsapp',[('Admin','12345','',''),('User','54321','','')])


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500,450)

        self.ism_label=QLabel(f'Foydalanuvchi nomi:        {login}')

        self.box=QVBoxLayout()
        self.kiruvchi=QLabel('Kiruvchi xabar:') 
        self.text=QTextEdit()
        self.yuboruvchi=QLabel('Yuboriluvchi xabar:')
        self.text_1=QTextEdit()

        self.btn_box=QHBoxLayout()
        self.back=QPushButton('Back')
        self.btn=QPushButton('Send')
        self.btn_box.addWidget(self.back)
        self.btn_box.addWidget(self.btn)

        self.hbox=QHBoxLayout()
        self.label=QLabel('     Login : ')
        self.ledit=QLineEdit()
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.ledit)

        self.box.addWidget(self.ism_label)
        self.box.addWidget(self.kiruvchi)
        self.box.addWidget(self.text)
        self.box.addWidget(self.yuboruvchi)
        self.box.addWidget(self.text_1)
        self.box.addLayout(self.hbox)
        self.box.addLayout(self.btn_box)
        
        self.setLayout(self.box)
        self.text.setText(message)
        self.btn.clicked.connect(self.tekshir)
        self.back.clicked.connect(self.ortga)


    def tekshir(self):
        lgn=self.ledit.text()
        malumot=self.text_1.toPlainText()
        result = data.search_info('telegram', 'watsapp',f'login = "{lgn}"')
        if result != ():
            data.update_table('telegram',f'update watsapp set inchat="" where login="{login}"')
            data.update_table('telegram',f'update watsapp set inchat="{malumot}" where login="{login}"')

            data.update_table('telegram',f'update watsapp set outchat="" where login="{lgn}"')
            data.update_table('telegram',f'update watsapp set outchat="{malumot}" where login="{lgn}"')
            QMessageBox.warning(None, "Xabarnoma", "message yuborildi", QMessageBox.Ok)
            self.ledit.clear()
        else:
            QMessageBox.warning(None, "Xabarnoma", "Foydalanuvchi topilmadi", QMessageBox.Ok)

            
    def ortga(self):
        self.hide()
        self.loyiha=Loyiha()
        self.loyiha.show()
        
        



if __name__=="__main__":
    app=QApplication([])
    window=Loyiha()
    window.show()
    app.exec_()