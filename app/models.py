from datetime import datetime

from app import db, Required


class File(db.Entity):
    name = Required(str)
    time = Required(datetime)
    size = Required(str)
    url = Required(str)


db.generate_mapping(create_tables=True)
