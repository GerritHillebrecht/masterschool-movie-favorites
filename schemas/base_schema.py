from utils.to_dict_mixin_schema import ToDictMixin
from database.extensions import db


class BaseModel(ToDictMixin, db.Model):
    """
    Custom Parent-class to extend from, easily extendable, especially useful
    for scalability. Inherits to_dict functionality.
    """
    __abstract__ = True
