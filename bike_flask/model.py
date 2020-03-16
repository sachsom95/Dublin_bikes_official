from sqlalchemy import *

db_uri = "mysql://root:lhb280214@localhost:3306/dublin_bike"
engine = create_engine(db_uri)

metadata = MetaData()
# print(metadata)
# census = Table('census', metadata, autoload=True, autoload_with=engine)

inspector = inspect(engine)
print(inspector.get_table_names()) # 获取数据库的所有table信息
print(inspector.get_columns('position'))  #获取某个table的所有column
print("*********")
sql = "select * from position "
result = engine.execute(sql)

print("result is",result)
print(type(result))

# for r in result:
#   print(r)
#   print(type(r))

# result_list = result.fetchall()
# print("set is", result_list)
# print(type(result_list[0]))
