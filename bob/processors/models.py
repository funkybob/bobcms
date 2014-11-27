
from django.db import models

from polymorphic import PolymorphicModel


class Processor(PolymorphicModel):
    '''
    Base class for a Page processor.
    '''
    description = models.CharField(max_length=200, blank=True)
