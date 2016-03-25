#-*-ecoding=utf-8-*-
#!/usr/bin/env python
"""Basic regular expression demostration facility (Perl style syntax)."""

from tkinter import *
import re

class ReDemo:

    def __init__(self, master):
        self.master = master

        self.promptdisplay = Label(self.master, anchor=W,
                text="正则表达式:")
        self.promptdisplay.pack(side=TOP, fill=X)

        self.regexdisplay = Entry(self.master)
        self.regexdisplay.pack(fill=X)
        self.regexdisplay.focus_set()
        self.addoptions()
        self.statusdisplay = Label(self.master, text="", anchor=W)
        self.statusdisplay.pack(side=TOP, fill=X)

        self.labeldisplay = Label(self.master, anchor=W,
                text="字 符 串:")
        self.labeldisplay.pack(fill=X)
        self.labeldisplay.pack(fill=X)

        self.showframe = Frame(master)
        self.showframe.pack(fill=X, anchor=W)

        self.showvar = StringVar(master)
        self.showvar.set("first")

        self.stringdisplay = Text(self.master, width=60, height=4)
        self.stringdisplay.pack(fill=BOTH, expand=1)
        self.stringdisplay.tag_configure("hit", background="yellow")

        self.grouplabel = Label(self.master, text="匹配结果:", anchor=W)
        self.grouplabel.pack(fill=X)

        self.grouplist = Listbox(self.master)
        self.grouplist.pack(expand=1, fill=BOTH)

        self.regexdisplay.bind('<Key>', self.recompile)
        self.stringdisplay.bind('<Key>', self.reevaluate)

        self.compiled = None
        self.recompile()

        btags = self.regexdisplay.bindtags()
        self.regexdisplay.bindtags(btags[1:] + btags[:1])

        btags = self.stringdisplay.bindtags()
        self.stringdisplay.bindtags(btags[1:] + btags[:1])

    def addoptions(self):
        self.frames = []
        self.boxes = []
        self.vars = []
        name1=['IGNORECASE','LOCALE','MULTILINE','DOTALL', 'VERBOSE']
        name2=['不区分大小写','本地化识别','忽略^和$','忽略换行符  ', '松散正则']
        for name in range(0,5):
            if len(self.boxes) % 3 == 0:
                frame = Frame(self.master)
                frame.pack(fill=X)
                self.frames.append(frame)
            val = getattr(re, name1[name])
            var = IntVar()
            box = Checkbutton(frame,
                    variable=var, text=name2[name],
                    offvalue=0, onvalue=val,
                    command=self.recompile)
            box.pack(side=LEFT)
            self.boxes.append(box)
            self.vars.append(var)

    def getflags(self):
        flags = 0
        for var in self.vars:
            flags = flags | var.get()
        flags = flags
        return flags

    def recompile(self, event=None):
        try:
            print (self.regexdisplay.get(),000)
            self.compiled = re.compile(self.regexdisplay.get(),
                                       self.getflags())
            bg = self.promptdisplay['background']
            self.statusdisplay.config(text="", background=bg)
        except (re.error, msg):
            self.compiled = None
            self.statusdisplay.config(
                    text="正则错误: %s" % str(msg),
                    background="red")
        self.reevaluate()

    def reevaluate(self, event=None):
        try:
            self.stringdisplay.tag_remove("hit", "1.0", END)
        except TclError:
            pass
        try:
            self.stringdisplay.tag_remove("hit0", "1.0", END)
        except TclError:
            pass
        self.grouplist.delete(0, END)
        if not self.compiled:
            return
        self.stringdisplay.tag_configure("hit", background="yellow")
        self.stringdisplay.tag_configure("hit0", background="orange")
        text = self.stringdisplay.get("1.0", END)
        last = 0
        nmatches = 0
        while last <= len(text):
            m = self.compiled.findall(text, last)
            if m[0]=='' and m[0]=='':
                break
            if len(m) !=0:
                for i in range(len(m)):
                    g = u"第%d个: %s" % (i+1, m[i])
                    self.grouplist.insert(END, g)
            nmatches = nmatches + 1
            if self.showvar.get() == "first":
                break

        if nmatches == 0:
            self.statusdisplay.config(text="(不匹配)",
                                      background="yellow")
        else:
            self.statusdisplay.config(text="")


def main():
    pass
    root = Tk()
    demo = ReDemo(root)
    root.title('Python正则测试器')
    root.protocol('WM_DELETE_WINDOW', root.quit)
    root.mainloop()

if __name__ == '__main__':
    main()
