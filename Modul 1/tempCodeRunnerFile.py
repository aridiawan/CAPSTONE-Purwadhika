import csv
import sys
import tabulate
import pyinputplus as pypi

path = "D:\PURWADHIKA\PLAYGROUND\PYTHON\Modul 1\Capstone Project\CAPSTONE-Purwadhika\Modul 1\important_number_jogja.csv"

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
    # default display: All Data w/ Bookmark on top
def show(data):
    print(tabulate.tabulate([data[i].values() for i in range(len(data))], data[0].keys(), tablefmt='outline'))
    # Sub Menu:
    # a. Fitur Search
    # b. Show by Filter
def filter():
    key = pypi.inputMenu(prompt='Pilih kolom yang akan difilter:\n', choices=header[1:], numbered=True)
    listvalue = list({dataset[i][key] for i in range(len(dataset))})
    value = pypi.inputMenu(prompt='Pilih value:\n', choices=listvalue, numbered=True)
    filterDataset = []
    for i in range(len(dataset)):
        if value in dataset[i][key]:
            filterDataset.append(dataset[i])  

    show(filterDataset)

    # c. Show Summary Kontak
def summary():
    key = header[3:5]

    # JENIS
    listvalue1 = list(dataset[i][key[0]] for i in range(len(dataset)))
    listvalue2Unique = list({dataset[i][key[0]] for i in range(len(dataset))})
    listCount1 = []
    # Create list data
    for i in range(len(listvalue2Unique)):
        listCount1.append([
            listvalue2Unique[i],listvalue1.count(listvalue2Unique[i])])

    # Sort Descending
    for i in range(len(listCount1)):    
        for j in range(i+1, len(listCount1)):    
            if(listCount1[i][1] < listCount1[j][1]):    
                temp = listCount1[i]    
                listCount1[i] = listCount1[j]    
                listCount1[j] = temp

    print('\nData Jumlah Kontak berdasarkan Jenis')
    print(tabulate.tabulate(listCount1, [key[0],'jumlah kontak'], tablefmt='outline'))   
    print('\n') 

    # KABUPATEN KOTA
    listvalue2 = list(dataset[i][key[1]] for i in range(len(dataset)))
    listvalue2Unique = list({dataset[i][key[1]] for i in range(len(dataset))})
    listCount2 = []
    # Create list data
    for i in range(len(listvalue2Unique)):
        listCount2.append([
            listvalue2Unique[i],listvalue2.count(listvalue2Unique[i])])

    # Sort Descending
    for i in range(len(listCount2)):    
        for j in range(i+1, len(listCount2)):    
            if(listCount2[i][1] < listCount2[j][1]):    
                temp = listCount2[i]    
                listCount2[i] = listCount2[j]    
                listCount2[j] = temp

    print('Data Jumlah Kontak berdasarkan Kabupaten Kota')
    print(tabulate.tabulate(listCount2, [key[1],'jumlah kontak'], tablefmt='outline'))   
    print('\n')

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
    for i in range(len(dataset)):
        if id == list(dataset[i].values())[0]:
            del dataset[i]

    show(dataset)

# 4. Mengedit Data Kontak
def edit():
    
    id = int(input('Masukkan id yang ingin diedit :'))

    for i in range(len(dataset)):
        if id == list(dataset[i].values())[0]:
            while True:
                key = pypi.inputMenu(prompt='Pilih info yang mau diupdate :\n', choices=header[1:], numbered=True)
                value = input('Input value :')
                dataset[i][key] = value
                
                contEdit = pypi.inputYesNo(prompt='Ingin mengedit lagi?(Y/N) :')
                if contEdit == 'no':
                    break

    show(dataset)

def main():
    global dataset

    while True:
        print('\n---Welcome to Yogyakarta IMPORTANT Contact System---\n')
        prompt = f'Silahkan Pilih Menu :\n'
        choice = ['Menampilkan Daftar Kontak', 'Menambah Kontak', 'Menghapus Kontak', 'Mengedit Kontak', 'Exit']

        response = pypi.inputMenu(prompt=prompt, choices=choice, numbered=True)

        if response == choice[0]:
            show(dataset)
            while True:
                choiceDisp = ['Search Nama','Filter','Summary Kontak-mu','Back to Main Menu']
                respDisp = pypi.inputMenu(choices=choiceDisp, numbered=True)
                if respDisp == choiceDisp[0]:
                    print('fitur otw')
                elif respDisp == choiceDisp[1]:
                    filter()
                elif respDisp == choiceDisp[2]:
                    summary()
                else:
                    break
        elif response == choice[1]:
            add()
        elif response == choice[2]:
            delete()
        elif response == choice[3]:
            edit()
        else:
            break

    file = open(path, 'w', newline = '')

    writer = csv.writer(file, delimiter=';')

    datasetVal = [header]
    for i in range(len(dataset)):
        datasetVal.append(dataset[i].values())

    writer.writerows(datasetVal)

    file.close()

main()
sys.exit()