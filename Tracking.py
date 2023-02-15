import cv2

def tracking_in_time(L, plan, tol_alt=20):

    """
    Objectif :
        Faire le tracking de chaque coordonnées de point (x,y,z) de t à t+1 en labellisant les éléments de la liste en entrée.

    Entrée :
        L : liste de tous les points (x,y,z) détectés, matchés et clusterisés de toutes les images. type = list
        plan : plan d'étude / mouvement de la colonne ('XY', 'XZ' ou 'YZ'). type = str
        tol_alt : tolérance de déplacement d'un point dans la direction ortogonale au plan d'étude en pixel. type = int (exemple : si mouvement dans le plan 'XZ', tol_alt est la valeur de déplacement sur y d'une bille entre t et t+1.)

    Sortie :
        L : liste de tous les points (x,y,z) détectés, matchés, clusterisés et labellisés de toutes les images. type = list
    """

# définition du repère de travail

    vect1 = None
    vect2 = None

    if plan == 'XZ'or plan == 'ZX':
        vect1 = 0
        vect2 = 2
        vect_alt = 1

    elif plan == 'YZ' or plan == 'ZY':
        vect1 = 1
        vect2 = 2
        vect_alt = 0

    elif plan == 'XY' or plan == 'YX' :
        vect1 = 0
        vect2 = 1
        vect_alt = 2

# création de la liste rep, que l'on manipulera pour une recherche facilitée d'indices

    # on part d'une liste : L -> Im1,Im2,...,Imn dont Im1 -> X, Y, Z dont X_cluster -> clusterx_1, clusterx_2,..,clusterx_p dont clusterx_1 -> (x_bille1, x_bille2,...,x_bille_m)
    # on crée une liste : rep -> Im1,Im2,...,Imn dont Im1 -> cluster1, cluster2,...,clusterp dont cluster1 -> (point_cluster1_1, point_cluster1_2,...,point_cluster1_m) dont point_cluster1_1 -> (x_cluster1_1, y_cluster1_1, z_cluster1_1)

    rep = []

    for i in range (0,len(L)) :
        'i parcourt toutes les images dans la liste. Im1 , Im2, ... , Imn'

        L_j = []
        for j in range(0, len(L[i][0])) :
            'j parcourt les listes X, Y, Z'
            L_k = []

            for k in range (0, len(L[i][0][j])) :
                'k parcours toutes les coordonnées d un point dans un cluster'
                L_k.append([L[i][0][j][k], L[i][1][j][k], L[i][2][j][k]])

            L_j.append(L_k)

        rep.append(L_j)

#recherche des points de corrélations pour tous les points des tous les clusters

    # sol est la copie de rep et sera la liste dont les points corrélés seront manipulés afin de les ordonner.
    # Dans les fait, pour prenant un point i à t, on souhaite trouver sa position à t+1. Le point à t+1 correspondant se trouve à la position j dans rep. Donc, on place ce point à la position i dans sol.
    sol = rep.copy()

    # on étudie image par image. avant de corréler t+1 et t+2, on commence par t et t+1.
    for image in range(1, len(rep)) :

        cor = []

        # on corrèle les points en etudiant uniquement les cluster, car de t à t+1, le nombre de points par cluster reste le même car le contenu des clusters au cours du temps reste identique.
        for cluster in range(0,len(sol[image-1])) :
            """on parcourt les différents clusters"""
            ind=[]
            for points in range(0, len(sol[image-1][cluster])):
                """il faut trouver le point correspondant dans l'autre image avec le point que l'on a"""
                L_dist =[]
                L_dx = []
                L_dy = []

                L_delta_altitude = []

                # pour déterminer quel point à t+1 correspond à celui que l'on étudie à t, on compare les distances du point t à tous les points à t+1. Le candidat retenu est celui dont l'altitude (cf. explication tol_alt en intro) est la plus faible et dont la distance est la plus faible
                for i in range(0, len(sol[image][cluster])):
                    dx = sol[image][cluster][i][vect1]-sol[image-1][cluster][points][vect1]
                    L_dx.append(dx)

                    dy = sol[image][cluster][i][vect2]-sol[image-1][cluster][points][vect2]
                    L_dy.append(dy)

                    dist = (dx**2+dy**2)**0.5
                    L_dist.append(dist)

                    dz = abs(sol[image][cluster][i][vect_alt]-sol[image-1][cluster][points][vect_alt])
                    L_delta_altitude.append(dz)

                'On associe le point de l image 1 au point correspondant de l image 2'

                'position du candidat'
                for i in range (0, len(L_dist)) :

                    if L_dist[i] == min(L_dist):
                        c=0
                        b=0
                        v = i
                        delta_z = abs(sol[image][cluster][v][vect_alt] - sol[image-1][cluster][points][vect_alt])
                        while delta_z - min(L_delta_altitude) > tol_alt :
                            L_dist[i] = 10000
                            minimum = min(L_delta_altitude)
                            v = L_delta_altitude.index(minimum)
                            delta_z = abs(sol[image][cluster][v][vect_alt] - sol[image-1][cluster][points][vect_alt])
                        if v not in ind :
                            ind.append(v)

            cor.append(ind)

# modification de la liste sol

        #on modifie la position des points corrélés afin de labelliser sol.
        solution_image = []
        for cluster2 in range(0,len(rep[image-1])) :
            solution_image_inter = []
            for indice in range(0, len(cor[cluster2])):

                b = rep[image][cluster2][cor[cluster2][indice]]

                solution_image_inter.append(b)

            solution_image.append(solution_image_inter)
        sol[image] = solution_image.copy()

# transformer la liste sol en une liste de forme identique à celle d'entrée


    # on transforme la liste sol dans un format identique à celui de la liste d'entrée.
    ext = []

    for image in range (0,len(sol)) :
        'image parcourt toutes les images de sol. Im1 , Im2, ... , Imn'

        ext_X = []
        ext_Y = []
        ext_Z = []

        for cluster in range(0, len(sol[image])) :
            'cluster parcourt les cluster de sol parmi une image donnée'
            ext_clust_x = []
            ext_clust_y = []
            ext_clust_z = []

            for points in range (0, len(sol[image][cluster])) :
                'points parcourt tous les (x,y,z) dans un cluster donnée dans une image donnée'

                ext_clust_x.append(sol[image][cluster][points][0])
                ext_clust_y.append(sol[image][cluster][points][1])
                ext_clust_z.append(sol[image][cluster][points][2])


            ext_X.append(ext_clust_x)
            ext_Y.append(ext_clust_y)
            ext_Z.append(ext_clust_z)

        ext.append([ext_X, ext_Y, ext_Z])

    return(ext)









