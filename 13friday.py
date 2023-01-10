import datetime

def friday_the_13th():
    year = int(input("Enter a year: "))  # ユーザーに年を入力してもらう
    # 年と月を指定して、その年の13日の金曜日を求める
    for month in range(1, 13):
        if datetime.datetime(year, month, 13).weekday() == 4:
            print(datetime.datetime(year, month, 13).strftime("%Y/%m/%d"))
friday_the_13th()
