# This is for generate a csv file illustrating
# the relationship between RPT and number of mined blocks in 24 hours
# The RNodes info are retrieved via CPC fusion APIs
# And the number of mined blocks are crawled from cpcstates.com
# Thanks to Erwin_nl@telegram's spectacular website :)

from cpc_fusion import Web3
import requests
import csv
import codecs
import time


defined_timeout = 100


# it is for writing the csv
def csv_write(list_result):

    # open a csv
    # each line in csv is a tuple containing address, rpt and number of blocks
    with codecs.open('rnode.csv', 'w', 'gb18030') as f:
        writer = csv.writer(f)
        for item in list_result:
            line = []
            line.append(item["Address"])
            line.append(str(item["Rpt"]))
            line.append(str(item["Block"]))
            writer.writerow(line)


# it is for crawl data from cpcstats.com
def mined_blocks_parser(rnode):
    addr = rnode["Address"]
    # index_url = "https://cpchain.io/explorer/rnode/"
    index_url = "https://cpcstats.com/transactions/" + addr

    content = requests.post(index_url, timeout=defined_timeout)

    str_content = content.text
    # print(str_content)

    # locate the number of blocks in the website
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


# initiate the connection
def connect():
    cf = Web3(Web3.HTTPProvider('http://127.0.0.1:8501'))
    return cf


def main():

    cf = connect()

    # a list of dictionary, containing info for each RNode
    RNodes_list = cf.cpc.getRNodes
    RNodes_list_with_blocks = []

    # traverse all RNodes
    for item in RNodes_list:
        try:
            item = mined_blocks_parser(item)
            RNodes_list_with_blocks.append(item)
            # sleep 10 seconds
            time.sleep(10)
        except:
            # save all crawled data if connection fails
            print("Connection error")
            break

    # write down RNodes info in csv format
    csv_write(RNodes_list_with_blocks)
    # print(RNodes_list_with_blocks)


if __name__ == '__main__':
    main()
