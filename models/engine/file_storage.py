#!/usr/bin/python3
"""\
Serializes instances to JSON file and deserializes JSON file to instances.\
"""
import json
import os.path
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class FileStorage:
    """Serializes to a JSON file and deserializes from a JSON file."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary object"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the given obj with key <obj class name>.id"""
        self.__objects[obj.__class__.__name__ + "." + obj.id] = obj

    def save(self):
        """Serializes __objects to defined JSON file"""
        with open(self.__file_path, "w") as file:
            tmp_dict = {key: obj.to_dict() for key, obj in
                   self.__objects.items()}
            json.dump(tmp_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, "r") as file:
                tmp_dict = json.load(file)
                for key, value in tmp_dict.items():
                    self.__objects[key] = eval(key.split(".")[0])(**value)
