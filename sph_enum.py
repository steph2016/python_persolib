"""
sph_enum
========

definition for a convenient enum:

    - based on http://sametmax.com/faire-des-enums-en-python

    - adapted to accept several spellings/synonyms for each keywords (see example below)

"""
def sph_enum(enumName, *listValueNames):
    """
In this example, enum_name is an enumeration that can be: 'a' (associated with value 0), 'b' (with 1), 'c' (with 2), 'd' (with 3), 'altitude' (with 4), 'alt' (with 4) or 'z' (with 4)

>>> list_possible_values =['a','b','c','d',['altitude','alt','z']]
>>> enum_name = sph_enum('enum_name',*list_possible_values)

* each keyword is associated with an integer. for instance:
    >>> enum_name.a,enum_name.b,enum_name.alt
    (0, 1, 4)

* 2 reversed dict are built: one (noted 'dictReverse' and convenient for compatibility with previous codes) containing only the first spelling/synonym of each keyword in the original format (usually strings, as presented in the above example); another (noted 'dictReversecomplete') containing lists (1 list for each keyword) of all possible spellings/synonyms:
    >>> enum_name.dictReverse[1]
    'b'
    >>> enum_name.dictReverse.keys()
    dict_keys([0, 1, 2, 3, 4])
    >>> enum_name.dictReversecomplete.keys()
    dict_keys([0, 1, 2, 3, 4])
    >>> enum_name.dictReverse.values()
    dict_values(['a', 'b', 'c', 'd', 'altitude'])
    >>> enum_name.dictReversecomplete.values()
    dict_values([['a'], ['b'], ['c'], ['d'], ['altitude', 'alt', 'z']])
    >>> enum_name.dictReversecomplete[1]
    ['b']
    >>> enum_name.dictReversecomplete[4]
    ['altitude', 'alt', 'z']
    """
    mainlist = []
    synonymlist = []
    for i,j in enumerate(listValueNames):
        if isinstance(j,list):
            mainlist.append(j[0])
            if len(j)>1:
                synonymlist.append(j[1:])
            else:
                synonymlist.append('NOSYN')
        else:
            mainlist.append(j)
            synonymlist.append('NOSYN')
    listValueNumbers = range(len(mainlist))

    dictAttrib = dict( zip(mainlist, listValueNumbers) )
    # is there a pythonic way for doing this ?
    for i,j in enumerate(synonymlist):
        if j != 'NOSYN':
            for k,l in enumerate(j):
                dictAttrib[l]=i
        
    dictReversemain = dict( zip(listValueNumbers, mainlist) ) # contains only the main spelling but has no list
    dictAttrib["dictReverse"] = dictReversemain
    
    dictReversecomplete = dict() # contains lists of all possible spellings
    for i,j in enumerate(synonymlist):
        dictReversecomplete[i]=[]
        dictReversecomplete[i].append(mainlist[i])
        if j != 'NOSYN':
            for k,l in enumerate(j):
                dictReversecomplete[i].append(l)
    dictAttrib["dictReversecomplete"] = dictReversecomplete
    
    mainType = type(enumName, (), dictAttrib)
    return mainType

# reminder to declare such an enum (in this example the type 'toto' can be 'a','b','c' or 'r'):
# toto = sph_enum('toto',\
#                 'a','b','c','r')
# reminder to list all possible values:
# toto.dictReverse.values()
