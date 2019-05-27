from cpc_fusion import Web3
import csv


def csv_write(list_result):

    with codecs.open('rnode.csv', 'a', 'gb18030') as f:
        writer = csv.writer(f)
        for item in list_result:
            line = item["addr"] + ", " + item["RPT"]
            writer.writerow(line)


def csv_write_simplied(detailed_info):
    attributes = ["num", "city", "supervision_code", "PJ_title", "addr", "area", "source", "used_for", "method",
                  "useful_life", "category",
                  "soil_level", "price", "pay_num", "scheduled_pay_date", "scheduled_price", "remarks",
                  "owner", "lower_bound", "upper_bound", "scheduled_begin_time",
                  "actual_begin_time", "approver", "scheduled_handing_time", "scheduled_end_time",
                  "actual_end_time", "sign_date"]
    with codecs.open('mengtian_detailed.csv', 'a', 'gb18030') as f:
        writer = csv.writer(f)
        line = []
        for item in attributes:
            line.append(detailed_info[item])
        writer.writerow(line)


def connect():
    cf = Web3(Web3.HTTPProvider('http://3.1.81.79:8501'))
    return cf


def main():

    cf = connect()
    # RNodesList = dict()
    RNodesList = cf.cpc.getRNodes
    print(RNodesList)


if __name__ == '__main__':
    main()
