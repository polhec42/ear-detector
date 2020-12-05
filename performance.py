from rectangle import Rectangle
from data_preprocessing import getFileName
import cv2, sys

def calculate_recall():
    try:
        recall = detections["TP"]/(detections["TP"] + detections["FN"])
        return recall
    except ZeroDivisionError:
         return 0
def calculate_precision():
    try:
        precision = detections["TP"]/(detections["TP"] + detections["FP"])
        return precision
    except ZeroDivisionError:
         return 0

def calculate_Fscore():
    try:
        F_score = 2 * ((calculate_precision() * calculate_recall())/(calculate_precision() + calculate_recall()))
        return F_score
    except ZeroDivisionError:
         return 0

def load_masks():
    result_rectangles = []

    rectangle_file = open('test_rectangles.csv', 'r')

    for image in rectangle_file.readlines():
        rectangles = []
        ears = image.split(",")
        for ear in ears:
            values = ear.split("\t")
            rectangles.append(Rectangle(int(values[0]),int(values[1]), int(values[2]), int(values[3])))
        result_rectangles.append(rectangles)

    rectangle_file.close()

    return result_rectangles

def detectEar(img, scale, min_neighbours):
	detectionList = cascadeEar.detectMultiScale(img, scale, min_neighbours)
	return detectionList

cascadeEar = cv2.CascadeClassifier("classifier/cascade.xml")
testImagesDirectory = "AWEForSegmentation/test/"

scales = [1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07, 1.08, 1.1]
neighbors = [2, 4, 6, 8, 10, 12]

#scales = [1.05]
#neighbors = [5]

pastConfigurationsFile = open("configurations.csv", "r+")
past_configurations = []

firstLine = True

for configuration in pastConfigurationsFile.readlines():
    if firstLine:
        firstLine = False
        continue
    splittedLine = configuration.split("\t")
    past_configurations.append((splittedLine[0], splittedLine[1]))

mask_rectangles = load_masks()

for scale in scales:
    for neighbor in neighbors:
        
        already_run = False

        for past_configuration in past_configurations:
            if float(past_configuration[0]) == scale and float(past_configuration[1]) == neighbor:
                already_run = True
                break
        
        if already_run:
            continue

        detections = {"TP": 0, "FP": 0, "FN": 0}

        for i in range(0,250):
            print(scale, neighbor, i)
            imageName = testImagesDirectory + getFileName(i)
            image = cv2.imread(imageName)

            segmented_ears = mask_rectangles[i]
            detected_ears = []

            detectionList = detectEar(image, scale, neighbor)
            for x,y,w,h in detectionList:
                detected_ears.append(Rectangle(x,y,w,h))

            number_of_tp = 0
            for detected_ear in detected_ears:

                was_classified = False

                for segmented_ear in segmented_ears:
                    
                    overlap = Rectangle.overlap(detected_ear, segmented_ear)

                    if overlap > int(0.42 * (segmented_ear.area() + detected_ear.area() - overlap)):
                        number_of_tp += 1
                        was_classified = True
                        detections["TP"] += 1
                        break
                    elif overlap > 0:
                        was_classified = True
                        detections["FP"] += 1  
                        break    

                if not was_classified:
                    detections["FP"] += 1

            detections["FN"] += len(segmented_ears) - number_of_tp

        pastConfigurationsFile.write("{},{},{},{},{},{}\n".format(scale, neighbor, detections, calculate_recall(), calculate_precision(), calculate_Fscore()))
    
pastConfigurationsFile.close()


