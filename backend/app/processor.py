import cv2
from tracker import *


class RailwayTrack:
    def __init__(self, id, entry_tracker, exit_tracker, entry_detector, exit_detector, entry_y1, entry_y2, entry_x1, entry_x2, exit_y1, exit_y2, exit_x1, exit_x2, callback=None):
        self.id = id

        self.entry_tracker = entry_tracker
        self.exit_tracker = exit_tracker

        self.entry_detector = entry_detector
        self.exit_detector = exit_detector

        self.entry_y1 = entry_y1
        self.entry_y2 = entry_y2

        self.entry_x1 = entry_x1
        self.entry_x2 = entry_x2

        self.exit_y1 = exit_y1
        self.exit_y2 = exit_y2

        self.exit_x1 = exit_x1
        self.exit_x2 = exit_x2

        self.entry_status = True
        self.exit_status = True

        self.entry_true_count = 0
        self.entry_false_count = 0

        self.exit_true_count = 0
        self.exit_false_count = 0

        self.is_free = True
        self.count = 0
        self.callback = callback

    def detect_entry_roi(self, roi):
        mask = self.entry_detector.apply(roi)

        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        detections = []

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:
                x, y, w, h = cv2.boundingRect(contour)
                detections.append([x, y, w, h])

        boxes = self.entry_tracker.update(detections)

        return boxes

    def detect_exit_roi(self, roi):
        mask = self.exit_detector.apply(roi)

        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        detections = []

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:
                x, y, w, h = cv2.boundingRect(contour)
                detections.append([x, y, w, h])

        boxes = self.exit_tracker.update(detections)

        return boxes

    def show_frame(self, frame):
        entry_roi = frame[self.entry_y1:self.entry_y2, self.entry_x1:self.entry_x2]
        exit_roi = frame[self.exit_y1:self.exit_y2, self.exit_x1:self.exit_x2]

        entry_roi_boxes = self.detect_entry_roi(entry_roi)
        exit_roi_boxes = self.detect_exit_roi(exit_roi)

        if entry_roi_boxes and self.entry_status:
            self.entry_false_count = 0
            self.entry_true_count += 1
            if self.entry_true_count > 100:
                self.entry_status = False
                self.is_free = False
                if self.callback:
                        self.callback(self.id, 'free')

        if not entry_roi_boxes and not self.entry_status:
            self.entry_true_count = 0
            self.entry_false_count += 1
            if self.entry_false_count > 100:
                self.entry_status = True
                self.count += 1
                if not self.is_free and self.count == 2:
                    self.is_free = True
                    self.count = 0
                    if self.callback:
                        self.callback(self.id, 'free')

        for box in entry_roi_boxes:
            x, y, w, h, id = box
            cv2.putText(entry_roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(entry_roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if exit_roi_boxes and self.exit_status:
            self.exit_false_count = 0
            self.exit_true_count += 1
            if self.exit_true_count > 100:
                self.exit_status = False
                self.is_free = False
                if self.callback:
                        self.callback(self.id, 'free')

        if not exit_roi_boxes and not self.exit_status:
            self.exit_true_count = 0
            self.exit_false_count += 1
            if self.exit_false_count > 100:
                self.exit_status = True
                self.count += 1
                if not self.is_free and self.count == 2:
                    self.is_free = True
                    self.count = 0
                    if self.callback:
                        self.callback(self.id, 'free')

        for box in exit_roi_boxes:
            x, y, w, h, id = box
            cv2.putText(exit_roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(exit_roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

        #cv2.imshow('frame', frame)

        #cv2.imshow('entry_roi', entry_roi)
        #cv2.imshow('exit_roi', exit_roi)

        return frame



# track_5 = RailwayTrack(5, EuclideanDistTracker(), EuclideanDistTracker(), cv2.createBackgroundSubtractorKNN(history=5000), cv2.createBackgroundSubtractorKNN(history=5000), 230, 320, 860, 960, 130, 200, 450, 550)

#tracks = {
#    'Путь 5': track_5,
#}
# # ../data/videos/20241018101022078_b4fea72a54e944b0a747f235d2757196_AC1418956.mp4

# capture = cv2.VideoCapture('./data/videos/20241011123759351_d700c44db5524303970688d087e40afa_AC1418956.mp4')

# while True:
#     ret, frame = capture.read()

#     if ret:
#         height, width, _ = frame.shape
#         for track in tracks.keys():
#             tracks[track].show_frame(frame)
#            # print(tracks[track].is_free)

#     key = cv2.waitKey(30)
#     if key == 27:
#         break

# capture.release()
#cv2.destroyAllWindows()
