import cv2
import urllib.request 
import numpy as np

url = 'http://172.20.10.4/cam-hi.jpg'
winNameCamera = 'ESP32 CAMERA'
winNameCounter = 'Person Counter'

cv2.namedWindow(winNameCamera, cv2.WINDOW_NORMAL)  # Create a resizable camera window
cv2.namedWindow(winNameCounter, cv2.WINDOW_NORMAL)  # Create a resizable counter window

classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

personCount = 0

while True:
    imgResponse = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)

    classIds, confs, bbox = net.detect(img, confThreshold=0.5)

    # Draw bounding boxes around detected objects
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color=(0, 255, 0), thickness=3)
            cv2.putText(img, classNames[classId - 1], (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Count the number of person detections
            if classNames[classId - 1] == 'person':
                personCount += 1

    # Display the camera feed
    cv2.imshow(winNameCamera, img)

    # Display the person count
    counterImg = np.zeros((100, 300, 3), dtype=np.uint8)
    cv2.putText(counterImg, f'Persons: {personCount}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow(winNameCounter, counterImg)

    # Reset the person count for the next frame
    personCount = 0

    key = cv2.waitKey(5) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()
