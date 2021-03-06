
import os
import os.path


class BuildError(Exception):
    '''Generic exception for custom build errors'''
    def __init__(self, msg):
        super(BuildError, self).__init__(msg)
        self.message = msg


def run_command(command, args=[], cwd=None, env=None, name='command'):
    def cmd_args_to_str(cmd_args):
        return ' '.join([arg if not ' ' in arg else '"%s"' % arg for arg in cmd_args])

    assert isinstance(command, str) and isinstance(args, list)
    args = [command] + args

    check_call_args = {}
    if cwd is not None:
        check_call_args['cwd'] = cwd
    if env is not None:
        check_call_args['env'] = env

    import subprocess
    try:
        print('Running command \'%s\': %s' % (name, subprocess.list2cmdline(args)))
        subprocess.check_call(args, **check_call_args)
        print('Command \'%s\' completed successfully' % name)
    except subprocess.CalledProcessError as e:
        raise BuildError('\'%s\' exited with error code: %s' % (name, e.returncode))


def source(script: str, cwd=None) -> dict:
    popen_args = {}
    if cwd is not None:
        popen_args['cwd'] = cwd

    import subprocess
    proc = subprocess.Popen('bash -c \'source %s; env -0\'' % script, stdout=subprocess.PIPE, shell=True, **popen_args)
    output = proc.communicate()[0]
    return dict(line.split('=', 1) for line in output.decode().split('\x00') if line)


# Creates the directory if no other file or directory with the same path exists
def mkdir_p(path):
    if not os.path.exists(path):
        print('creating directory: ' + path)
        os.makedirs(path)


# Remove files and/or directories recursively
def rm_rf(*paths):
    from shutil import rmtree
    for path in paths:
        if os.path.isfile(path):
            print('removing file: ' + path)
            os.remove(path)
        elif os.path.isdir(path):
            print('removing directory and its contents: ' + path)
            rmtree(path)


ENV_PATH_SEP = ';' if os.name == 'nt' else ':'


def find_executable(name) -> str:
    is_windows = os.name == 'nt'
    windows_exts = ENV_PATH_SEP.split(os.environ['PATHEXT']) if is_windows else None
    path_dirs = ENV_PATH_SEP.split(os.environ['PATH'])

    search_dirs = path_dirs + [os.getcwd()] # cwd is last in the list

    for dir in search_dirs:
        path = os.path.join(dir, name)

        if is_windows:
            for extension in windows_exts:
                path_with_ext = path + extension

                if os.path.isfile(path_with_ext) and os.access(path_with_ext, os.X_OK):
                    return path_with_ext
        else:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                return path

    return ''


def replace_in_new_file(src_file, search, replace, dst_file):
    with open(src_file, 'r') as file:
        content = file.read()

    content = content.replace(search, replace)

    with open(dst_file, 'w') as file:
        file.write(content)


def replace_in_file(filepath, search, replace):
    replace_in_new_file(src_file=filepath, search=search, replace=replace, dst_file=filepath)


def touch(filepath: str):
    import pathlib
    pathlib.Path(filepath).touch()


def get_emsdk_root():
    # Shamelessly copied from Godot's detect.py
    em_config_file = os.getenv('EM_CONFIG') or os.path.expanduser('~/.emscripten')
    if not os.path.exists(em_config_file):
        raise BuildError("Emscripten configuration file '%s' does not exist" % em_config_file)
    with open(em_config_file) as f:
        em_config = {}
        try:
            # Emscripten configuration file is a Python file with simple assignments.
            exec(f.read(), em_config)
        except StandardError as e:
            raise BuildError("Emscripten configuration file '%s' is invalid:\n%s" % (em_config_file, e))
    if 'BINARYEN_ROOT' in em_config and os.path.isdir(os.path.join(em_config.get('BINARYEN_ROOT'), 'emscripten')):
        # New style, emscripten path as a subfolder of BINARYEN_ROOT
        return os.path.join(em_config.get('BINARYEN_ROOT'), 'emscripten')
    elif 'EMSCRIPTEN_ROOT' in em_config:
        # Old style (but can be there as a result from previous activation, so do last)
        return em_config.get('EMSCRIPTEN_ROOT')
    else:
        raise BuildError("'BINARYEN_ROOT' or 'EMSCRIPTEN_ROOT' missing in Emscripten configuration file '%s'" % em_config_file)


def globs(pathnames, dirpath='.'):
    import glob
    files = []
    for pathname in pathnames:
        files.extend(glob.glob(os.path.join(dirpath, pathname)))
    return files
