"""
sph_table
=========

Quick definitions to handle a table without astropy (indeed, it may be convenient to avoid the astropy module that is huge). TBC: dirty, needs to be optimised...

""" 
class SPH_column:
    """
    TBD
    """
    def __init__(self,name):
        self._name = name
        self._fmt = 'string' # as long as fmt is 'string', that only means the type was not set (then everything is treated as string)
        self._values = []

    def addval(self,val):
        self._values.append(val)
        
    def fmt(self):
        fmtint=True
        fmtfloat=True
        for i,j in enumerate(self._values):
            try:
                temp = int(j)
            except ValueError:
                if fmtint:
                    fmtint = False
                try:
                    temp = float(j)
                except ValueError:
                    if fmtfloat:
                        fmtfloat = False
        if fmtint:
            temp = int
            self._fmt = 'int'
        elif fmtfloat:
            temp = float
            self._fmt = 'float'
        if fmtint or fmtfloat:
            for i,j in enumerate(self._values):
                self._values[i] = temp(j)
#
######################
#
class SPH_table:
    """
    TBD
    """
    def __init__(self,filename='gas_species.in',commentsign='!',columnnames=None,separationsign=' '):
        self._filename = filename
        self._commentsign = commentsign
        self._columnnames = columnnames
        self._core = []
        self._commentline = []
        self._listcol = []
        for line in open(filename,'rt'):
            if line[-1]=='\n':
                line = line[0:-1]
            if line[0] == commentsign:
                line = line[1:]
                self._commentline.append(line)
            else:
                self._core.append(line)
        self._nblines = len(self._core)
        self._nbcol = len(columnnames)
        for i,j in enumerate(columnnames):
            self._listcol.append(SPH_column(j))
        for i,j in enumerate(self._core):
            s = j.split(' ')
            while '' in s:
                s.remove('')
            while ' ' in s:
                s.remove(' ')
            for k,l in enumerate(s):
                self._listcol[k].addval(l)
        for i,j in enumerate(columnnames):
            self._listcol[i].fmt()

    def getcolumn(self,colname):
        if colname in self._columnnames:
            pos = self._columnnames.index(colname)
        else:
            print('warning: column ',colname,' not in table ==> will crash')
            pos = -1
        return self._listcol[pos]
