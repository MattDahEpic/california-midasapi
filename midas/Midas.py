from midas.authentication import Midas as MidasAuth
from midas.ratelist import Midas as MidasRateList

class Midas(MidasAuth, MidasRateList):
    """
    Python API for California's energy price database MIDAS.

    Main class, imports most things from modules.
    """