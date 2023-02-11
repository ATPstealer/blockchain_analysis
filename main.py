import datetime
from include.bc import BC
import multiprocessing
import mysql.connector

bc = BC()


def handle_tx(tx_id):
    tx = bc.get_transaction(tx_id)
    tx_date = bc.get_tx_date(tx)
    day_uniq_value = 0.0
    month_uniq_value = 0.0
    year_uniq_value = 0.0
    turnover_value = 0.0
    for vin in tx['vin']:
        if "coinbase" not in vin.keys():
            prev_tx = bc.get_transaction(vin['txid'])
            tx_vout = vin['vout']
            if bc.get_tx_date(prev_tx).date() != tx_date.date():
                day_uniq_value += prev_tx['vout'][tx_vout]['value']
                if bc.get_tx_date(prev_tx).month != tx_date.month and bc.get_tx_date(prev_tx).year != tx_date.year:
                    month_uniq_value += prev_tx['vout'][tx_vout]['value']
                    if bc.get_tx_date(prev_tx).year != tx_date.year:
                        year_uniq_value += prev_tx['vout'][tx_vout]['value']
            turnover_value += prev_tx['vout'][tx_vout]['value']
    return day_uniq_value, month_uniq_value, year_uniq_value, turnover_value


if __name__ == '__main__':
    start_block = 774502  # 2023-01-31 23:58:16 last december block
    end_block = 716583  # 2022-01-01 00:13:32 start 2022

    pool_obj = multiprocessing.Pool()

    cnx = mysql.connector.connect(user='emailamuli_bc', password='8j$7HRT4GJC7ZB4P', host='77.222.61.40',
                                  database='emailamuli_bc')
    cursor = cnx.cursor(buffered=True)

    query = ("SELECT * FROM block WHERE block_height=%s")
    add_block = ("INSERT INTO block (block_height, time) VALUES (%s, %s)")
    update_block = ("UPDATE block SET day_uniq_value = %s, month_uniq_value = %s, year_uniq_value = %s, turnover_value = %s WHERE block_height = %s")

    for block_height in range(start_block, end_block - 1, -1):
        cursor.execute(query, (str(block_height),))
        if cursor.rowcount > 0:
            continue

        block = bc.get_block(block_height)
        block_date = bc.get_block_date(block)

        cursor.execute(add_block, (block_height, block_date))
        cnx.commit()

        print(str(block_height) + "  Block time: " + str(block_date) + "  Now: " + str(datetime.datetime.now()))

        collect_day_uniq_value = 0.0
        collect_month_uniq_value = 0.0
        collect_year_uniq_value = 0.0
        collect_turnover_value = 0.0

        # main multi process loop
        block_turnover = pool_obj.map(handle_tx, block['tx'])
        for day_uniq_value, month_uniq_value, year_uniq_value, turnover_value in block_turnover:
            collect_day_uniq_value += day_uniq_value
            collect_month_uniq_value += month_uniq_value
            collect_year_uniq_value += year_uniq_value
            collect_turnover_value += turnover_value

        data_block = (collect_day_uniq_value, collect_month_uniq_value, collect_year_uniq_value, collect_turnover_value, block_height)
        cursor.execute(update_block, data_block)
        cnx.commit()

    cursor.close()
    cnx.close()
