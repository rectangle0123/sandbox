from datetime import datetime
from sqlalchemy import Column, ForeignKey, Float, Integer, String, Table
from sqlalchemy.orm import relationship

from database import Base

# 従業員と役職の紐付けテーブル（多対多）
employees_positions = Table(
    'employees_positions',
    Base.metadata,
    Column(
        'employee_id',
        ForeignKey('employees.id', ondelete='CASCADE',),
        primary_key=True,
    ),
    Column(
        'position_id',
        ForeignKey('positions.id', ondelete='CASCADE',),
        primary_key=True,
    ),
)

class Employee(Base):
    """ 従業員モデル """
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    joined_at = Column(Float, nullable=False)
    positions = relationship(
        'Position',
        secondary=employees_positions,
        back_populates='employees',
        cascade='all, delete',
        lazy='joined',
    )

    def __repr__(self):
        return '%s, %s, %s, %s' % (
            self.id,
            self.name,
            datetime.fromtimestamp(self.joined_at).strftime('%Y-%m-%d'),
            self.positions,
        )

class Position(Base):
    """ 役職モデル """
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    employees = relationship(
        'Employee',
        secondary=employees_positions,
        back_populates='positions',
        lazy='joined',
    )

    def __repr__(self):
        return self.name
