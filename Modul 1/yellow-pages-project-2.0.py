import csv
import sys
import tabulate
import pyinputplus as pypi

# 1. Menampilkan Daftar Kontak
    # default display: All Data w/ Bookmark on top
def show(data):
    print(tabulate.tabulate([data[i].values() for i in range(len(data))], data[0].keys(), tablefmt='outline'))
    # Sub Menu:
    # a. Fitur Search
def search():
    print('Secara default fitur ini hanya mencari berdasar kolom nama dan no hp:')
    value = input('input your value :')
    scDataset = []
    for i in range(len(dataset)):
        if value.upper() in list(dataset[i].values())[1] or value in list(dataset[i].values())[2]:
            scDataset.append(dataset[i])
    
    if len(scDataset) > 0:
        show(scDataset)
    else:
        print('!!!Data not found!!!\n') 

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

    print(f'\nTotal Kontak : {len(dataset)}')

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
def addNormal():
    listJenis = list(set(list(dataset[i].values())[3] for i in range(len(dataset))))
    listKabkot = list(set(list(dataset[i].values())[4] for i in range(len(dataset))))
    listId = [list(dataset[i].values())[0] for i in range(len(dataset))]

    no_telepon = pypi.inputStr(prompt='input no telepon :', blockRegexes=[r'[A-Za-z]'])

    datNo = []
    # check no hp ada di database / tidak
    for i in range(len(dataset)):
        if no_telepon == list(dataset[i].values())[2]:
            print('''Nomor sudah ada di dalam database :''')
            datNo.append(dataset[i])
            break
    
    if len(datNo) > 0:
        show(datNo)
    else:          
        nama = input('input name :').upper()
        jenis = pypi.inputMenu(prompt='input jenis :\n', choices=listJenis, numbered=True)
        kabKot = pypi.inputMenu(prompt='input kabupaten / kota :\n', choices=listKabkot, numbered=True)

        dataset.append({
            header[0] : max(listId)+1,
            header[1] : nama,
            header[2] : no_telepon,
            header[3] : jenis,
            header[4] : kabKot,
            header[5] : 'no'
        })

        print('Data Sucessufully Added !\n')
        show(dataset)

# 3. Menghapus Data Kontak
# a. Delete by ID
def deleteID():
    # Collect id to delete
    listID  = []
    while True:
        id = input('Masukkan id yang ingin dihapus :')
        if id == '':
            break
        else:
            listID.append(int(id))
    listID = list(set(listID))

    # Validate listID ada isinya gak
    if len(listID) == 0:
        print('!!! NO ID INPUTED !!!')
    else:
        # Confirmation (Show data that will be deleted)
        print(listID)
        conData = []
        for i in listID:
            for j in range(len(dataset)):
                if i == list(dataset[j].values())[0]:
                    conData.append(dataset[j])
        
        if len(conData) == 0:
            print('\n??? ID tidak ditemukan ???\n')
        else:
            show(conData)

            prompt = '\nAre you sure to delete this data ?(Y/N) :'
            con = pypi.inputYesNo(prompt=prompt)

            if con == 'yes':
                # Delete process
                for dat in dataset.copy():
                    if dat in conData:
                        dataset.remove(dat)

                print(f'{len(conData)} data dihapus \n')
                show(dataset)
            else:
                print('data tidak jadi dihapus !!!')

# b. Delete by Jenis/Kabupaten Kota
def deleteGroup():
    group = header[3:5]
    key1 = pypi.inputMenu(prompt='Pilih Group (1):\n', choices=group, numbered=True)
    listvalue1 = list({dataset[i][key1] for i in range(len(dataset))})
    value1 = pypi.inputMenu(prompt='Pilih value:\n', choices=listvalue1, numbered=True)
    filterDataset1 = []
    for i in range(len(dataset)):
        if value1 in dataset[i][key1]:
            filterDataset1.append(dataset[i])  
    show(filterDataset1)

    group.remove(key1)

    conf = pypi.inputYesNo(prompt=f'Tambah pilih Group (2) by {group[0]} : ')
    if conf == 'yes':
        key2 = group[0]
        listvalue2 = list({dataset[i][key2] for i in range(len(dataset))})
        value2 = pypi.inputMenu(prompt='Pilih value:\n', choices=listvalue2, numbered=True)
        filterDataset2 = []
        for i in range(len(dataset)):
            if value2 in dataset[i][key2] and value1 in dataset[i][key1]:
                filterDataset2.append(dataset[i])  
        show(filterDataset2)

        conf = pypi.inputYesNo(prompt='\nAnda yakin mau hapus semua data diatas?\n')
        if conf == 'yes':
            for dat in dataset.copy():
                if dat in filterDataset2:
                    dataset.remove(dat)
            show(dataset)

# 4. Mengedit Data Kontak
def edit():
    listId = [list(dataset[i].values())[0] for i in range(len(dataset))]

    id = int(input('Masukkan id yang ingin diedit :'))

    if id not in listId:
        print('ID NOT FOUND !')
    else:
        for i in range(len(dataset)):
            if id == list(dataset[i].values())[0]:

                print('This data will be edited :')
                show([dataset[i]])

                while True:
                    listJenis = list(set(list(dataset[i].values())[3] for i in range(len(dataset))))
                    listKabkot = list(set(list(dataset[i].values())[4] for i in range(len(dataset))))

                    key = pypi.inputMenu(prompt='Pilih info yang mau diupdate :\n', choices=header[1:], numbered=True)
                    
                    if key == header[1]:
                        val = input('input name :').upper()
                    elif key == header[2]:
                        val = pypi.inputStr(prompt='input no telepon :', blockRegexes=[r'[A-Za-z]'])
                    elif key == header[3]:
                        val = pypi.inputMenu(prompt='input jenis :\n', choices=listJenis, numbered=True)
                    elif key == header[4]:
                        val = pypi.inputMenu(prompt='input kabupaten / kota :\n', choices=listKabkot, numbered=True)
                    else:
                        val = pypi.inputYesNo(prompt='bookmark kontak ini?(Y/N) :')

                    print('Before :')
                    show([dataset[i]])

                    dataset[i][key] = val

                    print('\nAfter')
                    show([dataset[i]])

                    if key == header[5] and val == 'yes':
                        dataset.insert(0,dataset.pop(i))
                    
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
                choiceDisp = ['Tampilkan Semua','Search Nama','Filter','Summary Kontak-mu','Back to Main Menu']
                respDisp = pypi.inputMenu(choices=choiceDisp, numbered=True)
                if respDisp == choiceDisp[0]:
                    show(dataset)
                if respDisp == choiceDisp[1]:
                    search()
                elif respDisp == choiceDisp[2]:
                    filter()
                elif respDisp == choiceDisp[3]:
                    summary()
                else:
                    break
        elif response == choice[1]:
            while True:
                choiceDisp = ['Tambah Data','Back to Main Menu']
                respDisp = pypi.inputMenu(choices=choiceDisp, numbered=True)
                if respDisp == choiceDisp[0]:
                    addNormal()
                else:
                    break
        elif response == choice[2]:
            while True:
                choiceDisp = ['Hapus Data Berdasar ID','Hapus Data Berdasar Jenis/Kabupaten Kota','Back to Main Menu']
                respDisp = pypi.inputMenu(choices=choiceDisp, numbered=True)
                if respDisp == choiceDisp[0]:
                    deleteID()
                elif respDisp == choiceDisp[1]:
                    deleteGroup()
                else:
                    break     
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

if __name__ == "__main__":
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

    main()
    sys.exit()