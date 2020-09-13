import sqlite3

connection = sqlite3.connect('admin.db')
cursor = connection.cursor()


#delete admin

name = '2'
# tripcode ='TqOzGmy5V.'

cursor.execute('DELETE From admin  WHERE name="{}"'.format(name))
connection.commit()

# #check admin list

# tripcode = 'TqOzGmy5V.'

#cursor.execute('SELECT name From admin ')
#check = cursor.fetchall()
# valid = []
# print()

#admin = ""
#for i in range(len(check)):
#    admin += '@{}\n'.format(check[i][0])
#print(admin)




#procurando admin

# tripcode = 'TqOzGmy5V.'

# cursor.execute('SELECT tripcode From admin  WHERE tripcode="{}"'.format(tripcode))
# check = cursor.fetchall()
# valid = []
# #print(check[0][0])
# if check[0][0] == tripcode:
#       print('e')

# print()

#admin = ""
#for i in range(len(check)):
#    admin += '@{}\n'.format(check[i][0])
#print(admin)




#procurando admin

# tripcode = 'TqOzGmy5V.'

# cursor.execute('SELECT tripcode From admin  WHERE tripcode="{}"'.format(tripcode))
# check = cursor.fetchall()
# valid = []
# #print(check[0][0])
# if check[0][0] == tripcode:
#       print('e')
# else:
#       print('e admin')

#adicionando novo admin
#name = 'londarks'
#tripcode ='TqOzGmy5V.'

#cursor.execute(f"INSERT INTO admin (name,tripcode) VALUES ('{name}','{tripcode}')")
#connection.commit()

#adicionando novo admin
#name = 'londarks'
#tripcode ='TqOzGmy5V.'

#cursor.execute(f"INSERT INTO admin (name,tripcode) VALUES ('{name}','{tripcode}')")
#connection.commit()
