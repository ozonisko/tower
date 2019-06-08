import config as c
import math
from PIL import Image, ImageTk, ImageDraw
from numpy import ones, vstack
from numpy.linalg import lstsq


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

def convertToCanvasCoord(coordinate):
    canvasCoordinate = coordinate * c.kratka + c.kratka // 2
    return canvasCoordinate

def RGBAImage(imagePath):
    return Image.open(imagePath).convert("RGBA")

def RGBAImageTk(image):
    return ImageTk.PhotoImage(image)

def createCircle(image):
    imageCopy = image.copy()
    w, h = image.size
    x = int(w/2)
    y = int(h/2)

    draw = ImageDraw.Draw(imageCopy)
    draw.ellipse((0, 0, 2*x, 2*y), outline=(25, 186, 181, 255))
    draw.ellipse((1, 1, 2 * x - 1, 2 * y - 1), outline=(10, 186, 181, 255))

    return imageCopy

def findLineIncludingTwoPoints(x1, y1, x2, y2):
    points = [(x1, y1), (x2, y2)]
    x_coords, y_coords = zip(*points)
    A = vstack([x_coords,ones(len(x_coords))]).T
    a, b = lstsq(A, y_coords)[0]
    return a, b

def linearFunction(a, b, x):
    y = a*x + b
    return y

def generateValuesInBetween(start, stop, step):
    values = []
    inverseNeeded = start > stop

    start_ = int(start)
    stop_ = int(stop)

    if inverseNeeded:
        start_, stop_ = stop_, start_

    for value in range(start_ + step, stop_, step):
        values.append(value)

    if inverseNeeded:
        values = values[::-1]

    return values
