# import datetime
#
# print(datetime.datetime.now())
# print(20)
# print(datetime.datetime.now() + datetime.timedelta(days=20)

# from src.apps.settings import cass_session
# cql = "SELECT * FROM users.user_by_publish WHERE user_name = 'user2' AND state = '已通过' ALLOW FILTERING;"
# rows = cass_session.execute(cql)
# print(rows.all())