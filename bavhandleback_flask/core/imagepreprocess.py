import os
import pydicom
from flask import jsonify
from tqdm import tqdm
from bavhandleback_flask.core.pydicom_PIL import show_PIL
import logging
from imageio import imread
import bavhandleback_flask.core.morphsnakes as ms
from matplotlib import pyplot as plt


import numpy as np

column_all_c = ['ID', '姓名', '年龄', '检查设备', '检查时间', '身高\体重','分辨率']

features_list = ['PatientID', 'PatientName', 'Age', 'Modality', 'StudyDate','H_W', 'ImageSize']


def is_dicom_file(filename):
    #判断某文件是否是dicom格式的文件
    file_stream = open(filename, 'rb')
    file_stream.seek(128)
    data = file_stream.read(4)
    file_stream.close()
    if data == b'DICM':
        return True
    return False

def load_patient(src_dir):
    '''
        读取某文件夹内的所有dicom文件
    :param src_dir: dicom文件夹路径
    :return: dicom list
    '''
    files = os.listdir(src_dir)
    slices = []
    for s in files:
        if is_dicom_file(src_dir + '/' + s):
            instance = pydicom.read_file(src_dir + '/' + s)
            slices.append(instance)

    # try:
    #     slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    # except:
    #     slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
    #
    # for s in slices:
    #     s.SliceThickness = slice_thickness
    return slices

def dicomconvertpng(dicom_dir, png_path, patient_info=None):
    # 读取dicom文件的元数据(dicom tags)
    slices = load_patient(dicom_dir)
    for i in tqdm(range(len(slices))):
        # 输出png文件目录
        img_path = png_path+"/img_" + str(i).rjust(4, '0') + "_" + str(i) + ".png" #Linux--Mac
        # img_path = png_path + "\img_" + str(i).rjust(4, '0') + "_" + str(i) + ".png" #Windows
        filename = "img_" + str(i).rjust(4, '0') + "_" + str(i) + ".png"
        show_PIL(slices[i], img_path)
        pat_name = slices[i].PatientName
        # display_name = pat_name.family_name + ", " + pat_name.given_name
        display_type = str(pat_name.family_name).split("-")[0]
        display_name = str(pat_name.family_name).split("-")[2]
        patient_info = {"PatientID":  slices[i].PatientID ,"PatientName": display_name, "Modality":  slices[i].Modality ,"StudyDate":  str(slices[i].StudyDate) ,"ImageSize":  str(slices[i].Columns) + "x"+ str(slices[i].Rows),"H_W":pat_name.given_name,"Type":display_type,"PatientBirthDate":slices[i].PatientBirthDate,"Sex":slices[i].PatientSex}
        # image_info[i].append('PatientName',display_name)
        # image_info[i].append('PatientID',str(slices[i].PatientID))
        # image_info[i].append('Modality',str(slices[i].Modality))
        # image_info[i].append('StudyDate',str(slices[i].StudyDate))
        # image_info[i].append('ImageSize',str(slices[i].Rows) + "x"+ str(slices[i].Columns))
        print(f"Patient's Name...: {pat_name.family_name}")
        print(f"Patient ID.......: {slices[i].PatientID}")
        print(f"Modality.........: {slices[i].Modality}")
        print(f"Study Date.......: {slices[i].StudyDate}")
        print(f"Image size.......: {slices[i].Rows} x {slices[i].Columns}")
        print(slices[i].to_json_dict())
        # print(f"Pixel Spacing....: {instance.PixelSpacing}")

        #读取Dicom转PNG后的PNG文件，并进行处理

        return filename,patient_info


def rgb2gray(img):
    """Convert a RGB image to gray scale."""
    return 0.2989 * img[..., 0] + 0.587 * img[..., 1] + 0.114 * img[..., 2]


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
        fig.savefig(("./static/handleimage/imag.jpg"))
        # fig.savefig("G:\ghs_Work2018\\bavcloudJoe\\bavhandleback_flask\static\handleimage\imag.jpg")
        plt.pause(0.001)

    return callback


def example_starfish(org_img_path):

        logging.info('Running: example_starfish (MorphGAC)...')

        # Load the image.
        imgcolor = imread(org_img_path) / 255.0
        img = rgb2gray(imgcolor)

        # g(I)
        gimg = ms.inverse_gaussian_gradient(img, alpha=100000, sigma=1)

        # Initialization of the level-set.
        # init_ls = ms.circle_level_set(img.shape, (163, 137), 135)
        init_ls = ms.circle_level_set(img.shape, None, None)
        # Callback for visual plotting
        callback = visual_callback_2d(imgcolor)

        # MorphGAC.
        u,count = ms.morphological_geodesic_active_contour(gimg, iterations=26,
                                                 init_level_set=init_ls,
                                                 smoothing=4, threshold='auto',
                                                 balloon=-1, iter_callback=callback)

        return "imag.jpg",count,0

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # #dicom文件目录
    # dicom_dir = '../data/dicom'
    # # 读取dicom文件的元数据(dicom tags)
    # slices = load_patient(dicom_dir)
    # for i in tqdm(range(len(slices))):
    #     # 输出png文件目录
    #     img_path = "../data/image/img_" + str(i).rjust(4, '0') + "_"+str(i)+".png"
    #     show_PIL(slices[i],img_path)
    #
    #
    # print(dicomconvertpng(dicom_dir,'../data/image'))

    ##Windows
    copy_image_path = "G:\ghs_Work2018\\bavcloudJoe\\bavhandleback_flask\static\image"
    copy_dicom_path = "G:\ghs_Work2018\\bavcloudJoe\\bavhandleback_flask\data\\tmp\ct"
    org_img_path, patient_info = dicomconvertpng(r"G:\ghs_Work2018\bavcloudJoe\bavhandleback_flask\data\dicom", copy_image_path,
                                                               patient_info=None)
    example_starfish(copy_image_path +"\\"+ org_img_path)