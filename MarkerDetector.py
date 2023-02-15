import cv2

def DetectMarkers(imageThresholded):

    image1 = cv2.imread(imageThresholded)

    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 33;  # Change thresholds
    params.maxThreshold = 199;
    params.filterByArea = True  # Filter by Area.
    params.minArea = 30
    params.maxArea = 3000
    params.filterByCircularity = True  # Filter by Circularity
    params.minCircularity = 0.7
    params.maxCircularity = 1
    params.filterByConvexity = True  # Filter by Convexity
    params.minConvexity = 0.9
    params.maxConvexity = 2
    params.filterByInertia = True  # Filter by Inertia
    params.minInertiaRatio = 0.5
    params.maxInertiaRatio = 1
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(image1)
    points = []
    for point in keypoints:
        points.append([int(point.pt[0]),int(point.pt[1])])

    return points