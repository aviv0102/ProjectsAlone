"""
Written by:
    Aviv Shisman
"""

# imports:
from tkinter import *
from functools import partial
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# params:
root = Tk()


'''
showing prediction results in graphs with gui
'''
def main():

    # show start menu
    showMenu()

    # run gui
    root.winfo_toplevel().title("prediction")
    root.configure(background='cyan')
    root.mainloop()

    return

'''
Menu page
'''
def showMenu():

    # clean screen
    for ele in root.winfo_children():
        ele.destroy()
    root.geometry("300x200")

    # create buttons and title:
    T = Text(root, height=2, width=30,bg = 'cyan',font=('Arial', 12, 'bold', 'italic'),borderwidth = -1)
    T.place(x=40, y=15)
    T.insert(END, "Welcome to prediction viewer")

    start= Button(root,text ='Start',command = choose_office,bg='white',font=('Arial', 8, 'bold', 'italic'))
    start.place(x=50,y=70 ,height = 20 , width = 200)
    exit = Button(root,text ='Exit',command = root.quit,bg='white',font=('Arial', 8, 'bold', 'italic'))
    exit.place(x=50,y=120,height = 20 , width = 200)



    return

'''
choose office page,(second page)
'''
def choose_office():

    # clear screen
    for ele in root.winfo_children():
        ele.destroy()
    root.geometry("700x700")

    # add title
    T = Text(root, height=2, width=30,bg = 'cyan',font=('Arial', 12, 'bold', 'italic'),borderwidth = -1)
    T.place(x=20, y=10)
    T.insert(END, "Select office")

    # get office ids
    office_ids = load_office_ids()

    # get office choice from buttons
    for j,id in enumerate (office_ids):
        b = Button(root, text=id, command=partial(choose_date,id) , bg='white', font=('Arial', 8, 'bold', 'italic'))
        b.place(x=200, y=60 +j*30, height=20, width=200)

    # exit or back option
    ret = Button(root,text ='Return',command = showMenu,bg='white',font=('Arial', 8, 'bold', 'italic'))
    ret.place(x=20,y=640,height = 20 , width = 200)
    exit = Button(root,text ='Exit',command = root.quit,bg='white',font=('Arial', 8, 'bold', 'italic'))
    exit.place(x=20,y=675,height = 20 , width = 200)



'''
choose date you wish to see (third page)
'''
def choose_date(office_choice):

    # clear
    for ele in root.winfo_children():
        ele.destroy()
    root.geometry("700x700")

    # title
    T = Text(root, height=2, width=100, bg='cyan', font=('Arial', 12, 'bold', 'italic'), borderwidth=-1)
    T.place(x=20, y=10)
    T.insert(END, "These are the available dates for office:  "+ str(office_choice))
    T = Text(root, height=2, width=100, bg='cyan', font=('Arial', 12, 'bold', 'italic'), borderwidth=-1)
    T.place(x=20, y=80)
    T.insert(END, "Select which one you wish to see")


    # get dates + data of predictions related to the office you chose
    available_dates, data = load_data(office_choice)


    # get office choice from buttons
    k = 0
    for j,date in enumerate (available_dates):
        b = Button(root, text=date, command=partial(show_date,(date,office_choice,data)) , bg='white',
                   font=('Arial', 8, 'bold', 'italic'))
        if j%7 ==0:
            k+=1
        b.place(x=5 + (j%7)*100, y=80 +k*40, height=30, width=100)


    # exit or back option
    ret = Button(root,text ='Return',command = choose_office,bg='white',font=('Arial', 8, 'bold', 'italic'))
    ret.place(x=20,y=640,height = 20 , width = 200)
    exit = Button(root,text ='Exit',command = root.quit,bg='white',font=('Arial', 8, 'bold', 'italic'))
    exit.place(x=20,y=675,height = 20 , width = 200)

    return

'''
show prediction for date
'''
def show_date(args):
    # clear
    for ele in root.winfo_children():
        ele.destroy()
    root.geometry("700x700")

    # show date
    curr_date = args[0]

    # title
    T = Text(root, height=2, width=100, bg='cyan', font=('Arial', 12, 'bold', 'italic'), borderwidth=-1)
    T.place(x=20, y=10)
    T.insert(END, "predictions for "+curr_date)

    predictions = get_predictions_by_date(curr_date,args[2])

    start = graph_plotter(root,predictions)

    # exit or back option
    ret = Button(root,text ='Return',command = partial(choose_date,args[1]),bg='white',font=('Arial', 8, 'bold', 'italic'))
    ret.place(x=20,y=640,height = 20 , width = 200)
    exit = Button(root,text ='Exit',command = root.quit,bg='white',font=('Arial', 8, 'bold', 'italic'))
    exit.place(x=20,y=675,height = 20 , width = 200)

    return


'''
load predictions file, get all predictions for the specific office + order them to dates
'''
def load_data(office_id):
    predictions_file = open('prediction.csv','r')

    # params:
    data =[]
    latest_day = -1
    available_dates = []
    temp = []

    for i,line in enumerate(predictions_file.readlines()):
        entry = line.rstrip('\n').split(',')
        if entry[0] == str(office_id):  # learn only data from the specific office
            entry.remove(entry[0])
            if i == 1:                  # order the predictions into groups of specific dates
                available_dates.append(entry[4])
                latest_day = entry[1]
                temp.append(entry)
            elif entry[1] == latest_day:
                temp.append(entry)
            else:
                data.append(temp)
                temp = []
                available_dates.append(entry[4])
                latest_day = entry[1]
                temp.append(entry)
    data.append(temp)
    predictions_file.close()

    return available_dates,data


'''
load office id's
'''
def load_office_ids():
    office_ids = []
    office_ids_file = open("offices.txt", 'r')
    for line in office_ids_file.readlines():
        office_ids.append(line.rstrip('\n'))
    office_ids_file.close()

    return office_ids


'''
get the predictions for specific date
'''
def get_predictions_by_date(date,data):

    x_hour= []  # x will be hours
    y_pred = [] # y will be predictions

    for en in data:
        try:
            if date == en[0][4]:
                for day in en:
                    x_hour.append(day[2])
                    y_pred.append(day[3])
                break
        except Exception:
            continue



    return (x_hour,y_pred)


'''
graph class
'''
class graph_plotter:
    def __init__(self,  window,predictions):
        self.window = window
        self.pred = predictions
        self.plot()

    def plot (self):
        x=np.array (self.pred[0])
        y=np.array (self.pred[1])

        fig = Figure(figsize=(5,5),dpi=100)
        a = fig.add_subplot(111)
        a.plot(x,y,color='red')
        a.invert_yaxis()

        a.set_title ("daily prediction", fontsize=16)
        a.set_ylabel("occupancy", fontsize=14)
        a.set_xlabel("hour", fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.get_tk_widget().place(x=100,y=100)
        canvas.draw()



if __name__ == '__main__':
    main()
