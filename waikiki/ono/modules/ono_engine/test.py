from turtle import end_fill
import cv2 as cv
import numpy as np
from os import listdir
from os.path import isfile, join
import datetime as pydatetime
from ono.models import Token, Crawled

def testComparison(ipfs_path):
    print("[testComparison] ipfs_path = ", ipfs_path)
    time_start = pydatetime.datetime.now()

    '''
    여기서 이미지 처리

    예)
    Crawled table의 자료를 가져올 때는,
    crawledList = list(Crawled.objects.filter()) # 다 가져오기
    또는
    crawledItem = Crawled.objects.get(id=1) # 1번 DB에 있는 것만 가져오기
    crawledItem.ipfs_path # 저장되어있는 ipfs_path 에 접근
    # Crawled data의 항목들은 waikiki/ono/models.py 의 class Crawled(models.Model) 참조
    '''
    similarity = 99.999

    time_finish = pydatetime.datetime.now()
    print("[testComparison] Time duration : ", time_finish - time_start)

    response = {
        "result": "successful",
        "reason": "OK",
        "similarity": similarity,
        "duration": time_finish - time_start
    }
    return response

### [DELETE THIS][TESTCODE][S] {
# from ono.models import TestInfo

# def printTest(s):
#     ti = TestInfo.objects.get(id=1)
#     print("[PrintTest] " + s)
#     print("[PrintTest] " + ti.user_name)
#     print("[PrintTest] " + str(ti.image))
### [DELETE THIS][TESTCODE][E] }