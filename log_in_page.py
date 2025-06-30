#log_in page
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader

import data as d

class Log_in:

    def __init__(self,app): 
        self.app=app
        uiLoader = QUiLoader()
        self.ui = uiLoader.load('ui/log_in.ui')
        self.ui.bt_complete.clicked.connect(self.getText)

        with open('data/a_and_p.txt', 'r', encoding='utf-8') as f:
            aAndP=f.read().split('\n')
        self.accounts=[aAndP[i] for i in range(len(aAndP)) if i%2==0]
        self.passwords=[aAndP[i] for i in range(len(aAndP)) if i%2==1]

        self.guard=0#密码正确才能进入

    def getText(self):
        account = self.ui.input_account.text()
        password = self.ui.input_password.text()
        if account=='':
            QMessageBox.critical(
            self.ui,
            "提示", 
            "请输入用户名", 
            QMessageBox.Ok 
            )
            return
        if password=='':
            QMessageBox.critical(
            self.ui,
            "提示", 
            "请输入密码", 
            QMessageBox.Ok 
            )
            return
        if account in self.accounts and password==self.passwords[self.accounts.index(account)]:
            self.guard=1
            d.user=d.Person(account,password)
            self.ui.close()
            self.ui.deleteLater()
        elif account not in self.accounts:
            with open('data/a_and_p.txt', 'a', encoding='utf-8') as f:
                text='\n'+account+'\n'+password
                f.write(text)
            QMessageBox.information(
                self.ui,
                '提示',
                '已自动创建账号',
                QMessageBox.Ok
            )
            self.guard=1
            d.user=d.Person(account,password)
            self.ui.close()
            self.ui.deleteLater()
        else:
            QMessageBox.critical(
            self.ui,
            "提示", 
            "用户名或密码错误", 
            QMessageBox.Ok 
            )
            return