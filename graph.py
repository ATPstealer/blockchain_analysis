import mysql.connector
import matplotlib.pyplot
import matplotlib.dates
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

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

list_week_time = list()
list_week_uniq_value = list()

list_month_time = list()
list_month_uniq_value = list()

list_year_time = list()
list_year_uniq_value = list()


for (id, block_height, time, day_uniq_value, week_uniq_value, month_uniq_value, year_uniq_value, turnover_value) in cursor:
    if time.date() not in list_time:
        list_time.append(time.date())
        list_day_uniq_value.append(0.0)
        list_turnover_value.append(0.0)
    index = list_time.index(time.date())
    list_day_uniq_value[index] += day_uniq_value
    list_turnover_value[index] += turnover_value

    week = time.date() + timedelta(days=3-time.weekday())
    if week not in list_week_time:
        list_week_time.append(week)
        list_week_uniq_value.append(0.0)
    index = list_week_time.index(week)
    list_week_uniq_value[index] += week_uniq_value

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

# Middle price
list_price_month_time = list()
list_price_month_count = list()
list_price_month = list()
for price, time in zip(list_price, list_price_time):
    month = datetime.strptime(str(time.year) + "-" + str(time.month) + "-15 12:00:00", '%Y-%m-%d %H:%M:%S')
    if month not in list_price_month_time:
         list_price_month_time.append(month)
         list_price_month.append(0.0)
         list_price_month_count.append(0)
    index = list_price_month_time.index(month)
    list_price_month[index] += price
    list_price_month_count[index] += 1
list_price_month_value = [i / j for i, j in zip(list_price_month, list_price_month_count)]


averaging_period = 7
i = 0
middle_price_time = 0
middle_price = 0
list_middle_price_time = list()
list_middle_price = list()
for middle in range(0, len(list_price_time)):
    i += 1
    middle_price_time = list_price_time[middle]
    middle_price += list_price[middle]
    if i == averaging_period:
        list_middle_price_time.append(middle_price_time - timedelta(days=averaging_period/2))
        list_middle_price.append(middle_price/averaging_period)
        i = 0
        middle_price_time = 0
        middle_price = 0

# Average per days
averaging_period = 5
i = 0
middle_time = 0
middle_day_uniq_value = 0
middle_day_turnover_value = 0
list_middle_time = list()
list_middle_day_uniq_value = list()
list_middle_day_turnover_value = list()
for middle in range(0, len(list_time)):
    i += 1
    middle_time = list_time[middle]
    middle_day_uniq_value += list_day_uniq_value[middle]
    middle_day_turnover_value += list_turnover_value[middle]
    if i == averaging_period:
        list_middle_time.append(middle_time - timedelta(days=averaging_period/2))
        list_middle_day_uniq_value.append(middle_day_uniq_value/averaging_period)
        list_middle_day_turnover_value.append(middle_day_turnover_value/averaging_period)
        i = 0
        middle_time = 0
        middle_day_uniq_value = 0
        middle_day_turnover_value = 0

# Middle line
day_middle = 0.0
count = 0
for price in list_day_uniq_value:
    day_middle += price
    count += 1
day_middle /= count

week_middle = 0.0
count = 0
for price in list_week_uniq_value:
    week_middle += price
    count += 1
week_middle /= count

month_middle = 0.0
count = 0
for price in list_month_uniq_value:
    month_middle += price
    count += 1
month_middle /= count

year_middle = 0.0
count = 0
for price in list_year_uniq_value:
    year_middle += price
    count += 1
year_middle /= count

# Capital
list_capital = list()
list_capital_time = list()
for time in list_price_month_time:
    if time in list_month_time:
        list_capital_time.append(time)
        index_1 = list_month_time.index(time)
        index_2 = list_price_month_time.index(time)
        print(list_month_uniq_value[index_1], list_price_month[index_2])
        list_capital.append(list_month_uniq_value[index_1]*list_price_month[index_2])

# Plot
dates = matplotlib.dates.date2num(list_capital_time)
dates_price = matplotlib.dates.date2num(list_middle_price_time)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.title("Capital $ values")
ax2.plot_date(dates, list_capital, 'g')
ax1.plot_date(dates_price, list_middle_price, 'r')
ax2.set_ylabel("Capital $")
ax1.set_ylabel("Price")
# matplotlib.pyplot.yscale("log")
plt.show()

dates = matplotlib.dates.date2num(list_middle_time)
dates_price = matplotlib.dates.date2num(list_middle_price_time)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.title("Day uniq  values")
ax2.axhline(y=day_middle)
ax2.plot_date(dates, list_middle_day_uniq_value, 'g')
ax1.plot_date(dates_price, list_middle_price, 'r')
ax2.set_ylabel("Uniq Green")
ax1.set_ylabel("Price")
# matplotlib.pyplot.yscale("log")
plt.show()

dates = matplotlib.dates.date2num(list_time)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.title("Day uniq  values")
ax2.axhline(y=day_middle)
ax2.plot_date(dates, list_day_uniq_value, markersize=1, color="green")
ax1.plot_date(list_price_time, list_price, 'r')
ax2.set_ylabel("Uniq Green")
ax1.set_ylabel("Price")
# matplotlib.pyplot.yscale("log")
plt.show()

dates = matplotlib.dates.date2num(list_time)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.title("Day turnover")
ax2.plot_date(dates, list_turnover_value, markersize=2, color="green")
ax1.plot_date(list_price_time, list_price, 'r')
ax2.set_ylabel("Turnover green points")
ax1.set_ylabel("Price")
plt.show()

dates = matplotlib.dates.date2num(list_week_time)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.title("Week uniq values")
ax2.axhline(y=week_middle)
ax2.plot_date(dates, list_week_uniq_value, 'g', linestyle="-")
ax1.plot_date(list_price_time, list_price, 'r')
ax2.set_ylabel("Week uniq value")
ax1.set_ylabel("Price")
plt.show()

dates = matplotlib.dates.date2num(list_month_time)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.title("Month uniq values")
ax2.axhline(y=month_middle)
ax2.plot_date(dates, list_month_uniq_value, 'g', linestyle="-")
ax1.plot_date(list_price_time, list_price, 'r')
ax2.set_ylabel("Month uniq value")
ax1.set_ylabel("Price")
plt.show()

dates = matplotlib.dates.date2num(list_year_time)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.title("Year uniq values")
ax2.axhline(y=year_middle)
ax2.plot_date(dates, list_year_uniq_value, 'g', linestyle="-")
ax1.plot_date(list_price_time, list_price, 'r')
ax2.set_ylabel("Year uniq value")
ax1.set_ylabel("Price")
plt.show()
