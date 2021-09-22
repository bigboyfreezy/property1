import pymysql
def conn():
    conn = pymysql.connect(host='localhost',user='root', password='', database='property')

    return conn