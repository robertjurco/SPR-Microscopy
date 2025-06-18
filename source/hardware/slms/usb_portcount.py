import wmi
import re

def get_connected_usb_devices():
    c = wmi.WMI()
    results = []

    for assoc in c.query("SELECT * FROM Win32_USBControllerDevice"):
        try:
            # Extract controller and device paths
            controller_path = assoc.Antecedent
            device_path = assoc.Dependent

            # Clean the device ID from WMI string format
            device_id = re.search(r'DeviceID="([^"]+)"', device_path).group(1).replace('\\\\', '\\')
            controller_id = re.search(r'DeviceID="([^"]+)"', controller_path).group(1).replace('\\\\', '\\')

            # Get actual device and controller objects
            device = c.query(f"SELECT * FROM Win32_PnPEntity WHERE DeviceID = '{device_id}'")
            controller = c.query(f"SELECT * FROM Win32_USBController WHERE DeviceID = '{controller_id}'")

            if device and controller:
                dev = device[0]
                ctrl = controller[0]
                results.append({
                    "DeviceName": dev.Name,
                    "Manufacturer": dev.Manufacturer,
                    "DeviceID": dev.DeviceID,
                    "Controller": ctrl.Name,
                    "USBVersionHint": "3.x" if "xHCI" in ctrl.Name else "2.0 or older",
                    "Status": dev.Status
                })
        except Exception as e:
            continue

    return results

# Print results
devices = get_connected_usb_devices()
for d in devices:
    print(f"\nDevice: {d['DeviceName']}")
    print(f"  Manufacturer: {d['Manufacturer']}")
    print(f"  DeviceID: {d['DeviceID']}")
    print(f"  Connected to Controller: {d['Controller']}")
    print(f"  USB Version (Hint): {d['USBVersionHint']}")
    print(f"  Status: {d['Status']}")
