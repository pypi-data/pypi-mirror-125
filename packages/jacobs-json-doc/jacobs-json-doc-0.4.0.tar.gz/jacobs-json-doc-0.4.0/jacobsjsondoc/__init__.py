try:
    from .document import Document
except ModuleNotFoundError:
    import sys
    if 'setup' not in sys.modules['__main__'].__file__:
        raise
from . import _version

__version__ = _version.__version__
__version_info__ = _version.__version_info__

from .loader import PrepopulatedLoader

def parse(text_data):
    ppl = PrepopulatedLoader()
    ppl.prepopulate(None, text_data)
    doc = Document(uri=None, resolver=None, loader=ppl)
    return doc