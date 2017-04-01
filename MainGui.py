# Main GUI window
# -*- coding: utf-8 -*-
import sys
import Controller
from Tkinter import *
from itertools import groupby
import tkMessageBox


def processEntities():
    # text = 'Bridgestone Sports Co. said that Friday it had set up a joint venture in Taiwan with a local concern and a Japanese trading house to produce golf clubs to be supplied to Japan. The joint venture, Bridgestone Sports Taiwan Co., capitalized at 20 million new Taiwan dollars, will start production in January 1990 with production of 20,000 iron and “metal wood” clubs a month. The Whitehouse in Washington'
    # T.insert(INSERT, text)
    # create controller object
    T2.delete("1.0", END)
    inputText = T.get("1.0", END)
    if (len(inputText) != 0):
        textObj = Controller.ControllerUnit(T.get("1.0", END))

        # perform Named Entity Recognition
        nerOutput = textObj.performNER()
        entities = []
        for tag, chunk in groupby(nerOutput, lambda x: x[1]):
            if tag != "O":
                entity = " ".join(w for w, t in chunk)
                if entity not in entities:
                    T2.insert(END, tag + ":\t" + entity + "\n")
                    entities.append(entity)
                    # T2.insert(END,nerOutput)

                    # perform Date-time extraction
                    # dateTimeOutput = textObj.performDateTimeExtraction()
                    # T2.insert(END, dateTimeOutput)

                    # perform relation extraction
    else:
        tkMessageBox.showwarning("Warning", "Please insert Text.")


def processRelations():
    T2.delete("1.0", END)
    textObj = Controller.ControllerUnit(T.get("1.0", END))
    orgLocRelation = textObj.orgLocRelationExtraction()
    T2.insert(END, "Organization-Location Relations:\n")
    for relation in orgLocRelation:
        T2.insert(END, relation)
        T2.insert(END, "\n")
    perOrgRelation = textObj.perOrgRelationExtraction()
    T2.insert(END, "Person-Organization Relations:\n")
    for rel in perOrgRelation:
        T2.insert(END, rel)
        T2.insert(END, "\n")


root = Tk()
root.title("Main")
root.geometry("500x400")
button = Button(root, text='Extract Entities', command=processEntities, fg='black', bg='gray').pack()
button1 = Button(root, text='Extract Relations', command=processRelations, fg='black', bg='gray').pack()
T = Text(root, height=10, width=50)
T2 = Text(root, height=7, width=50)
label1 = Label(root, text="Input Text:")
label2 = Label(root, text="Output:")
label1.pack()
T.pack()
label2.pack()
T2.pack()
root.mainloop()
