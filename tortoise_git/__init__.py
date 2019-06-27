#
# Load the libraries that are used in these commands.
#
import subprocess
import locale
from fman import DirectoryPaneCommand, show_status_message, show_alert
from fman import DirectoryPaneListener
from fman import QuicksearchItem, show_quicksearch
from fman.url import as_human_readable


class GitInfo(DirectoryPaneListener):
    def on_path_changed(self):
        try:
            cmd = 'git rev-parse --abbrev-ref HEAD'
            path = as_human_readable(self.pane.get_path())
            result = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=path, shell=True)
            branch = result.stdout.decode(locale.getpreferredencoding())[:-1]
            if branch != '':
                show_status_message('Git branch ' + branch)
            else:
                show_status_message('')
        except NotADirectoryError as e:
            pass


class ListGitCommands(DirectoryPaneCommand):
    _git_commands = [
        QuicksearchItem('add', 'Add', highlight=range(0,1)),
        QuicksearchItem('switch', 'Checkout/Switch Branch', highlight=range(4,5)),
        QuicksearchItem('clone', 'Clone', highlight=range(3,4)),
        QuicksearchItem('commit', 'Commit', highlight=range(0,1)),
        QuicksearchItem('diff', 'Diff', highlight=range(0,1)),
        QuicksearchItem('log', 'Logs Folder', highlight=range(0,1)),
        QuicksearchItem('log_file', 'Logs File', highlight=range(5,6)),
        QuicksearchItem('pull', 'Pull', highlight=range(0,1)),
        QuicksearchItem('push', 'Push', highlight=range(2,3)),
    ]
    _git_keys = ['a', 'k', 'n', 'c', 'd', 'l', 'f', 'p', 's']

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
        if not query:
            for command in self._git_commands:
                yield command
        else:
            option = query.lower()
            try:
                yield self._git_commands[self._git_keys.index(option)]
            except ValueError:
                # If it it not one of the letters, tries to filter
                for item in self._git_commands:
                    try:
                        index = item.title.lower().index(query.lower())
                        highlight = range(index, index + len(query))
                        yield QuicksearchItem(item.value, item.title, highlight=highlight)
                    except ValueError:
                        continue
