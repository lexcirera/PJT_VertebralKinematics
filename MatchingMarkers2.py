import PIL.Image
from PIL import Image, ImageEnhance
import numpy as np
from sklearn.cluster import DBSCAN
from pylab import *
import copy

def IndicePoint(pointofInterest, lst):
    for i in range(len(lst)):
        if pointofInterest == lst[i]:
            return i


def MatchPoints(pts1, pts2, Threshold=18):
    Points1 = copy.copy(pts1)
    Points2 = copy.copy(pts2)

    MatchedPoints = []
    UnMatchedPoints1 = []
    UnMatchedPoints2 = []
    Unmatched=[]

    while len(Points1) != 0 and len(Points2) != 0:
        PointOfInterest = Points1.pop(0)
        MatchingPointCandidates = []

        for i in range(len(Points2)):
            if np.abs(Points2[i][1] - PointOfInterest[1]) < Threshold:
                MatchingPointCandidates.append(Points2[i])

        if len(MatchingPointCandidates) == 0:

            UnMatchedPoints1.append(PointOfInterest)
        elif len(MatchingPointCandidates) > 1:
            # on prend le plus proche
            distances = [np.abs(PointOfInterest[1] - MatchingPointCandidates[i][1]) for i in
                         range(len(MatchingPointCandidates))]
            minpos = distances.index(min(distances))
            MatchingPointCandidates = MatchingPointCandidates[minpos]
            MatchedPoints.append([PointOfInterest, MatchingPointCandidates])
            Points2.pop(IndicePoint(MatchingPointCandidates, Points2))
        else:  # single succeful point
            MatchedPoints.append([PointOfInterest, MatchingPointCandidates[0]])
            Points2.pop(IndicePoint(MatchingPointCandidates[0], Points2))
    UnMatchedPoints2.append(Points2)


    if len(UnMatchedPoints1)!=0:
        for i in range(len(UnMatchedPoints1)):
            print("dans 1",UnMatchedPoints1[i])
            Unmatched.append(UnMatchedPoints1[i])

    if len(UnMatchedPoints2)>0:
        for i in range(len(UnMatchedPoints2)):
            Unmatch_point=UnMatchedPoints2[i]
            if len(Unmatch_point)> 0:
                Unmatched.append(Unmatch_point[0])
    return MatchedPoints,Unmatched



def clustering(x,y,z, threshold =95):
    """
    clusters the markers to identify each vertebra, clustering in two times: #1 bruteforce clustering
    using Density Based Spatial clustering Application with Noise (DBSCAN), #2 cluster the remaining points
    by matching their Z coordinate with the average Z coordinate of the previously identified clusters.
    :param x: list of X coordinates, format [x1,x2,...]
    :param y: list of Y coordinates, format [y1,y2,...]
    :param z: list of Z coordinates, format [z1,z2,...]
    :param threshold: !!! WARNING !!! to adjust according to the density of the points to cluster
    :return: t-uple of clustered points, format [[x1_cluster1,x2_cluster1],...,[x1_cluster2,x2_cluster2]]
    """
    #clustering using DBSCAN
    X = [[y[i],z[i]]for i in range(len(y))]
    db = DBSCAN(eps=120, min_samples=3).fit(X)
    labels = db.labels_
    cluster_speration = list(db.labels_) # label "-1" is for noisy unclustered points, clusters are numbered by an int number starting at 0

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    # creates final lists of clustered points, number of elements in Xclusters dependant on the amount of detected clusters
    Xclusters = [[] for i in range(n_clusters_)]
    Yclusters = [[] for i in range(n_clusters_)]
    Zclusters = [[] for i in range(n_clusters_)]
    # creates lists of unclustered pointed ( noisy point identified by the label "-1")
    Xunclustered = []
    Yunclustered = []
    Zunclustered = []

    #building the lists of succesfully clustered points:
    for i in range(len(cluster_speration)):
        for j in range(n_clusters_):
            if cluster_speration[i] == j:
                Xclusters[j].append(x[i])
                Yclusters[j].append(y[i])
                Zclusters[j].append(z[i])
        if cluster_speration[i] == -1: #unclusered
            Xunclustered.append(x[i])
            Yunclustered.append(y[i])
            Zunclustered.append(z[i])

    #dealing with the unclsutered points

    Xreclustered =[]
    Yreclustered = []
    Zreclustered = []

    for i in range(len(Zclusters)):
        AverageZ = np.average(Zclusters[i])

        for j in range(len(Zunclustered)):
            if np.abs(AverageZ-Zunclustered[j]) < threshold:
                Zclusters[i].append(Zunclustered[j])
                Yclusters[i].append(Yunclustered[j])
                Xclusters[i].append(Xunclustered[j])
                Xreclustered.append(Xunclustered[j])
                Yreclustered.append(Xunclustered[j])
                Zreclustered.append(Xunclustered[j])

    for i in range(len(Xreclustered)):
        if Xunclustered.count(Xreclustered[i]) != 0:
            Zunclustered.pop(Xunclustered.index(Xreclustered[i]))
            Yunclustered.pop(Xunclustered.index(Xreclustered[i]))
            Xunclustered.pop(Xunclustered.index(Xreclustered[i]))

    unclustered =[[Xunclustered[i],Yunclustered[i],Zunclustered[i]] for i in range(len(Zunclustered))]
    '''
    if len(unclustered) != 0:
        print("\n failed to cluster all points, please proceed Manually")
        print("unclesutered z:")
        print(unclustered)
    else:
        print("clustered successfully all points \n")
    '''

    return Xclusters,Yclusters,Zclusters,unclustered