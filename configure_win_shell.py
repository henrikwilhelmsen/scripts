# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Configure Windows Terminal and Powershell with my personal settings."""

import json
from pathlib import Path
from subprocess import check_output

win_terminal_data = {
    "application": {
        "alwaysShowNotificationIcon": False,
        "alwaysShowTabs": True,
        "copyFormatting": "none",
        "copyOnSelect": False,
        "minimizeToNotificationArea": False,
        "showTabsInTitlebar": True,
        "startOnUserLogin": False,
        "useAcrylicInTabRow": True,
    },
    "profiles": {
        "defaults": {
            "adjustIndistinguishableColors": "always",
            "colorScheme": "JetBrains Darcula",
            "cursorShape": "filledBox",
            "experimental.retroTerminalEffect": False,
            "font": {
                "face": "JetBrainsMono Nerd Font",
                "size": 16,
            },
            "opacity": 90,
            "padding": "24",
            "useAcrylic": False,
        },
    },
    "schemes": [
        {
            "background": "#202020",
            "black": "#000000",
            "blue": "#4581EB",
            "brightBlack": "#555555",
            "brightBlue": "#6D9DF1",
            "brightCyan": "#60D3D1",
            "brightGreen": "#67FF4F",
            "brightPurple": "#FB82FF",
            "brightRed": "#FB7172",
            "brightWhite": "#EEEEEE",
            "brightYellow": "#FFFF00",
            "cursorColor": "#FFFFFF",
            "cyan": "#33C2C1",
            "foreground": "#ADADAD",
            "green": "#126E00",
            "name": "JetBrains Darcula",
            "purple": "#FA54FF",
            "red": "#FA5355",
            "selectionBackground": "#1A3272",
            "white": "#ADADAD",
            "yellow": "#C2C300",
        },
    ],
}

powershell_profile_data = """oh-my-posh --init --shell pwsh --config "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/ys.omp.json" | Invoke-Expression

Import-Module -Name Terminal-Icons
Import-Module PSReadLine

Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineOption -EditMode Windows
"""  # noqa: E501


def get_powershell_profile() -> Path:
    """Get the path to the PowerShell user Profile.ps1 file.

    Creates the file if it does not already exist.
    """
    documents_dir = check_output(
        args=["powershell.exe", "[Environment]::GetFolderPath('MyDocuments')"],
        encoding="utf-8",
        shell=True,
    ).splitlines()[0]

    powershell_profile = Path(documents_dir) / "PowerShell" / "Profile.ps1"
    if not powershell_profile.exists():
        powershell_profile.touch()

    return powershell_profile


def get_win_terminal_config() -> Path:
    """Get the path to the Windows Terminal settings.json file.

    Raises:
        FileNotFoundError: If a file does not exist at the expected path
    """
    config_dir = Path.home().joinpath(
        "AppData",
        "Local",
        "Packages",
        "Microsoft.WindowsTerminal_8wekyb3d8bbwe",
        "LocalState",
        "settings.json",
    )

    if not config_dir.exists():
        msg = "Unable to locate Windows Terminal config."
        raise FileNotFoundError(msg)

    return config_dir


def update_terminal_config() -> None:
    """Update settings in existing terminal config file.

    The Windows Terminal settings file usually contains system specific settings in
    addition to schemes etc, so just overriding everything is not an option.
    Only insert the settings we want to maintain between systems.
    """
    target_file = get_win_terminal_config()
    with target_file.open(mode="r") as f:
        target_data = json.load(f)

    # update default profile settings
    target_data["profiles"]["defaults"] = win_terminal_data["profiles"]["defaults"]

    # update schemes, only add/override schemes found in source data
    source_schemes: list[dict[str, str]] = win_terminal_data["schemes"]
    target_schemes: list[dict[str, str]] = target_data["schemes"]
    source_scheme_names = [x["name"] for x in source_schemes]

    # remove any destination scheme that exists in source schemes
    for n, scheme in enumerate(target_schemes):
        if scheme["name"] in source_scheme_names:
            target_schemes.pop(n)

    # add source schemes to destination schemes
    target_schemes.extend(source_schemes)
    target_data["schemes"] = target_schemes

    # update application settings, not nested in destination only source
    source_application_data = win_terminal_data["application"]
    for key, value in source_application_data.items():
        target_data[key] = value

    # write target data to file
    with target_file.open("w", encoding="utf-8") as file:
        json.dump(target_data, file, indent=2)

    print(f"Updated Windows Terminal settings file: '{target_file.as_posix()}'")  # noqa: T201


def update_powershell_profile() -> None:
    """Write settings to the PowerShell Profile.ps1 file."""
    powershell_profile = get_powershell_profile()
    powershell_profile.write_text(data=powershell_profile_data, encoding="utf-8")
    print(f"Updated PowerShell profile: '{powershell_profile.as_posix()}'")  # noqa: T201


def main() -> None:
    """Update the Windows Terminal and PowerShell settings."""
    update_terminal_config()
    update_powershell_profile()


if __name__ == "__main__":
    main()
