class ToDictMixin:
    """
    Adds the "to_dict" functionality to Table-classes.
    Makes returning python dictionaries from these classes
    manageable.
    """

    # def __init__(self):
    #     self.__mapper__ = None
    #     self.__table__ = None
    #     self.id = None

    def to_dict(self, visited=None):
        # Prevent endless recursion
        if visited is None:
            visited = set()
        if self in visited:
            return {'id': self.id}

        visited.add(self)

        # Add table-columns with values to dict
        dict_representation = {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
        }

        # Add relationships if existing
        for rel in self.__mapper__.relationships:
            related_obj = getattr(self, rel.key)

            if related_obj is not None:
                if isinstance(related_obj, list):
                    dict_representation[rel.key] = [item.to_dict(visited) for item in related_obj]
                else:
                    dict_representation[rel.key] = related_obj.to_dict(visited)

        return dict_representation
