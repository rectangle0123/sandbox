from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import sessionmaker

from database import Base, engine 
from models import Employee, Position
from utils import MemcachedUtils

# セッション
Session = sessionmaker(engine)

def main():
    """ メインプログラム """
    try:
        while True:
            ope = input('メインメニュー: [N]名前検索 [Y]勤続年検索 [Q]システム終了 > ')
            if ope == 'N':
                search_by_name()
            elif ope == 'Y':
                search_by_years()
            elif ope == 'Q':
                exit()

    except KeyboardInterrupt:
        print('\n')
        exit()

def search_action(func):
    """ 検索デコレータ """
    def wrapper(*args, **kwargs):
        # セッション準備
        with engine.connect() as connection:
            with Session(bind=connection) as session:
                # 検索実施
                items = func(session)
                # 結果出力
                for item in items:
                    print(item)
    return wrapper

@search_action
def search_by_name(session: Session):
    """ 名前検索 """
    employees = []
    while True:
        name = input('名前検索: 名前を入力してください > ')
        # 入力がない場合は検索しない
        if not name:
            continue
        # キャッシュを探す
        cached = MemcachedUtils.get(name)
        if cached:
            print('DEBUG: Found in memcached.')
            for e in cached:
                print(e)
            break
        # キャッシュになければ検索する
        employees = session.query(Employee).filter(Employee.name.like(f'%\\{name}%', escape='\\')).all()
        if not employees:
            print('該当するデータがありませんでした')
            break
        # キャッシュに登録
        MemcachedUtils.set(name, employees)
        break
    return employees

@search_action
def search_by_years(session: Session):
    """ 勤続年数 """
    employees = []
    while True:
        years = input('勤続年検索: 年数を入力してください > ')
        # 入力がない場合は検索しない
        if not years:
            continue
        # 入力値をタイムスタンプに変換する
        try:
            threshold = (datetime.now() - relativedelta(years=int(years))).timestamp()
        except:
            print('年数を数字で入力してください')
            continue
        # キャッシュを探す
        cached = MemcachedUtils.get(str(years))
        if cached:
            print('DEBUG: Found in memcached.')
            for e in cached:
                print(e)
            break
        # キャッシュになければ検索する
        employees = session.query(Employee).filter(Employee.joined_at <= threshold).all()
        if not employees:
            print('該当するデータがありませんでした')
            break
        # キャッシュに登録
        MemcachedUtils.set(str(years), employees)
        break
    return employees


if __name__ == '__main__':
    main()
