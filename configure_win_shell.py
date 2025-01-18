# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Configure Windows Terminal and Powershell with my personal settings."""

import json
from pathlib import Path
from subprocess import check_output

OMP_THEME = "negligible"
WIN_TERMINAL_THEME = "Monokai Pro"
WIN_TERMINAL_FONT = "CaskaydiaCove Nerd Font"

powershell_profile_data = f"""oh-my-posh --init --shell pwsh --config "$env:POSH_THEMES_PATH/{OMP_THEME}.omp.json" | Invoke-Expression

Import-Module -Name Terminal-Icons
Import-Module -Name PSReadLine

Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineOption -EditMode Windows
"""  # noqa: E501

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
            "colorScheme": WIN_TERMINAL_THEME,
            "cursorShape": "filledBox",
            "experimental.retroTerminalEffect": False,
            "font": {
                "face": WIN_TERMINAL_FONT,
                "size": 16,
            },
            "opacity": 90,
            "padding": "24",
            "useAcrylic": False,
        },
    },
    "schemes": [
        {
            "name": "Monokai Pro",
            "black": "#403e41",
            "red": "#ff6188",
            "green": "#a9dc76",
            "yellow": "#ffd866",
            "blue": "#fc9867",
            "purple": "#ab9df2",
            "cyan": "#78dce8",
            "white": "#fcfcfa",
            "brightBlack": "#727072",
            "brightRed": "#ff6188",
            "brightGreen": "#a9dc76",
            "brightYellow": "#ffd866",
            "brightBlue": "#fc9867",
            "brightPurple": "#ab9df2",
            "brightCyan": "#78dce8",
            "brightWhite": "#fcfcfa",
            "background": "#403e41",
            "foreground": "#fcfcfa",
            "selectionBackground": "#fcfcfa",
            "cursorColor": "#fcfcfa",
        },
        {
            "name": "Monokai Pro (Filter Octagon)",
            "black": "#000000",
            "red": "#d81e00",
            "green": "#5ea702",
            "yellow": "#cfae00",
            "blue": "#427ab3",
            "purple": "#89658e",
            "cyan": "#00a7aa",
            "white": "#dbded8",
            "brightBlack": "#686a66",
            "brightRed": "#f54235",
            "brightGreen": "#99e343",
            "brightYellow": "#fdeb61",
            "brightBlue": "#84b0d8",
            "brightPurple": "#bc94b7",
            "brightCyan": "#37e6e8",
            "brightWhite": "#f1f1f0",
            "background": "#282a3a",
            "foreground": "#eaf2f1",
        },
        {
            "name": "Monokai Pro (Filter Ristretto)",
            "black": "#403838",
            "red": "#FD6883",
            "green": "#ADDA78",
            "yellow": "#F9CC6C",
            "blue": "#F38D70",
            "purple": "#A8A9EB",
            "cyan": "#85DACC",
            "white": "#FFF1F3",
            "brightBlack": "#72696A",
            "brightRed": "#FD6883",
            "brightGreen": "#ADDA78",
            "brightYellow": "#F9CC6C",
            "brightBlue": "#F38D70",
            "brightPurple": "#A8A9EB",
            "brightCyan": "#85DACC",
            "brightWhite": "#FFF1F3",
            "background": "#2C2525",
            "foreground": "#FFF1F3",
            "selectionBackground": "#C3B7B8",
            "cursorColor": "#FFF1F3",
        },
    ],
}


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
