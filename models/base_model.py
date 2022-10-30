#!/usr/bin/python3
"""Defines all classes/attributes common to other classes. \
It is the base model of the current model."""

import uuid
from datetime import datetime, date, time
import models


class BaseModel:
    """Defines all fields and methods common to other classes"""

    def __init__(self, *args, **kwargs):
        """Initializing BaseModel"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key == '__class__':
                    continue
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Prints: [<class name>] (<self.id>) <self.__dict__>"""
        tmp = '[{}] ({}) {}'
        return tmp.format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance"""
        new_dictionary = self.__dict__.copy()
        new_dictionary.update({'__class__': str(type(self).__name__)})
        new_dictionary["created_at"] = self.created_at.isoformat()
        new_dictionary["updated_at"] = self.updated_at.isoformat()
        return new_dictionary
