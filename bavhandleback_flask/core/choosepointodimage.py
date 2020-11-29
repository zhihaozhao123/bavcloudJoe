import cv2
import numpy as np
import math

# 图片路径
img = cv2.imread('C:\\Users\Freeform\Documents\GitHub\\bavcloudJoe\\bavhandleback_flask\static\image\img_0000_0.png')
xlable = []
ylable = []


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if (event == cv2.EVENT_LBUTTONDOWN) :
        if len(xlable) == 2:
            return xlable[0], ylable[0], xlable[1], ylable[1], 'You are choosed two points of the image,please close the window'
        xy = "%d,%d" % (x, y)
        xlable.append(x)
        ylable.append(y)
        cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("Please choose two points of the image", img)



def choosetwopointsofimage(img_path):
    img = cv2.imread(img_path)
    cv2.namedWindow("Please choose two points of the image")
    cv2.setMouseCallback("Please choose two points of the image", on_EVENT_LBUTTONDOWN)
    cv2.imshow("Please choose two points of the image", img)
    cv2.waitKey(0)
    if len(xlable) == 2 :
        # cv2.destroyAllWindows()
        return xlable[0],ylable[0],xlable[1],ylable[1],'You are choosed two points of the image,please close the window'
    else :
        return None,None,None,None,'Please choose two points of the image'

def caculateroi(xlable_0, ylable_0, xlable_1, ylable_1,len_a_b,roipixles,roilen):
    perpixle = math.hypot(abs((int(xlable_0)-int(xlable_1))),abs((int(ylable_0)-int(ylable_1))))
    perpixle = len_a_b/perpixle
    roi_s = perpixle*perpixle*int(roipixles)
    roi_l = int(roilen)*perpixle
    return format(roi_s,'.4f'),format(roi_l,'.4f')

if __name__ == '__main__':
    # cv2.namedWindow("image")
    # cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    # cv2.imshow("image", img)
    # cv2.waitKey(0)

   print( choosetwopointsofimage('G:\ghs_Work2018\\bavcloudJoe\\bavhandleback_flask\static\image\img_0000_0.png'))
