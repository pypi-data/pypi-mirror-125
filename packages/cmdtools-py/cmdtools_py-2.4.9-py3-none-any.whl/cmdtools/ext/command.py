"""
cmdtools extension

Class:
    Command:
        Parameters:
            - name: command name

    CommandObject:
        Parameters:
            - name: command name
            - object_: command module or object

    CommandDir:
        Parameters:
            - rootdir: root directory of command files

    CommandModule:
        Parameters:
            - filename: filename or module name

    CommandRunner:
        Parameters:
            - command: CommandObject class to run

    CommandRunnerContainer:
        Parameters:
            - commands: list of CommandObject class to run

    CommandWrapperObject:
        -

    CommandWrapper:
        Parameters:
            - commands: list of CommandWrapperObject class to run

"""

import os
import inspect
import logging
import importlib
import cmdtools
from typing import Any, Callable, List, Union, Optional


class RunnerError(Exception):
    """
    raised when running an unmatched command name
    or some other exceptions
    """


class CommandObject:
    """command object container"""

    def __init__(self, object_: Union[Callable, object], name: str = None):
        self.object = object_

        # try get the command name from the module or class first
        # if no preset name, use command file name as the command name
        self.name = getattr(self.object, "name", name)  # type: str

    @property
    def aliases(self) -> List[str]:
        """get command aliases"""
        return getattr(self.object, "__aliases__", [])

    @property
    def callback(self) -> Optional[Callable]:
        """get command callback"""
        return getattr(self.object, self.name, None)

    @property
    def error_callback(self) -> Optional[Callable]:
        """get command error callback"""
        return getattr(self.object, "error_" + self.name, None)

    @classmethod
    def _checkfunc(cls, func) -> bool:
        """check is object callable"""
        if func is not None and (
            inspect.isfunction(func)
            or inspect.ismethod(func)
            or inspect.iscoroutinefunction(func)
        ):
            return True

        return False

    def is_coroutine(self) -> bool:
        """check whether command is coroutine or not, based by the callbacks"""
        if self.has_callback():
            return inspect.iscoroutinefunction(self.callback)
        if self.has_callback() and self.has_error_callback():
            return inspect.iscoroutinefunction(
                self.callback
            ) and inspect.iscoroutinefunction(self.error_callback)

        # not a coroutine or object does not have command callback
        return False

    def has_callback(self) -> bool:
        """check whether callback is exist or not"""
        return self._checkfunc(self.callback)

    def has_error_callback(self) -> bool:
        """check whether error callback is exist or not"""
        return self._checkfunc(self.error_callback)


class Command(CommandObject):
    """main command class inheritance"""

    def __init__(self, name: str):
        super().__init__(name=name, object_=self)


class CommandWrapperObject:
    """instance of wrapped command object"""

    def __init__(self):
        self.name = None
        self.aliases = []
        self.callback = None
        self.error_callback = None

    def error(self, func: Callable) -> Callable:
        """error handler function wrapper"""
        self.error_callback = func

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    def __call__(self):
        return self.callback(*getattr(self, '_args', ()), **getattr(self, '_kwargs', {}))

    @classmethod
    def _checkfunc(cls, func: Callable) -> bool:
        """check is object callable"""
        if func is not None and (
            inspect.isfunction(func)
            or inspect.ismethod(func)
            or inspect.iscoroutinefunction(func)
        ):
            return True

        return False

    def is_coroutine(self) -> bool:
        """check whether command is coroutine or not, based by the callbacks"""
        if self.has_callback():
            return inspect.iscoroutinefunction(self.callback)
        if self.has_callback() and self.has_error_callback():
            return inspect.iscoroutinefunction(
                self.callback
            ) and inspect.iscoroutinefunction(self.error_callback)

        # not a coroutine or object does not have command callback
        return False

    def has_callback(self) -> bool:
        """check whether callback is exist or not"""
        return self._checkfunc(self.callback)

    def has_error_callback(self) -> bool:
        """check whether error callback is exist or not"""
        return self._checkfunc(self.error_callback)


class CommandWrapper:
    """wrapper for commands (?)"""
    def __init__(self, commands: List[CommandObject] = None):
        if commands is None:
            commands = []

        self.commands = commands

    def command(self, **kwargs) -> Optional[CommandWrapperObject]:
        """base decorator for callbacks"""
        def decorator(obj):
            if (inspect.isfunction(obj), inspect.ismethod(obj), inspect.iscoroutinefunction(obj)).count(True) > 0:
                wrapper = CommandWrapperObject()

                for attr in kwargs.items():
                    setattr(wrapper, attr[0], attr[1])

                wrapper.name = kwargs.get('name', obj.__name__)
                wrapper.aliases = kwargs.get('aliases', [])
                wrapper.callback = obj
                self.commands.append(wrapper)

                def func_wrapper(*args, **kwargs):
                    setattr(wrapper, "_args", args)
                    setattr(wrapper, "_kwargs", kwargs)
                    return wrapper
                return func_wrapper()

            if inspect.isclass(obj):
                if CommandObject in inspect.getmro(obj):
                    self.commands.append(obj())
            else:
                raise TypeError("Cannot assign command for object:", type(obj))
        return decorator

    async def run(self, cmd: Union[cmdtools.Cmd, cmdtools.AioCmd], attrs: dict = None) -> Any:
        """run command instance"""
        if attrs is None:
            attrs = {}

        if not isinstance(cmd, (cmdtools.Cmd, cmdtools.AioCmd)):
            raise TypeError(f"object {type(cmd)} is not a Cmd or AioCmd instance")

        for command in self.commands:
            if command.name == cmd.name or cmd.name in command.aliases:
                args = []
                if command.has_callback():
                    args.append(command.callback)
                else:
                    return logging.error("Command name '%s' has no callback", command.name)
                if command.has_error_callback():
                    args.append(command.error_callback)

                if command.is_coroutine():
                    return await cmd.process_cmd(*args, attrs=attrs)

                return cmd.process_cmd(*args, attrs=attrs)

        raise RunnerError(f"Couln't find command '{cmd.name}'")


class CommandRunner:
    """command single runner class"""

    def __init__(self, command: CommandObject):
        self.command = command

    async def run(self, cmd: Union[cmdtools.Cmd, cmdtools.AioCmd], attrs: dict = None) -> Any:
        """run command from parsed command object"""

        if not isinstance(cmd, (cmdtools.Cmd, cmdtools.AioCmd)):
            raise TypeError(f"object {type(cmd)} is not a Cmd or AioCmd instance")

        if attrs is None:
            attrs = {}

        if self.command.name == cmd.name or cmd.name in self.command.aliases:
            args = []
            if self.command.has_callback():
                args.append(self.command.callback)
            else:
                return logging.error("Command name '%s' has no callback", self.command.name)
            if self.command.has_error_callback():
                args.append(self.command.error_callback)

            if self.command.is_coroutine():
                return await cmd.process_cmd(*args, attrs=attrs)

            return cmd.process_cmd(*args, attrs=attrs)

        raise RunnerError("Command name is invalid")


class CommandRunnerContainer:
    """command runner container class inheritance"""

    def __init__(self, commands: List[CommandObject]):
        self.commands = commands

    async def run(self, cmd: Union[cmdtools.Cmd, cmdtools.AioCmd], attrs: dict = None) -> Any:
        """run command from parsed command object"""

        if not isinstance(cmd, (cmdtools.Cmd, cmdtools.AioCmd)):
            raise TypeError(f"object {type(cmd)} is not a Cmd or AioCmd instance")

        if attrs is None:
            attrs = {}

        for command in self.commands:
            if command.name == cmd.name or cmd.name in command.aliases:
                args = []
                if command.has_callback():
                    args.append(command.callback)
                else:
                    return logging.error("Command name '%s' has no callback", command.name)
                if command.has_error_callback():
                    args.append(command.error_callback)

                if command.is_coroutine():
                    return await cmd.process_cmd(*args, attrs=attrs)

                return cmd.process_cmd(*args, attrs=attrs)

        raise RunnerError(f"Couln't find command '{cmd.name}'")


class CommandModule(CommandRunnerContainer):
    """command module container class"""

    def __init__(self, filename: str, *, load_classes: bool = True):
        self.filename = filename
        self.commands = []

        self.load_classes = load_classes

        self.load_module(load_classes=self.load_classes)
        super().__init__(commands=self.commands)

    def load_module(self, load_classes: bool) -> None:
        """load command classes from a module"""
        if self.filename.endswith(".py"):
            modulestr = (
                self.filename.rsplit(".py", 1)[0].replace(os.sep, ".").strip(".")
            )
            module = importlib.import_module(modulestr)

            if load_classes:
                for obj in dir(module):
                    obj_ = getattr(module, obj, None)

                    if inspect.isclass(obj_) and obj_.__module__ == module.__name__:
                        if CommandObject in inspect.getmro(obj_):
                            self.commands.append(obj_())
            else:
                self.commands.append(CommandObject(module))


class CommandDir(CommandRunnerContainer):
    """command directory container class"""

    def __init__(self, rootdir: str, *, search_tree: bool = False, load_classes: bool = False):
        self.rootdir = rootdir.replace("/", os.sep).replace("\\", os.sep)
        self.commands = []
        self.search_tree: bool = search_tree
        self.load_classes: bool = load_classes

        self.load_commands(search_tree=self.search_tree, load_classes=self.load_classes)
        super().__init__(commands=self.commands)

    def load_commands(self, search_tree: bool, load_classes: bool) -> None:
        """load commands from files inside rootdir"""
        dirs = []
        if search_tree:
            for root in os.walk(self.rootdir):
                dirs.append(root[0])

        if self.rootdir not in dirs:
            dirs.append(self.rootdir)

        for path in dirs:
            for file in os.listdir(path):
                if os.path.isfile(path + os.sep + file) and file.endswith(".py"):
                    module = importlib.import_module(
                        path.replace(os.sep, ".").strip(".")
                        + "."
                        + file.rsplit(".py", 1)[0]
                    )
                    if load_classes is False:
                        self.commands.append(
                            CommandObject(module, file.rsplit(".py", 1)[0])
                        )
                    else:
                        for obj in dir(module):
                            obj_ = getattr(module, obj, None)

                            if inspect.isclass(obj_) and obj_.__module__ == module.__name__:
                                if CommandObject in inspect.getmro(obj_):
                                    self.commands.append(obj_())


def get_command_names(commands: List[CommandObject], get_aliases=False) -> List[str]:
    """get command names from command list of CommandObject"""
    names = []
    for command in commands:
        names.append(command.name)

        if hasattr(command, "aliases") and get_aliases:
            names.extend(command.aliases)

    return names
