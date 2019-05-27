# I was trying to crawl data from cpchain.io/explorer/rnode
# but I later realized that using API is much easier
# this file is no more useful :)


import time
import requests
import urllib.parse
import sys
import codecs
import csv
import os



defined_timeout = 100
# url = "https://cpchain.io/explorer/rnode/"


"""
post_data = {"TAB_QuerySubmitPagerData": "3",
             "tabid": "263",
             'wmguid': '75c72564-ffd9-426a-954b-8ac2df0903b7&p=9f2c3acd-0256-4da2-a659-6949c4671a2a%3a2010-9-1%7e2011-9-1%7cec9f9d83-914e-4c57-8c8d-2c57185e912a%3a051%7e%u6279%u53d1%u96f6%u552e%u7528%u5730%7c8fd0232c-aff0-45d1-a726-63fc4c3d8ea9%3a23%7e%u6302%u724c%u51fa%u8ba9'}

"""


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


def addr_parser(content, numOfRnode):

    Rnodes = []
    left_anchor = 0
    right_anchor = 1
    for i in range(0, numOfRnode):
        temp_element = {"addr": "", "RPT": 0}
        left_anchor = content.find(r"/explorer/address/", right_anchor)
        right_anchor = content.find(r"\" ", left_anchor)

        print(left_anchor, right_anchor)
        input()
        temp_element["addr"] = content[left_anchor + 1: right_anchor]

        left_anchor = content.find(r"<div class=\"col-2 text-truncate card-grey\"", right_anchor)
        right_anchor = content.find(r"<", left_anchor)
        # temp_element["RPT"] = int(content[left_anchor + 1: right_anchor])
        temp_element["RPT"] = content[left_anchor + 1: right_anchor]

        # print(content[left_anchor+1: left_anchor+20])
        print(temp_element)
        input()
        Rnodes.append(temp_element)

    return Rnodes


def rnode_parser(numOfRnode):
    # index_url = "https://cpchain.io/explorer/rnode/"
    index_url = "https://cpcstats.com/transactions/0x27e81a296f5b80d319d2f3008f2d5998530e79e4"

    content = requests.post(index_url, timeout=defined_timeout)
    str_content = content.text
    print(str_content)
    detailed_info = addr_parser(str_content, numOfRnode)
    # csv_write_simplied(detailed_info)
    # time.sleep(3)

    # print(detailed_info)
    csv_write(detailed_info)


def main():

    numOfRnode = 10
    url = "https://cpchain.io/explorer/rnode/"

    if len(sys.argv) >= 2:
        numOfRnode = sys.argv[1]
    if len(sys.argv) >= 3:
        url = sys.argv[2]
    print(url)

    rnode_parser(numOfRnode)


if __name__ == '__main__':
    main()
