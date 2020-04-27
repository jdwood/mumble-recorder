import shlex

class CommandListener:
    def __init__(self, cmd_prefix="!", commands=None):
        if commands is None:
            commands = []
        self.cmd_prefix = cmd_prefix
        self.commands = commands

    def _split_input(self, cmd_input):
        return shlex.split(cmd_input)

    def _extract_name(self, arg):
        return arg.replace(self.cmd_prefix, "", 1)
    
    def _has_cmd_prefix(self, arg):
        return arg.startswith(self.cmd_prefix)

    def create_command(self, cmd_input):
        args = self._split_input(cmd_input)
        first_arg = args[0]
        if not self._has_cmd_prefix(first_arg):
            return
        cmd_name = self._extract_name(first_arg)
        for Cmd in self.commands:
            if Cmd.name() == cmd_name:
                return Cmd(args[1:])