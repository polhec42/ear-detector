from data_preprocessing import findRectangles, getFileName
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

def save_image(img, name, detectionList):
	for x, y, w, h in detectionList:
		cv2.rectangle(img, (x,y), (x+w, y+h), (128, 255, 0), 4)
	cv2.imwrite(name, img)
	
def classify(detections, file_name, mode):
	mask_name = file_name.replace("test", "testannot_rect")
	mask = cv2.imread(mask_name)
	rectangles = findRectangles(mask)
	
	tps = 0
	fps = 0
	tns = 0

	for x, y, w, h in detections:
		rec = Rectangle(x,y,w,h)
		was_classified = False
		for rectangle in rectangles:
			overlap = Rectangle.overlap(rec, rectangle)
			if overlap > int(0.42 * (rec.area() + rectangle.area() - overlap)):
				tps += 1
				was_classified = True
			elif overlap > 0:
				fps += 1
				was_classified = True
		if not was_classified:
			fps += 1
	tns += len(rectangles) - tps

	if mode == 'manually':
		vizualization(cv2.imread(file_name), detections)
	else:
		save_image(cv2.imread(file_name), "classifier/evaluation/" + file_name[-8:], detections)
		results.write("TP: {}\tFP:{}\tTN:{}\n".format(tps, fps, tns))

if __name__ == "__main__":
	
	filename = sys.argv[1]

	if len(sys.argv) == 2:
		img = cv2.imread(filename)
		detectionList = detectEar(img)
		vizualization(img, detectionList) 	
	else:
		if sys.argv[2] == '--classify':
			img = cv2.imread(filename)
			detectionList = detectEar(img)
			classify(detectionList, filename, 'manually')
		if sys.argv[2] == '--classify-all':
			results = open("classifier/evaluation/results.csv", "w")
			for i in range(0, 250):
				img = cv2.imread(filename + "/" + getFileName(i))
				detectionList = detectEar(img)
				results.write(str(i) + ": ")
				classify(detectionList, filename + "/" + getFileName(i), 'auto')
			results.close()