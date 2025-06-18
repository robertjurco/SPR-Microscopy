import wmi
import re
from collections import defaultdict


def get_usb_device_tree():
    c = wmi.WMI()

    # Get all USB devices with their details
    devices = {}

    # Query USB devices
    for dev in c.query("SELECT * FROM Win32_PnPEntity WHERE PNPClass = 'USB'"):
        if not hasattr(dev, 'DeviceID') or not dev.DeviceID:
            continue

        devices[dev.DeviceID] = {
            "Name": getattr(dev, 'Name', "Unknown Device"),
            "DeviceID": dev.DeviceID,
            "Status": getattr(dev, 'Status', "Unknown"),
            "IsController": False
        }

    # Query USB controllers
    for controller in c.query("SELECT * FROM Win32_USBController"):
        if not hasattr(controller, 'DeviceID') or not controller.DeviceID:
            continue

        devices[controller.DeviceID] = {
            "Name": getattr(controller, 'Name', "Unknown Controller"),
            "DeviceID": controller.DeviceID,
            "Status": getattr(controller, 'Status', "Unknown"),
            "IsController": True
        }

    # Build the tree structure
    connections = defaultdict(list)

    for assoc in c.query("SELECT * FROM Win32_USBControllerDevice"):
        try:
            # Convert WMI objects to strings
            antecedent = str(assoc.Antecedent)  # Controller
            dependent = str(assoc.Dependent)  # Device

            # Try both possibilities and see which one works
            # Try first interpretation (Antecedent=Controller, Dependent=Device)
            ctrl_match1 = re.search(r'DeviceID ?= ?\"?([^\";\\n]+)', antecedent)
            dev_match1 = re.search(r'DeviceID ?= ?\"?([^\";\\n]+)', dependent)

            # Try reverse interpretation (Antecedent=Device, Dependent=Controller)
            ctrl_match2 = re.search(r'DeviceID ?= ?\"?([^\";\\n]+)', dependent)
            dev_match2 = re.search(r'DeviceID ?= ?\"?([^\";\\n]+)', antecedent)

            # Check first interpretation
            if ctrl_match1 and dev_match1:
                controller_id = ctrl_match1.group(1)
                device_id = dev_match1.group(1)

                # Only add if controller_id is a controller and device_id is a device
                if controller_id in devices and device_id in devices:
                    if devices[controller_id].get("IsController", False):
                        connections[controller_id].append(device_id)

            # Check second interpretation
            if ctrl_match2 and dev_match2:
                controller_id = ctrl_match2.group(1)
                device_id = dev_match2.group(1)

                # Only add if controller_id is a controller and device_id is a device
                if controller_id in devices and device_id in devices:
                    if devices[controller_id].get("IsController", False):
                        connections[controller_id].append(device_id)

        except Exception as e:
            print(f"Error: {str(e)}")

    return connections, devices


def count_usb_ports():
    connections, devices = get_usb_device_tree()

    total_ports = 0
    occupied_ports = 0

    # Count total ports and occupied ports
    for controller_id, connected_devices in connections.items():
        total_ports += 1
        if connected_devices:
            occupied_ports += 1

    free_ports = total_ports - occupied_ports

    return total_ports, occupied_ports, free_ports


# Run the script to count USB ports
try:
    total_ports, occupied_ports, free_ports = count_usb_ports()
    print(f"Total USB ports: {total_ports}")
    print(f"Occupied USB ports: {occupied_ports}")
    print(f"Free USB ports: {free_ports}")
except Exception as e:
    import traceback

    print(f"Error: {str(e)}")
    traceback.print_exc()
