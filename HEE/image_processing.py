from collections import namedtuple
from tkinter import Tk, filedialog

import cv2
import numpy as np
from imutils import contours


def get_user_image_path():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    PATH = filedialog.askopenfilename()
    root.destroy()
    root.mainloop()
    return PATH


Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')


# noinspection PyBroadException
def process_image(img_path):
    im = cv2.imread(img_path)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    th, threshed = cv2.threshold(gray, 200, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    morphed = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, np.ones((2, 2)))

    cnts = cv2.findContours(morphed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

    (cnts, _) = contours.sort_contours(cnts, method="left-to-right")

    holder = []

    for cnt in cnts:
        bbox = cv2.boundingRect(cnt)
        holder.append(list(bbox))

    # holder -> contours
    # hold -> bounding reacts

    for hold in holder:
        for hold2 in holder:
            if hold != hold2:
                area = (getIntersection(hold, hold2))
                x, y, w, h = hold2

                if w > 2 * h:
                    hold2[1] -= int(w / 2)
                    hold2[3] += w + h

                if hold2[2] * hold2[3] < 100:
                    # noinspection PyBroadException
                    try:
                        holder.remove(hold2)
                    except:
                        pass
                    continue

                if hold[2] * hold[3] > hold2[2] * hold2[3]:
                    if hold2[2] * hold2[3] - area < 20 and area != 0:
                        try:
                            holder.remove(hold2)
                        except:
                            pass
                        continue
                else:
                    if hold[2] * hold[3] - area < 20 and area != 0:
                        try:
                            holder.remove(hold)
                        except:
                            pass
                        continue

                if area > 5000:
                    if hold[2] * hold[3] > hold2[2] * hold2[3]:
                        # x,y,w,h = hold2[0],hold2[1],hold2[2],hold2[3]
                        # image = im[y:y+h,x:x+w]
                        # cv2.imshow("img" ,image )
                        # cv2.waitKey()
                        try:
                            holder.remove(hold2)
                        except:
                            pass

                    else:
                        # x,y,w,h = hold[0],hold[1],hold[2],hold[3]
                        # image = im[y:y+h,x:x+w]
                        # cv2.imshow("img" ,image )
                        # cv2.waitKey()
                        try:
                            holder.remove(hold)
                        except:
                            pass

    final_list = []
    i = 0
    for hold in holder:
        # cv2.rectangle(im, (hold[0], hold[1]), (hold[0] + hold[2], hold[1] + hold[3]), (255, 0, 255), 1, cv2.LINE_AA)
        x, y, w, h = hold[0], hold[1], hold[2], hold[3]
        x -= 4
        y -= 4
        w += 8
        h += 8
        image = im[y:y + h, x:x + w]

        cv2.imwrite('Images/' + str(i) + '.png', image)
        img = cv2.imread('Images/' + str(i) + '.png')
        img = cv2.resize(img, (28, 28))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, img = cv2.threshold(img, 165, 255, cv2.THRESH_BINARY)
        cv2.imwrite('Images/' + str(i) + '.png', img)
        img = cv2.imread('Images/' + str(i) + '.png')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        final_list.append(img)
        i += 1
    return final_list


def getIntersection(rect1, rect2):
    x1 = rect1[0]
    y1 = rect1[1]
    w1 = rect1[2]
    h1 = rect1[3]

    x2 = rect2[0]
    y2 = rect2[1]
    w2 = rect2[2]
    h2 = rect2[3]

    # check if they are intersecting

    a = Rectangle(x1, y1, x1 + w1, y1 + h1)
    b = Rectangle(x2, y2, x2 + w2, y2 + h2)

    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)

    if (dx >= 0) and (dy >= 0):
        return dx * dy

    return 0
