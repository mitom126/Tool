import session
from datetime import datetime, timedelta
import matplotlib
def function1():
    url = 'https://api.vietstock.vn/finance/toptrading?type=7&catID=1'
    headers = {
        'Host': 'api.vietstock.vn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Origin': 'https://finance.vietstock.vn',
        'Referer': 'https://finance.vietstock.vn/',
        'Connection': 'close'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        stock_codes = []
        data = response.json()
        for entry in data:
            stock_code = entry['StockCode']
            stock_codes.append(stock_code)
    print("Top 10 ma co phieu:")
    print(stock_codes)
    return stock_codes
def function2(stock_codes):
    stock_codes=function1()
    end = datetime.now()
    start = end - timedelta(days=30)
    url2 = 'https://finance.vietstock.vn/data/gettradingresult'
    data1 = {
            'Code': stock_codes,
            'OrderBy': '',
            'OrderDirection': 'desc',
            'PageIndex': 1,
            'PageSize': 30,
            'FromDate': start.strftime('%Y-%m-%d'),
            'ToDate': end.strftime('%Y-%m-%d'),
            'ExportType': 'default',
            'Cols': 'TradingDate%2CTime%2CStockCode',
            'ExchangeID': 1,
            '__RequestVerificationToken': 'qdoINiv3-1r8dhM2Nv87wr_ueDvpnpEKrQoGC63VQuZyDk4zc_atDC4TC9CE1bTZaNeXMPAScSVEIrng3XSTO4gu6-VEorD16KTf98N6rio1',
        }

    headers2 = {
        'Cookie': 'language=vi-VN; _pbjs_userid_consent_data=3524755945110770; Theme=Light; _ga_EXMM0DKVEX=GS1.1.1705208243.4.1.1705210012.50.0.0; _ga=GA1.2.490142181.1705163513; AnonymousNotification=; isShowLogin=true; dable_uid=49923647.1705163515001; _gid=GA1.2.554192545.1705163517; __gads=ID=59dc0930680af65a:T=1705163516:RT=1705209911:S=ALNI_MZXqLQ3v4-lbIRf1uma5M_fm0TpYw; __gpi=UID=00000cd9133b3afd:T=1705163516:RT=1705209911:S=ALNI_MbeXYY1ZDHiF--wMyS0ZbOYDVdmmg; ASP.NET_SessionId=uc0vaiwa0ygtrdal5zzi2kop; __RequestVerificationToken=1keH94S8x9Nd9UczG0bhJsQ7ICEbivSj2SODRqaAyB3MhxfwMa7MOjHnGKLyQQXouJ7ya9HeFPcAcme9mv7dX-86rzPIyF3MrGhrzVWemJI1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Accept': '/',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
        }

    resp = requests.post(url2, data=data1, headers=headers2)
    if resp.status_code == 200:
        data = resp.json()['Data']
        for element in data:
                trading_date_str= element.get('TradingDate')
                trading_date = datetime.fromtimestamp(int(trading_date_str[6:-2]) / 1000).strftime('%Y-%m-%d')
                totalVal = element.get('ClosePrice')
                stock_code = element.get('StockCode')
                
                print(f"Stock Code: {stock_code}, Trading Date: {trading_date}, ClosePrice : {totalVal}")
    else:
            print(f"Loi ne: {resp.status_code}")
stock_codes = function1()
print('Nhap ma co phieu trong top 10:')
x = input()
function2(x)
