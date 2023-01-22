from datetime import datetime
from sqlalchemy.orm import sessionmaker

from database import Base, engine 
from models import Employee, Position

# テーブル再作成
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# セッション
Session = sessionmaker(engine)

# データ投入
with engine.connect() as connection:
    with Session(bind=connection) as session:
        # 役職
        p1 = Position(name='PM')
        p2 = Position(name='PG')
        p3 = Position(name='Tester')

        # 従業員 1
        e1 = Employee(name='Lorand', joined_at=datetime.strptime('1990-12-31', '%Y-%m-%d').timestamp())
        e1.positions.append(p1)
        session.add(e1)

        # 従業員 2
        e2 = Employee(name='Andy', joined_at=datetime.strptime('2000-1-1', '%Y-%m-%d').timestamp())
        e2.positions.append(p2)
        e2.positions.append(p3)
        session.add(e2)

        # 従業員 3
        e3 = Employee(name='Andy%', joined_at=datetime.strptime('2020-4-1', '%Y-%m-%d').timestamp())
        e3.positions.append(p2)
        session.add(e3)

        session.commit()

print('Initializing Application completed.')
