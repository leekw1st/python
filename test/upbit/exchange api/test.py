from re import I
import pyupbit
import pprint
import datetime

with open("../upbit.txt") as f:
    lines = f.readlines()
    access = lines[0].strip()
    secret = lines[1].strip()

    # Exchange API 사용을 위한 객체 생성
    upbit = pyupbit.Upbit(access, secret)

    #balances = upbit.get_balances()
    #pprint.pprint(balances)

    # 원화 잔고 조회
    #print(upbit.get_balance(ticker="KRW"))          # 보유 KRW
    #print(upbit.get_amount('ALL'))                  # 총매수금액
    #print(upbit.get_balance(ticker="KRW-BTC"))      # 비트코인 보유수량
    #print(upbit.get_balance(ticker="KRW-XRP"))      # 리플 보유수량
    result = upbit.get_order('KRW-REP', state='done')

    #print(datetime.datetime.strptime(result[0]['created_at'][0:10], '%Y-%m-%d'))
    #print(datetime.datetime.strptime(result[0]['created_at'][11:19], '%H:%M:%S'))


    tmp_time = result[0]['created_at'][0:10] + ' ' + result[0]['created_at'][11:19]
    time_term = datetime.datetime.now() - datetime.datetime.strptime(tmp_time, '%Y-%m-%d %H:%M:%S')
    print(time_term)
    print(time_term.seconds)
    print(time_term.seconds%60)


