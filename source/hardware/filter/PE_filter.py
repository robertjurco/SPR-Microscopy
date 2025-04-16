from ctypes import *

STATUS_CODE = {
    0: "PE_SUCCESS Function executed successfully.",
    1: "PE_INVALID_HANDLE Supplied handle is corrupted or has a NULL value.",
    2: "PE_FAILURE Communication with system failed.",
    3: "PE_MISSING_CONFIGFILE Configuration file is missing",
    4: "PE_INVALID_CONFIGURATION Configuration file is corrupted",
    5: "PE_INVALID_WAVELENGTH Requested wavelength is out of bound.",
    6: "PE_MISSING_HARMONIC_FILTER Nor harmonic filter present in the system configuration",
    7: "PE_INVALID_FILTER Requested filter does not match any available.",
    8: "PE_UNKNOWN An unknown status code has been returned by the system.",
    9: "PE_INVALID_GRATING Requested grating does not match any available.",
    10: "PE_INVALID_BUFFER Output buffer has a NULL value.",
    11: "PE_INVALID_BUFFER_SIZE Output buffer size is too small to receive the value.",
    12: "PE_UNSUPPORTED_CONFIGURATION The system configuration is not supported by this SDK.",
    13: "PE_NO_FILTER_CONNECTED No filter connected.",
}


class PEDevice:
    def __init__(self, dll_path, config_file_path):
        self.dll_path = dll_path
        self.config_file_path = config_file_path
        self.pe_dll = CDLL(self.dll_path)

        self.pe_create = self.pe_dll.PE_Create
        self.pe_create.restype = c_int
        self.pe_create.argtypes = [c_char_p, POINTER(c_void_p)]

        self.pe_get_system_name = self.pe_dll.PE_GetSystemName
        self.pe_get_system_name.restype = c_int
        self.pe_get_system_name.argtypes = [c_void_p, c_int, c_char_p, c_size_t]

        self.pe_open = self.pe_dll.PE_Open
        self.pe_open.restype = c_int
        self.pe_open.argtypes = [c_void_p, c_char_p]

        self.pe_set_wavelength = self.pe_dll.PE_SetWavelength
        self.pe_set_wavelength.restype = c_int
        self.pe_set_wavelength.argtypes = [c_void_p, c_double]

        self.pe_close = self.pe_dll.PE_Close
        self.pe_close.restype = c_int
        self.pe_close.argtypes = [c_void_p]

        self.pe_destroy = self.pe_dll.PE_Destroy
        self.pe_destroy.restype = c_int
        self.pe_destroy.argtypes = [c_void_p]

        self.pe_get_wavelength_range = self.pe_dll.PE_GetWavelengthRange
        self.pe_get_wavelength_range.restype = c_int
        self.pe_get_wavelength_range.argtypes = [
            c_void_p,
            POINTER(c_double),
            POINTER(c_double),
        ]

        self.pe_handle = c_void_p()
        self.MAX_SYSTEM_NAME_LEN = 256
        self.system_name = create_string_buffer(self.MAX_SYSTEM_NAME_LEN)

    def initialize(self):
        status = self.pe_create(
            self.config_file_path.encode("utf-8"), byref(self.pe_handle)
        )
        if status != 0:
            raise RuntimeError(
                f"PE_Create failed with status: {status} - {STATUS_CODE[status]}"
            )

        status = self.pe_get_system_name(
            self.pe_handle, 0, self.system_name, self.MAX_SYSTEM_NAME_LEN
        )
        if status != 0:
            raise RuntimeError(
                f"PE_GetSystemName failed with status: {status} - {STATUS_CODE[status]}"
            )
        print(f"System Name: {self.system_name.value.decode('utf-8')}")

        status = self.pe_open(self.pe_handle, self.system_name)
        if status != 0:
            raise RuntimeError(
                f"PE_Open failed with status: {status} - {STATUS_CODE[status]}"
            )

        min_wavelength = c_double()
        max_wavelength = c_double()
        status = self.pe_get_wavelength_range(
            self.pe_handle, byref(min_wavelength), byref(max_wavelength)
        )
        if status != 0:
            raise RuntimeError(
                f"PE_GetWavelengthRange failed with status: {status} - {STATUS_CODE[status]}"
            )
        print(f"Wavelength Range: {min_wavelength.value}, {max_wavelength.value}")

    def set_wavelength(self, wavelength):
        status = self.pe_set_wavelength(self.pe_handle, c_double(wavelength))
        if status != 0:
            raise RuntimeError(
                f"PE_SetWavelength failed with status: {status} - {STATUS_CODE[status]}"
            )
        print(f"Wavelength Set: {wavelength}")

    def close(self):
        status = self.pe_close(self.pe_handle)
        if status != 0:
            raise RuntimeError(
                f"PE_Close failed with status: {status} - {STATUS_CODE[status]}"
            )

    def destroy(self):
        status = self.pe_destroy(self.pe_handle)
        if status != 0:
            raise RuntimeError(
                f"PE_Destroy failed with status: {status} - {STATUS_CODE[status]}"
            )


if __name__ == "__main__":
    dll_path = r"C:\Users\jurco\PycharmProjects\SPR-Microscopy\source\hardware\filter\PE_Filter_SDK.dll"
    config_file_path = r"C:\Program Files\Photon etc\PHySpecV2\Devices\M000010666.xml"

    device = PEDevice(dll_path, config_file_path)
    device.initialize()
    device.set_wavelength(420)
    device.close()
    device.destroy()