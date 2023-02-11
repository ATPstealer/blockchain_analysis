import datetime
import json
from include.bc import BC
import multiprocessing
from pathlib import Path

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


def create_date(date_dict, date):
    if date.year not in date_dict:
        date_dict[date.year] = {"year_uniq_value": 0, "year_turnover_value": 0}
    if date.month not in date_dict[date.year]:
        date_dict[date.year][date.month] = {"month_uniq_value": 0, "month_turnover_value": 0}
    if date.day not in date_dict[date.year][date.month]:
        date_dict[date.year][date.month][date.day] = {"day_uniq_value": 0, "day_turnover_value": 0}


if __name__ == '__main__':
    start_block = 774502  # 2023-01-31 23:58:16 last december block
    end_block = 716583  # 2022-01-01 00:13:32 start 2022
    result_data = dict()
    # with open('result_data.json', 'r') as data:
    #     result_data = json.loads(data.readline())

    pool_obj = multiprocessing.Pool()

    for block_height in range(start_block, end_block - 1, -1):
        block = bc.get_block(block_height)
        block_date = bc.get_block_date(block)
        print(str(block_height) + "  Block time: " + str(block_date) + "  Now: " + str(datetime.datetime.now()))
        create_date(result_data, block_date)

        # main multi process loop
        block_turnover = pool_obj.map(handle_tx, block['tx'])
        for day_uniq_value, month_uniq_value, year_uniq_value, turnover_value in block_turnover:
            result_data[block_date.year][block_date.month][block_date.day]["day_uniq_value"] += day_uniq_value
            result_data[block_date.year][block_date.month]["month_uniq_value"] += month_uniq_value
            result_data[block_date.year]["year_uniq_value"] += year_uniq_value
            result_data[block_date.year][block_date.month][block_date.day]["day_turnover_value"] += turnover_value
            result_data[block_date.year][block_date.month]["month_turnover_value"] += turnover_value
            result_data[block_date.year]["year_turnover_value"] += turnover_value

        try:
            Path("result_data.json").replace("result_data_last.json")
        except:
            print("result_data don't exist")

        with open('result_data.json', 'w') as data:
            data.write(json.dumps(result_data))

        with open('block_id', 'w') as data:
            data.write(str(block_height))
