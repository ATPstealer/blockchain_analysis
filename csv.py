import csv
from datetime import datetime
import mysql.connector


with open('bitcoin.csv', 'r') as read_obj:
    csv_reader = csv.reader(read_obj)
    list_of_csv = list(csv_reader)

    cnx = mysql.connector.connect(user='emailamuli_bc', password='8j$7HRT4GJC7ZB4P', host='77.222.61.40',
                                  database='emailamuli_bc')
    add_price = ("INSERT INTO price (date, price) VALUES (%s, %s)")


    for _ in range(1, len(list_of_csv)-1):
        cursor = cnx.cursor(buffered=True)
        cursor.execute(add_price, (datetime.strptime(list_of_csv[_][0].split(" ")[0], '%Y-%m-%d').date(), list_of_csv[_][1]))
        cnx.commit()
    cursor.close()
    cnx.close()
