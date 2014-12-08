
import logging
import subprocess
import dmt.util
import dmt.error
import os

log = logging.getLogger(__name__)


class ContainerBuilder(object):
    def __init__(self, project):
        self.project = project

    def build(self, names, force=False, quiet=False):
        """Build the named containers according to config."""
        assert type(names) == list
        for name in names:
            conf = self.project.get_container(name)
            if not conf.build:
                log.info('Skipping build for container: %s' % conf.name)
                continue
            with dmt.util.working_directory(conf.work_dir):
                cmd = ['docker', 'build']
                cmd += ['--rm=false']
                if force:
                    cmd += ['--no-cache']
                if quiet:
                    cmd += ['-q']
                cmd += ['-t', conf.tag]
                cmd += ['.']
                # Do want to chdir into there? Or like, run the command
                # with that as it's PWD?
                log.info('Running build command: %s', ' '.join(cmd))
                rc = subprocess.call(cmd)
                if rc != 0:
                    msg = 'Failed to build container: %s' % conf.name
                    raise dmt.error.BuildFailedError(msg)

   
    def build_parallel(self, names, *args, **kwargs):
        assert type(names) == list
        children = []
        for name in names:
            pid = os.fork()
            if pid:
                children.append(pid)
            else:
                self.build([name], *args, **kwargs)
                os._exit(0)

        for i, child in enumerate(children):
            os.waitpid(child, 0)

