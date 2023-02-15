import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import glob
from os import walk


def Marker_Detector_Correlation(image):

    """
    Objectif :
        détecter les coordonnées des billes dans une image

    Entrée:
        fichier image au format png

    Sortie :
        Liste de points (x,y) permettant de localiser toutes les billes détectées.

    """

    #attention de bien placer le template dans un endroit qui n'est pas modifié car le template est fixe
    template_image = '#####Change Path####/Template_Bille/Template_bille.png'


    #création de la liste à retourner en sortie
    points = []
    k=0

    #on parcourt tous les fichiers image du dossier à traiter
    for arbre_image in glob.glob(arbre_dossier) :

        #on importe les images que dont on souhaite faire la détection de points
        img_rgb = cv2.imread(arbre_image)

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        # on importe le template de bille
        template = cv2.imread(template_image,0)
        w, h = template.shape[::-1]

        # en utilisant cv2.matchTemplate, on fait parcourir le template sur tous les pixels de l'image importée et on test si on trouve une bille.
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)

        # valeur de threshold à modifier au besoin
        # plus threshold est petit, plus il est susceptible de prendre des points non désirés (threshold petit -> beaucoup de points détectés)
        # threshold = 0.8 permet un bon compromis de détection, peu de faux négatifs et peu de faux positifs.
        threshold = 0.8

        loc = np.where( res >= threshold)

        # Dans res, il peut y avoir des redondances de détection des billes, ainsi on crée une liste points_images dans laquelle on ajoutera tous les points détectés en assurant l'absence de doublons.
        points_images = []

        #i agit comme compteur pour la boucle itérative ci-dessous
        i =0

        it_pr = []
        for pt in zip(*loc[::-1]):

            #la condition if sert à eliminer les redondances de rectangle. En effet, sans ce if, plusieurs rectangles se créeraient au même endroit a quelques pixels près
            if i == 0 :
                #le premier point se met directement dedans car ne peut pas être comparé à d'autres points précédents
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

                #on calcule le centre du rectangle
                rectx, recty = ((2*pt[0]+w)/2,(2*pt[1]+h)/2)
                rectcenter = int(rectx), int(recty)
                i+=1

                # on rajoute le centre du rectangle dans la liste points_images car ces coordonnées seront les données que nous traiterons par la suite
                points_images.append([rectcenter[1],rectcenter[0]])

            # la redondance des points se fait à cause de matchTemplate qui, pour la même bille, trouve deux points écartés d'1 pixel sur x et/ou 1 pixel sur y.
            elif pt[0]- it_pr[0] > 1 or pt[1]- it_pr[1] > 1 :
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
                rectx, recty = ((2*pt[0]+w)/2,(2*pt[1]+h)/2)
                rectcenter = int(rectx), int(recty)
                i+=1
                points_images.append([rectcenter[1],rectcenter[0]])
            else :
                i+=1

            #on garde en mémoire le point pt pour pouvoir le comparer à l'itération suivante au point suivante de zip
            it_pr = pt

            #on affiche le ppint sur l'image
            img_rgb[rectcenter[1],rectcenter[0]]=[0,0,255]

        points.append(points_images)

        #on crée une image 'res' qui affiche les rectangles de détection de billes ainsi que le centre de ces rectangles qui correspondent au centre des billes, i.e. les coordonnées (x,y) que l'on souhaite retourner.
        cv2.imwrite('#####Write the path of the image to write####',img_rgb)
        cv2.imshow('test', img_rgb)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return points


"""
performances du code :
 sur image test1 : 20 billes à détecter : 19 points détectés dont 2 faux négatifs et 1 faux positif -> 95%
 sur image test 2 : 20 billes à détecter : 16 points détectés dont 4 faux négatifs -> 80%
"""
