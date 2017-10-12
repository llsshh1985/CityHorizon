from InfoManager import *
import os
import hashlib
CITY = "Guangzhou"
SOURCE = "Guangzhou_img_info_file_filtered.txt"

def create(CITYname, SOURCEname, DB):
    info = open(SOURCEname, 'r', encoding='UTF-8')
    info = info.readlines()
    infobox = []
    for i in info:
        temp = i.replace('\n', '')
        temp = temp.replace('\t', '')
        temp = temp.split('_')
        heading = int(temp[1])
        heading = heading % 90
        temp[1] = heading
        temp = tuple(temp)
        infobox.append(temp)
        # DB.savein_tuple("Beijing",temp)
    DB.savein_list(CITYname, infobox)

def update(CITYname, SOURCEname, DB):
    info = open(SOURCEname, 'r', encoding='UTF-8')
    info = info.readlines()
    infobox = []
    for i in info:
        temp = i.replace('\n', '')
        temp = temp.replace('\t', '')
        temp = temp.split('_')
        heading = int(temp[1])
        heading = heading % 90
        temp[1] = heading
        temp = tuple(temp)
        infobox.append(temp)
        # DB.savein_tuple("Beijing",temp)
    DB.update_list(CITYname, infobox)

test = InfoManager("test_"+CITY+".db")
#test.creNewTable(CITY)
#create(CITY,SOURCE,test)

'''
test2 = InfoManager("test_"+CITY+".2db")
r = test.fetchall(CITY)
r2 = test2.fetchall(CITY)
for i in r2:
    if(i in r):
        print (str(i))
'''

#test.dropTable(CITY)

#r = test.selectByRange(CITY,(23.1,23.3),(113.70,113.79))
#print(r)

#test.update_tuple(CITY,('10061041150328113033300', 39, 23.274725, 113.767901, '广东省广州市增城区', '增城区荔城街道杰利百货南'))

'''hashit =hashlib.md5()
file = open ("test_"+CITY+".db","rb")
while True:
    blk = file.read(4096) # 4KB per block
    if not blk: break
    hashit.update(blk)
print (hashit.hexdigest())'''

#update(CITYname=CITY, SOURCEname= SOURCE,DB=test)
t = [("pano", "%12111%")]
r = test.select(t,CITY)
print(r)
for i in r:
    print(i)
test.showTables()


