class AAWEMGError(Exception):
    """Base exception for aawlab-emg."""


class DeviceDisconnectedError(AAWEMGError):
    """Raised when the serial device stops producing data."""


class ProtocolVersionError(AAWEMGError):
    """Raised when an unsupported packet version is detected."""
