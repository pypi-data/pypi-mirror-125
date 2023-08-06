from os import geteuid
from subprocess import call, check_output

from py_cui import PyCUI

from recoverpy.utils.logger import LOGGER


def is_user_root(window: PyCUI) -> bool:
    """Check if user has root privileges.

    The method is simply verifying if EUID == 0.
    It may be problematic in some edge cases. (Some particular OS)
    But, as grep search will not exit quickly, exception handling
    can't be used.

    Args:
        window (PyCUI): PyCUI window to display popup.

    Returns:
        bool: User is root
    """
    if geteuid() == 0:
        LOGGER.write("info", "User is root")
        return True

    window.show_error_popup("Not root :(", "You have to be root or use sudo.")
    LOGGER.write("warning", "User is not root")
    return False


def lsblk() -> list:
    """Use lsblk to generate a list of detected system partitions."

    Returns:
        list: List of system partitions.
    """
    lsblk_output = check_output(
        ["lsblk", "-r", "-n", "-o", "NAME,TYPE,FSTYPE,MOUNTPOINT"],
        encoding="utf-8",
    )
    partitions_list_raw = [
        line.strip()
        for line in lsblk_output.splitlines()
        if " loop " not in line and "swap" not in line
    ]
    partitions_list_formatted = [line.split(" ") for line in partitions_list_raw]

    LOGGER.write(
        "debug",
        str(partitions_list_formatted),
    )

    return partitions_list_formatted


def format_partitions_list(window: PyCUI, raw_lsblk: list) -> dict:
    """Format found partition list to a dict.

    Args:
        window (PyCUI): PyCUI window to display popup.
        raw_lsblk (list): Raw lsblk output.

    Returns:
        dict: Found partitions with format :
            {Name: FSTYPE, IS_MOUNTED, MOUNT_POINT}
    """
    # Create dict with relevant infos
    partitions_dict = {}
    for partition in raw_lsblk:
        if len(partition) < 3:
            # Ignore if no FSTYPE detected
            continue

        if len(partition) < 4:
            is_mounted = False
            mount_point = None
        else:
            is_mounted = True
            mount_point = partition[3]

        partitions_dict[partition[0]] = {
            "FSTYPE": partition[2],
            "IS_MOUNTED": is_mounted,
            "MOUNT_POINT": mount_point,
        }

    # Warn the user if no partition found with lsblk
    if not partitions_dict:
        LOGGER.write("Error", "No partition found !")
        window.show_error_popup("Hum...", "No partition found.")
        return None

    LOGGER.write("debug", "Partition list generated using 'lsblk'")
    LOGGER.write("debug", f"{len(partitions_dict)} partitions found")

    return partitions_dict


def is_installed(command: str) -> bool:
    """Verify if 'progress' tool is installed on current system.

    Args:
        command (str): Command to be queried.

    Returns:
        bool: 'progress' is installed.
    """
    output = call(["which", command])

    return output == 0
