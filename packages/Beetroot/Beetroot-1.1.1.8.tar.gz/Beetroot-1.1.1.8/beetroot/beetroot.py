#Beetroot, a general purpose library for all sorts of uses.

#Imports
import sys

from .exception import *

if not str(sys.version).startswith("3"):
    #HOW DARE YOU USE PYTHON2 IDIOT. or python4, if that ever exists
    #well I mean, if it's like a massive database or smth and you don't wanna migrate 1k+ lines of code then I understand, BUT STILL.
    raise VersionError("Python version is not supported.")

#More imports
import platform
import getpass
import socket
import uuid
import hashlib
import webbrowser
import datetime
import lzma
import base64
import codecs

try:
    import ujson as json
    
except (ModuleNotFoundError, ImportError):
    try:
        import simplejson as json
        
    except (ModuleNotFoundError, ImportError):
        import json
    
try:
    import PIL
    
except (ModuleNotFoundError, ImportError):
    pass

try:
    import pyautogui
    
except (ModuleNotFoundError, ImportError):
    pass

try:
    import psutil
    
except (ModuleNotFoundError, ImportError):
    pass

from pathlib import Path as p

from .metadata import *
from .random import *
from .stopwatch import *
from .file import *
from .tts import *
from .objtype import *

#Constants
gen = mrandom.SystemRandom()
sys.setrecursionlimit(32767)
    
def strhash(str_, secure=True):
    """Hash Function that uses MD5 or SHA512."""
    
    if objtype(secure) != "bool":
        raise InvalidHashSecurityValue("Argument \"secure\" can only be boolean")
    
    if secure:
        return hashlib.sha512(str(str_).encode("iso-8859-1")).hexdigest()
    
    elif not secure:
        return hashlib.md5(str(str_).encode("iso-8859-1")).hexdigest()
        
    else:
        raise UnknownError("¯\_(ツ)_/¯")
    
def bytehash(b, secure=True):
    """Hash Function that uses MD5 or SHA512."""
    
    if objtype(secure) != "bool":
        raise InvalidHashSecurityValue("Argument \"secure\" can only be boolean")
    
    if objtype(b) != "bytes":
        raise InvalidHashTypeError("Argument \"b\" can only be bytestring")
    
    if secure:
        return hashlib.sha512(b).hexdigest()
    
    elif not secure:
        return hashlib.md5(b).hexdigest()
        
    else:
        raise UnknownError("¯\_(ツ)_/¯")
        
def test():
    """Test"""
    print("Hello, world!")
    return 0
    
def quicksort(array):
    """Quicksort algorithm"""

    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        
        for x in array:
            if x < pivot:
                less.append(x)
                
            elif x == pivot:
                equal.append(x)
                
            elif x > pivot:
                greater.append(x)
                
        return quicksort(less) + equal + quicksort(greater)
    
    else:
        return array

def lsep(str_, sep=" "):
    """Seperates string str_ by seperator sep whilst avoiding all strings containing whitespace"""
    a = str_.split(sep)
    
    out = []
    for i in range(0, len(a)):
        if (not a[i].isspace()) and a[i] != "":
            out.append(a[i])
            
    return out

def execfile(file):
    """Executes a python .py script"""
    with open(p(file), "r", encoding="iso-8859-1") as f:
        exec(f.read())
        f.close()
        
    return 0

def systemstats():
    """Returns info about system and hardware"""
    return [getpass.getuser(), platform.system(), platform.version(), platform.machine(), platform.node(), socket.gethostbyname(socket.gethostname()), ':'.join(("%012X" % uuid.getnode())[i:i+2] for i in range(0, 12, 2)).lower()]

def unline(str_):
    """Makes multi-line strings single-line"""
    return str(str_).replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r").replace("\a", "\\a").replace("\b", "\\b")

def reline(str_):
    """Reverses beetroot.unline()"""
    return str(str_).replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r").replace("\\a", "\a").replace("\\b", "\b")

def pixelgrab(i_x, i_y):
    try:
        import PIL.ImageGrab
        return PIL.ImageGrab.grab().load()[int(i_x), int(i_y)]
    
    except (ModuleNotFoundError, ImportError):
        raise ModuleError("PIL most be installed to use beetroot.pixelgrab(). Try pip install pillow.")
    
    except ValueError:
        raise InvalidTypeError("Arguement \"i_x\" and \"i_y\" must be ints or floats")
    
def mousepixelgrab():
    try:
        import PIL.ImageGrab
        import pyautogui
        
        pos = pyautogui.position()
        return PIL.ImageGrab.grab().load()[pos.x, pos.y]

    except (ModuleNotFoundError, ImportError):
        raise ModuleError("PIL and pyautogui most be installed to use beetroot.mousepixelgrab(). Try pip install pillow pyautogui.")
    
def strobfuscate(str_):
    """Minorly obfuscates a string. While it is unreadable,
    don't expect this to stand up to anyone with a bit
    of python knowledge"""
    try:
        return lzma.compress(base64.a85encode(codecs.encode(str(str_)[::-1], "rot-13").encode("utf-8"))).decode("iso-8859-1")[::-1]
    
    except UnicodeDecodeError:
        return lzma.compress(base64.a85encode(codecs.encode(str(str_)[::-1], "rot-13").encode("iso-8859-1"))).decode("iso-8859-1")[::-1]
    
def strunobfuscate(str_):
    """Unobfuscates a string obfuscated by beetroot.strobfuscate()"""
    try:
        return codecs.encode(base64.a85decode(lzma.decompress(str_[::-1].encode("iso-8859-1"))).decode("utf-8"), "rot-13")[::-1]
    
    except UnicodeDecodeError:
        return codecs.encode(base64.a85decode(lzma.decompress(str_[::-1].encode("iso-8859-1"))).decode("iso-8859-1"), "rot-13")[::-1]
    
def byteobfuscate(b):
    """Minorly obfuscates a bytestring. While it is unreadable,
    don't expect this to stand up to anyone with a bit
    of python knowledge"""
    if objtype(b) != "bytes":
        raise InvalidTypeError("Argument \"b\" can only be bytestring")
        
    return lzma.compress(base64.a85encode(codecs.encode(str(b.decode("iso-8859-1"))[::-1], "rot-13").encode("iso-8859-1"))).decode("iso-8859-1")[::-1].encode("iso-8859-1")
    
def byteunobfuscate(b):
    """Unobfuscates a string obfuscated by beetroot.strobfuscate()"""
    if objtype(b) != "bytes":
        raise InvalidTypeError("Argument \"b\" can only be bytestring")
    
    return codecs.encode(base64.a85decode(lzma.decompress(b.decode("iso-8859-1")[::-1].encode("iso-8859-1"))).decode("iso-8859-1"), "rot-13")[::-1].encode("iso-8859-1")
    
def mem():
    try:
        yee = psutil.virtual_memory()
        return [yee.total, yee.used, yee.free]
    
    except NameError:
        raise ModuleError("psutil must be installed to use beetroot.mem(). Use pip install psutil or pip install beetroot[ram].")
    
def swapmem():
    try:
        yee = psutil.swap_memory()
        return [yee.total, yee.used, yee.free]
    
    except NameError:
        raise ModuleError("psutil must be installed to use beetroot.mem(). Use pip install psutil or pip install beetroot[ram].")
    
def beetroot():
    """BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT-"""
    while True:
        get_beetrolled = True
        print("""

██████╗░███████╗███████╗████████╗██████╗░░█████╗░░█████╗░████████╗
██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
██████╦╝█████╗░░█████╗░░░░░██║░░░██████╔╝██║░░██║██║░░██║░░░██║░░░
██╔══██╗██╔══╝░░██╔══╝░░░░░██║░░░██╔══██╗██║░░██║██║░░██║░░░██║░░░
██████╦╝███████╗███████╗░░░██║░░░██║░░██║╚█████╔╝╚█████╔╝░░░██║░░░
╚═════╝░╚══════╝╚══════╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░░╚════╝░░░░╚═╝░░░""", end="", flush=True)
        time.sleep(0.5)
        
    return 69420

def totally_not_a_rickroll():
    for i in range(0, 100):
        rickrolled = True
        
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ", new=0)
    return "".join(["U JUST GOT RICKROLLED IN ", str(datetime.datetime.now().year)])