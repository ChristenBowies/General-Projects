from tkinter import *
import datetime
import shelve
from time import time, sleep, localtime

class MainMenu(Frame):
    def __init__(self, parent, db):
        Frame.__init__(self, parent)
        self.root = parent
        self.parent = Frame(self.root)
        self.parent.grid(row=1,column=0)
        self.db = db
        self.root.title('Time Tool')
        self.headerText = StringVar()
        self.info = {'welcome':'Welcome to Time Tool',
                     'login': 'Please input username and password',
                     'create': 'Please input user informations',
                     'logged': 'You are logged in as: '}
        self.userOK = False
        self.initSquares()        

    def initSquares(self):
        self.headerText.set(self.info['welcome'])
        self.header = Label(self.root, fg = 'Blue',textvariable = self.headerText)
        self.b01 = Button(self.parent, text = 'Login', height=9, width=15,
                    padx=3, pady=3, activeforeground='Red', command=self.runLogin)
        self.b11 = Button(self.parent, text = 'Logout', height=9, width=15,
                    padx=3, pady=3, activeforeground='Red', command=self.runLogout)
        self.b02 = Button(self.parent, text='Create\nUser', height=9, width=15,
                    padx=3, pady=3, activeforeground='Red', command=self.runCreateUser)        
        self.b03 = Button(self.parent, text='Time\nLogger', height=9, width=15,
                    padx=3, pady=3, activeforeground='Red', command=self.runTimer)
        self.b04 = Button(self.parent, text='Manual\nTime Entry', height=9, width=15,
                    padx=3, pady=3, activeforeground='Red', command=self.runManual)        

        self.b05 = Button(self.parent, text='Reports', height=9, width=15,
                    padx=3, pady=3, activeforeground='Red')
        self.b06 = Button(self.parent, text='Settings', height=9, width=15,
                    padx=3, pady=3, activeforeground='Red')
        self.b07 = Button(self.parent, text='Exit', height=9, width=32,
                    padx=3, pady=3, activeforeground='Red', command=self.runExit)


        self.header.grid(row=0,pady=3,sticky='N')
        self.b01.grid(row=0,column=0) # Login Button (0,0)
        self.b02.grid(row=0,column=1) # Create User Button (0,1)        
        self.b03.grid(row=1,column=0)# Time Logger Button (1,0)
        self.b04.grid(row=1,column=1)# Manual Entry Button (1,1)
        self.b05.grid(row=2,column=0) # Reports Button (2,0)
        self.b06.grid(row=2,column=1) # Settings Button (2,1)
        self.b07.grid(row=3,column=0, columnspan = 2) # Exit Button (2,2)        

        self._buttonStatus('disabled')
        if self.db.is_DB_Empty():
            self.b01.config(state = 'disabled')

    def runExit(self):
        self.root.destroy()

    def runTimer(self):
        self.b11.config(state = 'disabled')
        self.b03.config(state = 'disabled')
        self.b04.config(state = 'disabled')
        self.b07.config(state = 'disabled')
        w = Frame(self.root)
        w.grid(row = 1, column = 2, sticky = 'N')        
        ti = TimerUI(w, self.db)
        ti.bind('<Destroy>', self._onTimerWindowExit)

    def _onTimerWindowExit(self, event):
        self.b11.config(state = 'normal')
        self.b03.config(state = 'normal')
        self.b04.config(state = 'normal')
        self.b07.config(state = 'normal')

    def runManual(self):
        self.b11.config(state = 'disabled')
        self.b03.config(state = 'disabled')
        self.b04.config(state = 'disabled')
        self.b07.config(state = 'disabled')        
        w = Frame(self.root)
        w.grid(row = 1, column = 2, sticky = 'N') 
        mt = ManualTimerUI(w, self.db)
        mt.bind('<Destroy>', self._onManualTimerUIExit)

    def _onManualTimerUIExit(self, event):
        self.b11.config(state = 'normal')
        self.b03.config(state = 'normal')
        self.b04.config(state = 'normal')
        self.b07.config(state = 'normal')

    def _buttonStatus(self, stateButton):
        self.b03.config(state = stateButton)
        self.b04.config(state = stateButton)
        self.b05.config(state = stateButton)
        self.b06.config(state = stateButton)

    def runLogout(self):
        self.db.saveUserData()
        self.headerText.set(self.info['welcome'])
        self._buttonStatus('disabled')
        self.b02.config(state = 'normal')        
        self.b11.grid_remove()
        self.b01.grid(row=0,column=0)
        self.db.desactivateActualUserID()

    def runLogin(self):
        self.headerText.set(self.info['login'])
        self.b01.config(state = 'disabled')
        self.b02.config(state = 'disabled')
        self.b07.config(state = 'disabled')
        w = Frame(self.root)
        w.grid(row = 1, column = 2, sticky = 'N')
        l = LoginUI(w, self.db)
        l.bind('<Destroy>', self._onLoginWindowExit)
    
    def _onLoginWindowExit(self, event):
        self.b01.config(state = 'normal')
        self.b07.config(state = 'normal')
        
        if self.db.getActualUserID():
            self.b01.grid_remove()
            self.b11.grid(row=0,column=0)
            self._buttonStatus('normal')
            self.headerText.set(self.info['logged'] + self.db.getUserRealName())
            self.db.tmpUserData = self.db.getUserData() # gets user data from data base and assign
                                                        # them to self.db.tmpUserData
        else:
            self.headerText.set(self.info['welcome'])
            self._buttonStatus('disabled')
            self.b02.config(state = 'normal')        

    def runCreateUser(self):
        self.b01.config(state = 'disabled')
        self.b02.config(state = 'disabled')
        self.b07.config(state = 'disabled')
        
        self.headerText.set(self.info['create'])
        w = Frame(self.root)
        w.grid(row = 1, column = 2, sticky = 'N')
        cu = CreateUserUI(w, self.db)
        cu.bind('<Destroy>', self._onCreateUserWindowExit)

    def _onCreateUserWindowExit(self, event):
        if self.db.is_DB_Empty():
            self.b01.config(state = 'disabled')
        else:
            self.b01.config(state = 'normal')
            self.b07.config(state = 'normal')
        if self.db.getActualUserID():
            self.b01.grid_remove()
            self.b11.grid(row=0,column=0)
            self._buttonStatus('normal')
            self.headerText.set(self.info['logged'] + self.db.getUserRealName())
            self.db.tmpUserData = self.db.getUserData() # gets user data from data base and assign
                                                        # them to self.db.tmpUserData                                
        else:
            self.headerText.set(self.info['welcome'])
            self._buttonStatus('disabled')
            self.b02.config(state = 'normal')        



class NewEntry(Frame):
    def __init__(self, parent, db, sel):
        Frame.__init__(self, parent)
        self.db = db
        self.parent = parent
        self.parent.grid(sticky = 'SW')
        self.selectType = sel
        self.inputVar = StringVar()
        self.setSelection()
        self.makeWidget()

    def setSelection(self):
        if self.selectType == 'CAT':
            self.inputText = 'Input new category'
        elif self.selectType == 'PROJECT':
            self.inputText = 'Input new project'

    def makeWidget(self):
        inputFrame = LabelFrame(self.parent, labelanchor = 'nw', text = self.inputText)
        inputFrame.grid()
        self.entry = Entry(inputFrame, textvariable = self.inputVar)
        self.b1 = Button(inputFrame, text = 'Save', height=3, width=4,
                         command = self.save,   activeforeground='Red')
        self.b2 = Button(inputFrame, text = 'Exit', height=3, width=4,
                         command = self.runExit,   activeforeground='Red')

        self.entry.grid(row = 0, column = 0, columnspan = 2,padx = 2, pady = 1)
        self.b1.grid(row = 1, column = 0, padx = 2, pady = 1, sticky = 'NW')
        self.b2.grid(row = 1, column = 1, padx = 2, pady = 1, sticky = 'NE')

    def save(self):
        self.b1.config(state = 'disabled')
        self.b2.config(state = 'normal')
        self.db.tmpUserData[self.selectType].append(self.inputVar.get())

    def runExit(self):
        self.parent.destroy()        
        

class Selection(Frame):
    def __init__(self, parent, db, sel):
        Frame.__init__(self, parent)
        self.db = db
        self.selected  = None        
        self.selectType = sel
        self.parent = parent
        self.parent.grid()
        self.selectionList = StringVar()
        self.setSelection()
        self.makeWidget()

    def setSelection(self):
        if self.selectType == 'CAT':
            self.catFrameText = 'Category'
            s = self.parseSelection(self.db.tmpUserData[self.selectType])
        elif self.selectType == 'PROJECT':
            self.catFrameText = 'Project'
            s = self.parseSelection(self.db.tmpUserData[self.selectType])
        self.selectionList.set(s)       


    def makeWidget(self):
        catFrame = LabelFrame(self.parent, labelanchor = 'nw', text = self.catFrameText)
        catFrame.grid()
        
        self.b1 = Button(catFrame, text = 'Select', height=3, width=4,
                         command = self.select, activeforeground='Red')
        self.b2 = Button(catFrame, text = 'New', height=3, width=4,
                         command = self.new,   activeforeground='Red')
        self.b3 = Button(catFrame, text = 'Save', height=3, width=4,
                         command = self.save,   activeforeground='Red')
        self.b4 = Button(catFrame, text = 'Exit', height=3, width=4,
                         command = self.runExit,   activeforeground='Red')

        self.lb1 = Listbox(catFrame, width = 14, height = 7, listvariable = self.selectionList)
        self.lb1.grid(row = 0, column = 2, rowspan = 2, sticky = 'E', padx = 3, pady = 3)
        
        self.b1.grid(row = 0, column = 0, padx = 2, pady = 1, sticky = 'NW')
        self.b2.grid(row = 0, column = 1, padx = 2, pady = 1, sticky = 'NW')
        self.b3.grid(row = 1, column = 0, padx = 2, pady = 1, sticky = 'NW')
        self.b4.grid(row = 1, column = 1, padx = 2, pady = 1, sticky = 'NW')
        
        self.b3.config(state = 'disabled')

    def parseSelection(self, sel):
        ''''Converts list to string: ["a", "b", "c"] ---> "a b c"'''
        return (' ').join(sel)

    def select(self):
        self.b1.config(state = 'disabled')
        self.b2.config(state = 'disabled')        
        try:
            sel = self.lb1.curselection()[0]
            self.selected = self.lb1.get(sel)
        except:
            self.b1.config(state = 'normal')
            self.b2.config(state = 'normal')

    def new(self):
        self.b1.config(state = 'disabled')
        self.b2.config(state = 'disabled')
        self.b3.config(state = 'disabled')
        self.b4.config(state = 'disabled')        
        w = Frame(self.parent)
        w.grid(row = 3, column = 0, sticky = 'N')        
        ne = NewEntry(w, self.db, self.selectType)
        ne.bind('<Destroy>', self._onNewEntryWindowExit)

    def _onNewEntryWindowExit(self, event):
        self.b1.config(state = 'normal')
        self.b2.config(state = 'normal')
        self.b3.config(state = 'disabled')
        self.b4.config(state = 'normal')
        self.setSelection()


    def save(self):
        self.b1.config(state = 'disabled')
        self.b2.config(state = 'disabled')
        self.b3.config(state = 'disabled')

    def runExit(self):
        self.db.tmpLog[self.selectType] = self.selected
        self.parent.destroy()
   
class TimerUI(Frame):
    def __init__(self, parent, db):
        Frame.__init__(self, parent)
        self.db = db
        self.parent = parent


        self._n = 0 # counter of start/stop numbers
        self.timeStamp = 0
        self._start = 0
        self._run = 0
        self._recording = False
        self._saveOK = False # if user accepted log fo saving
        self.out = StringVar()
        self.db.createNewLog(self.db.getActualUserID())

        self.initUI()

    def initUI(self):
        self.timeTxt()
        clockFrame = LabelFrame(self.parent, labelanchor = 'nw', text = 'Time Logger')
        clockFrame.grid(row = 0, column = 0, padx = 3)
        
        clockLabel = Label(clockFrame, textvariable = self.out, font = ('Helvetica', 24)) # , width = 32, height = 8
        clockLabel.grid(row=0, columnspan = 3)

        self.b1 = Button(clockFrame, text = 'Start', height=3, width=4,
                         command = self.record, activeforeground='Red')
        self.b2 = Button(clockFrame, text = 'Stop', height=3, width=4,
                         command = self.stop,   activeforeground='Red')
        self.b3 = Button(clockFrame, text = 'Save', height=3, width=4,
                         command = self.save,   activeforeground='Red')
        self.b4 = Button(clockFrame, text = 'Exit', height=3, width=4,
                         command = self.runExit,   activeforeground='Red')
        self.b5 = Button(clockFrame, text = 'Reset', height=3, width=4,
                         command = self.reset,  activeforeground='Red')

        self.b5.grid(row = 0, column = 3, padx = 2, pady = 2)
        self.b1.grid(row = 1, column = 0, padx = 2, pady = 2)
        self.b2.grid(row = 1, column = 1, padx = 2, pady = 2)
        self.b3.grid(row = 1, column = 2, padx = 2, pady = 2)
        self.b4.grid(row = 1, column = 3, padx = 2, pady = 2)        

        selectionFrame = LabelFrame(self.parent, labelanchor = 'nw', text = 'Selection')
        selectionFrame.grid(row = 1, column = 0, padx = 3, pady = 3, sticky = 'NW')
        
        self.b6 = Button(selectionFrame, anchor = NW, text = 'Category\nNONE', height=3, width=12,
                         command = lambda: self.selection('CAT'),  activeforeground='Red')        
        self.b7 = Button(selectionFrame, anchor = NW, text = 'Project\nNONE', height=3, width=12,
                         command = lambda: self.selection('PROJECT'),  activeforeground='Red')
        self.b6.grid(row = 0, column = 0, padx = 2, pady = 2)
        self.b7.grid(row = 1, column = 0, padx = 2, pady = 2)

        entryFrame = LabelFrame(selectionFrame, labelanchor = 'nw', text = 'Memo')
        entryFrame.grid(row = 0, column = 1, rowspan = 2, padx = 3, pady = 3, sticky = 'NW')
        self.memoEntry = Text(entryFrame, width = 16, height=6)
        self.memoEntry.grid()

        self.b2.config(state = 'disabled')
        self.b3.config(state = 'disabled')
        self.b5.config(state = 'disabled')

    def selection(self, sel):
        self.b6.config(state = 'disabled')
        self.b7.config(state = 'disabled')        
        w = Frame(self.parent)
        w.grid(row = 2, column = 0, sticky = 'N')        
        se = Selection(w, self.db, sel)
        se.bind('<Destroy>', self._onSelectionWindowExit)

    def _onSelectionWindowExit(self, event):
        self.b6.config(state = 'normal')
        self.b7.config(state = 'normal')
        self.b6.config(text = 'Category\n' + (self.db.tmpLog['CAT'] or 'NONE'))
        self.b7.config(text = 'Project\n' + (self.db.tmpLog['PROJECT'] or 'NONE'))

    def project(self):
        pass
        
    def save(self):
        self._saveOK = True
        self._n = 0 # start/stop counter set to zero
        self.b1.config(state = 'disabled')
        self.b2.config(state = 'disabled')
        self.b3.config(state = 'disabled')
        self.b5.config(state = 'disabled')
        self.b6.config(state = 'disabled')
        self.b7.config(state = 'disabled')        
        if self._saveOK:
            self.db.tmpLog['TYPE'] = 'ti' # timer imput
            self.db.tmpLog['TS'] = self.timeStamp
            self.db.tmpLog['DURA'] = int(self._run)
            self.db.tmpLog['INFO'] = self.memoEntry.get(1.0, END)

    def runExit(self):
        self.db.saveNewLogRecord()
        self.parent.destroy()
        self._recording = False
        self._saveOK = False
        
    def timeTxt(self):
        self.out.set(datetime.timedelta(seconds=int(self._run)))

    def record(self):
        self.b1.config(state = 'disabled')
        self.b2.config(state = 'normal')
        self.b3.config(state = 'disabled')        
        if not self._recording:
            self._n += 1
            self._start = time() - self._run
            self._update()
            self._recording = True
            self.b4.config(state = 'disabled')            

    def _update(self):
        self._run = time() - self._start
        self.timeTxt()
        self._timer = self.after(1000, self._update)
        
    def stop(self):
        self.b1.config(state = 'normal')        
        self.b2.config(state = 'disabled')        
        self.b3.config(state = 'normal')
        self.b5.config(state = 'normal')
        if self._n == 1:
            self.timeStamp = self._start # here TimeStamp of first recording is stored
            print(self.timeStamp)
        if self._recording:
            self.after_cancel(self._timer)            
            self._run = time() - self._start    
            self.timeTxt()
            self._recording = False
            self.b4.config(state = 'normal')

    def reset(self):
        self.b2.config(state = 'disabled')
        self.b3.config(state = 'disabled')
        self.b5.config(state = 'disabled')
        self._n = 0
        self._start = time()         
        self._run = 0.0    
        self.timeTxt()

#--------------------------------------
class ManualTimerUI(Frame):
    def __init__(self, parent, db):
        Frame.__init__(self, parent)
        self.db = db
        self.parent = parent

        self.timeStamp = 0
        self._start = 0
        self.duration = 0
        self._recording = False
        self._saveOK = False # if user accepted log for saving
        self.out = StringVar()
        self.db.createNewLog(self.db.getActualUserID())

        self.initUI()

    def initUI(self):
        timeFrame = LabelFrame(self.parent, labelanchor = 'nw', text = 'Time Input')
        timeFrame.grid(row = 0, column = 0, padx = 3)
        
        self.l1 = Label(timeFrame)
        self.e1 = Entry(timeFrame)
        self.e2 = Entry(timeFrame)
        self.e1.grid(sticky = 'NE')
        self.e2.grid(sticky = 'NE')
        
        
        self.b3 = Button(timeFrame, text = 'Save', height=3, width=4,
                         command = self.save,   activeforeground='Red')
        self.b4 = Button(timeFrame, text = 'Exit', height=3, width=4,
                         command = self.runExit,   activeforeground='Red')
        self.b3.grid(sticky = 'SW')
        self.b4.grid(sticky = 'SE')


        
        selectionFrame = LabelFrame(self.parent, labelanchor = 'nw', text = 'Selection')
        selectionFrame.grid(row = 1, column = 0, padx = 3, pady = 3, sticky = 'NW')
        
        self.b6 = Button(selectionFrame, anchor = NW, text = 'Category\nNONE', height=3, width=12,
                         command = lambda: self.selection('CAT'),  activeforeground='Red')        
        self.b7 = Button(selectionFrame, anchor = NW, text = 'Project\nNONE', height=3, width=12,
                         command = lambda: self.selection('PROJECT'),  activeforeground='Red')
        self.b6.grid(row = 0, column = 0, padx = 2, pady = 2)
        self.b7.grid(row = 1, column = 0, padx = 2, pady = 2)

        entryFrame = LabelFrame(selectionFrame, labelanchor = 'nw', text = 'Memo')
        entryFrame.grid(row = 0, column = 1, rowspan = 2, padx = 3, pady = 3, sticky = 'NW')
        self.memoEntry = Text(entryFrame, width = 16, height=6)
        self.memoEntry.grid()


    def runExit(self):
#        self.db.saveNewLogRecord()
        self.parent.destroy()
        self._saveOK = False

    def selection(self, sel):
        self.b6.config(state = 'disabled')
        self.b7.config(state = 'disabled')        
        w = Frame(self.parent)
        w.grid(row = 2, column = 0, sticky = 'N')        
        se = Selection(w, self.db, sel)
        se.bind('<Destroy>', self._onSelectionWindowExit)

    def _onSelectionWindowExit(self, event):
        self.b6.config(state = 'normal')
        self.b7.config(state = 'normal')
        self.b6.config(text = 'Category\n' + (self.db.tmpLog['CAT'] or 'NONE'))
        self.b7.config(text = 'Project\n' + (self.db.tmpLog['PROJECT'] or 'NONE'))
        
    def save(self):
        self._saveOK = True
        self.b3.config(state = 'disabled')
        self.b6.config(state = 'disabled')
        self.b7.config(state = 'disabled') 
#        if self._saveOK:
#            self.db.tmpLog['TYPE'] = 'mi' # manual imput
#            self.db.tmpLog['TS'] = self.timeStamp
#            self.db.tmpLog['DURA'] = int(self.duration)
#            self.db.tmpLog['INFO'] = self.memoEntry.get(1.0, END)

#--------------------------------------




class CreateUserUI(Frame):
    def __init__(self, parent, db):
        Frame.__init__(self, parent)
        self.db = db
        self.parent = parent
        
        self.username = StringVar()
        self.password = StringVar()
        self.password2 = StringVar()
        self.realName = StringVar()
        self.realSurname = StringVar()
        
        self.initUI()

    def initUI(self):
        self.lf1 = LabelFrame(self.parent, text = 'username', relief = GROOVE, labelanchor = 'nw',
                        width = 100,height = 50, padx = 3, pady = 3)        
        self.e1 = Entry(self.lf1, textvariable = self.username)
        self.lf2 = LabelFrame(self.parent, text = 'password', relief = GROOVE, labelanchor = 'nw',
                        width = 100,height = 50, padx = 3, pady = 3)        
        self.e2 = Entry(self.lf2, textvariable = self.password, show = '*')

        self.lf3 = LabelFrame(self.parent, text = 'confirm password', relief = GROOVE,
                              labelanchor = 'nw', width = 100,height = 50, padx = 3, pady = 3)        
        self.e3 = Entry(self.lf3, textvariable = self.password2, show = '*')

        self.lf4 = LabelFrame(self.parent, text = 'Your name', relief = GROOVE, labelanchor = 'nw',
                        width = 100,height = 50, padx = 3, pady = 3)        
        self.e4 = Entry(self.lf4, textvariable = self.realName)
        
        self.lf5 = LabelFrame(self.parent, text = 'Your surname', relief = GROOVE, labelanchor = 'nw',
                        width = 100,height = 50, padx = 3, pady = 3)        
        self.e5 = Entry(self.lf5, textvariable = self.realSurname)        
        
        self.b1 = Button(self.parent, text = 'OK', activeforeground='Red', height = 3, width = 4,
                         command = self.runOK)
        self.b2 = Button(self.parent, text = 'Cancel', activeforeground='Red', height = 3, width = 4,
                         command = self.runCancel)
    

        self.lf1.pack(side = TOP, fill = X, pady = 3, padx = 3)        
        self.e1.pack(side = TOP, fill = X, pady = 3, padx = 3)
        self.lf2.pack(side = TOP, fill = X, pady = 3, padx = 3)         
        self.e2.pack(side = TOP, fill = X, pady = 3)
        self.lf3.pack(side = TOP, fill = X, pady = 3, padx = 3)        
        self.e3.pack(side = TOP, fill = X, pady = 3, padx = 3)        
        self.lf4.pack(side = TOP, fill = X, pady = 3, padx = 3)        
        self.e4.pack(side = TOP, fill = X, pady = 3, padx = 3)  
        self.lf5.pack(side = TOP, fill = X, pady = 3, padx = 3)        
        self.e5.pack(side = TOP, fill = X, pady = 3, padx = 3)  
        self.b1.pack(side = RIGHT, pady = 3, padx = 3)
        self.b2.pack(side = LEFT, pady = 3, padx = 3)

    def runCancel(self):
        self.parent.destroy()
        pass

    def runOK(self):
        if self.validateNewUserLogin():
            self.db.createNewUser(self.username.get(), self.password.get(),
                                  self.realName.get(), self.realSurname.get()
                                  )
            self.parent.destroy()
        else:
            messagebox.showerror('User creation error', 'some errors - correct')

    def validateNewUserLogin(self):
        u = self.username.get()
        p1 = self.password.get()
        p2 = self.password2.get()
        con1 = len(u) > 3
        con2 = len(p1) > 5
        con3 = p1 == p2
        if self.db.is_DB_Empty():
            con4 = True
        else:    
            con4 = not self.db.isUserInDB(u)
        con5 = len(self.realName.get()) != 0
        con6 = len(self.realSurname.get()) != 0
        conditions = con1 and con2 and con3 and con4 and con5 and con6
        return conditions
    
class DataBase:
    def __init__(self):
        self.user_ID = None
        self.fileDB = 'testDB-3.db'
        self.tmpLog = None
        self.tmpUserData = None

    def createNewUser(self, loginname, password, name, surname):
        '''Creates new user and sets 'so far known' data in to data base.'''
        self.makeNewDataBase() # if DataBase is empty will it initialize
        USER_ID = self.makeNewUserID() 
        self.prepareUserForWritingData(USER_ID)# prepare structure for new user entry
        db = shelve.open(self.fileDB, writeback = True)
        db['LOGINS'][USER_ID] = (loginname, password)        
        db['USERS'][USER_ID]['USER_ID'] = USER_ID
        db['USERS'][USER_ID]['NAME'] = name
        db['USERS'][USER_ID]['SURNAME'] = surname
        db.close()
        self.user_ID = USER_ID # makes newly created user active (logged in)        

    def createNewLog(self, USER_ID):
        '''Creates and stores new log entry.'''
        LOG_ID = self.makeNewLogID()
        self.tmpLog = {'LOG_ID': LOG_ID,
               'USER_ID': USER_ID,
               'TYPE': '',
               'PROJECT': '',                               
               'CAT': '',
               'TS': '',                               
               'DURA': '',
               'INFO': ''
               }
    
    def makeNewDataBase(self):
        ''' Creates new Data Base with basic structure '''
        if self.is_DB_Empty(): # if DataBase is empty will it initialize
            db = shelve.open(self.fileDB)
            db['LOGINS'] = {}
            db['USERS'] = {}
            db['LOGS'] = {}
            db['BLANK_USR'] = {'USER_ID': '',
                               'NAME': '',
                               'SURNAME': '',
                               'LOGS': [],
                               'PROJECT': [],
                               'CAT': []
                               }
            db['BLANK_LOG'] = {'LOG_ID': '',
                               'USER_ID': '',
                               'TYPE': '',
                               'PROJECT': '',                               
                               'CAT': '',
                               'TS': 0.0,                               
                               'DURA': 0,
                               'INFO': ''
                               }
            db['BLANK_LOGIN'] = {'USER_ID': ('','')}
            db.close()

    def getCategoryList(self):
        '''Retrives category list from USERS'''
        db = shelve.open(self.fileDB)
        cat = db['USERS'][self.user_ID]['CAT']
        db.close()
        return cat

    def getProjectList(self):
        '''Retrives project list from USERS'''
        db = shelve.open(self.fileDB)
        pro = db['USERS'][self.user_ID]['PROJECTS']
        db.close()
        return pro

    def prepareUserForWritingData(self, USER_ID):
        '''puts empty record from BLANK_USR to db['USERS'][USER_ID].'''
        db = shelve.open(self.fileDB, writeback = True)
        db['USERS'][USER_ID] = db['BLANK_USR'] 
        db.close()

    def prepareLogForWritingData(self, LOG_ID):
        '''puts empty record from BLANK_USR to db['USERS'][USER_ID].'''
        db = shelve.open(self.fileDB, writeback = True)
        db['LOGS'][LOG_ID] = db['BLANK_LOG'] 
        db.close()
        
    def checkAuthentication(self, name, password):
        ''' cheks if any entry in LOGINS subDataBase matches username and password.
            If YES: sets self.user_ID; if NO self.user_ID remains None'''
        db = shelve.open(self.fileDB)
        id_tmp = None
        for i in db['LOGINS']:
            if db['LOGINS'][i] == (name, password):
                self.user_ID = i
        db.close()

    def is_DB_Empty(self):
        ''' Checks if DataBase has any registered users'''
        db = shelve.open(self.fileDB)
        try:
            db['LOGINS']
            db.close()
            return False
        except KeyError:
            db.close()
            return True
        
    def getActualUserID(self):
        ''' Returns actual user_ID'''
        return self.user_ID

    def desactivateActualUserID(self):
        ''' Sets self.user_ID to None'''
        self.user_ID = None

    def makeNewUserID(self):
        ''' makes new USER_ID. The Data Base structure must be not empty.'''
        db = shelve.open(self.fileDB)
        if len(db['LOGINS']) == 0:
            newUserID = 'USR1000'
        else:
            newUserID = 'USR' + str(int(max(db['LOGINS'].keys())[3:]) + 1)
        db.close()
        return newUserID

    def makeNewLogID(self):
        ''' makes new LOG_ID. The Data Base structure must be not empty.'''
        db = shelve.open(self.fileDB)
        if len(db['LOGS']) == 0:
            newLogID = 'ID1000'
        else:
            newLogID = 'ID' + str(int(max(db['LOGS'].keys())[2:]) + 1)
        db.close()
        return newLogID    
    
    def isUserInDB(self, login):
        ''' cheks if login name is in LOGINS '''
        result = False
        db = shelve.open(self.fileDB)
        for i in db['LOGINS']:
            if db['LOGINS'][i][0] == login:
                result = True
        db.close()
        return result
 
    def saveNewLogRecord(self):
        db = shelve.open(self.fileDB, writeback=True)
        db['LOGS'][self.tmpLog['LOG_ID']] = self.tmpLog
        db.close()
        self.tmpLog = None

    def saveUserData(self):
        db = shelve.open(self.fileDB, writeback=True)
        db['USERS'][self.user_ID] = self.tmpUserData
        db.close()
        self.tmpUserData = None

    def getUserData(self):
        ''' Returns user data from USERS'''
        db = shelve.open(self.fileDB)
        userData = db['USERS'][self.user_ID]
        db.close()
        return userData

    def getUserRealName(self):
        ''' Returns user NAME and SURENAME from USERS'''
        db = shelve.open(self.fileDB)
        name = db['USERS'][self.user_ID]['NAME']
        surname = db['USERS'][self.user_ID]['SURNAME']
        return name + ' ' + surname
    
class LoginUI(Frame):
    def __init__(self, parent, db):
        Frame.__init__(self, parent)
        self.db = db
        self.parent = parent
        self.username = StringVar()
        self.password = StringVar()
        self.password2 = StringVar()        
        self.initUI()

    def initUI(self):
        self.lf1 = LabelFrame(self.parent, text = 'username', relief = GROOVE, labelanchor = 'nw',
                        width = 100,height = 50, padx = 3, pady = 3)        
        self.e1 = Entry(self.lf1, textvariable = self.username)
        self.lf2 = LabelFrame(self.parent, text = 'password', relief = GROOVE, labelanchor = 'nw',
                        width = 100,height = 50, padx = 3, pady = 3)        
        self.e2 = Entry(self.lf2, textvariable = self.password, show = '*')
        
        self.b1 = Button(self.parent, text = 'OK', activeforeground='Red', height=3, width=4,
                         command = self.runOK)
        self.b2 = Button(self.parent, text = 'Cancel', activeforeground='Red', height = 3, width = 4,
                         command = self.runCancel)

        self.lf1.pack(side = TOP, fill = X, pady = 3, padx = 3)        
        self.e1.pack(side = TOP, fill = X, pady = 3, padx = 3)
        self.lf2.pack(side = TOP, fill = X, pady = 3, padx = 3)         
        self.e2.pack(side = TOP, fill = X, pady = 3)
        self.b1.pack(side = RIGHT, pady = 3, padx = 3)
        self.b2.pack(side = LEFT, pady = 3, padx = 3)

    def runCancel(self):
        self.parent.destroy()
        pass

    def runOK(self):
        self.db.checkAuthentication(self.username.get(), self.password.get())
        if self.db.getActualUserID():
            self.parent.destroy()
        else:
            messagebox.showerror('Login incorrect', 'some errors - correct')
            self.username.set('')
            self.password.set('')

class UserWindow(Frame):
    def __init__(self, parent, db):
        Frame.__init__(self, parent)
        self.frame = parent
        self.db = db
        self.frame.title('Manual Time Entry')
        self.user = self.db.getActualUserID()
        self.userData = self.db.getUserData(self.user)
        print(self.userData)

        '''Initialize empty variables for .get() capture'''
        self.Duration = StringVar() 
        self.Time = StringVar()         
        self.date = StringVar()
        self.Note = StringVar()
        self.type = 'ml'

        '''Initialize UI'''
        self.initUI()           

    def initUI(self):
        self.initLabels()               
        self.initButtons()
        self.pop_menu()

    def initLabels(self):   
        self.L1 = LabelFrame(self.frame, text='Project',relief = GROOVE, labelanchor='nw',
                            width=300, height=40)
        
        self.L5 = LabelFrame(self.frame, text='Category', relief = GROOVE, labelanchor = 'nw',
                             width = 300, height = 75)
        self.L5.pack(side=TOP, fill = X)
        
        self.L2 = LabelFrame(self.frame, text='Date(Year/Month/Day)', relief = GROOVE, labelanchor = 'nw',
                             width = 300, height = 40)

        self.e2 = Entry(self.L2, textvariable = self.date)
        self.e2.pack(side = TOP, fill = X)
        
        self.L3 = LabelFrame(self.frame, text='Time(H:M)', relief = GROOVE, labelanchor = 'nw',
                            width = 300, height = 40)

        self.e3 = Entry(self.L3, textvariable = self.Time)
        self.e3.pack(side = TOP, fill = X)
        
        self.L4 = LabelFrame(self.frame, text='Duration', relief = GROOVE, labelanchor = 'nw',
                             width = 300, height = 40)

        self.e4 = Entry(self.L4, textvariable = self.Duration)
        self.e4.pack(side = TOP, fill = X)
        
        self.N1 = LabelFrame(self.frame, text='Notes', relief = GROOVE, labelanchor = 'nw',
                             width = 300, height = 75)

        self.e1 = Entry(self.N1, textvariable = self.Note)
        self.e1.pack(side = TOP, fill = X)

        self.L1.pack(side=TOP, fill = X)
        self.L2.pack(side=TOP, fill = X)
        self.L3.pack(side=TOP, fill = X)
        self.L4.pack(side=TOP, fill = X)
        self.N1.pack(side=TOP, fill = X)

    def initButtons(self):

        self.b1 = Button(self.frame, text = 'OK', relief = GROOVE, command = self.get_vars)
        self.b1.pack(side = LEFT, padx = 3, pady = 3)
        
        ''' Create the drop down menu from current categories in database'''
    def pop_menu(self):
        self.var = StringVar()
        self.category = self.userData['PROJECTS']
        self.op1 = OptionMenu(self.L1, self.var, *self.category)
        self.op1.pack(side = LEFT, fill = X)
        self.var1 = StringVar()
        self.category1 = self.userData['CAT']
        self.op2 = OptionMenu(self.L5, self.var1, *self.category1)
        self.op2.pack(side = LEFT, fill = X)

        
        '''Capture all variables from all fields. If a field is not populated it populates ('') '''
    def get_vars(self):
        z = self.var.get()
        y = self.var1.get()
        a = self.date.get()
        b = self.Time.get()
        c = self.Duration.get()
        d = self.Note.get()
        TS = self.makeTS(a,b)
        tmp = {'USER_ID':self.user, 'PROJECT':z, 'TYPE':self.type, 'DURA':c, 'INFO':d, 'CAT':y, 'TS': tuple(TS)}
        ID = self.db.makeNewLogID()
        self.db.saveNewLogRecord(ID, tmp)
        self.frame.destroy()

    def makeTS(self, date, time):
        date = date.split('/')
        time = time.split(':')
        tmpTS = date + time
        TS = tuple([int(i) for i in tmpTS])
        return TS

    def getManualLog(self):
        return self.tmp


class ReportMenu(Frame):
    def __init__(self, parent, db):
        Frame.__init__(self, parent)
        self.frame = parent
        self.frame.title('Reports')
        self.db = db
        self.initDisplay()


    def initDisplay(self):
        self.list1 = Listbox(self.frame, width = 8, relief = GROOVE)
        self.list2 = Listbox(self.frame, width = 8, relief = GROOVE)
        self.list3 = Listbox(self.frame, width = 8, relief = GROOVE)
        self.list4 = Listbox(self.frame, width = 8, relief = GROOVE)
        self.list5 = Listbox(self.frame, width = 8, relief = GROOVE)
        self.list6 = Listbox(self.frame, width = 20, relief = GROOVE)
        
        self.list1.grid(row=1, column=0)
        self.list2.grid(row=1, column=1)
        self.list3.grid(row=1, column=2)
        self.list4.grid(row=1, column=3)
        self.list5.grid(row=1, column=4)
        self.list6.grid(row=1, column=5)

        self.Label1 = Label(self.frame, relief = GROOVE, anchor = CENTER,
                            height = 1, width = 8, text='Type')
        self.Label2 = Label(self.frame, relief = GROOVE, anchor = CENTER,
                            height = 1, width = 8, text='Project')
        self.Label3 = Label(self.frame, relief = GROOVE, anchor = CENTER,
                            height = 1, width = 8, text='Category')
        self.Label4 = Label(self.frame, relief = GROOVE, anchor = CENTER,
                            height = 1, width = 8, text='Time')
        self.Label5 = Label(self.frame, relief = GROOVE, anchor = CENTER,
                            height = 1, width = 8, text='Duration')
        self.Label6 = Label(self.frame, relief = GROOVE, anchor = CENTER,
                            height = 1, width = 20, text='Notes')

        self.Label1.grid(row=0, column=0)
        self.Label2.grid(row=0, column=1)
        self.Label3.grid(row=0, column=2)
        self.Label4.grid(row=0, column=3)
        self.Label5.grid(row=0, column=4)
        self.Label6.grid(row=0, column=5)

        self.b1 = Button(self.frame, text='OK', height = 1, width=2, relief = GROOVE)
        self.b1.grid(row=5, column=3)

        
        def populateReports(self):
            self.list1.insert(END, db[self.tmpUserData]['TYPE'])
            self.list2.insert(END, db[self.tmpUserData]['PROJECT'])
            self.list3.insert(END, db[self.tmpUserData]['CAT'])
            self.list4.insert(END, db[self.tmpUserData]['TS'])
            self.list5.insert(END, db[self.tmpUserData]['DURA'])
            self.list5.insert(END, db[self.tmpUserData]['INFO'])
    
def main():
    root = Tk()
    db = DataBase()
    app = MainMenu(root, db)
    
main()
