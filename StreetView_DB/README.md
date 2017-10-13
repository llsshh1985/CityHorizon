# 数据管理类
---------------
### 初始化
```
CITY = "Guangzhou"#设置城市名
SOURCE = "Guangzhou_img_info_file_filtered.txt"#需要读取的文件。支持处理当前文件夹下的文件，或给出绝对地址的文件。
```
文件内数据编码：UTF-8  
文件内数据格式：

```
%pano[23-ntext]%_%haeding[int]%_%lat[float]%_%lng[float]%_%address[ntext]%_%description[ntext]%\n
```

### 连接数据库
```
test = InfoManager("test_"+CITY+".db")
```
支持给出目录绝对地址，之后在目录下链接数据库，无则创建。  
支持在当前目录下连接数据库，无则失败。  
支持给出数据库绝对地址，无则失败。  

### 在数据库内创建表单
```
test.creNewTable(CITY)
```

### 载入
在表单CITY中从SOURCE文件中载入数据
```
create(CITY,SOURCE,test)
```

### 删除
删除数据库中的表单CITY（表单内的数据消失，不可恢复）
```
test.dropTable(CITY)
```

### 更新
按pano更新表单CITY中的点，无则创建，有则更新数据。  
单点更新
```
test.update_tuple(CITY,('10061041150328113033300', 39, 23.274725, 113.767901, '广东省广州市增城区', '增城区荔城街道杰利百货南'))
```
批量更新
```
update(CITYname=CITY, SOURCEname= SOURCE,DB=test)
```

### 搜索
在表单CITY中在经纬度范围内搜索数据：
```
r = test.selectByRange(CITY,(23.1,23.3),(113.70,113.79))
``` 
*返回值为list，包含的元素为元组，包含满足条件点的所有信息*

打印数据库中所有表单的名称：
```
test.showTables()
```

按条件搜索：
```
t = [("pano", "%12111%"),("lat","23.3121")]
r = test.select(args=t,tablename=CITY)
print(r)
for i in r:
    print(i)
```
按照要求获取信息，返回值为list。  
args需为list，元素为元组。  
每个元组包含两个元素，前一个必须为str，代表选取的列的名称，如；“pano”。  
如果列类型为ntext，则匹配模式为like，支持模糊匹配查找。搜索语法举例："%12"-以"12"结尾；"12%"-以"12"开头；"%12%"-中间有字符串为12。  
如果列类型为num，则匹配模式为数值等于，若想使用数值模糊匹配，可以使用selectByRange。  
元组中后一个可以为数值或文本，代表查找内容。此处不限制参数类型，由上游模块过滤筛选。  


## TEST
------------
update_double-check test
```
test2 = InfoManager("test_"+CITY+".2db")
r = test.fetchall(CITY)
r2 = test2.fetchall(CITY)
for i in r2:
    if(i in r):
        print (str(i))
```

```
hashit =hashlib.md5()
file = open ("test_"+CITY+".db","rb")
while True:
    blk = file.read(4096) # 4KB per block
    if not blk: break
    hashit.update(blk)
print (hashit.hexdigest())
```