import pigpio
from engines import *
import time
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
pi, ESC, STEER = setup_gpio()
spd = 1560
ang = 90

if cap.isOpened() == False:
    print("Cant get frame")
    exit()

img_size = [360, 200]

arc = np.float32([[-146, 200],
                 [495, 200],
                 [275, 116],
                 [45, 116]])

arc_draw = np.array(arc, dtype=np.int32)

dst = np.float32([[0, img_size[1]],
                  [img_size[0], img_size[1]],
                  [img_size[0], 0],
                  [0, 0]])

while True:
    ret, frame = cap.read()

    if ret == False:
        print("No frame")
        continue

    resized = cv.resize(frame, (img_size[0], img_size[1]))
    r_image = resized[:, :, 2]
    g_image = resized[:, :, 1]
    b_image = resized[:, :, 0]

    '''
    cv2.imshow('r_image', r_image)
    cv2.imshow('g_image', g_image)
    cv2.imshow('b_image', b_image)
    '''

    b_binary = np.zeros_like(b_image)
    b_binary[(b_image > 225)] = 255
    #cv2.imshow('b_binary', b_binary)

    g_binary = np.zeros_like(g_image)
    g_binary[(g_image > 225)] = 255
    #cv2.imshow('g_binary', g_binary)

    r_binary = np.zeros_like(r_image)
    r_binary[(r_image > 225)] = 255
    #cv2.imshow('r_binary', r_binary)

    allBinary = r_binary & g_binary & b_binary
    cv.imshow('all_binary', allBinary)

    matrix = cv.getPerspectiveTransform(arc, dst)
    warp = cv.warpPerspective(allBinary, matrix, (img_size[0], img_size[1]), flags=cv.INTER_LINEAR)

    histogram = np.sum(warp[warp.shape[0] // 2:, :], axis=0)
    mid = histogram.shape[0] // 2
    r_index = np.argmax(histogram[:mid])
    l_index = np.argmax(histogram[mid:]) + mid

    n_windows = 9
    window_height = np.int(warp.shape[0] / n_windows)
    windows_half = 25

    x_lcenter = l_index
    x_rcenter = r_index

    left_lane = np.array([], dtype=np.int16)
    right_lane = np.array([], dtype=np.int16)

    out_img = np.dstack((warp, warp, warp))

    non_zero = warp.nonzero()
    whitePixelY = np.array(non_zero[0])
    whitePixelX = np.array(non_zero[1])
    for window in range(n_windows):
        win_y1 = warp.shape[0] - (window + 1) * window_height
        win_y2 = warp.shape[0] - (window) * window_height

        left_win_x1 = x_lcenter - windows_half
        left_win_x2 = x_lcenter + windows_half
        right_win_x1 = x_rcenter - windows_half
        right_win_x2 = x_rcenter + windows_half

        good_left_indexs = ((whitePixelY >= win_y1) & (whitePixelY <= win_y2) & (whitePixelX >= left_win_x1) & (
                whitePixelX <= left_win_x2)).nonzero()[0]
        good_right_indexs = ((whitePixelY >= win_y1) & (whitePixelY <= win_y2) & (whitePixelX >= right_win_x1) & (
                whitePixelX <= right_win_x2)).nonzero()[0]

        left_lane = np.concatenate((left_lane, good_left_indexs))
        right_lane = np.concatenate((right_lane, good_right_indexs))

        if len(good_left_indexs) > 50:
            x_lcenter = np.int(np.mean(whitePixelX[good_left_indexs]))
        if len(good_right_indexs) > 50:
            x_rcenter = np.int(np.mean(whitePixelX[good_right_indexs]))

    leftx = whitePixelX[left_lane]
    lefty = whitePixelY[left_lane]
    rightx = whitePixelX[right_lane]
    righty = whitePixelY[right_lane]

    if len(righty) == 0 or len(lefty) == 0:
        ang = 97
        control(pi, ESC, spd, STEER, ang)
        continue

    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)
    center_fit = ((left_fit + right_fit) / 2)

    error_val = img_size[0] / 2 - center_fit[-1]

    if abs(error_val) < 10:
        ang = 84
    elif error_val <= -10:
        ang = 64
    else:
        ang = 99

    print(error_val)
    control(pi, ESC, spd, STEER, ang)
    if (cv.waitKey(1) == 27):
        break
    
print("Exiting...")
cap.release()
control(pi, ESC, 0, STEER, 0)
cv.destroyAllWindows()
