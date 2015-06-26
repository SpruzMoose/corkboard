from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    """Category object

    Attributes:

    * id
        * Integer
        * PrimaryKey
    * name
        * CharField
        * max_length=127
    """
    name = models.CharField(max_length=127)
    def __unicode__(self):
        return unicode("(%s)" % (self.name))

class Pin(models.Model):
    """Pin Object

    Attributes:

    * id
        * Integer
        * PrimaryKey
    * image
        * ImageField
    * caption
        * CharField
        * max_length=255
    * category
        * ForeignKey to Category
    * creation_time
        * DateTimeField
        * auto_now_add=True
    * modification_time
        * DateTimeField
        * auto_now=True

    Note on modification_time:

    In future, this will alow updates to be communicated to user.
    May only flash a Pin to indicate changes ; to be deterimined.
    """
    image = models.ImageField(upload_to='pins')
    caption = models.CharField(max_length=255)
    category = models.ForeignKey('Category')
    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return unicode("{%s %s}" % (self.category.__unicode__(), self.caption))

class Board(models.Model):
    """Board object

    Attributes:

    * id
        * Integer
        * PrimaryKey
    * name
        * CharField
        * max_length=127
    * owner
        * Integer
        * ForeignKey to User
    """
    name = models.CharField(max_length=127)
    owner = models.ForeignKey(User)
    def __unicode__(self):
        return unicode("[%s]" % (self.name))

class PinToBoard(models.Model):
    """ PinToBoard object

    This is an association object which matches Pin to Board

    Attributes:

    * id
        * Integer
        * PrimaryKey
    * pin
        * Integer
        * ForeignKey to Pin
    * board
        * Integer
        * ForeignKey to Board
    * creation_time
        * DateTimeField
        * auto_now_add=True
    * rank
        * DateTimeField
        * blank=True
        * null=True

    Note on rank:

    Older objects first, newer objects last (by creation_time).
    To push newer objects ahead of older, the rank will be set
    one second before the PinBoard it is intended to supercede.
    The view will sort by rank (if not null) then creation_time.

    """
    pin = models.ForeignKey('Pin')
    board = models.ForeignKey('Board')
    creation_time = models.DateTimeField(auto_now_add=True)
    rank = models.DateTimeField(blank=True, null=True)
    def __unicode__(self):
        return unicode("%s >> %s" % (self.pin.__unicode__(),
            self.board.__unicode__()))

