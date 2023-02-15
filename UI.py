import tkinter as tk
from os import *
import cv2


def count_files(directory):
    # Récupérer la liste de tous les fichiers dans le répertoire
    import os as osmodule
    file_list = osmodule.listdir(directory)

    # Compter le nombre de fichiers dans la liste
    file_count = 0
    for file in file_list:
        if osmodule.path.isfile(osmodule.path.join(directory, file)):
            file_count += 1
    return file_count


import tkinter as tk

def init_UI():
    menu_in=tk.Tk()
    menu_in.geometry('1920x1080')
    menu_in.title("Vertebral Kinematics")
    message = tk.Label(text="Ceci est la page de garde")
    message.pack()

    def ini_menu_UI():
        menu_UI(menu_in)


    button_start=tk.Button(menu_in,text='Start',command=ini_menu_UI)
    button_start.pack()
    button_quite=tk.Button(menu_in,text='Quit',command=menu_in.destroy)
    button_quite.pack()
    menu_in.mainloop()

#init_UI()



def menu_UI(menu_in):
    menu_in.destroy()
    menu_start=tk.Tk()
    menu_start.geometry('1920x1080')
    menu_start.title("Vertebral Kinematics")
    message = tk.Label(text="Ceci est le menu de départ")
    message.pack()


    def ini_menu_simu():
        menu_simu(menu_start)

    def ini_menu_infos():
        menu_infos(menu_start)

    def ini_menu_quit():
        menu_quit(menu_start)


    button_simu=tk.Button(menu_start,text='Choose options',command=ini_menu_simu)
    button_simu.pack()
    button_infos=tk.Button(menu_start,text='Informations',command=ini_menu_infos)
    button_infos.pack()
    button_quit=tk.Button(menu_start,text='Quit',command=ini_menu_quit)
    button_quit.pack()
    menu_start.mainloop()





def menu_simu(menu_start):
    menu_start.destroy()
    simu_choice=tk.Tk()
    simu_choice.geometry('1920x1080')
    simu_choice.title("Vertebral Kinematics")
    message = tk.Label(text="Ceci est le menu de choix des méthodes")
    message.pack()

    def go_to_selected_simu():
        if type_simu.get()==0:
            ini_tracking_kin(simu_choice)


    def back_to_menu():
        menu_UI(simu_choice)

    TYPES_simu = [ ( "Tracking + Kinematics" , 0)]
    type_simu = tk.IntVar ()
    type_simu.set ( 0 )
    for text, mode in TYPES_simu:
        simu_button_choice = tk.Radiobutton (simu_choice, text = text, variable = type_simu, value = mode)
        simu_button_choice.pack ()

    message_dev = tk.Label(text="More choices are currently in development")
    message_dev.pack()


    button_select=tk.Button(simu_choice,text='Select this option',command=go_to_selected_simu)
    button_select.pack()
    button_back=tk.Button(simu_choice,text='Back to menu',command=back_to_menu)
    button_back.pack()

    simu_choice.mainloop()





def menu_infos(menu_start):
    menu_start.destroy()
    infos=tk.Tk()
    infos.geometry('1920x1080')
    infos.title("Vertebral Kinematics")
    message = tk.Label(text="Ceci est la page d'informations sur le logiciel")
    message.pack()

    def back_to_menu():
        menu_UI(infos)


    button_back=tk.Button(infos,text='Back to menu',command=back_to_menu)
    button_back.pack()
    infos.mainloop()

def menu_quit(menu_start):
    menu_start.destroy()






def ini_tracking_kin(simu_choice,nb_vertebrae=0,nb_markers=0):
    simu_choice.destroy()
    from Main import input_images_directory_path
    track_conf_menu=tk.Tk()
    track_conf_menu.geometry('1920x1080')
    track_conf_menu.title("Vertebral Kinematics")

    message = tk.Label(text="Ceci est le menu de paramétrage du tracking")
    message.pack()

    message_pictures = tk.Label(track_conf_menu,text="Number of pictures detected in input repository: "+str(count_files(input_images_directory_path))+" pictures")
    message_pictures.pack()

    message_vertebrae = tk.Label(text="Number of vertebrae:")
    message_vertebrae.pack()
    nb_vert=tk.IntVar()
    nb_vert.set(nb_vertebrae)
    vert_id=tk.Entry(track_conf_menu,textvariable=nb_vert)
    vert_id.pack()

    message_markers = tk.Label(text="Number of markers:")
    message_markers.pack()
    nb_mark=tk.IntVar()
    nb_mark.set(nb_markers)
    vert_id=tk.Entry(track_conf_menu,textvariable=nb_mark)
    vert_id.pack()

    def refresh_images():
        ini_tracking_kin(track_conf_menu,nb_vert.get(),nb_mark.get())


    def confirm_track_ini():
        confirm_menu=tk.Tk()
        confirm_menu.geometry('400x200')
        confirm_menu.title("Vertebral Kinematics")

        nb_im=count_files(input_images_directory_path)
        message_confirm_pictures = tk.Label(confirm_menu,text="Starting for: "+str(nb_im)+" pictures")
        message_confirm_pictures.pack()

        message_confirm_vert = tk.Label(confirm_menu,text="Starting for: "+str(nb_vert.get())+" vertebrae")
        message_confirm_vert.pack()

        message_confirm_mark = tk.Label(confirm_menu,text="Starting for: "+str(nb_mark.get())+" markers")
        message_confirm_mark.pack()

        message_confirm_simu = tk.Label(confirm_menu,text="Confirm?")
        message_confirm_simu.pack()

        def confirmed_start():

            def warn_kill():
                mark_vert_warn_kill(warn,confirm_menu)

            if isinstance(nb_vert.get(),int)==False or isinstance(nb_mark.get(),int)==False:
                warn=tk.Tk()
                warn.geometry('400x80')
                warn.title("Vertebral Kinematics - Warning")

                message_warn = tk.Label(warn,text="Number of vertebrae/markers must be a positive integer")
                message_warn.pack()
                button_back=tk.Button(warn,text='Back to configuration',command=warn_kill)
                button_back.pack()
                warn.mainloop()


            elif nb_vert.get()<=0 or nb_mark.get()<=0:
                warn=tk.Tk()
                warn.geometry('400x80')
                warn.title("Vertebral Kinematics - Warning")

                message_warn = tk.Label(warn,text="Number of vertebrae/markers must be a positive integer")
                message_warn.pack()
                button_back=tk.Button(warn,text='Back to configuration',command=warn_kill)
                button_back.pack()
                warn.mainloop()


            else:
                ini_starting(track_conf_menu,confirm_menu,nb_im,nb_vert.get(),nb_mark.get())



        button_select=tk.Button(confirm_menu,text='Confirm and start',command=confirmed_start)
        button_select.pack()

        button_back=tk.Button(confirm_menu,text='Back to configuration',command=confirm_menu.destroy)
        button_back.pack()

        confirm_menu.mainloop()



    def back_to_menu():
        menu_simu(track_conf_menu)



    button_refresh=tk.Button(track_conf_menu,text='Refresh',command=refresh_images)
    button_refresh.pack()

    button_select=tk.Button(track_conf_menu,text='Confirm initialization',command=confirm_track_ini)
    button_select.pack()

    button_back=tk.Button(track_conf_menu,text='Back to simulations selection menu',command=back_to_menu)
    button_back.pack()

    track_conf_menu.mainloop()




def mark_vert_warn_kill(warn,confirm_menu):
    warn.destroy()
    confirm_menu.destroy()

def ini_starting(track_conf_menu,confirm_menu,nb_im,nb_vert,nb_mark):
    confirm_menu.destroy()
    track_conf_menu.destroy()

    #start auto detec
    List_Mark_Auto=[]
    for i in range(nb_im):
        from Main import input_images_directory_path
        id_im=input_images_directory_path+str('\\')+str(i+1)+'.jpg'
        from MarkerDetector import DetectMarkers
        detected_points=DetectMarkers(id_im)
        List_Mark_Auto.append(detected_points)

    manual_add(List_Mark_Auto,nb_im,nb_vert,nb_mark)





def manual_add(List_Mark_Auto,nb_im,nb_vert,nb_mark):

    manual_mark_menu=tk.Tk()
    manual_mark_menu.geometry('1920x1080')
    manual_mark_menu.title("Vertebral Kinematics")
    message = tk.Label(manual_mark_menu,text="Ceci est la page d'informations une fois le pointage auto effectué")
    message.pack()

    message_nb_mark = tk.Label(manual_mark_menu,text="For each image, "+str(nb_mark)+" should have been detected")
    message_nb_mark.pack()
    for i in range(nb_im):
        message_nb_mark_auto = tk.Label(manual_mark_menu,text="Image ID: "+str(i+1)+" - "+str(len(List_Mark_Auto[i]))+ " over "+str(nb_mark)+" succesfully detected")
        message_nb_mark_auto.pack()


    def continue_to_verif():
        choice_verif=type_action.get()

        if choice_verif == 0:
            manual_mark_det(manual_mark_menu,List_Mark_Auto,nb_im,nb_vert,nb_mark)

        '''
        elif choice_verif == 1:
            #partial verif


        elif choice_verif == 2:
                #☻continue regardless
        '''


    message_verif = tk.Label(manual_mark_menu,text="If detected points differents from the number of markers, human verification is required (recommended with current version")
    message_verif.pack()

    TYPES_actions = [ ( "Complete Human Verification" , 0),( "Partial Human Verification (not available in current version)" , 1),( "Continue regardless (not available in current version)" , 2)]
    type_action = tk.IntVar ()
    type_action.set ( 0 )
    for text, mode in TYPES_actions:
        button_choice = tk.Radiobutton (manual_mark_menu, text = text, variable = type_action, value = mode)
        button_choice.pack ()

    message_dev = tk.Label(text="(More options are currently in development)")
    message_dev.pack()

    button_continue=tk.Button(manual_mark_menu,text='Continue with selected option',command=continue_to_verif)
    button_continue.pack()
    manual_mark_menu.mainloop()



def manual_mark_det(manual_mark_menu,List_Mark_Auto,nb_im,nb_vert,nb_mark):
    manual_mark_menu.destroy()

    from ManualMarkers import manual_markers_det

    for i in range(nb_im):
        from Main import input_images_directory_path
        id_im=input_images_directory_path+str('\\')+str(i+1)+'.jpg'
        img = cv2.imread(id_im)
        List_Mark_Auto[i]=manual_markers_det(img,nb_mark,List_Mark_Auto[i])

        while len(List_Mark_Auto[i]) != nb_mark:

            id_im=input_images_directory_path+str('\\')+str(i+1)+'.jpg'
            img = cv2.imread(id_im)
            List_Mark_Auto[i]=manual_markers_det(img,nb_mark,List_Mark_Auto[i] )

    List_Markers=List_Mark_Auto

    manual_mark_out=tk.Tk()
    manual_mark_out.geometry('1920x1080')
    manual_mark_out.title("Vertebral Kinematics")
    message = tk.Label(manual_mark_out,text="Ceci est la page d'informations une fois le pointage manu effectué")
    message.pack()

    message_nb_mark = tk.Label(manual_mark_out,text="For each image, "+str(nb_mark)+" should have been detected")
    message_nb_mark.pack()

    def back_to_manual_verif():
        return_to_manual_menu(manual_mark_out,List_Markers,nb_im,nb_vert,nb_mark)

    def continue_to_match():
        auto_match(manual_mark_out,List_Markers,nb_im,nb_vert,nb_mark)


    message_verif = tk.Label(manual_mark_out,text="If needed, return to manual selection")
    message_verif.pack()

    button_continue=tk.Button(manual_mark_out,text='Continue to Match',command=continue_to_match)
    button_continue.pack()

    button_back=tk.Button(manual_mark_out,text='Return to manual selection',command=back_to_manual_verif)
    button_back.pack()

    manual_mark_out.mainloop()

def return_to_manual_menu(manual_mark_out,List_Markers,nb_im,nb_vert,nb_mark):
    manual_mark_out.destroy()
    manual_add(List_Markers,nb_im,nb_vert,nb_mark)


def auto_match(manual_mark_out,List_Markers,nb_im,nb_vert,nb_mark):
    manual_mark_out.destroy()
    auto_match_menu=tk.Tk()
    auto_match_menu.geometry('1920x1080')
    auto_match_menu.title("Vertebral Kinematics")
    message = tk.Label(auto_match_menu,text="Ceci est la page d'informations pour le match")
    message.pack()

    message_match = tk.Label(auto_match_menu,text="Match is completly automatic")
    message_match.pack()

    def back_to_manual_verif():
        return_to_manual_menu(manual_mark_out,List_Markers,nb_im,nb_vert,nb_mark)

    def continue_to_match():
        auto_match_ini(auto_match_menu,List_Markers,nb_im,nb_vert,nb_mark)


    message_verif = tk.Label(auto_match_menu,text="If needed, return to manual selection")
    message_verif.pack()

    button_continue=tk.Button(auto_match_menu,text='Start to match',command=continue_to_match)
    button_continue.pack()

    button_back=tk.Button(auto_match_menu,text='Return to manual selection',command=back_to_manual_verif)
    button_back.pack()

    auto_match_menu.mainloop()


def auto_match_ini(auto_match_menu,List_Markers,nb_im,nb_vert,nb_mark):
    auto_match_menu.destroy()
    List_Matched_Points=[]
    Unmatched_Points=[]

    from MatchingMarkers2 import MatchPoints

    for i in range(int(len(List_Markers)/2)):
        Marks_img1=List_Markers[2*i]
        Marks_img2=List_Markers[2*i+1]
        Matched,Unmatched_two_views=MatchPoints(Marks_img1,Marks_img2)
        List_Matched_Points.append(Matched)
        Unmatched_Points.append(Unmatched_two_views)




    auto_match_finish=tk.Tk()
    auto_match_finish.geometry('1920x1080')
    auto_match_finish.title("Vertebral Kinematics")
    message = tk.Label(auto_match_finish,text="Ceci est la page d'informations une fois les matchs finis")
    message.pack()





    for i in range(int(len(List_Markers)/2)):
        message_nb_match_auto = tk.Label(auto_match_finish,text="Set of images ID: "+str(i+1)+" - "+str(len(List_Matched_Points[i]))+ "match over "+str(nb_mark)+" markers succesfully detected")
        message_nb_match_auto.pack()

    message_match = tk.Label(auto_match_finish,text="Match is Done. You can continue to Clustering.")
    message_match.pack()

    def restare_match():
        auto_match(auto_match_finish,List_Markers,nb_im,nb_vert,nb_mark)

    def continue_to_verif():
        choice_verif=type_action.get()

        if choice_verif == 0:
            manual_match(auto_match_finish,List_Matched_Points,Unmatched_Points,nb_im,nb_vert,nb_mark)


        elif choice_verif == 1:
            a=1 #not implemented
            #partial verif


    message_verif = tk.Label(auto_match_finish,text="If detected matchs are differents from the number of markers, human verification is required (recommended with current version)")
    message_verif.pack()

    TYPES_actions = [ ( "Complete Human Verification" , 0),( "Partial Human Verification (not available in current version)" , 1)]
    type_action = tk.IntVar ()
    type_action.set ( 0 )
    for text, mode in TYPES_actions:
        button_choice = tk.Radiobutton (auto_match_finish, text = text, variable = type_action, value = mode)
        button_choice.pack ()

    message_dev = tk.Label(text="(More options are currently in development)")
    message_dev.pack()

    message_verif = tk.Label(auto_match_finish,text="If needed, restart matching operations")
    message_verif.pack()

    button_continue=tk.Button(auto_match_finish,text='Continue with selected option',command=continue_to_verif)
    button_continue.pack()

    button_restart=tk.Button(auto_match_finish,text='Return matching process',command=restare_match)
    button_restart.pack()

    auto_match_finish.mainloop()




def manual_match(auto_match_finish,Matched_Points,Unmatched_Points,nb_im,nb_vert,nb_mark):
    auto_match_finish.destroy()
    List_Match_Tot=[]
    from ManualMatch import manual_match_det

    for i in range(int(nb_im/2)):
        from Main import input_images_directory_path
        img1=input_images_directory_path+str('\\')+str(2*i+1)+'.jpg'
        img2=input_images_directory_path+str('\\')+str(2*i+2)+'.jpg'
        print('im1:',img1)
        print("img2:",img2)

        Points=Matched_Points[i]
        #offset the 2nd image

        for j in range(len(Points)):
            Points[j][1][0]+=1765

        Match_Tot=manual_match_det(img1,img2,nb_mark,Points,Unmatched_Points[i])


        #take out the offset
        for j in range(len(Match_Tot)):
            Match_Tot[j][1][0]-=1765
        List_Match_Tot.append(Match_Tot)




    manual_match_out=tk.Tk()
    manual_match_out.geometry('1920x1080')
    manual_match_out.title("Vertebral Kinematics")
    message = tk.Label(manual_match_out,text="Ceci est la page d'informations une fois le match manu effectué")
    message.pack()


    def continue_to_clustering():
        auto_clustering(manual_match_out,List_Match_Tot,nb_im,nb_vert,nb_mark)


    message_verif = tk.Label(manual_match_out,text="Match is done")
    message_verif.pack()

    button_continue=tk.Button(manual_match_out,text='Continue to Clustering',command=continue_to_clustering)
    button_continue.pack()


    manual_match_out.mainloop()




def auto_clustering(manual_match_out,List_Matched_Points,nb_im,nb_vert,nb_mark):
    manual_match_out.destroy()

    auto_clust_menu=tk.Tk()
    auto_clust_menu.geometry('1920x1080')
    auto_clust_menu.title("Vertebral Kinematics")
    message = tk.Label(auto_clust_menu,text="Ceci est la page d'informations pour le clustering")
    message.pack()

    message_clust = tk.Label(auto_clust_menu,text="Clustering is completly automatic")
    message_clust.pack()

    message_clust = tk.Label(auto_clust_menu,text="The system has been set to detect "+str(nb_vert)+" vertebrae")
    message_clust.pack()


    def continue_to_clustering():
        auto_clustering_ini(auto_clust_menu,List_Matched_Points,nb_im,nb_vert,nb_mark)



    button_continue=tk.Button(auto_clust_menu,text='Start clustering',command=continue_to_clustering)
    button_continue.pack()



    auto_clust_menu.mainloop()



def auto_clustering_ini(auto_clust_menu,List_Matched_Points,nb_im,nb_vert,nb_mark):
    auto_clust_menu.destroy()
    List_Im_Clust_Unclust_Data=[]
    for i in range(len(List_Matched_Points)):
        Matched_points=List_Matched_Points[i]

        from DataManipulation import coordinateLists
        xLst,yLst,zLst,xyzLst= coordinateLists(Matched_points)

        from DataManipulation import coordinateLists
        from MatchingMarkers2 import clustering
        xClustered,yClustered,zClustered,Unclustered=clustering(xLst,yLst,zLst)
        Im=[xClustered,yClustered,zClustered,Unclustered]
        List_Im_Clust_Unclust_Data.append(Im)





    auto_clust_finish=tk.Tk()
    auto_clust_finish.geometry('1920x1080')
    auto_clust_finish.title("Vertebral Kinematics")
    message = tk.Label(auto_clust_finish,text="Ceci est la page d'informations une fois le clustering terminé")
    message.pack()
    message_clust = tk.Label(auto_clust_finish,text="Clustering is Done.")
    message_clust.pack()

    for i in range(len(List_Im_Clust_Unclust_Data)):
        message_nb_clust_auto = tk.Label(auto_clust_finish,text="Set of images ID: "+str(i+1)+" - "+str(len(List_Im_Clust_Unclust_Data[i][0]))+ "clusters over "+str(nb_vert)+" vertebrae succesfully detected")
        message_nb_clust_auto.pack()


    message_clust = tk.Label(auto_clust_finish,text="You can continue to Correlation.")
    message_clust.pack()


    def restare_clustering():
        auto_clustering(auto_clust_finish,List_Matched_Points,nb_im,nb_vert,nb_mark)


    def continue_to_verif():
        choice_verif=type_action.get()

        if choice_verif == 0:
            manual_clust_det(auto_clust_finish,List_Im_Clust_Unclust_Data,nb_im,nb_vert,nb_mark)


        elif choice_verif == 1:
            a=1 #not implemented
            #partial verif


        elif choice_verif == 2:
                a=1 #not implemented
                #☻continue regardless



    message_verif = tk.Label(auto_clust_finish,text="If detected clusters are differents from the number of vertebrae, human verification is required (recommended with current version")
    message_verif.pack()

    TYPES_actions = [ ( "Complete Human Verification" , 0),( "Partial Human Verification (not available in current version)" , 1),( "Continue regardless (not available in current version)" , 2)]
    type_action = tk.IntVar ()
    type_action.set ( 0 )
    for text, mode in TYPES_actions:
        button_choice = tk.Radiobutton (auto_clust_finish, text = text, variable = type_action, value = mode)
        button_choice.pack ()

    message_dev = tk.Label(text="(More options are currently in development)")
    message_dev.pack()

    button_continue=tk.Button(auto_clust_finish,text='Continue with selected option',command=continue_to_verif)
    button_continue.pack()


    message_verif = tk.Label(auto_clust_finish,text="If needed, restart clustering")
    message_verif.pack()

    button_restart=tk.Button(auto_clust_finish,text='Restare clustering',command=restare_clustering)
    button_restart.pack()

    auto_clust_finish.mainloop()







def manual_clust_det(auto_clust_finish,List_Clust_Auto,nb_im,nb_vert,nb_mark):
    auto_clust_finish.destroy()

    List_Im_Data=[]
    from ManualClusters import manual_clust_det

    for i in range(int(nb_im/2)):
        from Main import input_images_directory_path
        img1=input_images_directory_path+str('\\')+str(2*i+1)+'.jpg'
        img2=input_images_directory_path+str('\\')+str(2*i+2)+'.jpg'

        List_Clust_im=List_Clust_Auto[i]
        List_Im_Data.append(manual_clust_det(img1,img2,nb_vert,List_Clust_im))

    manual_clust_out=tk.Tk()
    manual_clust_out.geometry('1920x1080')
    manual_clust_out.title("Vertebral Kinematics")
    message = tk.Label(manual_clust_out,text="Ceci est la page d'informations une fois le clust manu effectué")
    message.pack()


    def continue_to_time_correlation():
        menu_correlation(manual_clust_out,List_Im_Data,nb_im,nb_vert,nb_mark)


    message_verif = tk.Label(manual_clust_out,text="Clustering is done")
    message_verif.pack()

    button_continue=tk.Button(manual_clust_out,text='Continue to time correlation',command=continue_to_time_correlation)
    button_continue.pack()


    manual_clust_out.mainloop()





def menu_correlation(auto_clust_finish,List_Im_Data,nb_im,nb_vert,nb_mark):
    auto_clust_finish.destroy()



    correlation_choice=tk.Tk()
    correlation_choice.geometry('1920x1080')
    correlation_choice.title("Vertebral Kinematics")
    message = tk.Label(correlation_choice,text="Ceci est le menu de choix de la méthode de correlation des vues t à t+1")
    message.pack()

    def go_to_selected_corre():

        if type_corre.get()==0:
          auto_corre_quentin(correlation_choice,List_Im_Data,nb_im,nb_vert,nb_mark)



    TYPES_corre = [ ( "Qentin's method" , 0),( "Djian's method (not available in current version)" , 1)]
    type_corre = tk.IntVar ()
    type_corre.set ( 0 )
    for text, mode in TYPES_corre:
        simu_button_choice = tk.Radiobutton (correlation_choice, text = text, variable = type_corre, value = mode)
        simu_button_choice.pack ()

    message_dev = tk.Label(correlation_choice,text="More options are currently in development")
    message_dev.pack()


    button_select=tk.Button(correlation_choice,text='Select this correlation method',command=go_to_selected_corre)
    button_select.pack()

    correlation_choice.mainloop()


def auto_corre_quentin(correlation_choice,List_Im_Data,nb_im,nb_vert,nb_mark):
    correlation_choice.destroy()

    auto_quent_menu=tk.Tk()
    auto_quent_menu.geometry('1920x1080')
    auto_quent_menu.title("Vertebral Kinematics")
    message = tk.Label(auto_quent_menu,text="Ceci est la page d'informations meth quentin pour corrélation")
    message.pack()

    message_corr = tk.Label(auto_quent_menu,text="Choose an set to automatic correlation")
    message_corr.pack()

    TYPES_corre = [ ( "XZ" , 0),( "YZ" , 1),("XY",2)]
    type_corre = tk.IntVar ()
    type_corre.set ( 0 )
    for text, mode in TYPES_corre:
        simu_button_choice = tk.Radiobutton (auto_quent_menu, text = text, variable = type_corre, value = mode)
        simu_button_choice.pack ()

    message_dev = tk.Label(auto_quent_menu,text="If needed, change correlation method")
    message_dev.pack()



    def continue_to_quent_corre():
        plan=''
        if type_corre.get()==0:
            plan='XZ'

        elif type_corre.get()==1:
            plan="YZ"

        elif type_corre.get()==2:
            plan="XY"



        auto_corre_quentin_ini(auto_quent_menu,List_Im_Data,nb_im,nb_vert,nb_mark,plan)

    def return_to_corre_menu():
        menu_correlation(auto_quent_menu,List_Im_Data,nb_im,nb_vert,nb_mark)

    button_continue=tk.Button(auto_quent_menu,text='Start correlation',command=continue_to_quent_corre)
    button_continue.pack()

    button_back=tk.Button(auto_quent_menu,text='Back to correaltion menu',command=return_to_corre_menu)
    button_back.pack()

    auto_quent_menu.mainloop()






def auto_corre_quentin_ini(auto_quent_menu,List_Im_Data,nb_im,nb_vert,nb_mark,plan):
    auto_quent_menu.destroy()

    from Tracking import tracking_in_time
    List_Im_correlated_Data=tracking_in_time(List_Im_Data,plan)


    auto_quent_finish=tk.Tk()
    auto_quent_finish.geometry('1920x1080')
    auto_quent_finish.title("Vertebral Kinematics")
    message = tk.Label(auto_quent_finish,text="Ceci est la page d'informations une fois la corrélation t t+1 terminée")
    message.pack()

    message_corre = tk.Label(auto_quent_finish,text="Time correlation is Done.")
    message_corre.pack()



    message_clust = tk.Label(auto_quent_finish,text="You can continue to Save/Export.")
    message_clust.pack()


    def restare_corre():
        menu_correlation(auto_quent_finish,List_Im_Data,nb_im,nb_vert,nb_mark)

    def continue_to_save():
        save_export_tracking(auto_quent_finish,List_Im_correlated_Data)


    message_verif = tk.Label(auto_quent_finish,text="If needed, restart correlation")
    message_verif.pack()

    button_continue=tk.Button(auto_quent_finish,text='Continue to Save/Export',command=continue_to_save)
    button_continue.pack()

    button_restart=tk.Button(auto_quent_finish,text='Restare clustering',command=restare_corre)
    button_restart.pack()

    auto_quent_finish.mainloop()




def save_export_tracking(time_finish,List_Im_correlated_Data):
    time_finish.destroy()

    from CSVsave import data_structure,create_csv,save_csv
    List_to_save=data_structure(List_Im_correlated_Data)
    from Main import output_csv_directory_path
    save_csv(List_to_save,output_csv_directory_path)
    init_UI()















