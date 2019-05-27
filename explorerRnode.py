import time
import requests
import urllib.parse
import sys
import codecs
import csv


defined_timeout = 100
# url = "https://cpchain.io/explorer/rnode/"


"""
post_data = {"TAB_QuerySubmitPagerData": "3",
             "tabid": "263",
             'wmguid': '75c72564-ffd9-426a-954b-8ac2df0903b7&p=9f2c3acd-0256-4da2-a659-6949c4671a2a%3a2010-9-1%7e2011-9-1%7cec9f9d83-914e-4c57-8c8d-2c57185e912a%3a051%7e%u6279%u53d1%u96f6%u552e%u7528%u5730%7c8fd0232c-aff0-45d1-a726-63fc4c3d8ea9%3a23%7e%u6302%u724c%u51fa%u8ba9'}

"""


def csv_write(list_result):
    attributes = ["num", "city", "supervision_code", "PJ_title", "addr", "area", "source", "used_for", "method",
                  "useful_life", "category",
                  "soil_level", "price", "pay_num", "scheduled_pay_date", "scheduled_price", "remarks",
                  "owner", "lower_bound", "upper_bound", "scheduled_handing_time",
                  "scheduled_begin_time", "scheduled_end_time", "actual_begin_time", "actual_end_time",
                  "approver", "sign_date"]
    with codecs.open('mengtian_detailed.csv', 'a', 'gb18030') as f:
        writer = csv.writer(f)
        for item in list_result:
            line = []
            for item2 in attributes:
                line.append(item[item2])
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


def addr_parser(content, num):
    temp_element = {"num": num, "addr": "", RPT: 0}
    deliminator_key = "/explorer/address/"
    temp_element["city"] = content[left_anchor + 1: right_anchor]

    left_anchor = content.find("<div class=\"col-2 text-truncate card-grey\"", right_anchor)
    right_anchor = content.find("<", left_anchor)
    temp_element["RPT"] = int(content[left_anchor + 1: right_anchor])


    # print(content[left_anchor+1: left_anchor+20])
    print(temp_element)
    return temp_element


def land_parser(content):
    number_key = "gridTdNumber"
    content_key = "queryCellBordy"
    addr_key = "_blank"
    list_result = []
    temp_anchor = content.find(number_key)
    index_url = "http://www.landchina.com/"

    while(temp_anchor != -1):
        temp_element = {"num": "", "city": "", "addr": "", "area": "", "used_for": "", "method": "", "date": "",
                        "addr_link": ""}
        left_anchor = content.find(">", temp_anchor)
        right_anchor = content.find("<", left_anchor)
        print(content[left_anchor + 1:right_anchor - 1])
        temp_element["num"] = content[left_anchor + 1:right_anchor - 1]

        left_anchor = content.find(content_key, right_anchor)
        left_anchor = content.find(">", left_anchor)
        right_anchor = content.find("<", left_anchor)
        # temp_element['city'] = content[left_anchor + 1:right_anchor]

        left_anchor = content.find("default.aspx", right_anchor)
        right_anchor = content.find("target=", left_anchor)
        temp_element['addr_link'] = content[left_anchor:right_anchor - 2]
        try:
            addr_content = requests.post(index_url + temp_element['addr_link'], timeout=defined_timeout)
            str_content = addr_content.text
            detailed_info = addr_parser(str_content, temp_element["num"])
            list_result.append(detailed_info)
            # csv_write_simplied(detailed_info)
            # time.sleep(3)
        except:
        pass
            # raise

        temp_anchor = content.find(number_key, right_anchor)


        """
        left_anchor = content.find(addr_key, right_anchor)
        left_anchor = content.find(">", left_anchor)
        right_anchor = content.find("<", left_anchor)
        temp_element['addr'] = content[left_anchor + 1:right_anchor]

        left_anchor = content.find(content_key, right_anchor)
        left_anchor = content.find(">", left_anchor)
        right_anchor = content.find("<", left_anchor)
        temp_element['area'] = content[left_anchor + 1:right_anchor]

        left_anchor = content.find(content_key, right_anchor)
        left_anchor = content.find(">", left_anchor)
        right_anchor = content.find("<", left_anchor)
        temp_element['used_for'] = content[left_anchor + 1:right_anchor]

        left_anchor = content.find(content_key, right_anchor)
        left_anchor = content.find(">", left_anchor)
        right_anchor = content.find("<", left_anchor)
        temp_element['method'] = content[left_anchor + 1:right_anchor]

        left_anchor = content.find(content_key, right_anchor)
        left_anchor = content.find(">", left_anchor)
        right_anchor = content.find("<", left_anchor)
        temp_element['date'] = content[left_anchor + 1:right_anchor]
        """

    # print(list_result)
    csv_write(list_result)


def main():
    begin_page = "1"
    url = "https://cpchain.io/explorer/rnode/"

    if len(sys.argv) >= 2:
        url = sys.argv[1]
    if len(sys.argv) >= 3:
        begin_page = sys.argv[2]
    print(url)

    post_data = {"TAB_QuerySubmitPagerData": begin_page}

    content = requests.post(url, data=post_data, timeout=defined_timeout)
    str_content = content.text
    max_page_key = "previousSibling.value"
    left_anchor = str_content.find(max_page_key)
    right_anchor = str_content.find(")", left_anchor)
    max_page = str_content[left_anchor + 1 + len(max_page_key):right_anchor]
    print(int(max_page))

    # with codecs.open('mengtian.out', 'w', 'gbk') as f:
    #    f.write(str_content)

    land_parser(str_content)
    # max_page = 2
    for i in range(int(begin_page), int(max_page)):
        try:
            post_data["TAB_QuerySubmitPagerData"] = i + 1
            content = requests.post(url, data=post_data, timeout=defined_timeout)
            str_content = content.text
            land_parser(str_content)
        except:
            i -= 1
            # raise

        time.sleep(5)
        # print(str_content)


if __name__ == '__main__':
    main()
