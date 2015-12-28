
TEST_INPUT = """/:  Bus 04.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/6p, 5000M
    |__ Port 5: Dev 2, If 0, Class=Hub, Driver=hub/4p, 5000M
        |__ Port 4: Dev 3, If 0, Class=Hub, Driver=hub/4p, 5000M
/:  Bus 03.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/15p, 480M
    |__ Port 2: Dev 2, If 0, Class=Audio, Driver=usbfs, 12M
    |__ Port 2: Dev 2, If 1, Class=Audio, Driver=usbfs, 12M
    |__ Port 2: Dev 2, If 2, Class=Audio, Driver=usbfs, 12M
    |__ Port 2: Dev 2, If 3, Class=Human Interface Device, Driver=usbfs, 12M
    |__ Port 7: Dev 3, If 0, Class=Human Interface Device, Driver=usbhid, 12M
    |__ Port 7: Dev 3, If 1, Class=Human Interface Device, Driver=usbhid, 12M
    |__ Port 8: Dev 4, If 0, Class=Human Interface Device, Driver=usbhid, 1.5M
    |__ Port 9: Dev 5, If 0, Class=Hub, Driver=hub/4p, 480M
        |__ Port 4: Dev 8, If 0, Class=Hub, Driver=hub/4p, 480M
            |__ Port 2: Dev 10, If 0, Class=Wireless, Driver=btusb, 12M
            |__ Port 2: Dev 10, If 1, Class=Wireless, Driver=btusb, 12M
    |__ Port 11: Dev 6, If 0, Class=Hub, Driver=hub/3p, 12M
        |__ Port 1: Dev 9, If 0, Class=Human Interface Device, Driver=usbfs, 12M
        |__ Port 1: Dev 9, If 1, Class=Human Interface Device, Driver=usbfs, 12M
    |__ Port 13: Dev 7, If 0, Class=Human Interface Device, Driver=usbfs, 12M
    |__ Port 13: Dev 7, If 1, Class=Human Interface Device, Driver=usbfs, 12M
/:  Bus 02.Port 1: Dev 1, Class=root_hub, Driver=ehci-pci/2p, 480M
    |__ Port 1: Dev 2, If 0, Class=Hub, Driver=hub/8p, 480M
/:  Bus 01.Port 1: Dev 1, Class=root_hub, Driver=ehci-pci/2p, 480M
    |__ Port 1: Dev 2, If 0, Class=Hub, Driver=hub/6p, 480M"""

def main():
    pass

if __name__ == "__main__":
    main()
