# ################################################
# todo application
# > Enter your Tasks
# > Save your Tasks
# > Delete your Tasks
# > Load your saved Tasks
# -------------------------------By: Anupam Sharma
# ################################################


# Importing modules required in this project
# using --- PyQt6 ---
import sys
import time
import os
from PyQt6.QtCore import QThread, QSize, Qt
from PyQt6.QtWidgets import QApplication,QListWidget,QAbstractItemView, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QIcon


# --------Thread class---------------#
class WorkerThread(QThread):
    def run(self):
        time.sleep(2)
        print('time')


class todo(QWidget):
    def __init__(self):
        super().__init__()   
    
        # adding logo of the window 
        self.setWindowIcon(QIcon('icons/icon.png'))

        # setting the title of the window
        self.setWindowTitle('ToDo List')
        
        # fixed size window
        self.setFixedSize(350, 480)

        # defining layouts
        horizontalLayout = QHBoxLayout()
        horizontalLayoutforbutton = QHBoxLayout()
        verticalLayout = QVBoxLayout()

        # label widget
        self.label = QLabel('To Do''\'s')
        self.label.setObjectName('header')
        self.status = QLabel('Status:')
        self.status.setObjectName('status')
        self.toast = QLabel('...')
        #self.toast.setAlignment(Qt.Alignment.AlignCenter)
        self.toast.setObjectName('toast')
        

        # listwidget
        self.list = QListWidget()
        #self.list.setAlternatingRowColors(True)
        self.list.setAutoScroll(True)
        self.list.setWordWrap(True)
        # setting selection mode property
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.list.itemClicked.connect(self.item)
        
        # Textbox widget
        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText('Take a note!')
        self.textbox.setFocus()

        # Add button widget
        self.btn_addTask = QPushButton('Add Task')
        self.btn_addTask.clicked.connect(self.addTask)
        #self.btn_addTask.setIcon(QIcon('icons/plus.png'))
        self.btn_addTask.setObjectName('addButton')
        

        # Delete button widget
        self.btn_deleteTask =QPushButton()
        self.btn_deleteTask.clicked.connect(self.deleteT)
        self.btn_deleteTask.setIcon(QIcon('icons/trash-regular.png'))
        self.btn_deleteTask.setIconSize(QSize(20, 20))
        self.btn_deleteTask.setToolTip('Delete selected task')
        self.btn_deleteTask.setObjectName('deleteButton')

        # Save button widget
        btn_saveTask = QPushButton()
        btn_saveTask.clicked.connect(self.saveT)
        btn_saveTask.setIcon(QIcon('icons/save-regular.png'))
        btn_saveTask.setIconSize(QSize(20, 20)) 
        btn_saveTask.setToolTip('Save Your List')
        btn_saveTask.setObjectName('saveButton')

        # Load button widget
        btn_loadTask = QPushButton()
        btn_loadTask.clicked.connect(self.loadTask)
        btn_loadTask.setIcon(QIcon('icons/spreadsheet-regular.png'))
        btn_loadTask.setIconSize(QSize(20, 20))
        btn_loadTask.setToolTip('Load previously saved List')
        btn_loadTask.setObjectName('loadButton')
        
        # ClearAll button widget
        self.btn_clearAll = QPushButton('Clear All')
        self.btn_clearAll.clicked.connect(self.clearAllTask)
        self.btn_clearAll.setObjectName('clearAllButton')

        # setting Layouts
        verticalLayout.addWidget(self.label)
        horizontalLayout.addWidget(self.status)
        horizontalLayout.addWidget(self.toast,1)
        horizontalLayout.addWidget(btn_loadTask)
        horizontalLayout.addWidget(btn_saveTask)
        horizontalLayout.addWidget(self.btn_deleteTask)
        verticalLayout.addLayout(horizontalLayout)
        verticalLayout.addWidget(self.list)
        verticalLayout.addWidget(self.textbox)
        horizontalLayoutforbutton.addWidget(self.btn_clearAll)
        horizontalLayoutforbutton.addWidget(self.btn_addTask)
        verticalLayout.addLayout(horizontalLayoutforbutton)
        self.setLayout(verticalLayout)
    

    # Set Toast when item is selected from the list
    def item(self):
        self.toast.setText('Item Selected')
    

    # Event handling method when any key is pressed
    def keyPressEvent(self, event):
        print(event.key())
        self.textbox.setFocus()
        # when user press enter, it automatically add func() to add task in the list
        if event.key() == 16777220 or event.key() == 16777221:
            self.addTask()


    # clear listwidget and linedit  
    def clearAllTask(self):
        self.list.clear()
        self.textbox.clear()
        self.toast.setText('Reset')
        self.ThreadClass()


    # Adding listItem into the listwidget  
    def addTask(self):
        task = self.textbox.text()
        print(len(task))
        if task!="":
            self.list.addItem(task)
            self.textbox.clear()
            self.toast.setText('Item Added')
            self.ThreadClass()
        else:
            self.toast.setText('Add Item first')
            self.toast.setStyleSheet('''color:              #d9534f; ''')
            self.ThreadClass()
   

    # Delete the selected listItem 
    def deleteT(self):
        if(self.list.selectedItems()):
            for i in self.list.selectedItems():
                task_index = self.list.row(i)
                print(self.list.item(task_index).text())
                self.list.takeItem(task_index)
                self.toast.setText('Item deleted.')
            self.ThreadClass()
        else:
            self.toast.setText('Select! item')
            self.toast.setStyleSheet('''color:  #d9534f;''')
            self.ThreadClass()


    # Save the selected listItem
    def saveT(self):
        if(self.list.selectedItems()):
            with open('load.txt','a+') as file:
            # getting the current time
                t = time.asctime( time.localtime(time.time()) )
                print(self.list.count())
                for i in reversed(self.list.selectedItems()):
                    starter = '\n------------ {}'.format(t)
                    task_index = self.list.row(i)
                    strr = self.list.item(task_index).text()
                    print(strr)
                    # concatinate time after the list item
                    strr = strr[0:] + starter
                    # replacing '\n' (new line) with symbol '$$' in the list item
                    strr = strr.replace('\n','$$')
                    print(strr)
                    file.write(strr)
                    file.write('\n')
            self.toast.setText('Task saved')
            self.ThreadClass()
        else:
            self.toast.setText('Select! item')
            self.toast.setStyleSheet('''color:  #d9534f;''')
            self.ThreadClass()
    

    # Load the Saved task from the file named: load.txt
    def loadTask(self):
        try:
            if os.stat('load.txt').st_size != 0:
                self.list.clear()
                # reading the item one by one
                with open('load.txt','r') as file: 
                    for i in file.readlines():
                        # replacing '$$' with '\n' in the list item
                        i = i.replace('$$', '\n')
                        print(i)
                        self.list.addItem(i)
                self.toast.setText('Task Loaded')
                self.ThreadClass()
            else:
                self.toast.setText('Task List empty!')
                self.toast.setStyleSheet('''color: #d9534f;''')
                self.ThreadClass()
        except:
            file = open('load.txt','a+')
            print('file created !')
            self.loadTask() 
       

    # Default Toast Message
    def toast_msg(self):
        self.toast.setText('...')
        self.toast.setStyleSheet('''color: #1a73e8;''')

    
    # Thread function calling
    def ThreadClass(self):
        self.worker = WorkerThread()
        self.worker.start()
        self.worker.finished.connect(self.toast_msg)



#------------------Main---------------------#
app = QApplication(sys.argv)
app.setStyleSheet('''
    *{
        background-color:   #ffffff;
        font-family:        Century Gothic;
    }
    
    #header{
       font-size:           30px; 
       color:               #787c80;
       margin:              0px  5px;
       /*background-color:   #9ac8ef;*/
    }

    #toast, #status{
        font-size:          12px;
        /*background-color:   #e6f1fb;*/
        color:              #1a73e8;
        font-weight:        bold;
        margin-left:         5px;
    }

    QToolTip { 
        color:              #ffffff;
        background-color:   #01579b;
        padding:            5px; 
        border:             0px solid rgba(192, 192, 192, 0.12);
        opacity:            200 
    }
 
    QListWidget{
        /*background-color:   rgba(192, 192, 192, 0.05);*/
        background-color:   rgba(241, 243, 244, 1);
        border:             1px solid rgba(241, 243, 244,1);
        border-radius:      8px;
        padding:            0.8em 0.5em 0.8em 0.5em ;
        outline: 0;
        font-size:           15px;
        margin:2px 5px 8px 5px;
    }
    QListWidget::item {
        background-color:   #ffffff;
        /*background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #cccccc, stop:1 #fcfcfc);*/
        border-radius:      8px;
        margin-top:         0.4em;
        padding: 0.5em;       
    }
    QListWidget::item:selected {
        background-color:  #d2e3fc;
        border :  none;
        color: #0275d8;
    }
 
    #deleteButton{
        border-radius:      5px;
        /*border:             2px solid rgba(241, 243, 244, 1);*/
        /*background-color:   #0275d8;*/
        max-width:          2em;
        color:              #ffffff;
        padding: 0.2em;
        margin-left:0;
        margin-right:5px;
    }
    #deleteButton::hover, #loadButton::hover, #saveButton::hover{
        background-color:   #f0f0f0;
    }
    #deleteButton::pressed, #loadButton::pressed,  #saveButton::pressed{
        background-color:   #bbdefb;
    }

    #loadButton{
        border-radius:      5px;
        /*border:             0.5px solid rgba(192, 192, 192, 0.12);*/
        /*background-color:   #e7effd;*/
        max-width:          2em;
        color:              #ffffff;
        padding: 0.2em;
    }

    #saveButton{
        border-radius:      5px;
        /*background-color:   #0275d8;*/
        max-width:          2em;
        color:              #ffffff;
        margin-left:0;
        padding: 0.2em;
    }

    #addButton, #clearAllButton{
        padding:            1em;
        background-color:   #1a73e8;
        /*background-color:   #BBDEFB;*/
        margin-bottom: 5px;
        margin-top:3px;  
    }
    #clearAllButton{
        margin-left:5px;
    }
    #addButton{
        margin-right:5px;
    }

    QPushButton{
        font-size:          15px;
        border-radius:      8px;
        color:              #ffffff;
        font-weight:        bold;
    }  
    QPushButton::hover, #addButton::hover, #clearAllButton::hover{
        background-color:   #1967d2;
        color:              #ffffff
    }
    QPushButton::pressed, #addButton::pressed, #clearAllButton::pressed{
        background-color:   #185abc;
        color:              #ffffff
    }

    QLineEdit{
        background-color:   rgba(241, 243, 244, 1);
        /*border:             1px solid rgba(192, 192, 192, 0.12);*/
        border:             1px solid rgba(241, 243, 244,1);
        border-radius:      8px;
        max-height:         8em;
        min-height:         2em;
        padding:            0.5em;
        font-size:          16px;
        margin:5px 5px 0px 5px;
    }
    
    QScrollBar{
        border:             none;
        background-color:   rgba(241, 243, 244, 0.8);      
    }
    QScrollBar:vertical {              
        width:              18px;
    }
    QScrollBar:horizontal {              
        height:             10px;     
    }
    QScrollBar::handle:vertical{
        background :         #CFD1D0;
        border-radius:       5px;   
        margin-left: 0.5em; 
    }
    QScrollBar::handle:horizontal{
        background :         #CFD1D0;
        border-radius:       5px;    
    }
    QScrollBar::add-line:horizontal {
        border: none;
        /*background: rgba(241, 243, 244, 0.8);*/
        width: 20px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }
    QScrollBar::add-line:vertical {
        border: none;
        /*background: green;*/
        background: none;
        height: 20px;
        margin-left:5px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:horizontal {
        border: none;
        background: rgba(241, 243, 244, 0.8);
        width: 20px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical {
        border: none;
        background: rgba(241, 243, 244, 0.8);
        height: 20px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    } 
    ''')
window = todo()
window.show()
sys.exit(app.exec())