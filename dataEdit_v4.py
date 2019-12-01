# /Users/Juhun/PycharmProjects/simon_frypan/data : 데이터 파일 경로
# 0stim 1mapping 2updn 3orin 4setAns 5corrAns 6crrspndnc 7cndtn 8exp_A_key.keys 9crr 10rt 11participant

import csv
import os
import glob
import pandas as pd

df = []
tdf = []
m1df = pd.DataFrame()
m2df = pd.DataFrame()
m1avg = 0
m2avg = 0
m1cndtn1 = pd.DataFrame()
m1cndtn2 = pd.DataFrame()
m1cndtn3 = pd.DataFrame()
m1cndtn4 = pd.DataFrame()
m1cndtn1avg = pd.DataFrame(columns= ["crrspndnc", "rt"])
m1cndtn2avg = pd.DataFrame(columns= ["crrspndnc", "rt"])
m1cndtn3avg = pd.DataFrame(columns= ["crrspndnc", "rt"])
m1cndtn4avg = pd.DataFrame(columns= ["crrspndnc", "rt"])
m2cndtn1 = pd.DataFrame()
m2cndtn2 = pd.DataFrame()
m2cndtn3 = pd.DataFrame()
m2cndtn4 = pd.DataFrame()
m2cndtn1avg = pd.DataFrame(columns= ["crrspndnc", "rt"])
m2cndtn2avg = pd.DataFrame(columns= ["crrspndnc", "rt"])
m2cndtn3avg = pd.DataFrame(columns= ["crrspndnc", "rt"])
m2cndtn4avg = pd.DataFrame(columns= ["crrspndnc", "rt"])
csvCounter = 0
filenum = 1
missing = 0
missing_list = []
ans = input("몇 명?: ")                                              #    참가자 수 입력
numprt = int(ans)

homeDir = os.path.expanduser('~')   #   파일 저장 경로 코드     #-----------------------------------------------------------
targetDir = "%s/PycharmProjects/simon_frypan/" % homeDir
resultDir = targetDir + "output/"
rpt_resultDir = resultDir + "report/"
if not os.path.exists(resultDir):                                   #   경로 설정
    os.mkdir(resultDir)
if not os.path.exists(rpt_resultDir):                                   #   경로 설정
    os.mkdir(rpt_resultDir)
path = targetDir + "data/"
file_list = os.listdir(path)
if ".DS_Store" in file_list:
    file_list.remove(".DS_Store")                                       #   맥에서 자동 생성하는 파일을 삭제.

for file in file_list:  #   파일 로딩   #---------------------------------------------------------------------------------
    print("%d번째 로딩된 파일: " % filenum, file)                      #   불러들인 대상 프린트
    df = pd.read_csv(path + file)                                  #   csv파일 로드
    prt = df.participant[0]                                        #   prt변인에 csv의 "participant"열에 담긴 참가자 번호 추출
    # print(prt)
    df.drop(df.iloc[:, 8:19], axis="columns", inplace = True)      #    쓸모없는 열 제거
    df.drop(df.iloc[:, 12:], axis="columns", inplace = True)
    df.rename(columns = {"exp_A_key.corr": "crr"}, inplace = True)  #   정반응열과 반응시간 열의 인덱스 쉬운이름 바꾸기
    df.rename(columns = {"exp_A_key.rt": "rt"}, inplace = True)
    df.sort_values(["cndtn"], ascending = [True], inplace = True)   #   조건에 맞춰서 행을 재정렬
    df.reset_index(drop = True, inplace = True)
    dfrow = int(len(df))

    report = pd.DataFrame() #   교수님 파일 편집 코드    #-------------------------------------------------------------------
    report = report.append(df)
    report.drop(report.iloc[:, 11:12], axis="columns", inplace = True)
    report.drop(report.iloc[:, 7:9], axis="columns", inplace = True)
    report.drop(report.iloc[:, 5:6], axis="columns", inplace = True)
    report.to_csv(rpt_resultDir + "%s.csv" % prt)
    # print(report)
    # print(df)

    ctff = 0.7  #   극단치 제거 프로세스     #-------------------------------------------------------------------------------
    pcnt = 1  # 처리 횟수
    if df.mapping[0] == 1:
        for row1 in range(dfrow):
            if df.iloc[row1, 9] == 0:           #   "row1"번째 행의 "9"번째 열, 즉 crr(정답)열의 값이 "0(오답)"이라면
                df.iloc[row1, 10] = None        #   "row1"번째 행의 "10"번째 열, 즉 rt(반응시간)열의 값을 "None(결측치)"로 입력한.

        while True:
            m1ctff_bff = pd.DataFrame()
            m1ctff_bff = m1ctff_bff.append(df)
            m1row = len(m1ctff_bff)
            m1rtcnt = m1ctff_bff.rt.count()
            for row2 in range(m1row):
                if m1ctff_bff.iloc[row2, 10] >= ctff:
                    m1ctff_bff.iloc[row2, 10] = None

            m1rtcnt2 = m1ctff_bff.rt.count()
            m1prcnt = 100 - (m1rtcnt2 / m1rtcnt * 100)
            if m1prcnt < 7.5:
                break
            else:
                ctff += 0.1
                pcnt += 1

        print(prt, "mapping 1")
        print("처리 횟수: ", pcnt)
        print("컷 오프 라인: ", ctff)
        print("처리 전 m1 데이터 개수: ", m1rtcnt)
        print("처리 후 m1 데이터 개수: ", m1rtcnt2)
        print("제거된 데이터 퍼센트: ", m1prcnt)
        print("")
        m1df = m1df.append(m1ctff_bff)
    elif df.mapping[0] == 2:
        for row1 in range(dfrow):
            if df.iloc[row1, 9] == 0:
                df.iloc[row1, 10] = None
        while True:
            m2ctff_bff = pd.DataFrame()
            m2ctff_bff = m2ctff_bff.append(df)
            m2row = len(m2ctff_bff)
            m2rtcnt = m2ctff_bff.rt.count()

            for row2 in range(m2row):
                if m2ctff_bff.iloc[row2, 10] >= ctff:   # "10"번째 열, rt열 값이 "m2ctff"보다 크면
                    m2ctff_bff.iloc[row2, 10] = None      # 그 "rt"값을 "None(결측치)"로 입력한다.
            m2rtcnt2 = m2ctff_bff.rt.count()
            m2prcnt = 100 - (m2rtcnt2 / m2rtcnt * 100)
            if m2prcnt < 7.5:
                break
            ctff += 0.1
            pcnt += 1
        print(prt, "mapping 2")
        print("처리 횟수: ", pcnt)
        print("컷 오프 라인: ", ctff)
        print("처리 전 m1 데이터 개수: ", m2rtcnt)
        print("처리 후 m1 데이터 개수: ", m2rtcnt2)
        print("제거된 데이터 퍼센트: ", m2prcnt)
        print("")
        m2df = m2df.append(m2ctff_bff)

    filenum += 1
    m1ctff_bff = df
# m2df.to_csv(resultDir + "m2df.csv")

for row in range(numprt):   #   데이터 조건별 평균 계산   #-------------------------------------------------------------------
    num = row + 1
    # cmp_prt = "%da" % num
    if (m1df["participant"] == "%da" % num).any() == True:
        m1cndtn1 = m1df[(m1df["cndtn"] == 1) & (m1df["participant"] == "%da" % num)]
        m1cndtn2 = m1df[(m1df["cndtn"] == 2) & (m1df["participant"] == "%da" % num)]
        m1cndtn3 = m1df[(m1df["cndtn"] == 3) & (m1df["participant"] == "%da" % num)]
        m1cndtn4 = m1df[(m1df["cndtn"] == 4) & (m1df["participant"] == "%da" % num)]
        m1cndtn1avg.loc[row] = [m1cndtn1.iloc[0, 6], m1cndtn1["rt"].mean()]
        m1cndtn2avg.loc[row] = [m1cndtn2.iloc[0, 6], m1cndtn2["rt"].mean()]
        m1cndtn3avg.loc[row] = [m1cndtn3.iloc[0, 6], m1cndtn3["rt"].mean()]
        m1cndtn4avg.loc[row] = [m1cndtn4.iloc[0, 6], m1cndtn4["rt"].mean()]

    else:
        # print("There is no data")
        missing += 1
        m1cndtn1avg.loc[row] = [None, None]
        m1cndtn2avg.loc[row] = [None, None]
        m1cndtn3avg.loc[row] = [None, None]
        m1cndtn4avg.loc[row] = [None, None]
        missing_list.append("%da" % num)

for row in range(numprt):
    num = row + 1
    if (m2df["participant"] == "%db" % num).any() == True:
        m2cndtn1 = m2df[(m2df["cndtn"] == 1) & (m2df["participant"] == "%db" % num)]
        m2cndtn2 = m2df[(m2df["cndtn"] == 2) & (m2df["participant"] == "%db" % num)]
        m2cndtn3 = m2df[(m2df["cndtn"] == 3) & (m2df["participant"] == "%db" % num)]
        m2cndtn4 = m2df[(m2df["cndtn"] == 4) & (m2df["participant"] == "%db" % num)]
        m2cndtn1avg.loc[row] = [m2cndtn1.iloc[0, 6], m2cndtn1["rt"].mean()]
        m2cndtn2avg.loc[row] = [m2cndtn2.iloc[0, 6], m2cndtn2["rt"].mean()]
        m2cndtn3avg.loc[row] = [m2cndtn3.iloc[0, 6], m2cndtn3["rt"].mean()]
        m2cndtn4avg.loc[row] = [m2cndtn4.iloc[0, 6], m2cndtn4["rt"].mean()]

    else:
        # print("There is no data")
        missing += 1
        m2cndtn1avg.loc[row] = [None, None]
        m2cndtn2avg.loc[row] = [None, None]
        m2cndtn3avg.loc[row] = [None, None]
        m2cndtn4avg.loc[row] = [None, None]
        missing_list.append("%db" % num)


# m1cndtn1avg = m1cndtn1avg.append([m1cndtn1avg["rt"].mean()])  #분석파일 만들때 주석 처리하기   ------------------------------
# m1cndtn2avg = m1cndtn2avg.append([m1cndtn2avg["rt"].mean()])
# m1cndtn3avg = m1cndtn3avg.append([m1cndtn3avg["rt"].mean()])
# m1cndtn4avg = m1cndtn4avg.append([m1cndtn4avg["rt"].mean()])

# m2cndtn1avg = m2cndtn1avg.append([m2cndtn1avg["rt"].mean()])
# m2cndtn2avg = m2cndtn2avg.append([m2cndtn2avg["rt"].mean()])
# m2cndtn3avg = m2cndtn3avg.append([m2cndtn3avg["rt"].mean()])
# m2cndtn4avg = m2cndtn4avg.append([m2cndtn4avg["rt"].mean()])

# m1cndtn1avg.to_csv(resultDir + "m1_dn_l_crrs.csv", index = False)
# m1cndtn2avg.to_csv(resultDir + "m1_up_r_crrs.csv", index = False)
# m1cndtn3avg.to_csv(resultDir + "m1_up_l_ncrrs.csv", index = False)
# m1cndtn4avg.to_csv(resultDir + "m1_dn_r_ncrrs.csv", index = False)
# m2cndtn1avg.to_csv(resultDir + "m2_up_l_crrs.csv", index = False)
# m2cndtn2avg.to_csv(resultDir + "m2_dn_r_crrs.csv", index = False)
# m2cndtn3avg.to_csv(resultDir + "m2_dn_l_ncrrs.csv", index = False)
# m2cndtn4avg.to_csv(resultDir + "m2_up_r_ncrrs.csv", index = False)

#   편집 파일 저장    #----------------------------------------------------------------------------------------------------
rst = pd.DataFrame(columns= ["m1_dn_l_crrs", "m1_up_l_ncrrs", "m1_up_r_crrs", "m1_dn_r_ncrrs", "m2_up_l_crrs", "m2_dn_l_ncrrs", "m2_dn_r_crrs", "m2_up_r_ncrrs"])
rst["m1_dn_l_crrs"] = m1cndtn1avg["rt"]
rst["m1_up_l_ncrrs"] = m1cndtn3avg["rt"]
rst["m1_up_r_crrs"] = m1cndtn2avg["rt"]
rst["m1_dn_r_ncrrs"] = m1cndtn4avg["rt"]
rst["m2_up_l_crrs"] = m2cndtn1avg["rt"]
rst["m2_dn_l_ncrrs"] = m2cndtn3avg["rt"]
rst["m2_dn_r_crrs"] = m2cndtn2avg["rt"]
rst["m2_up_r_ncrrs"] = m2cndtn4avg["rt"]
print("%d개의 데이터가 빠져있습니다." % missing, "다음과 같습니다: ", missing_list)
print("처리된 결과는 다음과 같습니다.")
print(rst)
rst.to_csv(resultDir + "result.csv")

