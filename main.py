import os, csv, time, shutil
from hashlib import sha1, md5

'''------------------------'''
examiner = 'MB'
caseNumber = 'H-2652/20'
sourceName = input('Oznaczenie nośnika: ')
# print(os.path.abspath(path))  # Do raportu
'''------------------------'''


def saveToCsv(input_path, output_path, srcName):
    count = 0
    with open(f'{output_path}\\Raport_{srcName}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # definiujemy nagłówek (czyli nasze kolumny)
        fieldnames = ['Nazwa pliku', 'MD5', 'SHA1', 'Pełna ścieżka', 'Data modyfikacji', 'Data utworzenia',
                      'Rozmiar (w bajtach)']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # zapisujemy do pierwszej linii zdefiniowane wczesniej nazwy kolumn
        csvwriter.writeheader()

        for path, subfiles, files in os.walk(input_path):
            #     if len(subfiles):
            #         for i in subfiles:
            #             print(f'Podkatalog to: {i}')
            #             print(f'path to: {path}')
            if len(files):
                for i in files:
                    # print(f'path to: {path}\\{i}')
                    fp = path + '\\' + i
                    md5, sha1 = hashing(fp)
                    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fp)
                    file = {'Nazwa pliku': i,
                            'MD5': md5,
                            'SHA1': sha1,
                            'Pełna ścieżka': fp[2:],
                            'Data modyfikacji': time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(mtime)),
                            'Data utworzenia': time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(ctime)),
                            'Rozmiar (w bajtach)': size}
                    csvwriter.writerow(file)
                    count += 1
    csvfile.close()


def copyTree(source, destination):
    try:
        shutil.copytree(source, destination)
        counter = (sum([len(files) for r, d, files in os.walk(source)]),
                   sum([len(files) for r, d, files in os.walk(destination)]))
        return counter
    except FileExistsError:
        print('Folder o tej nazwie istnieje!')


def hashing(file):
    fileToHash = open(file, "rb")
    bs = 2048
    hash_sha1 = sha1()
    hash_md5 = md5()
    while True:
        chunk = fileToHash.read(bs)
        hash_sha1.update(chunk)
        hash_md5.update(chunk)
        if len(chunk) == 0:
            break
    fileToHash.close()
    return str(hash_md5.hexdigest()), str(hash_sha1.hexdigest())


source_path = 'B:\\'
destRoot = 'D:\Python\Destination'
destination_path = destRoot + '\\' + sourceName
counter = copyTree(source_path, destination_path)
saveToCsv(source_path, destRoot, sourceName)
if type(counter) is tuple:
    print(f'Skopiowano {counter[1]} z {counter[0]} plików.')
