import peewee as pw

sqlite_db = pw.SqliteDatabase(database='./sqlite.db')


class Record(pw.Model):
    id = pw.BigAutoField(primary_key=True)
    date = pw.DateTimeField(null=False)
    start_time = pw.DateTimeField(null=False)
    end_time = pw.DateTimeField(null=False)
    duration_minutes = pw.IntegerField(null=False)

    class Meta:
        database = sqlite_db
        table_name = 'record'


def create_tables(drop_before: bool = False):
    models = [Record]

    if drop_before:
        sqlite_db.drop_tables(models)

    sqlite_db.create_tables(models)


create_tables()
