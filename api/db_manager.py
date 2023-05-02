from sqlmodel import Session, create_engine, select

from settings import DB_URL
from api.db import City, VkManagerAccount, VkUsers

session = Session(create_engine(DB_URL))


class ObjectsMethods():
    def __init__(self) -> None:
        pass

    @property
    def statement(self):
        return select(self.model)

    def get(self, id):
        with session:
            try:
                return session.exec(
                    self.statement.where(
                        self.model.id == id)).all()[0]
            except IndexError:
                return None

    def filter(self, *args, **kwargs):
        try:
            f_key = list(kwargs.keys())[0], 
            f_value = list(kwargs.values())[0]
        except KeyError:
            return self.get_all()
        with session:
            return session.exec(self.statement.filter(self.model.__dict__[f_key] == f_value)).all()

    def get_all(self):
        with session:
            return session.exec(self.statement).all()

    def create(self, *args, **kwargs):
        new_object = self.model(*args, **kwargs)
        try:
            save_objects(new_object)
        except:
            pass
        finally:
            return self.model(*args, **kwargs)


class VkCityObjects(ObjectsMethods):
    model = City

class VkManagerObjects(ObjectsMethods):
    model = VkManagerAccount

class VkUserObjects(ObjectsMethods):
    model = VkUsers


def save_objects(instances):
    instances = [instances] if type(instances) != list else instances
    with session:
        for i in instances:
            session.add(i)
        session.commit()

def delete_objects(instances):
    instances = [instances] if type(instances) != list else instances
    with session:
        for i in instances:
            session.delete(i)
        session.commit()
