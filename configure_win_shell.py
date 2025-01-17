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
            "colorScheme": "GruvboxDark",
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
            "name": "GruvboxDark",
            "black": "#282828",
            "red": "#cc241d",
            "green": "#98971a",
            "yellow": "#d79921",
            "blue": "#458588",
            "purple": "#b16286",
            "cyan": "#689d6a",
            "white": "#a89984",
            "brightBlack": "#928374",
            "brightRed": "#fb4934",
            "brightGreen": "#b8bb26",
            "brightYellow": "#fabd2f",
            "brightBlue": "#83a598",
            "brightPurple": "#d3869b",
            "brightCyan": "#8ec07c",
            "brightWhite": "#ebdbb2",
            "background": "#282828",
            "foreground": "#ebdbb2",
            "selectionBackground": "#665c54",
            "cursorColor": "#ebdbb2",
        },
        {
            "name": "GitHub Dark",
            "black": "#000000",
            "red": "#f78166",
            "green": "#56d364",
            "yellow": "#e3b341",
            "blue": "#6ca4f8",
            "purple": "#db61a2",
            "cyan": "#2b7489",
            "white": "#ffffff",
            "brightBlack": "#4d4d4d",
            "brightRed": "#f78166",
            "brightGreen": "#56d364",
            "brightYellow": "#e3b341",
            "brightBlue": "#6ca4f8",
            "brightPurple": "#db61a2",
            "brightCyan": "#2b7489",
            "brightWhite": "#ffffff",
            "background": "#101216",
            "foreground": "#8b949e",
            "selectionBackground": "#3b5070",
            "cursorColor": "#c9d1d9",
        },
    ],
}
powershell_profile_data = """oh-my-posh --init --shell pwsh --config "$env:POSH_THEMES_PATH/negligible.omp.json" | Invoke-Expression

Import-Module -Name Terminal-Icons
Import-Module -Name PSReadLine

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
