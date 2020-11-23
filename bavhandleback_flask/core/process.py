import os
import logging
import numpy as np
from imageio import imread
import morphsnakes as ms
from matplotlib import pyplot as plt
#
# import SimpleITK as sitk
# import cv2
# import numpy as np
# # import torch
#
#
# def data_in_one(inputdata):
#     if not inputdata.any():
#         return inputdata
#     inputdata = (inputdata - inputdata.min()) / (inputdata.max() - inputdata.min())
#     return inputdata
#
#

def visual_callback_2d(background, fig=None):
    """
    Returns a callback than can be passed as the argument `iter_callback`
    of `morphological_geodesic_active_contour` and
    `morphological_chan_vese` for visualizing the evolution
    of the levelsets. Only works for 2D images.

    Parameters
    ----------
    background : (M, N) array
        Image to be plotted as the background of the visual evolution.
    fig : matplotlib.figure.Figure
        Figure where results will be drawn. If not given, a new figure
        will be created.

    Returns
    -------
    callback : Python function
        A function that receives a levelset and updates the current plot
        accordingly. This can be passed as the `iter_callback` argument of
        `morphological_geodesic_active_contour` and
        `morphological_chan_vese`.

    """

    # Prepare the visual environment.
    if fig is None:
        fig = plt.figure()
    fig.clf()
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.imshow(background, cmap=plt.cm.gray)

    ax2 = fig.add_subplot(1, 2, 2)
    ax_u = ax2.imshow(np.zeros_like(background), vmin=0, vmax=1)
    plt.pause(0.001)

    def callback(levelset):

        if ax1.collections:
            del ax1.collections[0]
        ax1.contour(levelset, [0.5], colors='r')
        ax_u.set_data(levelset)
        fig.canvas.draw()
        # fig.savefig(("image_",NUM,".jpg"))
        fig.savefig("imag.jpg")
        plt.pause(0.001)

    return callback


def pre_process(data_path):
    global test_image, test_mask
    image_list, mask_list, image_data, mask_data = [], [], [], []

    logging.info('Running: example_starfish (MorphGAC)...')
    file_name = os.path.split(data_path)[1].replace('.dcm', '')

    # 转为图片写入image文件夹

    # image_array = image_array.swapaxes(0, 2)
    # image_array = np.rot90(image_array, -1)
    # image_array = np.fliplr(image_array).squeeze()
    # # ret, image_array = cv2.threshold(image_array, 150, 255, cv2.THRESH_BINARY)
    # cv2.imwrite(f'./tmp/image/{file_name}.png', image_array, (cv2.IMWRITE_PNG_COMPRESSION, 0))

    # Load the image.
    imgcolor = imread(data_path) / 255.0
    # img = rgb2gray(imgcolor)
    #
    # # g(I)
    # gimg = ms.inverse_gaussian_gradient(img, alpha=1000, sigma=2)
    #
    # # Initialization of the level-set.
    # init_ls = ms.circle_level_set(img.shape, (163, 137), 135)
    #
    # # Callback for visual plotting
    # callback = visual_callback_2d(imgcolor)
    #
    # # MorphGAC.
    # ms.morphological_geodesic_active_contour(gimg, iterations=100,
    #                                          init_level_set=init_ls,
    #                                          smoothing=2, threshold=0.3,
    #                                          balloon=-1, iter_callback=callback)
    # image_tensor = torch.from_numpy(ROI_mask).float().unsqueeze(1)
    # # print(image_tensor.shape)
    # image_data.append(image_tensor)

    return image_data, file_name
#
#
# def last_process(file_name):
#     image = cv2.imread(f'./tmp/image/{file_name}.png')
#     mask = cv2.imread(f'./tmp/mask/{file_name}_mask.png', 0)
#     thresh, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     draw = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
#     cv2.imwrite(f'./tmp/draw/{file_name}.png', draw)
