from datetime import datetime

from pony import orm
from pony.converting import str2datetime

db = orm.Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)


class File(db.Entity):
    name = orm.Required(str)
    time = orm.Required(datetime)
    size = orm.Required(str)
    url = orm.Required(str)


db.generate_mapping(create_tables=True)
