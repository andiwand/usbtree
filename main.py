import usb

def main():
    r = usb.UsbUtil.getRegistry()
    for n in r._nodes:
        print n._path, n._identifier

if __name__ == "__main__":
    main()
