import cv2
import math

"""
this code works but still has bugs to fix - use at your own risk
assumes starting marking point is from the angle we want to meassure
"""

imagePath = "img_wide_lens_close/3.JPG"
coordinates = []
img = cv2.imread(imagePath)

"""
scale image if needed
"""
scale_percent = 40 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
# resized image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)


"""
passing event witch is a mouse click
x and y are the coordinates of the mouse click 
"""
def mousePoints(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # draw a circle at the coordinates of the click
        listSize = len(coordinates)
        if listSize != 0 and listSize % 3 != 0:
            cv2.line(resized, tuple(coordinates[round(((listSize-1)/3))*3]), (x,y),(0,0,255),2)
        cv2.circle(resized, (x, y), 5, (0, 0, 255), cv2.FILLED)
        coordinates.append([x, y])
        print(coordinates)
        #print(x, y)

"""
calc gradient
"""
def gradient(point1, point2):
    return (point2[1] - point1[1]) / (point2[0] - point1[0])

"""
get angle for coordinates
"""
def getAngle(coordinates):
    p1, p2, p3 = coordinates[-3:]
    n1 = gradient(p1, p2)
    n2 = gradient(p1, p3)
    angleR = math.atan((n2 - n1) / (1 + (n2 * n1))) # value in radians
    angleD = round(math.degrees(angleR))  # value in degrees
    cv2.putText(resized, str(angleD), (p1[0]-40, p1[1]-40), 
                cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 2)
    #print(angleD)


"""
Main loop
"""
while True:
    # calculate the angle every time the list of coordinated has 3 elements
    if len(coordinates) % 3 == 0 and len(coordinates) != 0:
        getAngle(coordinates)

    cv2.imshow("Image", resized)
    # on mouse call back run the mousePoints function
    cv2.setMouseCallback("Image", mousePoints)
    # clear the screen
    if cv2.waitKey(1) & 0xFF == ord('q'):
        coordinates = []
        img = cv2.imread(imagePath)




