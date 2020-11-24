import os
import pydicom
from flask import jsonify
from tqdm import tqdm
from bavhandleback_flask.core.pydicom_PIL import show_PIL

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

def dicomconvertpng(dicom_dir, png_path, image_info=None):
    # 读取dicom文件的元数据(dicom tags)
    slices = load_patient(dicom_dir)
    for i in tqdm(range(len(slices))):
        # 输出png文件目录
        img_path = png_path+"/img_" + str(i).rjust(4, '0') + "_" + str(i) + ".png"
        show_PIL(slices[i], img_path)
        pat_name = slices[i].PatientName
        display_name = pat_name.family_name + ", " + pat_name.given_name
        image_info = {"PatientName":  display_name , "PatientID":  slices[i].PatientID ,"Modality":  slices[i].Modality ,"StudyDate":  str(slices[i].StudyDate) ,"ImageSize":  str(slices[i].Rows) + "x"+ str(slices[i].Columns)}
        # image_info[i].append('PatientName',display_name)
        # image_info[i].append('PatientID',str(slices[i].PatientID))
        # image_info[i].append('Modality',str(slices[i].Modality))
        # image_info[i].append('StudyDate',str(slices[i].StudyDate))
        # image_info[i].append('ImageSize',str(slices[i].Rows) + "x"+ str(slices[i].Columns))
        print(f"Patient's Name...: {display_name}")
        print(f"Patient ID.......: {slices[i].PatientID}")
        print(f"Modality.........: {slices[i].Modality}")
        print(f"Study Date.......: {slices[i].StudyDate}")
        print(f"Image size.......: {slices[i].Rows} x {slices[i].Columns}")
        # print(f"Pixel Spacing....: {instance.PixelSpacing}")
        return img_path,image_info

if __name__ == '__main__':
    #dicom文件目录
    dicom_dir = '../data/dicom'
    # 读取dicom文件的元数据(dicom tags)
    slices = load_patient(dicom_dir)
    for i in tqdm(range(len(slices))):
        # 输出png文件目录
        img_path = "../data/image/img_" + str(i).rjust(4, '0') + "_"+str(i)+".png"
        show_PIL(slices[i],img_path)

    print(dicomconvertpng(dicom_dir,'../data/image'))