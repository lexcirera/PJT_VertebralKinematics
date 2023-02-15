import cv2 #pip install opencv-python
from cv2 import *
import numpy as np
import tkinter as tk



def manual_clust_det(img1,img2,nb_vert,Clustered_Unclustered_Points):
    '''
    img1: str -path of the first image (front or profile)
    img2: str -path of the associated iamge view
    nb_vert: int -number of clusters
    Clustered_Unclustered_Points: list -list of all images data
        example: [XClustered,YClustered,ZClustered,Unclustered]
                    XClustered=[X1,..,Xn]
                    YClustered=[Y1,..,Yn]
                    ZClustered=[Z1,..,Zn]
                        X1=[x1,...xn]
                        Y1=[y1,...yn]
                        Z1=[z1,...zn]
                    Unclustered=[[x1,y1,z1],...,[xk,yk,zk]]

    commands:
        - d: unlcuster a point
        - c: cluster a point
        - q: confirm to continue

    return:
        Clustered_Points: list [XClustered,YClustered,ZClustered] with Unclustered points integrated
    '''

    from Combine3view import CombineViews
    CombineViews(img1,img2)

    #change the path if needeed
    img=cv2.imread("#####Write the path of the image to read####")



    # Create a window to display the image
    cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    #Set a mouse callback function to capture the coordinates of the points clicked on the image
    operations=[]
    memory_clust=[]

    Unclusterd_Points=Clustered_Unclustered_Points.pop(-1)
    Clustered_Points=Clustered_Unclustered_Points
    offset=1765

    List_Colors=[]
    for i in range(nb_vert):
        color = np.random.randint(0,255,3)
        List_Colors.append(color)

    while len(Clustered_Points[0])<nb_vert:
        Clustered_Points[0].append([])
        Clustered_Points[1].append([])
        Clustered_Points[2].append([])


    def warn_popup():
        warn=tk.Tk()
        warn.geometry('400x80')
        warn.title("Vertebral Kinematics - Warning")
        message_warn = tk.Label(warn,text="Number of selected clusters must be equal to input vertebrae")
        message_warn.pack()
        button_back=tk.Button(warn,text='Back to configuration',command=warn.destroy)
        button_back.pack()
        warn.mainloop()

    # Display the image and wait for the user to select points
    while True:
        canvas = img.copy()

        #Draw colored cross at each cluster detected automatically
        for i in range(len(Clustered_Points[0])):
            XCluster = Clustered_Points[0][i]
            YCluster = Clustered_Points[1][i]
            ZCluster = Clustered_Points[2][i]
            color=List_Colors[i]
            for j in range(len(XCluster)):
                x,y,z=XCluster[j],YCluster[j],ZCluster[j]

                cv2.putText(canvas, str(i+1)+"."+str(j+1), (x+10, z),cv2.FONT_HERSHEY_SIMPLEX, 1, ((int(color[0]),int(color[1]),int(color[2]))),2 ,cv2.LINE_AA)

                cv2.line(canvas, (x-10, z), (x+10, z), (int(color[0]),int(color[1]),int(color[2])), 5)
                cv2.line(canvas, (x, z-10), (x, z+10), (int(color[0]),int(color[1]),int(color[2])), 5)


                cv2.putText(canvas, str(i+1)+"."+str(j+1), (y+10+offset, z),cv2.FONT_HERSHEY_SIMPLEX, 1, (int(color[0]),int(color[1]),int(color[2])),2 ,cv2.LINE_AA)

                cv2.line(canvas, (y+offset-10, z), (y+offset+10, z), (int(color[0]),int(color[1]),int(color[2])), 5)
                cv2.line(canvas, (y+offset, z-10), (y+offset, z+10), (int(color[0]),int(color[1]),int(color[2])), 5)


        #Draw red unclustered points
        if len(Unclusterd_Points)>0:
            for i in range(len(Unclusterd_Points)):
                point=Unclusterd_Points[i]
                x,y,z=point[0],point[1],point[2]
                cv2.putText(canvas, str(len(Clustered_Points[0])+i+1), (x+10, z),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2 ,cv2.LINE_AA)
                cv2.line(canvas, (x-10, z), (x+10, z), (0,0,255), 5)
                cv2.line(canvas, (x, z-10), (x, z+10), (0,0,255), 5)

                cv2.putText(canvas, str(len(Clustered_Points[0])+i+1), (y+offset+10, z),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2 ,cv2.LINE_AA)
                cv2.line(canvas, (y+offset-10, z), (y+offset+10, z), (0,0,255), 5)
                cv2.line(canvas, (y+offset, z-10), (y+offset, z+10), (0,0,255), 5)

        cv2.imshow("image", canvas)

        key = cv2.waitKey(1)

        #key: confirmation
        if key == ord("q"):

            if len(Clustered_Points[0]) != nb_vert :
                warn_popup()

            else:
                break


        #key: undo
        elif key == ord("u"):
            '''
            on supprime de la liste les coo du dernier point
            '''
            ope=0
            if len(operations) > 0:
                ope=operations[-1]

            if ope==1:
            # Remove the last clustered point
                if len(memory_clust) > 0:
                    clust_id=memory_clust.pop()
                    x=Clustered_Points[0][clust_id-1].pop()
                    y=Clustered_Points[1][clust_id-1].pop()
                    z=Clustered_Points[2][clust_id-1].pop()

                    Unclusterd_Points.append([x,y,z])

                operations.pop(-1)


            if ope == 2:
            #put back in cluster the last unclustered point
                if len(memory_clust) > 0:
                    point=memory_clust.pop()
                    print(point)
                    x=point[0]
                    y=point[1]
                    z=point[2]
                    clust_id=point[3]

                    Clustered_Points[0][clust_id].append(x)
                    Clustered_Points[1][clust_id].append(y)
                    Clustered_Points[2][clust_id].append(z)


                    Unclusterd_Points.pop(Unclusterd_Points.index([x,y,z]))
                    operations.pop(-1)

        #key: uncluster a points
        elif key == ord("d"):
            '''
            uncluster function with tkinter interface
            '''

            conf_un=tk.Tk()
            conf_un.geometry('300x180')
            conf_un.title("Uncluster a point")
            message = tk.Label(conf_un,text="ID of the cluster")
            message.pack()
            clust_id=tk.IntVar()
            clust_id.set(1)
            Clust_id=tk.Entry(conf_un,textvariable=clust_id)
            Clust_id.pack()

            message = tk.Label(conf_un,text="ID of the point")
            message.pack()
            point_id=tk.IntVar()
            point_id.set(1)
            Point_id=tk.Entry(conf_un,textvariable=point_id)
            Point_id.pack()


            def uncluster_point():
                unclust_clust_id=clust_id.get()
                unclust_point_id=point_id.get()

                if unclust_clust_id>0 and unclust_clust_id<=nb_vert:
                    if unclust_point_id>0 and unclust_point_id<=len(Clustered_Points[0][unclust_clust_id-1]):
                        x=Clustered_Points[0][unclust_clust_id-1].pop(unclust_point_id-1)
                        y=Clustered_Points[1][unclust_clust_id-1].pop(unclust_point_id-1)
                        z=Clustered_Points[2][unclust_clust_id-1].pop(unclust_point_id-1)

                        Unclusterd_Points.append([x,y,z])


                        memory_clust.append([x,y,z,unclust_clust_id-1])
                        operations.append(2)
                        conf_un.destroy()

                else:
                    conf_un.destroy()
                    conf2=tk.Tk()
                    conf2.geometry('300x80')
                    conf2.title("Warning")
                    message2 = tk.Label(text="Not a valid ID. Please retry")
                    message2.pack()
                    button=tk.Button(conf2,text='OK',command=conf2.destroy)
                    button.pack()
                    conf2.mainloop()

            button1=tk.Button(conf_un,text='Uncluster the point', command=uncluster_point)
            button1.pack()

            button2=tk.Button(conf_un,text='Cancel',command=conf_un.destroy)
            button2.pack()

            conf_un.mainloop()

        #key: cluster points
        elif key == ord("c"):
            '''
            cluster function with tkinter interface
            '''
            if len(Unclusterd_Points)>0:

                conf_clust=tk.Tk()
                conf_clust.geometry('300x180')
                conf_clust.title("Add a point to a cluster")

                message = tk.Label(conf_clust,text="ID of the point")
                message.pack()
                point_id=tk.IntVar()
                point_id.set(len(Clustered_Points[0])+1)
                Point_id=tk.Entry(conf_clust,textvariable=point_id)
                Point_id.pack()

                message = tk.Label(conf_clust,text="ID of the cluster")
                message.pack()
                clust_id=tk.IntVar()
                clust_id.set(1)
                Clust_id=tk.Entry(conf_clust,textvariable=clust_id)
                Clust_id.pack()


                def manual_clust():
                    clust_clust_id=clust_id.get()
                    clust_point_id=point_id.get()
                    if clust_clust_id>0 and clust_clust_id<=nb_vert:
                        if clust_point_id>0 and (clust_point_id-len(Clustered_Points[0]))<=len(Unclusterd_Points):

                            x=Unclusterd_Points[clust_point_id-len(Clustered_Points[0])-1][0]
                            y=Unclusterd_Points[clust_point_id-len(Clustered_Points[0])-1][1]
                            z=Unclusterd_Points[clust_point_id-len(Clustered_Points[0])-1][2]
                            Unclusterd_Points.pop(clust_point_id-len(Clustered_Points[0])-1)

                            Clustered_Points[0][clust_clust_id-1].append(x)
                            Clustered_Points[1][clust_clust_id-1].append(y)
                            Clustered_Points[2][clust_clust_id-1].append(z)


                            memory_clust.append(clust_clust_id-1)

                            operations.append(1)
                            conf_clust.destroy()

                    else:
                        conf_un.destroy()
                        conf2=tk.Tk()
                        conf2.geometry('300x80')
                        conf2.title("Warning")
                        message2 = tk.Label(text="Not a valid ID")
                        message2.pack()
                        button=tk.Button(conf2,text='OK',command=conf2.destroy)
                        button.pack()
                        conf2.mainloop()

                button1=tk.Button(conf_clust,text='Add the point to the Cluster', command=manual_clust)
                button1.pack()

                button2=tk.Button(conf_clust,text='Cancel',command=conf_clust.destroy)
                button2.pack()

                conf_clust.mainloop()





    # Close the window and exit
    cv2.destroyAllWindows()



    return Clustered_Points



