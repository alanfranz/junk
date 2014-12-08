
import os
import yaml
import logging
import contextlib
import dmt.error

log = logging.getLogger(__name__)


def load_yaml(path):
    try:
        with open(path, 'r') as fp:
            return yaml.safe_load(fp)
    except yaml.YAMLError, exc:
        log.exception('Error in configuration file: %s', path)
        if hasattr(exc, 'problem_mark'):
            mark = exc.problem_mark
            log.error("Error at line %s, column %s)" %
                      (mark.line+1, mark.column+1))
    except Exception, exc:
        log.exception('Error loading file: %s' % path)
    raise dmt.error.SyntaxError('Error loading file: %s' % path)


def is_same_directory_name(a, b):
    """Compare two directory names for equality."""
    return os.path.normpath(a) == os.path.normpath(b)


def is_subdir_of(top, maybe_subdir):
    """Return true if maybe_subdir is, in fact, a
    subdirectory of top."""
    top = os.path.abspath(top)
    maybe_subdir = os.path.abspath(maybe_subdir)
    return os.path.commonprefix([top, maybe_subdir]) == top


def find_file_upwards(filename, search_dir=None):
    """Traverse up directories starting at search_dir,
       returning the first directory where filename occurs
       or None if not found."""
    # If search dir is not specified, start looking here.
    if search_dir is None:
        search_dir = os.getcwd()
    search_dir = os.path.abspath(search_dir)

    # Is the file we want in this directory?
    if filename in os.listdir(search_dir):
        filepath = os.path.join(search_dir, filename)
        if os.path.isfile(filepath):
            return filepath

    # Have we hit the root of the filesystem?
    parent_dir = os.path.dirname(search_dir)
    if is_same_directory_name(search_dir, parent_dir):
        return None

    # OK, it's not here, go up and keep looking.
    return find_file_upwards(filename, parent_dir)


def find_files_down(top_dir, filter_fn):
    """Starting from top_dir, walk the directory tree below
    and yield filenames which satisfy filter_fn."""
    # XXX TODO FIXME: Do we care about symlinks here?
    for dirpath, dirnames, filenames in os.walk(top_dir):
        for f in filenames:
            path = os.path.join(dirpath, f)
            if filter_fn(path):
                yield path


@contextlib.contextmanager
def working_directory(path):
    """A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit."""
    prev_cwd = os.getcwd()
    os.chdir(path)
    log.debug('Enter directory: %s', os.getcwd())
    try:
        yield
    finally:
        os.chdir(prev_cwd)
