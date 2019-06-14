#!/usr/bin/env python

import cv2
import face_detector

detector   = face_detector.Detector(cv2)
video_feed = cv2.VideoCapture(0)
running    = True
