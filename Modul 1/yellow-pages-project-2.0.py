'''
-- IDEA --
Apps: Yellow pages (daftar buku telefon)

Function: mencari info kontak penting Yogyakarta
User: General

Fitur (CRUD):
1. Create
2. Read
3. Update
4. Delete

Menu:
CONCEPT I
1. Menampilkan Daftar Kontak
2. Menambah Data Kontak
3. Mengupdate Data Kontak
4. Menghapus Data Kontak
5. Bookmark Data Kontak
6. Mencari Data Kontak
7. Summary Data Kontak
8. Keluar Program

CONCEPT II
# 1. Menampilkan Daftar Kontak
#     a. Show All Data
#     b. Show Bookmark Only
#     c. Show by Filter
#     d. Show Summary Kontak
# 2. Menambah Data Kontak
# 3. Menghapus Data Kontak (Add notif buat konfirmasi)
# 4. Mengedit Data Kontak
# 5. Exit

Column:
id
nama
no_telepon
jenis
kabupaten_kota
bookmark


Rules (Complexity):

'''
import csv
import tabulate
import pyinputplus as pypi

path = "D:\PURWADHIKA\PLAYGROUND\PYTHON\Modul 1\Capstone Project\important_number_jogja.csv"

file = open(path)
reader = csv.reader(file, delimiter=';')

header = next(reader)
dataset = []

for row in reader:
    if 'yes' in row[5]:
        dataset.insert(0,{
            header[0] : int(row[0]),
            header[1] : str(row[1]).upper(),
            header[2] : str(row[2]),
            header[3] : str(row[3]).lower(),
            header[4] : str(row[4]).capitalize(),
            header[5] : str(row[5])
        })
    else:
        dataset.append({
            header[0] : int(row[0]),
            header[1] : str(row[1]).upper(),
            header[2] : str(row[2]),
            header[3] : str(row[3]).lower(),
            header[4] : str(row[4]).capitalize(),
            header[5] : str(row[5])
        })

file.close()

# 1. Menampilkan Daftar Kontak
def show(data):
    print(tabulate.tabulate([data[i].values() for i in range(len(data))], data[0].keys(), tablefmt='outline'))
    #  a. Show All Data
    #  b. Show Bookmark Only
    #  c. Show by Filter
    #  d. Show Summary Kontak

# 2. Menambah Data Kontak
def add():
    listJenis = {list(dataset[i].values())[3] for i in range(len(dataset))}
    listKabkot = list(set(list(dataset[i].values())[4] for i in range(len(dataset))))
    listId = [list(dataset[i].values())[0] for i in range(len(dataset))]

    nama = input('input name :').upper()
    no_telepon = input('input no telepon :')
    jenis = input('input jenis :').lower()
    kabKot = pypi.inputMenu(prompt='input kabupaten / kota :\n', choices=listKabkot, numbered=True)

    dataset.append({
        header[0] : max(listId)+1,
        header[1] : nama,
        header[2] : no_telepon,
        header[3] : jenis,
        header[4] : kabKot,
        header[5] : 'no'
    })

    show(dataset)

# 3. Menghapus Data Kontak
def delete():
    # notif konfirmasi

    id = int(input('Masukkan id yang ingin dihapus :'))

    # delete process
    for i in range(len(dataset)-1):
        if id == list(dataset[i].values())[0]:
            del dataset[i]

    show(dataset)

# 4. Mengedit Data Kontak
def edit():
    
    id = int(input('Masukkan id yang ingin diedit :'))

    for i in range(len(dataset)-1):
        if id == list(dataset[i].values())[0]:
            while True:
                key = pypi.inputMenu(prompt='Pilih info yang mau diupdate :\n', choices=header[1:], numbered=True)
                value = input('Input value :')
                dataset[i][key] = value
                
                contEdit = pypi.inputYesNo(prompt='Ingin mengedit lagi?(Y/N) :')
                if contEdit == 'no':
                    break

    show(dataset)

edit()
# 5. Exit