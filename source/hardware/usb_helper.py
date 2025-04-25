import wmi
import re
from collections import defaultdict


def get_usb_device_tree():
    c = wmi.WMI()

    # Get all USB devices with their details
    devices = {}

    # Query USB devices
    print("Getting USB devices...")
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
    print("Getting USB controllers...")
    for controller in c.query("SELECT * FROM Win32_USBController"):
        if not hasattr(controller, 'DeviceID') or not controller.DeviceID:
            continue

        devices[controller.DeviceID] = {
            "Name": getattr(controller, 'Name', "Unknown Controller"),
            "DeviceID": controller.DeviceID,
            "Status": getattr(controller, 'Status', "Unknown"),
            "IsController": True
        }

    # Print all found devices for debugging
    print(f"Found {len(devices)} USB devices/controllers")

    # Build the tree structure - IMPORTANT: This is where the fix is
    connections = defaultdict(list)
    print("Getting USB connections...")

    for assoc in c.query("SELECT * FROM Win32_USBControllerDevice"):
        try:
            # Convert WMI objects to strings
            antecedent = str(assoc.Antecedent)  # Controller
            dependent = str(assoc.Dependent)  # Device

            # Print association info for debugging
            print("\nAssociation found:")
            print(f"Antecedent (first 60 chars): {antecedent[:60]}...")
            print(f"Dependent (first 60 chars): {dependent[:60]}...")

            # IMPORTANT: The key fix - Win32_USBControllerDevice associations can be in two directions
            # Try both possibilities and see which one works

            # Try first interpretation (Antecedent=Controller, Dependent=Device)
            ctrl_match1 = re.search(r'DeviceID ?= ?"?([^";\n]+)', antecedent)
            dev_match1 = re.search(r'DeviceID ?= ?"?([^";\n]+)', dependent)

            # Try reverse interpretation (Antecedent=Device, Dependent=Controller)
            ctrl_match2 = re.search(r'DeviceID ?= ?"?([^";\n]+)', dependent)
            dev_match2 = re.search(r'DeviceID ?= ?"?([^";\n]+)', antecedent)

            # Check first interpretation
            if ctrl_match1 and dev_match1:
                controller_id = ctrl_match1.group(1)
                device_id = dev_match1.group(1)

                # Only add if controller_id is a controller and device_id is a device
                if controller_id in devices and device_id in devices:
                    if devices[controller_id].get("IsController", False):
                        connections[controller_id].append(device_id)
                        print(f"Added relationship: {controller_id[:30]}... -> {device_id[:30]}...")

            # Check second interpretation
            if ctrl_match2 and dev_match2:
                controller_id = ctrl_match2.group(1)
                device_id = dev_match2.group(1)

                # Only add if controller_id is a controller and device_id is a device
                if controller_id in devices and device_id in devices:
                    if devices[controller_id].get("IsController", False):
                        connections[controller_id].append(device_id)
                        print(f"Added relationship: {controller_id[:30]}... -> {device_id[:30]}...")

        except Exception as e:
            print(f"Error: {str(e)}")

    return connections, devices


def print_usb_tree():
    connections, devices = get_usb_device_tree()

    print("\n====== USB DEVICE TREE ======\n")

    # Find controller devices
    controllers = {device_id: info for device_id, info in devices.items()
                   if info.get("IsController", False)}

    # Print each controller and its devices
    for controller_id, info in controllers.items():
        name = info["Name"]
        status = info["Status"]

        print(f"🧰 CONTROLLER: {name}")
        print(f"   Status: {status}")
        print(f"   ID: {controller_id}")
        print()

        # Print connected devices
        connected_devices = connections.get(controller_id, [])
        if connected_devices:
            for i, device_id in enumerate(connected_devices):
                if device_id in devices:
                    device = devices[device_id]
                    last = i == len(connected_devices) - 1
                    prefix = "└─" if last else "├─"

                    print(f"   {prefix} 📱 {device['Name']}")
                    print(f"      Status: {device['Status']}")
                    print(f"      ID: {device_id}")
                    print()
        else:
            print("   No connected devices found.")
            print()

        print("-" * 50)


# Run the script
try:
    print_usb_tree()
except Exception as e:
    import traceback

    print(f"Error: {str(e)}")
    traceback.print_exc()