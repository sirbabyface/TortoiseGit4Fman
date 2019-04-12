#
# Load the libraries that are used in these commands.
#
from fman import DirectoryPaneCommand, show_status_message, show_alert
from fman import QuicksearchItem, show_quicksearch
from fman.url import as_human_readable
import subprocess


class GitCommand(DirectoryPaneCommand):
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


class ListGitCommands(GitCommand):
    _git_commands = [
        QuicksearchItem('add', 'Add'),
        QuicksearchItem('commit', 'Commit'),
        QuicksearchItem('log', 'Logs Folder'),
        QuicksearchItem('log_file', 'Logs File'),
        QuicksearchItem('pull', 'Pull'),
        QuicksearchItem('push', 'Push'),
    ]

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
        for item in self._git_commands:
            try:
                index = item.title.lower().index(query)
            except ValueError as not_found:
                continue
            else:
                # The characters that should be highlighted:
                highlight = range(index, index + len(query))
                yield QuicksearchItem(item.value, item.title, highlight=highlight)

class GitCommit(GitCommand):
    def __call__(self):
        self._execute('commit')
        