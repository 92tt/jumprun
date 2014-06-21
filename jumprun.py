#!/usr/bin/python3

"""Jumprun, your command line companion

Usage:
    jr add <name> <command> [-d WORKDIR] [-f]
    jr rm all
    jr rm <name>
    jr show
    jr show all
    jr show <name>
    jr rename <old> <new>
    jr <name>
    jr -h
    jr -v

Commands:
    add         Add a new shortcut
    rm          Delete a shortcut
    rename      Rename a shortcut
    show        List all shortcuts

Options:
    -h, --help                  Show this screen.
    --version                   Show version.
    --workdir <dir>, -d <dir>   Working directory for the command
    --force, -f                 If shortcut already exists, overwrite it.
"""

import sqlite3
import subprocess
import os
import sys
from termcolor import colored
from docopt import docopt

<<<<<<< HEAD
# Emoji's
S = "\xF0\x9F\x98\x83"
L = "\xF0\x9F\x8D\xAD"
B = "\xF0\x9F\x8D\xBA"
=======

def print_colored(string, color, on_color=None, attrs=None):
    """
    Print text using given color
    """
    print(colored(string, color, on_color=on_color, attrs=attrs))
>>>>>>> 78956efd02b57662c7e589733f1e369651a52cd5



def print_err(string):
    """
    Print error message
    """
<<<<<<< HEAD
    arg = docopt(__doc__, version=0.80)
    # creates a hidden database in users/documents
    db_path = os.path.expanduser("~/")
    db_path = db_path + "/" + ".jumprun"
    db = sqlite3.connect(db_path)
    # Creates table if doesn't exist on the execution of the script
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS path(id INTEGER PRIMARY KEY, name TEXT,
    path TEXT, filename TEXT)
        ''')
    db.commit()

# This condition handles the *add* command
    if arg['add']:
        # Get the path of the current dir
        current_dir = os.getcwd()
        name = arg['<name>']
        filename = arg['<filename>']
        if os.path.isfile(os.getcwd() + "/" + filename):
            cursor.execute('''
            SELECT path,filename FROM path WHERE name=?
                ''', (name,))
            pth = cursor.fetchone()
            # Checks for conflicts in the database
            if pth is None:
                cursor.execute('''
                INSERT INTO path(name, path, filename)
                VALUES (?, ?, ?)
                    ''', (str(name), str(current_dir), str(filename)))
                db.commit()
                msg = "%s has been added %s" % (name, L)
                print colored(msg, "cyan")
            else:
                print colored("The name %s already exists" % (name), "red")
        else:
            print "The File Doesn't Exist"

    if not arg['add'] and not arg['rm'] and not arg['rename'] and not \
        arg['show']:
        get_name = arg['<name>']
        cursor.execute('''
        SELECT path,filename FROM path WHERE name=?
            ''', (get_name,))
        pth = cursor.fetchone()
        # Checks if the user has made an entry using jr add
        if pth is None:
            print colored("Invalid name, type jr --help for more... " + "B",
                          "red")
        else:
            file_path = str(pth[0])
            file_name = str(pth[1])
            # Handles the execution of python/ruby scripts in the terminal
            if os.path.splitext(file_name)[1] == ".py":
                cmd = "python %s" % (file_name)
                os.chdir(file_path)
                print colored("Running Script:", "cyan")
                subprocess.call(cmd, shell=True)

            elif os.path.splitext(file_name)[1] == ".rb":
                cmd = "ruby %s" % (file_name)
                os.chdir(file_path)
                print colored("Running Script:", "cyan")
                subprocess.call(cmd, shell=True)

            elif os.path.splitext(file_name)[1] == ".pl":
                cmd = "perl %s" % (file_name)
                os.chdir(file_path)
                print colored("Running Script:", "cyan")
                subprocess.call(cmd, shell=True)

            else:
                ext = os.path.splitext(file_name)[1]
                print colored("The %s extension is not supported" % ext,
                              "red"
                              )

# This condition handles the *rm* command
    if arg['rm']:
        # Code for refreshing the entire database
        if arg['--all']:
            os.remove(db_path)
            print colored("The database has been refreshed %s" % S, "cyan")
        else:
            # Code for deleteing a specific name from database
            name = arg['<name>']
            cursor.execute('''
            SELECT path,filename FROM path WHERE name=?
            ''', (name,))
            pth = cursor.fetchone()
            # Checks if the shortcut to be deleted exists?
            if pth is None:
                print colored("%s doesn't exist" % (name), "red")
=======
    print_colored(string, 'red', attrs=['bold'])



def print_msg(string):
    """
    Print info message
    """
    print_colored(string, 'cyan')


# via: http://stackoverflow.com/a/3041990/2180189
def ask_yes_no(question, default="yes"):
    """
    Ask a yes/no question and return their answer.
    """
    valid = {
        "yes":  True,
        "y":    True,
        "ye":   True,
        "no":   False,
        "n":    False
    }

    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer: '%s'" % default)

    while True:
        print(colored(question, 'green') +  colored(prompt, 'cyan', attrs=['bold']) , end='')
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print_err("Please respond with 'y' or 'n'.")


class JumpRun:
    """
    JumpRun main class
    """


    def __init__(self):
        """
        Prepare database & init the object
        """

        self.args = docopt(__doc__, version=0.80)

        #creates a data folder in home dir
        path    = os.path.expanduser('~/.jumprun')
        path    = os.path.abspath(path)

        os.makedirs(path, exist_ok=True)
        self.dir = path

        # connect to db
        self.init_db()



    def run(self):
        """
        Perform the specified action
        """

        if self.args['add']:
            self.action_add()

        elif self.args['rm']:
            self.action_rm()

        elif self.args['show']:
            self.action_show()

        elif self.args['rename']:
            self.action_rename()

        else:
            self.action_run_command()



    def get_data_file(self, name):
        """
        Get path to a file in the data directory
        """
        return os.path.join(self.dir, name)



    def init_db(self):
        """
        Init database and prepare tables
        """

        # database file
        db_path = self.get_data_file("data.sqlite")

        # comect and create cursor
        self.db     = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

        # prep tables
        self.db_exec('''
            CREATE TABLE IF NOT EXISTS shortcuts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                command TEXT NOT NULL
            )
            ''')



    def db_query(self, query, args=None):
        """
        Execute a query in the DB
        """
        if args is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, args)



    def db_exec(self, query, args=None):
        """
        Execute a query in the DB
        """
        if args is None:
            self.db_query(query)
        else:
            self.db_query(query, args)

        self.db.commit()



    def db_fetch_one(self):
        """
        Fetch a results of last query
        """
        return self.cursor.fetchone()



    def db_fetch_all(self):
        """
        Fetch a results of last query
        """
        return self.cursor.fetchall()



    def shortcut_exists(self, name):
        """
        Check if a shortcut of given name already exists in the DB
        """

        self.db_query('''
            SELECT * FROM shortcuts WHERE name=?
            ''', (name,))

        pth = self.db_fetch_one()

        if pth is None or len(pth) == 0:
            return False
        else:
            return True



    def shortcut_str(self, path, cmd):
        """
        Get a string with colors describing a shortcut
        """

        s = colored('| path = ', 'cyan') + colored(path, 'yellow') + '\n' \
          + colored('| cmd  = ', 'cyan') + colored(cmd, 'green', attrs=['bold'])

        return s



    def action_add(self):
        """
        Add a new shortcut
        """

        # prepare values for new shortcut
        path    = self.args['--workdir'] or os.getcwd()
        name    = self.args['<name>']
        cmd     = self.args['<command>']

        overwrite = self.args['--force']

        # check for conflicts in DB
        if not overwrite and self.shortcut_exists(name):
            print_err('The shortcut "%s" already exists.' % name)
            return

        # if cmd has arguments, extract the command only
        cmd_parts   = [x.strip() for x in cmd.split(' ')]
        cmd_real    = cmd_parts[0]
        cmd_tail    = ' '.join(cmd_parts[1:])

        # if cmd_real starts with ./, remove that
        if cmd_real.startswith('./'):
            cmd_real = cmd_real[2:]


        # path to the file (if it's in the folder)
        localfile = os.path.abspath( os.path.join(path, cmd_real) )

        # check if the file is present at the path given
        if os.path.isfile(localfile):

            # file extension
            ext = os.path.splitext(cmd_real)[1]

            # check for exacutable bit
            if os.access(localfile, os.X_OK) and not ext == '.jar': # jar is executable, but cannot be run directly
                # file is executable
                cmd = ''

                if not cmd_real.startswith('/'):
                    cmd = './'

                cmd = cmd + cmd_real + ' ' + cmd_tail

>>>>>>> 78956efd02b57662c7e589733f1e369651a52cd5
            else:
                # not executable
                # try to find interpreter for the file

                interpreter = {
                    '.py': 'python',
                    '.rb': 'ruby',
                    '.pl': 'perl',
                    '.sh': 'sh',
                    '.php': 'php',
                    '.jar': 'java -jar',
                }.get(ext, None)

                # check if interpreter was found
                if interpreter is None:

                    msg = ('Could not make a shortcut to "%s":'\
                          + '\n - not executable & unknown extension.') % localfile;

                    print_err(msg)
                    return

                cmd = str(interpreter) + ' ' + str(cmd_real) + ' ' + str(cmd_tail)
        else:
            # use cmd, as given.
            pass

        if overwrite:
            self.db_exec('''
                    DELETE FROM shortcuts WHERE name=?
                    ''', (name,))
<<<<<<< HEAD
                db.commit()
                print colored("%s has been deleted %s" % (name, L), "cyan")

# This condition handles the *rename* command
    if arg['rename']:
        old_name = arg['<oldname>']
        new_name = arg['<newname>']
        cursor.execute('''
        SELECT name, path, filename FROM path WHERE name=?
            ''', (old_name,))
        pth = cursor.fetchone()
        # Checks if the shortcut to be renamed exists?
        if pth is None:
            print colored("%s doesn't exist" % (old_name), "red")
        else:
            cursor.execute('''
            SELECT path,filename FROM path WHERE name=?
            ''', (new_name,))
            q = cursor.fetchone()
            # Checks if the new shortcut name is already present
            if q is not None:
                print colored("The name %s already exists", "red")
            else:
                old_path = pth[1]
                old_filename = pth[2]
                cursor.execute('''
                DELETE FROM path WHERE name=?
                    ''', (old_name,))
                cursor.execute('''
                INSERT INTO path(name, path, filename)
                VALUES (?, ?, ?)
                ''', (str(new_name), str(old_path), str(old_filename)))
                db.commit()
                msg = "%s has been renamed to %s %s" % (old_name, new_name, L)
                print colored(msg, "blue")

# This condition handles the *show* command
    if arg['show']:
        if arg['--f']:
            cursor.execute('''
            SELECT name, filename FROM path
=======
        # save to DB
        self.db_exec('''
            INSERT INTO shortcuts (name, path, command)
            VALUES (?, ?, ?)
            ''', (str(name), str(path), str(cmd)))

        # show OK message
        msg = ('Shortcut "%s" has been created.\n' \
             + self.shortcut_str(path, cmd)) % name

        print_msg(msg)



    def action_rm(self):
        """
        Delete a shortcut
        """

        name = self.args['<name>']

        if self.args['all']:
            # delete all

            if ask_yes_no('Really delete ALL shortcuts?', default='no'):
                self.db_exec(''' DELETE FROM shortcuts ''')
                print_msg("All shortcuts deleted.")
            else:
                print_err("Aborted.")
                return

        else:
            # delete one

            # find by name
            self.db_exec('''
                SELECT id FROM shortcuts WHERE name=?
                ''', (name,))

            q = self.db_fetch_one()
            id = q[0]

            # delete if exists
            if q is None:
                print_err('Shortcut "%s" does not exist!' % name)

            else:
                self.db_exec('''
                    DELETE FROM shortcuts WHERE id=?
                    ''', (id,))

                # show OK message
                print_msg('Shortcut "%s" deleted.' % name)



    def action_rename(self):
        """
        Rename a shortcut
        """

        # get old and new name from args
        old = self.args['<old>']
        new = self.args['<new>']

        # select the old shortcut
        self.db_query('''
            SELECT id FROM shortcuts WHERE name=?
            ''', (old,))
        r = self.db_fetch_one()

        # error if old doesn't exist
        if r == None:
            print_err('Shortcut "%s" does not exist!' % old)
            return

        # error if new exists
        if self.shortcut_exists(new):
            print_err('Shortcut "%s" already exists!' % new)
            return

        id = r[0]

        # rename in DB
        self.db_exec('''
            UPDATE shortcuts SET name=? WHERE id=?
            ''', (new, id))

        # show OK message
        print_msg('Shortcut "%s" renamed to "%s".' % (old, new))



    def action_show(self):
        """
        Show shortcut(s) value
        """

        # helper function to display one row with colors
        # r = [name, path, command]
        def show_a_row(r):
            msg = colored('Shortcut: ', 'cyan') \
                + colored(r[0], 'white', attrs=['bold']) + '\n' \
                + self.shortcut_str(r[1], r[2]) + '\n'

            print(msg)


        name = self.args['<name>']

        if name is None or name == 'all':
            # select all shortcuts
            self.db_query('''
                SELECT name,path,command FROM shortcuts ORDER BY name
>>>>>>> 78956efd02b57662c7e589733f1e369651a52cd5
                ''')

            entries = self.db_fetch_all()

            # show the shortcuts
            if (entries is None) or (len(entries) == 0):
                print_err('No shortcuts defined.')
            else:
                for row in entries:
                    show_a_row(row)

        else:
            # select shortcut by name

            self.db_query('''
                SELECT name,path,command FROM shortcuts WHERE name=?
                ''', (name,))

            rec = self.db_fetch_one()

            # show the shortcut
            if rec is None:
                print_err('Shortcut "%s" does not exist.' % name)
            else:
                show_a_row(rec)



    def action_run_command(self):
        """
        Run a shortcut, if exists
        """

        name = self.args['<name>']

        # get entry from DB
        self.db_query('''
            SELECT path,command FROM shortcuts WHERE name=?
            ''', (name,))

        row = self.db_fetch_one()

        if row == None:
            print_err('Shortcut "%s" does not exist.' % name)
            return

        path = row[0]
        cmd  = row[1]

        # show message
        msg = colored('JumpRun shortcut', 'white', attrs=['bold']) + '\n' + \
              self.shortcut_str(path, cmd) + '\n'
        print(msg)

        # cd to the folder & run the command
        os.chdir(path)

        try:
            subprocess.call(cmd, shell=True)
        except KeyboardInterrupt:
            print('') # newline
            return



def main():
    """
    This is the main function run by *entry_point* in setup.py
    """
    jr = JumpRun()
    jr.run()



# start from terminal directly
if __name__ == "__main__":
    main()
