
import logging
import os
import subprocess
import dmt.util
import dmt.error

log = logging.getLogger(__name__)


class ContainerRunner(object):
    def __init__(self, project):
        self.project = project

    def run(self, names, extra_args=None, run_cmd=None, debug=False,
            dry_run=False):
        """Run the named containers according to config."""
        # TODO: FIXME: Don't allow debugging multiple containers.
        # TODO: FIXME: NEED container links!
        assert type(names) == list
        if debug and len(names) > 1:
            # TODO: FIXME: Exception / error here
            assert(0)

        for name in names:
            conf = self.project.get_container(name)

            # Delete any old containers with this name
            if not debug:
                delete_cmd = \
                    "docker inspect %s >/dev/null && docker rm -f %s || true" % (name, name)
                log.warn('CMD: delete old container: %s', delete_cmd)
                if not dry_run:
                    os.system(delete_cmd)

            # Create any required data volumes which don't exist
            for volume in conf.volumes_from:
                vol_cmd = "docker inspect %s >/dev/null 2>&1 || " \
                          "docker run --name %s %s true" % \
                          (volume.name, volume.name, volume.tag)
                log.warn('CMD: prepare data volumes: %s', vol_cmd)
                if not dry_run:
                    os.system(vol_cmd)

            cmd = ['docker', 'run']
            if not debug:
                cmd += ['--name', conf.name, '-d']

            for volume in conf.volumes_from:
                cmd += ['--volumes-from', volume.name]

            for volume in conf.volumes:
                cmd += ['-v', '%s:%s' % (volume.hostpath,
                                         volume.containerpath)]

            for portmap in conf.ports:
                cmd += ['-p', '%s:%s' % (portmap.host_port,
                                         portmap.private_port)]

            for link in conf.links:
                cmd += ['--link', '%s:%s' % (link.container_name, 
                                             link.alias_name)]

            for k, v in conf.environment.iteritems():
                cmd += ['-e', '%s=%s' % (k, v)]

            if extra_args:
                assert type(extra_args) == list
                cmd += extra_args

            # TODO: FIXME: instance number?
            # cmd += ['-h', conf.hostname]

            cmd += [conf.tag]

            if run_cmd:
                assert type(run_cmd) == list
                cmd += run_cmd

            log.warn('CMD: start container: %s', ' '.join(cmd))
            if not dry_run:
                rc = subprocess.call(cmd)
                if rc != 0:
                    msg = 'Failed to run container: %s' % conf.name
                    raise dmt.error.RunFailedError(msg)
