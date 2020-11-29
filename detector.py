from data_preprocessing import findRectangles
from rectangle import Rectangle
import cv2, sys

cascadeEar = cv2.CascadeClassifier("classifier/cascade.xml")

def showImage (image):
    cv2.imshow('sth', image)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()  

def detectEar(img):
	detectionList = cascadeEar.detectMultiScale(img, 1.01, 10)
	return detectionList
	
def vizualization(img, detectionList):
	for x, y, w, h in detectionList:
		cv2.rectangle(img, (x,y), (x+w, y+h), (128, 255, 0), 4)
	showImage(img)
	
def manually_classify(detections, file_name):
	mask_name = file_name.replace("test", "testannot_rect")
	mask = cv2.imread(mask_name)
	rectangles = findRectangles(mask)
	


	for x, y, w, h in detections:
		rec = Rectangle(x,y,w,h)
		for rectangle in rectangles:
			overlap = Rectangle.overlap(rec, rectangle)
			print(rec, overlap)
			if overlap > int(0.4 * rectangle.area()) and overlap > int(0.4*rec.area()):
				print("TP")
			print("")

	vizualization(cv2.imread(file_name), detections)

if __name__ == "__main__":
	
	filename = sys.argv[1]

	if len(sys.argv) == 2:
		img = cv2.imread(filename)
		detectionList = detectEar(img)
		vizualization(img, detectionList) 	
	else:
		if sys.argv[2] == '-classify':
			img = cv2.imread(filename)
			detectionList = detectEar(img)
			manually_classify(detectionList, filename)