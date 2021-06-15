from src.apps.settings import cass_session

publisher_query_list = ['Ike']
publisher_query_cql = "SELECT user_account FROM users.user WHERE user_name = %s;"
publisher_account_rows = cass_session.execute(publisher_query_cql, publisher_query_list)
print(((publisher_account_rows.all())[0]).get('user_account'))