
def coordinateLists(lstMatchedPoints):
    #building 3 lists of the x,y,z coordinates
    Z_Coordinates = []
    Y_Coordinates = []
    X_Coordinates = []
    for i in range(len(lstMatchedPoints)):
        X_Coordinates.append(lstMatchedPoints[i][0][0])
        Y_Coordinates.append(lstMatchedPoints[i][1][0])
        Z_Coordinates.append(lstMatchedPoints[i][0][1])

    threeUpleCoordinate = []
    for i in range(len(lstMatchedPoints)):
        threeUpleCoordinate.append([lstMatchedPoints[i][0][0],lstMatchedPoints[i][1][0],lstMatchedPoints[i][0][1]])
    return X_Coordinates,Y_Coordinates,Z_Coordinates,threeUpleCoordinate
