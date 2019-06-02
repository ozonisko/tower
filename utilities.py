import config as c
import math
from PIL import Image
from numpy import ones, vstack
from numpy.linalg import lstsq

def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

def convertToCanvasCoord(coordinate):
    canvasCoordinate = coordinate * c.kratka + c.kratka // 2
    return canvasCoordinate

def RBGAImage(imagePath):
    return Image.open(imagePath).convert("RGBA")

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
