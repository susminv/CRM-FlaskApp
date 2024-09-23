import urllib
class Config:
    SECRET_KEY = 'Some secret key'
    params = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-QFHFBJH\\SQLEXPRESS;DATABASE=crm;Trusted_Connection=yes;'
    connection_string = urllib.parse.quote_plus(params)
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % connection_string
    SQLALCHEMY_TRACK_MODIFICATIONS = False