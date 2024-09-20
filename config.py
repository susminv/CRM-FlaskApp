import urllib

class Config:
    SECRET_KEY='some secret key'

    params='DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-Q8SRJL9\\SQLEXPRESS;DATABASE=crmflask;Trusted_Connection=yes;'

    SQLALCHEMY_DATABASE_URI="mssql+pyodbc:///?odbc_connect=%s" % params

    SQLALCHEMY_TRACK_MODIFICATIONS=False