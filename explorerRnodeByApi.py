from cpc_fusion import Web3
import requests
import csv
import codecs
import time


defined_timeout = 100


def csv_write(list_result):

    with codecs.open('rnode.csv', 'w', 'gb18030') as f:
        writer = csv.writer(f)
        for item in list_result:
            line = []
            line.append(item["Address"])
            line.append(str(item["Rpt"]))
            line.append(str(item["Block"]))
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


def mined_blocks_parser(rnode):
    addr = rnode["Address"]
    # index_url = "https://cpchain.io/explorer/rnode/"
    index_url = "https://cpcstats.com/transactions/" + addr

    content = requests.post(index_url, timeout=defined_timeout)

    str_content = content.text
    # print(str_content)

    left_anchor = str_content.find(r"Mined blocks :", 0)
    left_anchor = str_content.find(r": ", left_anchor)
    right_anchor = str_content.find(u"\xa0", left_anchor+1)

    print(index_url)
    print(left_anchor, right_anchor)
    # input()
    blocks = str_content[left_anchor + 1: right_anchor]
    try:
        rnode["Block"] = int(blocks)
    except ValueError:
        rnode["Block"] = 0
    print(str_content[left_anchor + 1: right_anchor])

    print(rnode)
    # csv_write(detailed_info)
    return rnode


def connect():
    cf = Web3(Web3.HTTPProvider('http://3.1.81.79:8501'))
    return cf


def main():

    cf = connect()
    # RNodesList = dict()
    RNodes_list = cf.cpc.getRNodes
    RNodes_list_with_blocks = []
    for item in RNodes_list:

        try:
            item = mined_blocks_parser(item)
        except ConnectionError:
            time.sleep(10)
            print("Connection error")
        RNodes_list_with_blocks.append(item)

    csv_write(RNodes_list_with_blocks)
    #print(RNodes_list_with_blocks)


if __name__ == '__main__':
    main()
