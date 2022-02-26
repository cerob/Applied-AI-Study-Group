import cv2 as cv
import numpy as np


classNames = ["background", "person", "bicycle", "car", "motorcycle",
            "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
            "unknown", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
            "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "unknown", "backpack",
            "umbrella", "unknown", "unknown", "handbag", "tie", "suitcase", "frisbee", "skis",
            "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
            "surfboard", "tennis racket", "bottle", "unknown", "wine glass", "cup", "fork", "knife",
            "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
            "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "unknown", "dining table",
            "unknown", "unknown", "toilet", "unknown", "tv", "laptop", "mouse", "remote", "keyboard",
            "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "unknown",
            "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush" ] 


class Detector:
    def __init__(self):
        global cvNet, colors
        cvNet = cv.dnn.readNetFromTensorflow('myapp/model/frozen_inference_graph.pb',
                                             'myapp/model/ssd_mobilenet_v1_coco_2017_11_17.pbtxt')
        np.random.seed(543210)
        colors = np.random.uniform(0,255,size=(len(classNames),3))

    def detectObject(self, img):
        cvNet.setInput(cv.dnn.blobFromImage(cv.resize(img, (300, 300)), 0.007843, (300, 300), 130)) #input preparing
        detections = cvNet.forward() #output
        cols = img.shape[1] #input shapes
        rows = img.shape[0]

        for i in range(detections.shape[2]): # class output 
            confidence = detections[0, 0, i, 2]
            if confidence > 0.3: #threshold
                class_id = int(detections[0, 0, i, 1])

                xLeftBottom = int(detections[0, 0, i, 3] * cols)
                yLeftBottom = int(detections[0, 0, i, 4] * rows)
                xRightTop = int(detections[0, 0, i, 5] * cols)
                yRightTop = int(detections[0, 0, i, 6] * rows)

                cv.rectangle(img, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),colors[class_id], 7) 
                if class_id in range(len(classNames)): #label settling
                    label = classNames[class_id] + ": " + str(confidence)
                    labelSize, _ = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX,1.5, 4)
                    yLeftBottom = max(yLeftBottom, labelSize[1])
                    cv.putText(img, label, (xLeftBottom, yLeftBottom-30 if yLeftBottom > 60 else yLeftBottom+30),\
                                cv.FONT_HERSHEY_SIMPLEX, 1.5, colors[class_id], 5)

        return img

detector = Detector()
def detectImages(imName):
    img = cv.cvtColor(np.array(imName), cv.COLOR_BGR2RGB)
    f_img = detector.detectObject(img)
    return cv.imencode('.jpg', f_img)[1].tobytes() #encode image

def detectVideos(imName):
    cap = cv.VideoCapture(imName)
    while True:
        cv.waitKey(1)
        _,img=cap.read()
        f_img = detector.detectObject(img)
        _, buffer = cv.imencode('.jpg', f_img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')