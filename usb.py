import re
import os

class usbpath:
    def __init__(self, path=None, configuration=None, interface=None):
        if configuration == None: assert(interface == None)
        if interface == None: assert(configuration == None)
        
        self._path = tuple(path) if path != None else ()
        self._configuration = configuration
        self._interface = interface
    def __len__(self):
        return len(self._path)
    def __str__(self):
        result = ""
        if len(self._path) == 0: return result
        result += str(self._path[0])
        if len(self._path) == 1: return result
        result += "-" + ".".join(map(str, *self._path[1:]))
        if self._configuration != None: result += ":" + str(self._configuration) + "." + str(self._interface)
        return result
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self._path == other._path
                and self._configuration == other._configuration
                and self._interface == other._interface)
    def __hash__(self):
        return hash(self._path) + 31 * hash(self._configuration) + 37 * hash(self._interface)
    def isChild(self, other):
        return ((len(self._path) > len(other._path)
                    or (len(self._path) == len(other._path)
                    and self._configuration != None))
                and other._configuration == None
                and self._path[:len(other._path)] == other._path)
    def isParent(self, other):
        return other.isChild(self)

class usbidentifier:
    def __init__(self, idVendor, idDevice):
        self._vendor = idVendor if isinstance(idVendor, (int, long)) else int(idVendor, 16)
        self._device = idDevice if isinstance(idDevice, (int, long)) else int(idDevice, 16)
    def __str__(self):
        return hex(self._vendor)[2:].zfill(4) + ":" + hex(self._device)[2:].zfill(4)
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self._vendor == other._vendor
                and self._device == other._device)
    def __ne__(self, other):
        return not self.__eq__(other)

class usbnode:
    def __init__(self, path, identifier):
        self._path = path
        self._identifier = identifier
        self._parent = None
        self._children = set()
    def __str__(self):
        return str(self._path)
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self._path == other._path)
    def __hash__(self):
        return hash(self._path)
    def isRoot(self):
        return self._parent == None
    def isLeave(self):
        return len(self._children) == 0
    def size(self):
        return 1 + sum((child.size() for child in self._children))
    def depth(self, i):
        if self.isLeave(): return i
        return max((child.depth(i + 1) for child in self._children))
    def attach(self, other):
        if other._parent != None: return False
        if self == other: return False
        if not other._path.isChild(self._path): return False
        for child in self._children:
            if child.attach(other): return True
        children = set(self._children)
        self._children.add(other)
        other._parent = self
        for child in children:
            if child == other: continue
            if child._path.isChild(other._path):
                child.detach()
                other.attach(child)
        return True
    def detach(self):
        if self._parent == None: return False
        self._parent._children.remove(self)
        self._parent = None
        return True

class usbtree:
    def __init__(self):
        self._root = usbnode(usbpath([]), None)
        self._identifierMap = {}
    def size(self):
        return self._root.size() - 1
    def depth(self):
        return self._root.depth(0)
    def add(self, node):
        self._root.attach(node)
        if node._identifier != None:
            identifiers = self._identifierMap.get(node._identifier)
            if identifiers == None: identifiers = self._identifierMap[node._identifier] = []
            identifiers.add(node)

class usbutil:
    @staticmethod
    def usbtree():
        result = usbtree()
        path = "/sys/bus/usb/devices/"
        for f in os.listdir(path):
            subpath = os.path.join(path, f)
            if not os.path.islink(subpath): continue
            if not f.startswith("usb"): continue
            usbutil._usbtree_helper(result, subpath)
        return result
    @staticmethod
    def _usbtree_helper(tree, path):
        filename = os.path.basename(path)
        upath = usbutil._usbtree_path(filename)
        for f in os.listdir(path):
            subpath = os.path.join(path, f)
            
    @staticmethod
    def _usbtree_path(f):
        root_prefix = "usb"
        if f.startswith(root_prefix):
            num = int(f[len(root_prefix):])
            return usbpath((num,))
        file_regex = re.compile(r"(\d+)(?:-((?:(?:\d+\.)+)\d)(?:\:(\d+)\.(\d+))?)?")
        m = file_regex.match(f)
        if m:
            path = []
            path.append(int(m.group(1)))
            path.append(map(int, m.group(2).split(".")))
            configuration = None
            interface = None
            if m.groups > 2:
                configuration = int(m.group(3))
                interface = int(m.group(4))
            return usbpath(path, configuration, interface)
        return None

#t = usbutil.usbtree()
