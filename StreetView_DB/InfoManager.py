import sqlite3
import os
import logging

class InfoManager(object):
	__box_name ="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_abcdefghijklmnopqrstuvwxyz."
	__box_argsi = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	__create_table_sql = '''CREATE TABLE %s (
								`pano` ntext NOT NULL,
								`heading` int NOT NULL,
								`lat` decimal(13,9) NOT NULL,
								`lng` decimal(13,9) NOT NULL,
								`address` ntext NOT NULL,
								`description` ntext NOT NULL,
								PRIMARY KEY (`pano`)
								)'''
	__savein_sql = '''insert INTO %s values (?, ?, ?, ?, ?, ?)'''
	__update_sql = '''UPDATE %s SET heading = ?, lat = ?, lng = ?, address = ?, description = ? WHERE pano = ?'''
	__selectByRange_sql = ''' SELECT * FROM %s WHERE lat>=%f and lat<=%f and lng>=%f and lng<=%f'''
	__select_sql = ''' SELECT * FROM %s WHERE 1'''
	__key_box_ntext = ["pano", "address", "description"]
	__key_box_int = ["heading"]
	__key_box_float = ["lat", "lng"]
	def __init__(self, add = None, log_le = None):
		#logging
		logging.basicConfig(level= logging.INFO,
							filename="DB_InfoManager.log",
							filemode='a',
							format='%(asctime)s line:%(lineno)d,%(funcName)s %(levelname)s %(message)s',
                			datefmt='%d %b %H:%M:%S')
		#
		self.__conn=None
		add_temp=add
		address = ""
		if(add_temp is not None and os.path.exists(add_temp)):
			if(os.path.isfile(add_temp)):
				try:
					self.__conn= sqlite3.connect(add_temp)
				except Exception as err:
					logging.warning(str(err))
					print(str(err))
			else:
				address = add_temp
				print("The DB will be create under " + address)

		while(self.__checktablename(add_temp) == False):
			logging.warning("DB's name is not allowed.")
			#print("The address or is empty.If the file is not exist, one will be created.")
			add_temp = input ("Enter a name:")
		self.__add = address + add_temp
		#
		try:
			self.__conn= sqlite3.connect(self.__add)
		except Exception as err:
			logging.warning(str(err))
			print(str(err))

	def __get_cu(self ):
		if self.__conn is not None:
			return self.__conn.cursor()
		else:
			return None

	def __checktablename(self, tablename):
		if (tablename is None or type(tablename) is not str or tablename == ''):
			#logging.error("Type of tablename is not list(or None).")
			return False
		for i in tablename:
			if( i not in self.__box_name):
				return False
		return True
	def __checkargsi(self,name):
		if (name is None or type(name) is not str or name == ''):
			#logging.error("Type of tablename is not list(or None).")
			return False
		for i in name:
			if( i not in self.__box_argsi):
				return False
		return True
	def __checkdata(self, data, typename):
		if (data is None or type(data) is not typename):
			#logging.error("Type of data is not list(or None).")
			return False
		return True
	def __checknum(self, temp):
		if(temp is None):
			return False
		if(type(temp) is int or type(temp) is float):
			return True
		if(type(temp) is tuple or type(temp) is list):
			for i in temp:
				if(type(i) is not int and type(i) is not float):
					return False
			return True
		return False

	def creNewTable(self, tablename = None):
		if (self.__checktablename(tablename)==False):
			logging.error("Type of tablename is not list(or None).")
			print("Type of tablename is not list(or None).")
			return False
		#check tablename
		if (self.__checktablename(tablename) == False):
			logging.error("Type of tablename is not list(or None).")
			return False
		cu = self.__get_cu()
		sql = self.__create_table_sql %tablename
		try:
			cu.execute(sql)
			self.__conn.commit()
			logging.info(sql)
			cu.close()
		except Exception as err:
			logging.warning(str(err))
			print(str(err))
	'''Dengrous!!!'''

	def dropTable(self,tablename = None):
		if (self.__checktablename(tablename)==False):
			logging.error("Type of tablename is not list(or None).")
			print("Tablename is empty.")
			return False

		sql = "DROP TABLE IF EXISTS " + tablename
		cu = self.__get_cu()
		try:
			cu.execute(sql)
			self.__conn.commit()
			logging.info(sql)
			cu.close()
		except Exception as err:
			logging.warning(str(err))
			print(str(err))


	'''savein:按补充数据库中与之前不同的条目。若pano已存在，则保留先前条目，不进行更新'''
	def savein_list(self, tablename = None, data = None):
		if (self.__checkdata(data=data,typename=list)==False):
			logging.error("Type of data is not list(or None).")
			return False
		if(self.__checktablename(tablename)==False):
			logging.error("Type of tablename is not list(or None).")
			return False
		cu = self.__get_cu()
		if (cu is not None):
			for d in data:
				self.__savein(tablename=tablename,
							  cu=cu,
							  data=d)
			logging.info("")
			print("savein_list")
			try:
				self.__conn.commit()
				cu.close()
				return True
			except Exception as err:
				logging.warning(str(err))
				print(str(err))
				return False
		else:
			return False


	def __savein(self,tablename = None,data = None, cu = None):
		if (self.__checkdata(data=data, typename=tuple) == False):
			logging.error("Type of data is not list(or None).")
			return False
		if(cu == None):
			logging.error("Type of cu is not list(or None).")
			return False
		sql = self.__savein_sql % tablename
		try:
			cu.execute(sql, data)
		except Exception as err:
			logging.warning(str(err))
		return

	def savein_tuple(self, tablename = None, data = None):
		if (self.__checkdata(data=data, typename=tuple) == False):
			logging.error("Type of data is not list(or None).")
			return False

		if (self.__checktablename(tablename) == False):
			logging.error("Type of tablename is not list(or None).")
			return False

		cu = self.__get_cu()
		if (cu is not None):
			self.__savein(tablename=tablename,
						  cu=cu,
						  data=data)
			try:
				self.__conn.commit()
				logging.info(str(data))
				print("savein_tuple" + str(data))
				cu.close()
				return True
			except Exception as err:
				logging.warning(str(err))
				print(str(err))
				return False
		else:
			return False


	'''update:'''
	def update_list(self, tablename = None, data = None):
		if (self.__checkdata(data=data,typename=list)==False):
			logging.error("Type of data is not list(or None).")
			return False
		if(self.__checktablename(tablename)==False):
			logging.error("Type of tablename is not list(or None).")
			return False
		cu = self.__get_cu()
		if(cu is not None):
			for d in data:
				self.__update(tablename=tablename,
							  cu=cu,
							  data=d)
			logging.info("")
			print("update_list")
			try:
				self.__conn.commit()
				cu.close()
				return True
			except Exception as err:
				logging.warning(str(err))
				print(str(err))
				return False
		else:
			return False

	def __update(self, tablename = None, data = None, cu = None):
		if (self.__checkdata(data=data, typename=tuple) == False):
			logging.error("Type of data is not list(or None).")
			return False
		if (cu == None):
			logging.error("Type of cu is not list(or None).")
			return False
		sql = self.__update_sql % tablename
		d = []
		for i in range(1,len(data)):
			d.append(data[i])
		d.append(data[0])
		d = tuple(d)
		try:
			cu.execute(sql, d)
		except Exception as err:
			logging.warning(str(err))
		return

	def update_tuple(self, tablename = None, data = None):
		if (self.__checkdata(data=data, typename=tuple) == False):
			logging.error("Type of data is not list(or None).")
			return False

		if (self.__checktablename(tablename) == False):
			logging.error("Type of tablename is not list(or None).")
			return False

		cu = self.__get_cu()
		if(cu is not None):
			self.__update(tablename=tablename,
						  cu=cu,
						  data=data)
			try:
				self.__conn.commit()
				logging.info(str(data))
				print("update_tuple" + str(data))
				cu.close()
				return True
			except Exception as err:
				logging.warning(str(err))
				print(str(err))
				return False
		else:
			return False


	'''GetInfo'''
	def fetchall(self, tablename = None):
		if (self.__checktablename(tablename) == False):
			logging.error("Type of tablename is not list(or None).")
			return False
		sql = '''SELECT * FROM %s'''%tablename
		cu = self.__get_cu()
		r = None
		try:
			cu.execute(sql)
			r = cu.fetchall()
			logging.info(sql)
			self.__conn.commit()
			cu.close()
			print(sql)
		except Exception as err:
			logging.warning(str(err))
			print(str(err))
			return False
		return r

	def select(self, args = None, tablename =None):
		r = None
		if (self.__checktablename(tablename) == False):
			logging.error("Type of tablename is not list(or None).")
			return False
		if(type(args) is not list):
			logging.warning("args is not list")
			return False
		sql = self.__select_sql
		t =[]
		flag = 0
		for i in args:
			if(type(i) is not tuple):
				continue
			else:
				if(self.__checkargsi(i[0])==False):
					logging.warning("i[0] is not allowed.")
				else:
					if(i[0] in self.__key_box_ntext):
						flag = 1
						sql = sql +" and " + i[0] + " LIKE ?"
						t.append(i[1])
					else:
						if(i[0] in self.__key_box_int or i[0] in self.__key_box_float):
							flag = 1
							sql = sql + " and " + i[0] + "= ?"
							t.append(i[1])

		if(flag == 0):
			return False
		t = tuple(t)
		sql = sql % tablename
		print(sql)
		try:
			cu = self.__get_cu()
			cu.execute(sql,t)
			r =cu.fetchall()
			cu.close()
			logging.info(sql+str(t))
		except Exception as err:
			logging.warning(str(err))
			print(str(err))
		return r

	def selectByRange(self,tablename = None, latran = (0,0), lngran = (0,0)):
		if(self.__checktablename(tablename)==False):
			logging.error("Type of tablename is not list(or None).")
			print("Type of tablename is not list(or None).")
			return False
		if(self.__checknum(latran)==False or self.__checknum(lngran)==False):
			logging.error("Latran or lngran is not allowed.")
			print("Latran or lngran is not allowed.")
			return False
		sql = self.__selectByRange_sql %(tablename, latran[0], latran[1], lngran[0], lngran[1])
		print(sql)
		cu = self.__get_cu()
		r = None
		try:
			cu.execute(sql)
			r = cu.fetchall()
			print("selectByCircle:" + tablename)
			logging.info("selectByCircle:" + tablename +str(latran)+":"+str(lngran))
		except Exception as err:
			logging.warning(str(err))
			print(str(err))
		return r

	def showTables(self):
		cu = self.__get_cu()
		try:
			cu.execute("SELECT name FROM sqlite_master WHERE type='table'")
			r = cu.fetchall()
			print(r)
			logging.info(r)
			cu.close()
		except Exception as err:
			logging.warning(str(err))
			print(str(err))
			return False
		return r

	def __del__(self):
		self.__conn.close()
		print("close")