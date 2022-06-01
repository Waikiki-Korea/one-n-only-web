import cv2 as cv
import numpy as np
import datetime as pydatetime
import psycopg2
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from ono.models import Token, Crawled, TempUrl
import os


def compare_image(file_path):
    cur_path = os.path.dirname(os.path.abspath(__file__))
    print("cur exec file path = ", cur_path)
    print("[compare_image] file_path = ", file_path)
    time_start = pydatetime.datetime.now()

    # base 이미지 전처리
    base_img = cv.imread(file_path)
    hsv_base = cv.cvtColor(base_img, cv.COLOR_BGR2HSV)

    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges
    channels = [0, 1]

    hist_base = cv.calcHist([hsv_base], channels, None,
                            histSize, ranges, accumulate=False)
    cv.normalize(hist_base, hist_base, alpha=0,
                 beta=1, norm_type=cv.NORM_MINMAX)

    compare_method = cv.HISTCMP_CORREL
    temp_url_list = list(TempUrl.objects.all())
    token_list = list(Token.objects.all())

    max_similarity = 0
    max_path = ''

    for item in temp_url_list:
        product_img_url = item.ipfs_path

        # url 이미지 임시 저장 경로. 종료 시 삭제
        urllib.request.urlretrieve(product_img_url, cur_path+'/image.png')
        hsv_target = cv.cvtColor(
            cv.imread(cur_path+'/image.png'), cv.COLOR_BGR2HSV)
        hist_target = cv.calcHist(
            [hsv_target], channels, None, histSize, ranges, accumulate=False)
        cv.normalize(hsv_target, hsv_target, alpha=0,
                     beta=1, norm_type=cv.NORM_MINMAX)

        similarity = cv.compareHist(hist_base, hist_target, compare_method)

        if (similarity > 1.0):
            similarity = 1.0
        elif (similarity < 0.0):
            similarity = 0.0

        if (similarity > max_similarity):
            max_similarity = similarity
            max_path = item.ipfs_path

        print('[temp] similarity : ', similarity)

    for item in token_list:
        product_img_url = item.ipfs_path

        urllib.request.urlretrieve(product_img_url, cur_path+'/image.png') # url 이미지 임시 저장 경로. 종료 시 삭제
        hsv_target = cv.cvtColor(cv.imread(cur_path+'/image.png'), cv.COLOR_BGR2HSV)
        hist_target = cv.calcHist([hsv_target], channels, None, histSize, ranges, accumulate=False)
        cv.normalize(hsv_target, hsv_target, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)

        similarity = cv.compareHist(hist_base, hist_target, compare_method)

        if (similarity > 1.0):
            similarity = 1.0
        elif (similarity < 0.0):
            similarity = 0.0

        if (similarity > max_similarity) :
            max_similarity = similarity
            max_path = item.ipfs_path

        print('[token] similarity : ', similarity)

    time_finish = pydatetime.datetime.now()

    os.remove(cur_path+'/image.png') # 임시 저장 경로 파일 삭제
    
    print("[compare_image] Time duration : ", time_finish - time_start)

    if(max_similarity >= 1.0) :
        response = {
            "result": "unsuccessful",
            "reason": "identical image already exists",
            "similarity": max_similarity*100,
            "path": max_path,
            "duration": time_finish - time_start
        }
    else :
        response = {
            "result": "successful",
            "reason": "OK",
            "similarity": max_similarity*100,
            "path": max_path,
            "duration": time_finish - time_start
        }

    return response


# def testComparison(file_path):
#     cur_path= os.path.dirname(os.path.abspath(__file__))
#     print("cur exec file path = ", cur_path)
#     print("[testComparison] file_path = ", file_path)
#     time_start = pydatetime.datetime.now()

#     #base 이미지 전처리
#     base_img = cv.imread(file_path)
#     hsv_base = cv.cvtColor(base_img, cv.COLOR_BGR2HSV)

#     h_bins = 50
#     s_bins = 60
#     histSize = [h_bins, s_bins]
#     h_ranges = [0, 180]
#     s_ranges = [0, 256]
#     ranges = h_ranges + s_ranges
#     channels = [0, 1]

#     hist_base = cv.calcHist([hsv_base], channels, None, histSize, ranges, accumulate=False)
#     cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)

#     compare_method = cv.HISTCMP_CORREL

#     # webdriver 실행
#     #options = webdriver.ChromeOptions()
#     #options.add_argument("headless")

#     # dr = webdriver.Chrome(cur_path+'/chromedriver', options=options) #(linux)chromedriver 설치 경로
#     #dr = webdriver.Chrome(cur_path+'/chromedriver.exe', options=options) #(windows)chromedriver.exe 설치 경로

#     temp_url_list = list(TempUrl.objects.all())

#     max_similarity = 0
#     max_path=''
#     for item in temp_url_list:
#         # target page 접근
#         #dr.get(item.ipfs_path)

#         #html source 추출
#         #html_source = dr.page_source

#         #soup = BeautifulSoup(html_source, 'html.parser')
#         product_img_url = item.ipfs_path
#         urllib.request.urlretrieve(product_img_url, cur_path+'/image.png') #url 이미지 임시 저장 경로. 종료 시 삭제
#         hsv_target = cv.cvtColor(cv.imread(cur_path+'/image.png'), cv.COLOR_BGR2HSV)
#         hist_target = cv.calcHist([hsv_target], channels, None, histSize, ranges, accumulate=False)
#         cv.normalize(hsv_target, hsv_target, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)

#         similarity = cv.compareHist(hist_base, hist_target, compare_method)

#         similarity = 1.0 if (similarity > 1.0) else similarity
#         similarity = 0.0 if (similarity < 0.0) else similarity

#         if (similarity > max_similarity) :
#             max_similarity = similarity
#             max_path = item.ipfs_path

#         print('similarity : ', similarity)

#     time_finish = pydatetime.datetime.now()

#     os.remove(cur_path+'/image.png') #임시 저장 경로 파일 삭제
    
#     print("[testComparison] Time duration : ", time_finish - time_start)

#     if(max_similarity >= 1.0) :
#         response = {
#             "result": "unsuccessful",
#             "reason": "identical image already exists",
#             "similarity": max_similarity*100,
#             "path": max_path,
#             "duration": time_finish - time_start
#         }
#     else :
#         response = {
#             "result": "successful",
#             "reason": "OK",
#             "similarity": max_similarity*100,
#             "path": max_path,
#             "duration": time_finish - time_start
#         }

#     return response
