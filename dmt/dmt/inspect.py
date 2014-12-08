
import logging
import subprocess
import attrdict
import json
import dmt.util
import dmt.error

log = logging.getLogger(__name__)


class ContainerInspector(object):
    def __init__(self, project):
        self.project = project

    def inspect(self, container_name):
        # Run the docker inspect command, turn into an attrdict :)
        conf = self.project.get_container(container_name)
        cmd = ['docker', 'inspect', conf.tag]
        log.debug('Running inspect command: %s', ' '.join(cmd))
        try:
            json_str = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            data = json.loads(json_str)
            details = attrdict.AttrDict(data[0])
            # details = attrdict.AttrDict(json.loads(json)[0])
            return ContainerDetails(details)
        except subprocess.CalledProcessError as exc:
            # We expect non-zero return code if the container did not exist.
            if 'No such image or container' in exc.output:
                return ContainerDetails({}) 
        except Exception:
            # What happened?
            raise dmt.error.InternalError('Oops!')    
            

class ContainerDetails(object):
    def __init__(self, details):
        self.details = details

    @property
    def image(self):
        try:
            return self.details.Config.Image
        except AttributeError:
            return None

    @property
    def size(self):
        try:
            return self.details.Size
        except AttributeError:
            return None
    
    
