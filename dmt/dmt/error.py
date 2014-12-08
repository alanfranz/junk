
class DmtError(Exception):
    pass


class InternalError(DmtError):
    pass


class ProjectNotFoundError(DmtError):
    pass


class SyntaxError(DmtError):
    pass


class DuplicateContainerNameError(DmtError):
    pass


class ContainerNameNotFoundError(DmtError):
    pass


class NoContainerHereError(DmtError):
    pass


class BuildFailedError(DmtError):
    pass


class RunFailedError(DmtError):
    pass
