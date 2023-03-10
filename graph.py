import mysql.connector
import matplotlib.pyplot
import matplotlib.dates
import matplotlib.pyplot as plt
from datetime import datetime


query = ("SELECT * FROM block order by time")
try:
    cnx = mysql.connector.connect(user='emailamuli_bc', password='8j$7HRT4GJC7ZB4P', host='77.222.61.40',
                                  database='emailamuli_bc')
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query, ())
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))


list_time = list()
list_day_uniq_value = list()
list_turnover_value = list()

list_month_time = list()
list_month_uniq_value = list()

list_year_time = list()
list_year_uniq_value = list()


for (id, block_height, time, day_uniq_value, month_uniq_value, year_uniq_value, turnover_value) in cursor:
    if time.date() not in list_time:
        list_time.append(time.date())
        list_day_uniq_value.append(0.0)
        list_turnover_value.append(0.0)
    index = list_time.index(time.date())
    list_day_uniq_value[index] += day_uniq_value
    list_turnover_value[index] += turnover_value

    month = datetime.strptime(str(time.year) + "-" + str(time.month) + "-15 12:00:00", '%Y-%m-%d %H:%M:%S')
    if month not in list_month_time:
        list_month_time.append(month)
        list_month_uniq_value.append(0.0)
    index = list_month_time.index(month)
    list_month_uniq_value[index] += month_uniq_value

    year = datetime.strptime(str(time.year) + "-06-15 12:00:00", '%Y-%m-%d %H:%M:%S')
    if year not in list_year_time:
        list_year_time.append(year)
        list_year_uniq_value.append(0.0)
    index = list_year_time.index(year)
    list_year_uniq_value[index] += year_uniq_value

for index in range(0, len(list_day_uniq_value)):
    if list_day_uniq_value[index] > 40000000:
        print(str(list_time[index]) + " " + str(list_day_uniq_value[index]))

query = ("SELECT * FROM price order by date")
try:
    cursor.execute(query, ())
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))

list_price_time = list()
list_price = list()
for (id, date, price) in cursor:
    list_price_time.append(date)
    list_price.append(price)

dates = matplotlib.dates.date2num(list_time)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.title("Day uniq  values")
ax1.plot_date(dates, list_day_uniq_value, markersize=1, color="green")
ax2.plot_date(list_price_time, list_price, 'r')
ax1.set_ylabel("Uniq Green")
ax2.set_ylabel("Price")
# matplotlib.pyplot.yscale("log")
plt.show()

dates = matplotlib.dates.date2num(list_time)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.title("Day turnover")
ax1.plot_date(dates, list_turnover_value, markersize=2, color="green")
ax2.plot_date(list_price_time, list_price, 'r')
ax1.set_ylabel("Turnover green points")
ax2.set_ylabel("Price")
plt.show()

dates = matplotlib.dates.date2num(list_month_time)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.title("Month uniq values")
ax1.plot_date(dates, list_month_uniq_value, 'g', linestyle="-")
ax2.plot_date(list_price_time, list_price, 'r')
ax1.set_ylabel("Month uniq value")
ax2.set_ylabel("Price")
plt.show()


dates = matplotlib.dates.date2num(list_year_time)
matplotlib.pyplot.title("Year uniq values")
matplotlib.pyplot.plot_date(dates, list_year_uniq_value, 'g', linestyle="-")
plt.show()