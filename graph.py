import mysql.connector
import matplotlib.pyplot
import matplotlib.dates
import matplotlib.pyplot as plt


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
list_month_uniq_value = list()
list_year_uniq_value = list()
list_turnover_value = list()

for (id, block_height, time, day_uniq_value, month_uniq_value, year_uniq_value, turnover_value) in cursor:
    if time.date() not in list_time:
        list_time.append(time.date())
        list_day_uniq_value.append(0.0)
        list_month_uniq_value.append(0.0)
        list_year_uniq_value.append(0.0)
        list_turnover_value.append(0.0)
    index = list_time.index(time.date())
    list_day_uniq_value[index] += day_uniq_value
    list_month_uniq_value[index] += month_uniq_value
    list_year_uniq_value[index] += year_uniq_value
    list_turnover_value[index] += turnover_value

dates = matplotlib.dates.date2num(list_time)
matplotlib.pyplot.title("Day uniq and turnover values")
matplotlib.pyplot.plot_date(dates, list_day_uniq_value, 'g', linestyle="-")
matplotlib.pyplot.plot_date(dates, list_turnover_value, 'g', linestyle="--", color="red")
#matplotlib.pyplot.yscale("log")
plt.show()
