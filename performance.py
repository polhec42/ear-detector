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

scales = [1.05, 1.06, 1.08]
neighbors = [6, 8, 10]

#scales = [1.05]
#neighbors = [5]

pastConfigurationsFile = open("configurations.csv", "r+")
past_configurations = []

for configuration in pastConfigurationsFile.readlines():
    splittedLine = configuration.split("\t")
    past_configurations.append((splittedLine[0], splittedLine[1]))

resultFile = open("results.txt", "w")

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
                
                is_ear = False
                
                for segmented_ear in segmented_ears:
                    overlap = Rectangle.overlap(detected_ear, segmented_ear)

                    if overlap > 0:
                        if overlap > int(0.4 * segmented_ear.area()) and overlap > int(0.4*detected_ear.area()):
                            number_of_tp += 1
                            #print(i)
                            is_ear = True
                            detections["TP"] += 1
                            
                if not is_ear:
                    detections["FP"] += 1

            detections["FN"] += len(segmented_ears) - number_of_tp

        resultFile.write("scale: {}, neighbors: {} \n".format(scale, neighbor))
        resultFile.write(str(detections) + "\n")
        resultFile.write("Recall: " + str(calculate_recall()) + "\n")
        resultFile.write("Precision: " + str(calculate_precision()) + "\n")
        resultFile.write("F1 score: " + str(calculate_Fscore()) + "\n")
        resultFile.write("-------------------------------------\n")

        pastConfigurationsFile.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(scale, neighbor, detections, calculate_recall(), calculate_precision(), calculate_Fscore()))
    
resultFile.close()
pastConfigurationsFile.close()


