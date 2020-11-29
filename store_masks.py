from data_preprocessing import getFileName, findRectangles
import cv2, sys

def rectangles_of_masks(directory, s, e):

    rectangles = []
    for i in range(s,e):
        print(i)
        maskedName = directory + getFileName(i)
        mask = cv2.imread(maskedName)

        rectangles.append(findRectangles(mask))

    rectangle_file = open("test_rectangles.csv", "w")

    for image in rectangles:
        for i in range(len(image)):
            if i > 0:
                rectangle_file.write(",")
            rectangle_file.write("{}\t{}\t{}\t{}".format(image[i].x, image[i].y, image[i].width, image[i].height))
        rectangle_file.write("\n")

    rectangle_file.close()

testMasksDirectory = "AWEForSegmentation/testannot_rect/"
rectangles_of_masks(testMasksDirectory, 0, 250) 