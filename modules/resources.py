

class ResourcesManager(object):
    """
    Utility class for downloading files whose URLs are defined in the
    setup.cfg file.
    """
    def __init__(self):
        self._files = {}
