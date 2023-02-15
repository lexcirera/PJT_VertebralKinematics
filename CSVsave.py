import csv
import tkinter as tk


def data_structure(List_Im_data):

    Data = []

    for id_cluster in range(len(List_Im_data[0][0])):
        Cluster=[]
        for id_marker in range(len(List_Im_data[0][0][id_cluster])):
            x,y,z = [],[],[]
            for id_im in range(len(List_Im_data)):
                x.append(List_Im_data[id_im][0][id_cluster][id_marker])
                y.append(List_Im_data[id_im][1][id_cluster][id_marker])
                z.append(List_Im_data[id_im][2][id_cluster][id_marker])
            Marker=[x,y,z]
            Cluster.append(Marker)
        Data.append(Cluster)

    return Data



def create_csv(data, directory, filename):
    with open(f"{directory}/{filename}", "w",newline='') as file:
        writer = csv.writer(file)

        nb_im=len(data[0][0][0])
        im_id=[' ', 'Image ID']
        for i in range(nb_im):
            im_id.append(i+1)

        for id_cluster in range(len(data)):
            Cluster=data[id_cluster]
            writer.writerow(["Cluster "+str(id_cluster+1)])
            writer.writerow(im_id)
            for id_marker in range(len(Cluster)):
                Marker=Cluster[id_marker]
                writer.writerow(["Marker "+str(id_marker+1), 'x']+Marker[0])
                writer.writerow(([" ", 'y']+Marker[1]))
                writer.writerow(([" ", 'z']+Marker[2]))
                writer.writerow([''])
            writer.writerow([''])
            writer.writerow([''])




def save_csv(data, directory):
    conf=tk.Tk()
    conf.geometry('300x100')
    conf.title("Save")
    message = tk.Label(text="Name the file")
    message.pack()
    filename=tk.StringVar()
    filename.set(1)
    point_id=tk.Entry(conf,textvariable=filename)
    point_id.pack()
    button=tk.Button(conf,text='Save',command=conf.destroy)
    button.pack()
    conf.mainloop()

    create_csv(data,directory,filename.get()+str('.csv'))

    conf=tk.Tk()
    conf.geometry('700x80')
    conf.title("Save")
    message = tk.Label(text=f"File saved successfully to {directory}\{filename.get()}")
    message.pack()
    button=tk.Button(conf,text='OK',command=conf.destroy)
    button.pack()
    conf.mainloop()












