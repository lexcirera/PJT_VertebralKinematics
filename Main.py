import pathlib
import os as os
import tkinter as tk
import cv2

# current working directory
directory_path=pathlib.Path().absolute()
os.chdir(directory_path)



from Combine3view import *
from ComputeKinematics import *
from CSVsave import *
from DataManipulation import *
from DetectionCorrelation import *
from ManualClusters import *
from ManualMarkers import *
from ManualMatch import *
from MarkerDetector import *
from MatchingMarkers2 import *
from Tracking import *


from UI import *

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

print("Check directory_path:",directory_path)

input_images_directory_path=str(directory_path)+"\SourceImages"
output_csv_directory_path=str(directory_path)+"\csv_save"
output_images_directory_path=str(directory_path)+"\OutPutPictures"
det_marker_template=str(directory_path)+"\Template_marker.png"

print(str(input_images_directory_path))

init_UI()