import cv2, sys
import math
import numpy as np
from rectangle import Rectangle

imageDirectory = sys.argv[1]
masksDirectory = sys.argv[2]

def getFileName(number):
    zeros = ""
    zeros += (3 - int(math.log10(number+1))) * "0"
    zeros += str(number+1)
    return zeros + ".png"

def showImage (image):
    cv2.imshow('sth', image)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()  

def findRectangles(image):

    height = image.shape[0]
    width = image.shape[1]

    rectangles = []

    for i in range(0, height):
        for j in range(0, width):

            if np.sum(image[i,j]) != 0 and not (Rectangle.is_in_rectangles(rectangles, j, i)):

                h = i
                w = j

                while h < height and np.sum(image[h,j]) != 0:
                    h += 1
                while w < width and np.sum(image[i,w]) != 0:
                    w += 1

                rectangles.append(Rectangle(j, i, w-1-j, h-1-i))

    return rectangles


def createInfoFile(imageDirectory, masksDirectory, numberOfImages, fileName):

    file = open(fileName, "w")

    for i in range(0, numberOfImages+1):
        print(i)
        originalImage = imageDirectory + "/" + getFileName(i)
        maskedImage = masksDirectory + "/" + getFileName(i)
        mask = cv2.imread(maskedImage)
        
        rectangles = findRectangles(mask)

        #for rec in rectangles:
        #    mask[rec.y, rec.x] = [0,0,255]

        #showImage(mask)

        file.write(originalImage + " " + str(len(rectangles)) + " " + "\t".join(map(str, rectangles)) + "\n")

    file.close()

# maskedImage = img * maskedImage
createInfoFile(imageDirectory, masksDirectory, 750, "ears.info")

