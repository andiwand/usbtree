
class usbpath:
    def __init__(self, rootdev, subports=None, configuration=None, interface=None):
        if configuration == None: assert(interface == None)
        if interface == None: assert(configuration == None)
        
        self._rootdev = rootdev
        self._subports = tuple(subports) if subports != None else ()
        self._configuration = configuration
        self._interface = interface
    def __str__(self):
        result = str(self._rootdev) + "-"
        if len(self._subports) > 0: result += "-" + ".".join(map(str, self._subports))
        if self._configuration != None: result += ":" + str(self._configuration) + "." + str(self._interface)
        return result

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

class usbregistry:
    def __init__(self):
        pass
