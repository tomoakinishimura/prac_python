#-*-coding:utf-8-*-

import MySQLdb

conn = MySQLdb.connect(db='scraping',user='scrap',passwd='Nisitomo0226!!', charset='utf8mb4')

c = conn.cursor()
c.execute('drop table if exists cities')

c.execute('''
  create table cities(
    rank integer
    ,city text
    ,population integer
  )
''')

c.execute('insert into cities values (%s,%s,%s)',(1,b'è„äC',24150000))

conn.commit()

c.execute('select * from cities')
for row in c.fetchall():
  print(row)

conn.close()

