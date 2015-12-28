import os
import re
import util

class UsbIdentifier:
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
    def __hash__(self):
        return self._vendor + 31 * self._device

class UsbPath:
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
        result += "-" + ".".join(map(str, self._path[1:]))
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
    def getParent(self):
        if len(self) == 0: return None
        if self._configuration != None:
            return UsbPath(self._path)
        return UsbPath(self._path[:-1])

class UsbNode:
    def __init__(self, path, identifier):
        self._path = path
        self._identifier = identifier
    def __str__(self):
        return str(self._path)
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self._path == other._path)
    def __hash__(self):
        return hash(self._path)
    def isRoot(self):
        pass
    def isLeave(self):
        pass

class UsbRegistry:
    def __init__(self):
        self._nodes = set()
        self._byPath = {}
        self._byIdentifier = {}
    def addNode(self, node):
        if node in self._nodes: return
        self._nodes.add(node)
        self._byPath[node._path] = node
        if node._identifier not in self._byIdentifier:
            self._byIdentifier[node._identifier] = set()
        self._byIdentifier[node._identifier].add(node)
    def removeNode(self, node):
        if node not in self._nodes: return
        self._nodes.remove(node)
        del self._byPath[node._path]
        self._byIdentifier[node._identifier].remove(node)
        if not self._byIdentifier[node._identifier]:
            del self._byIdentifier[node._identifier]
    def getByPath(self, path):
        return self._byPath.get(path)
    def getByIdentifier(self, identifier):
        return set(self._byIdentifier.get(identifier))

class UsbUtil:
    @staticmethod
    def getRegistry():
        result = UsbRegistry()
        path = "/sys/bus/usb/devices/"
        for filename in os.listdir(path):
            subpath = os.path.join(path, filename)
            UsbUtil._getRegistryHelper(result, subpath)
        return result
    @staticmethod
    def _getRegistryHelper(registry, path):
        filename = os.path.basename(path)
        usbpath = UsbUtil.toUsbPath(filename)
        if usbpath == None: return
        
        vendorFile = os.path.join(path, "idVendor")
        deviceFile = os.path.join(path, "idProduct")
        usbidentifier = None
        if os.path.isfile(vendorFile) and os.path.isfile(deviceFile):
            usbidentifier = UsbIdentifier(util.readFile(vendorFile), util.readFile(deviceFile))
        
        node = UsbNode(usbpath, usbidentifier)
        registry.addNode(node)
    @staticmethod
    def toUsbPath(s):
        root_prefix = "usb"
        if s.startswith(root_prefix):
            num = int(s[len(root_prefix):])
            return UsbPath((num,))
        
        file_regex = re.compile(r"(\d+)(?:-((?:(?:\d+\.)+)?\d+)(?:\:(\d+)\.(\d+))?)?")
        m = file_regex.match(s)
        if m:
            path = []
            path.append(int(m.group(1)))
            path.extend(map(int, m.group(2).split(".")))
            configuration = None
            interface = None
            if m.group(3) != None:
                configuration = int(m.group(3))
                interface = int(m.group(4))
            return UsbPath(path, configuration, interface)
        
        return None
