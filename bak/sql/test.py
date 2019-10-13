
import warnings
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from flask_appbuilder.security.sqla.models import User, Role
from flask_appbuilder.models.sqla.filters import FilterStartsWith, FilterEqualFunction, FilterEqual
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models import Employee,Department, Function, EmployeeHistory, Benefit, Invoice, InvoiceItem, Customer, Category
from sqlalchemy.pool import QueuePool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
warnings.filterwarnings('ignore', r".*support Decimal objects natively",
                        SAWarning, r'^sqlalchemy\.sql\.sqltypes$')

engine = create_engine('sqlite:///piano.db', poolclass=QueuePool)

Session = sessionmaker(bind=engine)

session = Session()
# result = session.execute("select * from department").first()
# print(result['name'])
#
# userModel = SQLAInterface(User)
# userModel.session = session
#
# customerModel = SQLAInterface(Customer)
# customerModel.session = session
#
# # filters = [['is_enabled', FilterEqualFunction, True]]
# base_filters = [['first_name', FilterStartsWith, 'C']]
#
# # customerModel.base_filters = base_filters
# filters = customerModel.get_filters().add_filter('first_name', FilterStartsWith, 'C')
# # filters = customerModel.get_filters().add_filter('is_enabled', FilterEqual, False)
#
# # customerModel.get_filters().add_filter('is_enabled', customerModel.FilterEqual, False)
# # print(customerModel.get_filters().get_filter_value('is_enabled'))
# cnt, result = customerModel.query(filters=filters)
# print(cnt)
#
#
# u = userModel.get(1)
# print (u)

Base = declarative_base()
Base.metadata.create_all(engine)

engine.dispose()