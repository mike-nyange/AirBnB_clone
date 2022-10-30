#!/usr/bin/python3
"""program that contains the entry point of the command interpreter"""

import cmd
import shlex
import sys
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class HBNBCommand(cmd.Cmd):
    """Program that contains the entry point of the command interpreter"""

    prompt = '(hbnb) '
    intro = 'Welcome to AirBnB console program.\n'

    list_of_class = ["BaseModel", "User", "Amenity", "City",
                     "Place", "Review", "State"]

    def do_create(self, arg):
        """\nCreates a new class instance.\nUsage: create <class name>\n"""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()  # Splits arg into its space seperated constituents
        if args[0] not in self.list_of_class:
            print("** class doesn't exist **")
        else:
            new_inst = eval(args[0] + "()")
            print(new_inst.id)
            new_inst.save()

    def do_show(self, arg):
        """\nPrints the string representation of an instance based \
on the class name and id.\nUsage: show <class name> <id>\n"""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in self.list_of_class:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return
        else:
            try:
                tmp = args[0] + '.' + args[1]
                print(storage.all()[tmp])
            except KeyError:
                print("** no instance found **")
            finally:
                return

    def do_destroy(self, arg):
        """\nDeletes a class instance based on the class name and id.
Usage: destroy <class name> <id>\n"""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in self.list_of_class:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return
        else:
            try:
                tmp = args[0] + '.' + args[1]
                storage.all().pop(tmp)
                storage.save()
            except:
                print("** no instance found **")
            finally:
                return

    def do_all(self, arg):
        """\nPrints string representation of all instances in storage.
Usage 1 (all class instances): all\nUsage 2 (specific class instances): all <class name>\n"""
        if not arg:
            dic_str_list = []
            for key, value in storage.all().items():
                dic_str_list.append(str(value))
            if dic_str_list != []:
                print(dic_str_list)
                return
            else:
                print("Sorry, storage is empty!")
                return
        else:
            args = arg.split()
            if args[0] in self.list_of_class:
                dic_str_list = []
                for key, value in storage.all().items():
                    if str(key.split(".")[0]) == args[0]:
                        dic_str_list.append(str(value))
                if dic_str_list != []:
                    print(dic_str_list)
                    return
                else:
                    print("Sorry, no instance of \"{}\" exists in storage!".format(args[0]))
                    return
            else:
                print("** class doesn't exist **")
                return

    def do_update(self, arg):
        """\nUpdates an instance based on the class name and id.
Usage: update <class name> <id> <attribute name> "<attribute value>"\n"""
        if not arg:
            print("** class name missing **")
            return
        args = shlex.split(arg)
        if args[0] not in self.list_of_class:
            print("** class doesn't exist **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        else:
            try:
                tmp = args[0] + "." + args[1]
                storage.all()[tmp]
            except:
                print("** no instance found **")
                return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        elif len(args) == 3:
            print("** value missing **")
            return
        else:
            tmp = args[0] + "." + args[1]
            try:
                try:
                    value = int(args[3]) # Cast to int if value is int
                except ValueError:
                    value = float(args[3]) # Cast to float if value is float
            except ValueError:
                value = args[3].strip(":\"'") # Else value remains as string
            attr = args[2].strip(":\"'")
            setattr(storage.all()[tmp], attr, value)
            storage.save()

    def preloop(self):
        """Initialization prompter"""
        self.onecmd("help")
        return

    def emptyline(self):
        """Do nothing if no command is given"""
        return False

    def do_quit(self, arg):
        """\nExits the program.\nUsage: quit\n"""
        return True

    def do_EOF(self, arg):
        """\nExits the program.\nUsage 1: EOF\nUsage 2: Ctrl + D\n"""
        return True

    def default(self, line):
        """Initiates response to an invalid command line"""
        print("\"{}\": is not a valid action of AirBnB console program!".format(line))
        return

    def do_class_names(self, arg):
        """\nPrints a list of all class names available for instantiation.
Usage: class_names\n"""
        print(self.list_of_class)
        return

if __name__ == '__main__':
    HBNBCommand().cmdloop()
