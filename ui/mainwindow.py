from tkinter import *
from core.filecompare import *


class MainWindow:
    # Colors
    whiteColor = '#ffffff'
    redColor = '#ff9494'
    darkredColor = '#ff0000'
    grayColor = '#cccccc'
    lightGrayColor = '#eeeeee'
    greenColor = '#94ffaf'
    darkgreenColor = '#269141'
    yellowColor = '#f0f58c'
    darkYellowColor = '#ffff00'

    def __init__(self):
        self.__main_window = Tk()
        self.__main_window.title('dfcompare')

        self.leftArea = Text(self.__main_window)
        self.rightArea = Text(self.__main_window)
        self.leftArea.pack(side='left')
        self.rightArea.pack(side='right')
        self._configure_editors()

    def _configure_editors(self):
        self.leftArea.tag_configure('red', background=self.redColor)
        self.leftArea.tag_configure('darkred', background=self.darkredColor)
        self.leftArea.tag_configure('gray', background=self.grayColor)
        self.leftArea.tag_configure('search', background=self.darkYellowColor)
        self.rightArea.tag_configure('green', background=self.greenColor)
        self.rightArea.tag_configure('darkgreen', background=self.darkgreenColor)
        self.rightArea.tag_configure('gray', background=self.grayColor)
        self.rightArea.tag_configure('search', background=self.darkYellowColor)

    def set_text(self, diff):
        self.leftArea.delete(1.0, END)
        self.rightArea.delete(1.0, END)
        self.leftArea.config(state=NORMAL)
        self.rightArea.config(state=NORMAL)

        for line in diff:
            if line['code'] == DiffType.EQUAL:
                self.leftArea.insert('end', line['line'] + '\n')
                self.rightArea.insert('end', line['line'] + '\n')
            elif line['code'] == DiffType.LEFT_ONLY:
                self.leftArea.insert('end', line['line'] + '\n', 'red')
                self.rightArea.insert('end', '\n', 'gray')
            elif line['code'] == DiffType.RIGHT_ONLY:
                self.rightArea.insert('end', line['line'] + '\n', 'green')
                self.leftArea.insert('end', '\n', 'gray')
            elif line['code'] == DiffType.CHANGED:
                for (i, c) in enumerate(line['line'] + '\n'):
                    self.leftArea.insert('end', c,
                                         'darkred' if i in line['left_changes'] else 'red')
                for (i, c) in enumerate(line['new_line'] + '\n'):
                    self.rightArea.insert('end', c,
                                          'darkgreen' if i in line['right_changes'] else 'green')
        self.leftArea.config(state=DISABLED)
        self.rightArea.config(state=DISABLED)

    def mainloop(self):
        self.__main_window.mainloop()
