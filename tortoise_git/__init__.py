#
# Load the libraries that are used in these commands.
#
from fman import DirectoryPaneCommand, show_status_message, show_alert
from fman import QuicksearchItem, show_quicksearch
from fman.url import as_human_readable
import subprocess

class ListGitCommands(DirectoryPaneCommand):
    _git_commands = [
        QuicksearchItem('add', 'Add', highlight=range(0,1)),
        QuicksearchItem('commit', 'Commit', highlight=range(0,1)),
        QuicksearchItem('diff', 'Diff', highlight=range(0,1)),
        QuicksearchItem('log', 'Logs Folder', highlight=range(0,1)),
        QuicksearchItem('log_file', 'Logs File', highlight=range(5,6)),
        QuicksearchItem('pull', 'Pull', highlight=range(0,1)),
        QuicksearchItem('push', 'Push', highlight=range(2,3)),
    ]

    def _execute(self, command, path=None, close_on_end=2):
        arg_command = '/command:' + command
        if path is None:
            pane_path = self.pane.get_path()
            path = as_human_readable(pane_path)
        arg_path = '/path:"{}"'.format(path)
        arg_close_on_end = '/closeonend={}'.format(close_on_end)
        exec_command = ["TortoiseGitProc.exe", arg_command, arg_path,
                        arg_close_on_end]

        show_status_message(' '.join(exec_command))
        subprocess.run(' '.join(exec_command))

    def __call__(self):
        result = show_quicksearch(self._get_items)
        if result:
            query, value = result
            if value == 'log_file':
                file = self.pane.get_file_under_cursor()
                if file is None:
                    self._execute('log')
                else:
                    self._execute('log', as_human_readable(file))
            else:
                self._execute(value)
        else:
            pass

    def _get_items(self, query):
        if len(query) == 0:
            return _git_commands
        
        option = query.lower()
        if option == 'a':
            yield self._git_commands[0]
        elif option == 'c':
            yield self._git_commands[1]
        elif option == 'd':
            yield self._git_commands[2]
        elif option == 'l':
            yield self._git_commands[3]
        elif option == 'f':
            yield self._git_commands[4]
        elif option == 'p':
            yield self._git_commands[5]
        elif option == 's':
            yield self._git_commands[6]
        else:
            # If it it not one of the letters, tries to filter
            for item in self._git_commands:
                try:
                    index = item.title.lower().index(query.lower())
                except ValueError as not_found:
                    continue
                else:
                    # The characters that should be highlighted:
                    highlight = range(index, index + len(query))
                    yield QuicksearchItem(item.value, item.title, highlight=highlight)
