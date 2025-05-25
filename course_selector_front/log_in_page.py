#log_in page
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader

class Log_in:

    def __init__(self,app): 
        self.app=app
        uiLoader = QUiLoader()
        self.ui = uiLoader.load('ui/log_in.ui')
        self.ui.bt_complete.clicked.connect(self.getText)
        self.ui.bt_createAccount.clicked.connect(self.createAccount)

    def getText(self):
        account = self.ui.input_account.text()
        password = self.ui.input_password.text()
        if account=='':
            print("请输入账号")
            return
        if password=='':
            print("请输入密码")
            return
        # data.user.account=account
        # data.user.password=password
        self.ui.close()
        self.ui.deleteLater()


    def createAccount(self):
        #print("create account")
        pass