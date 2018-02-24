import sys
import time
import os
import numpy as np
import cv2
import inspect

def detect_face(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

	faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(150, 150),
    )

	if (len(faces) == 0):
		return None, None

	(x, y, w, h) = faces[0]

	return gray[y:y+w, x:x+h], faces[0]

def prepare_training_data(data_folder_path):
	dirs = os.listdir(data_folder_path)
	 
	faces = []
	labels = []
	 
	for dir_name in dirs:
	 
		if not dir_name.startswith("s"):
			continue;
	 
		label = int(dir_name.replace("s", ""))
		 
		subject_dir_path = data_folder_path + "/" + dir_name
		 
		subject_images_names = os.listdir(subject_dir_path)
		 
		for image_name in subject_images_names:
		 
			if image_name.startswith("."):
				continue;
		 
			image_path = subject_dir_path + "/" + image_name

			image = cv2.imread(image_path)
			 
			face, rect = detect_face(image)
			 
			if face is not None:
				faces.append(face)
				labels.append(label)
		 
	cv2.destroyAllWindows()
	cv2.waitKey(1)
	cv2.destroyAllWindows()
	 
	return faces, labels

def draw_rectangle(img, rect):
	(x, y, w, h) = rect
	cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
 
def draw_text(img, text, x, y):
	cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def predict(test_img):
	img = test_img.copy()
	face, rect = detect_face(img)

	label= face_recognizer.predict(face)
	label = label[0]
	label_text = subjects[label]
	 
	draw_rectangle(img, rect)
	draw_text(img, label_text, rect[0], rect[1]-5)
	 
	return label_text
	
def recognize():
	video_capture = cv2.VideoCapture(0)
	cascPath = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)

	noFace = True
	while noFace:
	    ret, frame = video_capture.read()
	
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	    faces = faceCascade.detectMultiScale(
	        gray,
	        scaleFactor=1.2,
	        minNeighbors=5,
	        minSize=(50, 50),
	    )

	    for (x, y, w, h) in faces:
	        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	       	cv2.imwrite("test.jpg", frame)
	       	noFace = False

	    cv2.imshow('Video', frame)

	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	video_capture.release()
	cv2.destroyAllWindows()

	test = cv2.imread("test.jpg")

	predicted_test = predict(test)

	print(predicted_test)
	return (predicted_test)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def initialization():
	global subjects
	subjects = ["", "s1", "s2"]

	global faces, labels
	faces, labels = prepare_training_data("training-data")
	
	global face_recognizer
	face_recognizer = cv2.createLBPHFaceRecognizer()
	
	face_recognizer.train(faces, np.array(labels))


