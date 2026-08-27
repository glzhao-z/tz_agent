import shutil



# 做一个方法接收文件夹然后压缩层zip
def zip_folder(folder_path):
    """
    压缩文件夹
    :param folder_path: 文件夹路径
    :return:
    """
    zip_path = folder_path + '.zip'
    shutil.make_archive(folder_path, 'zip', folder_path)
    return zip_path

print(zip_folder('test_folder'))
