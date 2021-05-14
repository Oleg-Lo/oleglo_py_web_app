import threading


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.deleted_objects = []

    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry

    def register_new(self, obj):
        self.new_objects.clear()
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.clear()
        self.dirty_objects.append(obj)

    def register_deleted(self, obj):
        self.deleted_objects.clear()
        self.deleted_objects.append(obj)

    def commit(self):
        self.insert_new()

    def insert_new(self):
        for object1 in self.new_objects:
            self.MapperRegistry.get_mapper(object1).insert(object1)

    def update_dirty(self):
        for object1 in self.dirty_objects:
            self.MapperRegistry.get_mapper(object1).update(object1)

    def delete_deleted(self):
        for object1 in self.deleted_objects:
            self.MapperRegistry.get_mapper(object1).delete(object1)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObj:
    def mark_as_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_as_del(self):
        UnitOfWork.get_current().register_deleted(self)

    def mark_as_dirty(self):
        UnitOfWork.get_current().register_dirty(self)
