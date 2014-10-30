#!/usr/bin/env python

import cv2
import time
import numpy
import sys
import audio

webcam = cv2.VideoCapture(0)

frontal_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
profile_face_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
upper_body_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
lower_body_cascade = cv2.CascadeClassifier('haarcascade_lowerbody.xml')
full_body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

result, last_frame, last_frame2 = numpy.array([]), numpy.array([]), numpy.array([])

tt = audio.TapTester()

while(True):
    ret, frame = webcam.read()

    frame = cv2.resize(frame, (0,0), fx=0.1, fy=0.1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    front_faces = frontal_face_cascade.detectMultiScale(gray, 1.1, 5)
    profile_faces = profile_face_cascade.detectMultiScale(gray, 1.1, 5)
    #full_bodies = full_body_cascade.detectMultiScale(gray, 1.3, 5)
    #upper_bodies = upper_body_cascade.detectMultiScale(gray, 1.3, 4)
    #lower_bodies = lower_body_cascade.detectMultiScale(gray, 1.3, 5)

    presence = False

    for (x, y, w, h) in front_faces:
        presence = True
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)

    for (x, y, w, h) in profile_faces:
        presence = True
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

    # for (x, y, w, h) in upper_bodies:
    #     presence = True
    #     cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)

    # for (x, y, w, h) in full_bodies:
    #     presence = True
    #     cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,255), 2)

    if presence:
        print 'Presence detected: face detection'
        sys.stdout.flush()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if (len(sys.argv) >= 2 and sys.argv[1] == '--display'):
        cv2.imshow('frame', frame)

    if last_frame.size > 0 and last_frame2.size > 0:
        d1 = cv2.absdiff(last_frame, gray)
        d2 = cv2.absdiff(last_frame2, gray)
        result = cv2.bitwise_and(d1, d2)
        ret, result = cv2.threshold(result, 20, 255, cv2.THRESH_BINARY)
        kernel_ones = numpy.ones((2,2), numpy.uint8)
        eroded = cv2.erode(result, kernel_ones, iterations=1)
        dilated = cv2.dilate(eroded, kernel_ones, iterations=1)

        changed_pixels = cv2.countNonZero(dilated)
        if changed_pixels > 0:
            print 'Presence detected: motion detection'
            sys.stdout.flush()

        if (len(sys.argv) >= 2 and sys.argv[1] == '--display'):
            cv2.imshow('motion diff', result)
            cv2.imshow('motion diff - eroded', eroded)
            cv2.imshow('motion diff - dilated', dilated)

    last_frame = last_frame2;
    last_frame2 = gray;

    for i in range(10):
        tt.listen()
