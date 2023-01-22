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

def withsession(func):
    """ DB接続デコレータ """
    def wrapper(*args, **kwargs):
        with engine.connect() as connection:
            with Session(bind=connection) as session:
                func(session)
    return wrapper

@withsession
def search_by_name(session: Session):
    """ 名前検索 """
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
            continue
        # キャッシュに登録
        MemcachedUtils.set(name, employees)
        for e in employees:
            print(e)
        break

@withsession
def search_by_years(session: Session):
    """ 勤続年数 """
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
            continue
        # キャッシュに登録
        MemcachedUtils.set(str(years), employees)
        for e in employees:
            print(e)
        break


if __name__ == '__main__':
    main()
