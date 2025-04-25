import wmi

def get_usb_devices_and_speeds():
    c = wmi.WMI()
    usb_devices = c.query("SELECT * FROM Win32_USBHub")
    usb_devices_info = {}

    for device in usb_devices:
        device_info = {}
        device_info["DeviceID"] = device.DeviceID
        device_info["Name"] = device.Name
        device_info["Status"] = device.Status
        device_info["USBVersion"] = device.USBVersion  # Use USBVersion instead of SpecVersion
        usb_devices_info[device.DeviceID] = device_info

    return usb_devices_info

usb_devices = get_usb_devices_and_speeds()
for device_id, info in usb_devices.items():
    print(f"Device ID: {device_id}")
    for key, value in info.items():
        print(f"  {key}: {value}")