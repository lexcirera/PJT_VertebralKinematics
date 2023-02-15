import cv2 #pip install opencv-python
import numpy as np
import tkinter as tk

def manual_match_det(img1,img2,nb_mark,Matched_points,Unmatched_points=[]):
    '''
    img1: str -path of the first image (front or profile)
    img2: str -path of the associated iamge view
    nb_mark: int -number of markers
    Matched_points: list -list of lists  of automatics points from all images

    Unmatched_points: list -list of lists of unmatched points coordinates

    commands:
        - d: unmatch a point
        - c: match points
        - q: confirm to continue

    return:
        auto_matched_points: list -list of list with all matched inside (no unmatch tolerated)
    '''
    from Combine3view import CombineViews
    CombineViews(img1,img2)

    #cahnge the path if needeed
    img=cv2.imread("#####Write the path of the image to read####")


    # Create a window to display the image
    cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Set a mouse callback function to capture the coordinates of the points clicked on the image
    auto_matched_points=Matched_points #copy of Matched_points to do manipulations
    operations=[]
    memory_match=[]

    List_Colors=[]
    for i in range(nb_mark):
        color = np.random.randint(0,255,3)
        List_Colors.append(color)

    def warn_popup():
        warn=tk.Tk()
        warn.geometry('400x80')
        warn.title("Vertebral Kinematics - Warning")
        message_warn = tk.Label(warn,text="Number of selected markers must be equal to input markers")
        message_warn.pack()
        button_back=tk.Button(warn,text='Back to configuration',command=warn.destroy)
        button_back.pack()
        warn.mainloop()

    # Display the image and wait for the user to select points
    while True:
        canvas = img.copy()

        #Draw colored cross at each automatic matched point
        for i in range(len(auto_matched_points)):
            point=auto_matched_points[i]
            if point in auto_matched_points:
                point1=point[0]
                point2=point[1]
                color = List_Colors[i]

                cv2.putText(canvas, str(i+1), (point1[0]+10, point1[1]),cv2.FONT_HERSHEY_SIMPLEX, 1, (int(color[0]),int(color[1]),int(color[2])),2 ,cv2.LINE_AA)

                cv2.line(canvas, (point1[0]-10, point1[1]), (point1[0]+10, point1[1]), (int(color[0]),int(color[1]),int(color[2])), 5)
                cv2.line(canvas, (point1[0], point1[1]-10), (point1[0], point1[1]+10), (int(color[0]),int(color[1]),int(color[2])), 5)


                cv2.putText(canvas, str(i+1), (point2[0]+10, point2[1]),cv2.FONT_HERSHEY_SIMPLEX, 1, (int(color[0]),int(color[1]),int(color[2])),2 ,cv2.LINE_AA)

                cv2.line(canvas, (point2[0]-10, point2[1]), (point2[0]+10, point2[1]), (int(color[0]),int(color[1]),int(color[2])), 5)
                cv2.line(canvas, (point2[0], point2[1]-10), (point2[0], point2[1]+10), (int(color[0]),int(color[1]),int(color[2])), 5)


        #Draw red unmatched point
        if len(Unmatched_points)>0:
            for i in range(len(Unmatched_points)):
                point=Unmatched_points[i]
                if point != []:
                    cv2.putText(canvas, str(len(auto_matched_points)+i+1), (point[0]+10, point[1]),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2 ,cv2.LINE_AA)

                    cv2.line(canvas, (point[0]-10, point[1]), (point[0]+10, point[1]), (0,0,255), 5)
                    cv2.line(canvas, (point[0], point[1]-10), (point[0], point[1]+10), (0,0,255), 5)


        cv2.imshow("image", canvas)
        key = cv2.waitKey(1)

        #key: confirmation
        if key == ord("q"):

            if len(auto_matched_points) != nb_mark :
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
            # Remove the last match
                match_to_unmatch=auto_matched_points.pop()
                Unmatched_points.append(match_to_unmatch[0])
                Unmatched_points.append(match_to_unmatch[1])

                operations.pop(-1)


            if ope == 2:
            #rematch the last unmatch
                if len(memory_match) > 0:
                    restore_set=memory_match.pop()
                    Unmatched_points.pop()
                    Unmatched_points.pop()
                    auto_matched_points.append(restore_set)
                    operations.pop(-1)

        #key: unmatch points
        elif key == ord("d"):
            '''
            unmatch function with tkinter interface
            '''

            conf_un=tk.Tk()
            conf_un.geometry('300x130')
            conf_un.title("Unmatch automatic matched points")
            message = tk.Label(conf_un,text="ID of the set to unmatch")
            message.pack()
            set_id=tk.IntVar()
            set_id.set(1)
            points_set_id=tk.Entry(conf_un,textvariable=set_id)
            points_set_id.pack()



            def unmatch_markers():
                unmatch_id=set_id.get()

                if unmatch_id>0 and unmatch_id<=len(auto_matched_points):


                    unmatch_set=auto_matched_points.pop(unmatch_id-1)
                    Unmatched_points.append(unmatch_set[0])
                    Unmatched_points.append(unmatch_set[1])

                    memory_match.append(unmatch_set)
                    operations.append(2)
                    conf_un.destroy()

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

            button1=tk.Button(conf_un,text='Unmatch', command=unmatch_markers)
            button1.pack()

            button2=tk.Button(conf_un,text='Cancel',command=conf_un.destroy)
            button2.pack()

            conf_un.mainloop()

        #key: match points
        elif key == ord("m"):
            '''
            match function with tkinter interface
            '''
            if len(Unmatched_points)>0:

                conf_match=tk.Tk()
                conf_match.geometry('300x180')
                conf_match.title("Match points")
                message = tk.Label(conf_match,text="ID of the 1st point to match")
                message.pack()
                id1=tk.IntVar()
                id1.set(len(auto_matched_points)+1)
                point1_id=tk.Entry(conf_match,textvariable=id1)
                point1_id.pack()

                message = tk.Label(conf_match,text="ID of the 2nd point to match")
                message.pack()
                id2=tk.IntVar()
                id2.set(len(auto_matched_points)+2)
                point2_id=tk.Entry(conf_match,textvariable=id2)
                point2_id.pack()

                def manual_match_points():
                    match_id1=id1.get()-len(auto_matched_points)-1
                    match_id2=id2.get()-len(auto_matched_points)-1
                    if (match_id1>=0 and match_id1<len(Unmatched_points)) and(match_id2>=0 and match_id2<len(Unmatched_points)) and (match_id1 != match_id2):



                        new_match=[Unmatched_points.pop(match_id1),Unmatched_points.pop(match_id2-1)]
                        auto_matched_points.append(new_match)
                        List_Colors.append(np.random.randint(0,255,3))

                        operations.append(1)


                        conf_match.destroy()

                    else:
                        conf_match.destroy()
                        conf2=tk.Tk()
                        conf2.geometry('300x80')
                        conf2.title("Warning")
                        message2 = tk.Label(text="Not a valid IDs (must be two differents integers")
                        message2.pack()
                        button=tk.Button(conf2,text='OK',command=conf2.destroy)
                        button.pack()
                        conf2.mainloop()

                button1=tk.Button(conf_match,text='Match', command=manual_match_points)
                button1.pack()

                button2=tk.Button(conf_match,text='Cancel',command=conf_match.destroy)
                button2.pack()

                conf_match.mainloop()





    # Close the window and exit
    cv2.destroyAllWindows()



    return auto_matched_points






