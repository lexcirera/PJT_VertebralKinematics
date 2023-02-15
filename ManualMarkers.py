import cv2 #pip install opencv-python
import numpy as np
import tkinter as tk

def manual_markers_det(img,nb_mark,auto_points=[]):
    '''
    img1: cv2.imread("image_path")

    nb_mark: int -number of markers
    auto_points: list -list of coordiantes of automatics points


    commands:
        - left click: select a point
        - d: unmark a point
        - u: ctrl+z, undo last operation
        - q: confirm to continue

    return:
        all_points: list -list of lists[x,y,z] of all points coordiantes
    '''
    # Create a window to display the image
    cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Set a mouse callback function to capture the coordinates of the points clicked on the image
    a_points=auto_points #copy of auto_points to do manipulations
    points = []
    operations=[]
    memory_point_delete=[]
    memory_id_delete=[]
    all_points=a_points+points


    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append([x, y])
            operations.append(1)


    def warn_popup():
        warn=tk.Tk()
        warn.geometry('450x80')
        warn.title("Vertebral Kinematics - Warning")
        message_warn = tk.Label(warn,text="Number of selected markers must be equal to input markers ("+str(nb_mark)+")")
        message_warn.pack()
        button_back=tk.Button(warn,text='Back to configuration',command=warn.destroy)
        button_back.pack()
        warn.mainloop()

    cv2.setMouseCallback("image", click_event)


    # Display the image and wait for the user to select points
    while True:
        canvas = img.copy()
        #Draw a black cross at each automatic detected point
        for i in range(len(auto_points)):
            point=auto_points[i]
            if point in a_points:
                cv2.putText(canvas, str(auto_points.index(point)+1), (point[0]+10, point[1]),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2 ,cv2.LINE_AA)

                cv2.line(canvas, (point[0]-10, point[1]), (point[0]+10, point[1]), (0, 0, 0), 5)
                cv2.line(canvas, (point[0], point[1]-10), (point[0], point[1]+10), (0, 0, 0), 5)



        # Draw a red cross at each of the selected point
        for point in points:
            cv2.line(canvas, (point[0]-10, point[1]), (point[0]+10, point[1]), (0, 0, 255), 3)
            cv2.line(canvas, (point[0], point[1]-10), (point[0], point[1]+10), (0, 0, 255), 3)


        cv2.imshow("image", canvas)
        key = cv2.waitKey(1)

        #key: confirmation
        if key == ord("q"):
            '''
            validation key
            '''
            all_points=a_points+points
            if len(all_points) != nb_mark:
                warn_popup()

            else:
                break


        #key: undo
        elif key == ord("u"):
            '''
            ctrl + z function
            '''
            ope=0
            if len(operations) > 0:
                ope=operations[-1]

            if ope==1:
            # Remove the last point selected
                if len(points) > 0:
                    points.pop()
                    operations.pop(-1)

            if ope == 2:
            #add the last deleted point
                if len(memory_point_delete) > 0:
                    restore_id=memory_id_delete.pop(-1)
                    restore_point=memory_point_delete.pop(-1)
                    a_points.append(restore_point)
                    operations.pop(-1)

        #key: delete
        elif key == ord("d"):
            '''
            delete function with tkinter interface
            '''

            conf=tk.Tk()
            conf.geometry('300x130')
            conf.title("Delete an automatic point")
            message = tk.Label(text="ID of the point to delete")
            message.pack()
            id=tk.IntVar()
            id.set(len(a_points))
            point_id=tk.Entry(conf,textvariable=id)
            point_id.pack()



            def delete_point():
                del_id=id.get()

                if del_id>0 and del_id<=len(a_points):
                    delpoint=a_points.pop(id.get()-1)
                    memory_point_delete.append(delpoint)
                    memory_id_delete.append(del_id)
                    operations.append(2)
                    conf.destroy()

                else:
                    conf.destroy()
                    conf2=tk.Tk()
                    conf2.geometry('300x80')
                    conf2.title("Warning")
                    message2 = tk.Label(text="Not a valid ID")
                    message2.pack()
                    button=tk.Button(conf2,text='OK',command=conf2.destroy)
                    button.pack()
                    conf2.mainloop()

            button1=tk.Button(conf,text='Delete', command=delete_point)
            button1.pack()

            button2=tk.Button(conf,text='Cancel',command=conf.destroy)
            button2.pack()

            conf.mainloop()

    all_points=a_points+points





    # Close the window and exit
    cv2.destroyAllWindows()



    return all_points








