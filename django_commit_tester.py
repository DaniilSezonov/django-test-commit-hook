import argparse
import os
import subprocess
from sys import platform

VENV_DIR = 'env'


def create_venv_dir():
    """
    Create virtualenv for running unit tests 
    """
    SHELL_EXEC = []
    SHELL_EXEC.append(F'set -e')
    SHELL_EXEC.append(F'virtualenv {VENV_DIR}')

    return_code = os.system(';'.join(SHELL_EXEC))
    return return_code


def main(argv=None):
    try:
        # Create parser for argumentsx
        parser = argparse.ArgumentParser()
        parser.add_argument('filenames', nargs='*')
        parser.add_argument('--testdir', type=str)
        parser.add_argument('--managedir', type=str)
        parser.add_argument('--requirements', type=str)

        args = parser.parse_args(argv)
        del args.filenames

        # Ensure parameter files and directories exist
        if not os.path.exists(args.testdir):
            return F'Test directory path does not exist. Given directory: {args.testdir}'
        if not os.path.exists(args.managedir):
            return F'manage.py directory path does not exist. Given directory: ' + \
                args.managedir
        if not os.path.exists(args.requirements):
            return F'Requirements directory path does not exist. Given directory: ' + \
                args.requirements

        # Check that virtualenv dir exists
        if not os.path.exists(VENV_DIR):
            return_code = create_venv_dir()
            if return_code != 0:
                return 'Could not create pre-commit virtual environment. ' + \
                    'Please ensure you have virtualenv installed and available. ' + \
                    'Install with: "pip install virtualenv"'

        # Parse Directories from args
        test_directory = args.testdir
        manage_directory = args.managedir
        manage_py_path = os.path.join(manage_directory, 'manage.py')

        # Build shell command
        SHELL_EXEC = []
        if platform == 'win32':
            v_env_activate = os.path.join(VENV_DIR, 'Scripts', 'activate.bat')
            SHELL_EXEC.append(F'{v_env_activate}')
            SHELL_EXEC.append(F'call {v_env_activate}')
        else:
            v_env_activate = os.path.join(VENV_DIR, 'bin', 'activate')
            SHELL_EXEC.append(F'set -e')
            SHELL_EXEC.append(F'source {v_env_activate}')
        SHELL_EXEC.append(F'pip install -r {args.requirements} --no-warn-conflicts')
        SHELL_EXEC.append(F'pytest')

        if platform == 'win32':
            return_code = os.system('&'.join(SHELL_EXEC))
        else:
            return_code = os.system(';'.join(SHELL_EXEC))

        if return_code != 0:
            return 1

        # Success
        return 0
    except Exception as e:
        print(e.args[0])
        return 1

if __file__ == 'main':
    main()
