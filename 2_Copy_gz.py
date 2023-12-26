import os
import shutil
import glob
import gzip
import zipfile

from pathlib import Path
import datetime
import time


def unpack_qz(filename_qz, filename):
    filename_csv = 'P:\TaskFiles\PROCESS_CSV' + '\\' + filename[:-3]
    print('---', filename_qz, '--', filename_csv)
    with gzip.open(filename_qz, 'rb') as f_in:
        with open(filename_csv, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


Path_Folder = 'P:\TaskFiles\ZIP\Rus'
Path_Folder_to = 'P:\TaskFiles\PROCESS_ZIP\Rus'
Path(Path_Folder_to).mkdir(parents=True, exist_ok=True)
List_ = os.listdir(Path_Folder)  # os.chdir(Path_Folder)
print(List_)
for x in List_:
    filename = os.fsdecode(x)
    FileFullPath_src = Path_Folder + '\\' + filename
    FileFullPath_dst = FileFullPath_src.replace('ZIP', 'PROCESS_ZIP')
    # FileFullPath_dst = 'P:\TaskFiles\PROCESS_ZIP\Rus' + '\\' + filename
    print(filename, Path_Folder, filename[-3:], FileFullPath_src)
    if os.path.isfile(FileFullPath_src):
        print('---is file')
        FileFullPath_src = Path_Folder + '\\' + filename
        # FileFullPath_dst = 'P:\TaskFiles\PROCESS_ZIP\Rus' + '\\' + filename
        print(FileFullPath_src, FileFullPath_dst)
        if filename[-3:] == '.gz':  # копируем только файлы с суффиксом '.gz'
            shutil.copyfile(FileFullPath_src, FileFullPath_dst)
            unpack_qz(FileFullPath_dst, filename)

    else:
        print('is folder')
        # Если это папка, то создаем аналогичную папку приемник второго уровня
        # и копируем туда файлы из источника 2 уровня
        Path(FileFullPath_dst).mkdir(parents=True, exist_ok=True)
        List_2 = os.listdir(FileFullPath_src)
        Path_Folder_2 = FileFullPath_src  # Имя папки источника второго уровня вложенности
        print(List_2)
        for y in List_2:
            filename = os.fsdecode(y)
            FileFullPath_src_2 = Path_Folder_2 + '\\' + filename
            FileFullPath_dst_2 = FileFullPath_src_2.replace('ZIP', 'PROCESS_ZIP')
            if os.path.isfile(FileFullPath_src_2):
                print(filename, ' is file')
                if filename[-3:] == '.gz' and "2018" not in filename:
                    shutil.copyfile(FileFullPath_src_2, FileFullPath_dst_2)
                    unpack_qz(FileFullPath_dst_2, filename)

# Архивация обработанных файлов csv Из папки folder_csv ='P:\TaskFiles\PROCESS_CSV' в zip файл.
filename_zip = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M.zip")
print(filename_zip)
filename_zip = 'P:\TaskFiles\ARH_CSV' + '\\' + filename_zip
folder_csv ='P:\TaskFiles\PROCESS_CSV'
List_3 = glob.glob('P:\TaskFiles\PROCESS_CSV\*.csv')
print(List_3)
with zipfile.ZipFile(filename_zip, mode='w') as fzip:
    for z in List_3:
        fzip.write(z)
# Удаление обработанных файлов csv Из папки folder_csv ='P:\TaskFiles\PROCESS_CSV'
for file in os.scandir(folder_csv):
    if file.name.endswith(".csv"):
        os.unlink(file.path)


