from . import Workflow
from shutil import rmtree
from app import chpc
from app.params import *
import re
from numpy import random
import numpy
from app import tweak
import logging


class Dopant(Workflow):

    middlewares = {
        'make'
    }

    def make(self, base=None):
        pass

    def submit(self):
        pass

    def abandon(self):
        pass

    def rate(self):
        pass

    def restart(self):
        pass

    def pull(self):
        pass
