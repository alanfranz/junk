
import logging
import os
import string
import dmt.util
import dmt.error
import toposort

log = logging.getLogger(__name__)

PROJECT_FILE = 'dmtproj.yml'
DOCKER_FILE = 'Dockerfile'


def is_container_config(path):
    return os.path.basename(path).endswith('.dmt.yml')


def load_project():
    # Find and load main project file
    project_file = dmt.util.find_file_upwards(PROJECT_FILE)
    if not project_file:
        raise dmt.error.ProjectNotFoundError()
    project = Project(project_file)

    # Load container definitions
    top_dir = project.top_dir
    for dmt_file in dmt.util.find_files_down(top_dir, is_container_config):
        try:
            conf = Container(dmt_file, project)
            project.add_container(conf)
        except dmt.error.DmtError:
            log.error('Failed to load container config: %s', dmt_file)

    return project


class Project(object):
    """A DMT project file, which container shared container settings
    and environment variables for a project."""
    def __init__(self, project_file):
        log.debug('Loading project config: %s', project_file)
        self.project_file = project_file
        self.top_dir = os.path.dirname(project_file)
        self.containers = {}
        self.container_groups = {}
        yaml = dmt.util.load_yaml(project_file)
        self.yaml = yaml
        # Load environment
        if 'environment' in yaml:
            if type(yaml['environment']) != dict:
                raise dmt.error.SyntaxError('environment must be dictionary!')
            self.environment = yaml['environment']
        else:
            self.environment = {}
        # Load container groups
        if 'groups' in yaml:
            import pprint
            pprint.pprint(yaml['groups'])
            if type(yaml['groups']) != list:
                raise dmt.error.SyntaxError('groups must be a list!')
            for group in yaml['groups']:
                key, value = group.popitem()
                self.container_groups[key] = value                

    def expand_vars(self, s):
        if type(s) is str:
            return string.Template(s).substitute(self.environment)
        else:
            return s

    def add_container(self, config):
        """Add a container configuration to the project."""
        try:
            other = self.get_container(config.name)
            log.warn('Duplicate container name: %s', config.name)
            log.warn('First instance at: %s', other.dmt_file)
            log.warn('Second instance at: %s', config.dmt_file)
            msg = 'Duplicate container name: %s' % config.name
            raise dmt.error.DuplicateContainerNameError(msg)
        except dmt.error.ContainerNameNotFoundError:
            pass
        self.containers[config.name] = config

    def get_container(self, name):
        """Retrieve a container configuration by name."""
        try:
            return self.containers[name]
        except KeyError:
            msg = 'Container name not found: %s' % name
            raise dmt.error.ContainerNameNotFoundError(msg)
        
    def is_container_group(self, name):
        return name in self.container_groups
    
    def container_group(self, name):
        return self.container_groups[name]

    def get_container_name_here(self):
        """Retrieve the name of the container configuration
        in the current working directory."""
        here = os.getcwd()
        for conf in self.containers.values():
            if conf.work_dir == here:
                return conf.name
        msg = 'No dmt file in this directory: %s' % here
        raise dmt.error.NoContainerHereError(msg)

    def get_container_names_under_here(self):
        """Retrieve the names of all container configurations
        under the current working directory."""
        here = os.getcwd()
        l = []
        for conf in self.containers.values():
            if dmt.util.is_subdir_of(top=here, maybe_subdir=conf.work_dir):
                l.append(conf.name)
        return l

    def all_container_names(self):
        """Return all the container names in the project."""
        return self.containers.keys()

    def all_tags(self):
        """Return all the tags of containers in this project."""
        return set([c.tag for c in self.containers.values()])

    def container_name_from_tag(self, tagname):
        for n, c in self.containers.iteritems():
            if c.tag == tagname:
                return n
        raise ValueError('Tag not found: %s', tagname) 

    def build_depends(self):
        """Return dependency groups for the project."""
        # TODO: de-uglify this some time.
        depends = {}
        our_tags = self.all_tags()
        for c in self.containers.values():
            if c.buildable:
                if c.depends_on_tag in our_tags:
                    depends[c.tag] = set([c.depends_on_tag])
                else:
                    depends[c.tag] = set([''])
        return depends

    def build_groups(self):
        """Return topological sort of dependency groups, i.e,
           list of sets of containers which can be built in groups."""
        result = []
        for t in list(toposort.toposort(self.build_depends())):
            if t == set(['']): # We don't have to build the null dependency
                continue
            group = []
            for tag in t:
                container_name = self.container_name_from_tag(tag)
                container = self.get_container(container_name)
                if container.buildable:
                    group.append(container_name)
            result.append(group)
        return result

    def sanity_check(self):
        # Check the uniqueness of container names.
        pass


class DataVolumeContainer(object):
    def __init__(self, name, tag):
        self.name = name
        self.tag = tag


class DataVolume(object):
    def __init__(self, hostpath, containerpath):
        self.hostpath = hostpath
        self.containerpath = containerpath


class MappedPort(object):
    def __init__(self, host_port, private_port):
        self.host_port = host_port
        self.private_port = private_port


class Link(object):
    def __init__(self, container_name, alias_name):
        self.container_name = container_name
        self.alias_name = alias_name


def read_docker_from(docker_file):
    try:
        for line in open(docker_file):
            if line.startswith('FROM'):
                _, tag = line.split()
                return tag
    except IOError:  # No such file
        return ''
    except:
        log.exception('Error reading Dockerfile')
        return ''


class Container(object):
    def __init__(self, dmt_file, project):
        # XXX: TODO: FIXME: parsing etc should not be in here. Let's just
        # externalise that and make this a data clas.
        log.debug('Loading container config: %s', dmt_file)
        self.dmt_file = dmt_file
        self.work_dir = os.path.dirname(dmt_file)
        self.docker_file = os.path.join(self.work_dir, 'Dockerfile')
        yaml = dmt.util.load_yaml(dmt_file)
        # pprint.pprint(self.yaml)
        self.name = yaml['name']
        self.tag = yaml['tag']
        self.build = True
        self.buildable = os.path.exists(self.docker_file)
        self.depends_on_tag = read_docker_from(self.docker_file)
        if 'build' in yaml:
            self.build = yaml['build']
        self.environment = {}
        self.ports = []
        self.volumes_from = []
        self.volumes = []
        self.links = []
        self._load_environment(yaml, project)
        self._load_ports(yaml, project)
        self._load_volumes_from(yaml, project)
        self._load_volumes(yaml, project)
        self._load_links(yaml, project)

    def _load_environment(self, yaml, project):
        if 'environment' in yaml:
            if type(yaml['environment']) != dict:
                raise dmt.error.SyntaxError('environment must be dictionary!')
            for k, v in yaml['environment'].iteritems():
                vv = project.expand_vars(v)
                self.environment[k] = vv

    def _load_ports(self, yaml, project):
        if 'ports' in yaml:
            if type(yaml['ports']) != list:
                raise dmt.error.SyntaxError('ports must be list!')
            for p in yaml['ports']:
                p2 = project.expand_vars(p)
                h, p = p2.split(':')
                mp = MappedPort(host_port=h, private_port=p)
                self.ports.append(mp)

    def _load_volumes_from(self, yaml, project):
        if 'volumes-from' in yaml:
            if type(yaml['volumes-from']) != list:
                raise dmt.error.SyntaxError('volumes_from must be a list!')
            for y in yaml['volumes-from']:
                vol_from = DataVolumeContainer(y['name'], y['tag'])
                self.volumes_from.append(vol_from)

    def _load_volumes(self, yaml, project):
        if 'volumes' in yaml:
            if type(yaml['volumes']) != list:
                raise dmt.error.SyntaxError('volumes must be a list!')
            for y in yaml['volumes']:
                hostpath = project.expand_vars(y['hostpath'])
                containerpath = project.expand_vars(y['containerpath'])
                vol = DataVolume(hostpath, containerpath)
                self.volumes.append(vol)

    def _load_links(self, yaml, project):
        if 'links' in yaml:
            if type(yaml['links']) != list:
                raise dmt.error.SyntaxError('links must be a list!')
            for l in yaml['links']:
                l2 = project.expand_vars(l)
                container, alias = l2.split(':')
                link = Link(container_name=container, alias_name=alias)
                self.links.append(link)

