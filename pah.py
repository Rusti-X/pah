import subprocess
from sys import argv
import rich
import libimpl


"""
@Copyright 2023 MRX

license: XOSL - X Open Software License ('unknown')

You are granted free permission to work with the Software without restrictions, including not
limited to, the rights to use, copy, modify, merge, publish, distribute.
All your developments using this software must also be open source and in the public domain.
You may not, however, sell copies of this software.
"""


PAH_VERSION = ['release', 1, 0]
PAH_LICENSE = 'X'


AUR_URL = 'https://aur.archlinux.org/'


if libimpl.user_uid == 0:
    rich.print('[bold red]You run aur helper as super user. It is forbidden![/]')
    exit(1)

libimpl.init_confdir()
libimpl.chdir_to_config()
libimpl.init_aur_pkgs()

try:
    if len(argv) > 2:
        if argv[1] in ['in', 'install']:
            ret_code_pkg = libimpl.install_pkg(argv[2], AUR_URL)
            if ret_code_pkg == 0:
                rich.print(f'[bold green]Package "{argv[2]}" installation completed successfully.[/]')

        elif argv[1] in ['rm', 'remove']:
            pkg = ''
            ret_code_pkg = 0
            if argv[2] in ['-rd', '--rm-deps']:
                pkg = argv[3]
                ret_code_pkg = libimpl.remove_pkg(pkg, del_deps=True)
            else:
                pkg = argv[2]
                ret_code_pkg = libimpl.remove_pkg(pkg, del_deps=False)

            if ret_code_pkg == 0:
                rich.print(f'[bold green]Package {pkg} removed successfully.[/]')

        else:
            libimpl.args_error()
            rich.print('[bold red]args len > 2 && undefined option[/]')

    elif len(argv) == 2:
        if argv[1] in ['upg', 'upgrade']:
            rich.print('[bold]Start updating all aur packages installed in the system by using pah[/]')
            if not libimpl.continue_ask():
                print('Exiting...')
                exit()
            rich.print('Upgrading packages...')
            for pkg in libimpl.aur_pkgs:
                upgrade_pkg_ret_code = libimpl.install_pkg(pkg, AUR_URL, ask=False)
                if upgrade_pkg_ret_code == 0:
                    rich.print(f'[bold green]Package "{pkg}" upgraded successfully.[/]')

        elif argv[1] in ['upd', 'update']:
            subprocess.run(['sudo', 'pacman', '-Syy'])

        elif argv[1] == 'aur-pkgs-list':
            subprocess.run(['pacman', '-Qm'])

        elif argv[1] == 'pkgs-list':
            subprocess.run(['pacman', '-Q'])

        elif argv[1] in ['h', 'help']:
            rich.print('[green]Help for pah:[/]')
            rich.print('[green]pah => python aur helper')
            print('Using:')
            print('\tinstall AUR pkg: pah [in, install] $package')
            print('\tremove pkg: pah [rm, remove] $package')
            print('\t        or: pah [rm, remove] [-rd, --rm-deps] $package')
            print('\tupgrade ALL AUR pkgs in the system: pah [upg, upgrade]')
            print('\tupdate repos: pah [upd, update]')
            print('\tprint all aur pkgs in the system: pah aur-pkgs-list')
            print('\tprint all pkgs in the system: pah pkgs-list')
            print('\tprint help: pah [h, help]')

        else:
            libimpl.args_error()
            rich.print('[bold red]args len == 2 && undefined option[/]')

    else:
        libimpl.args_error()
        rich.print('[bold red]args len !> 2 error[/]')

except KeyboardInterrupt:
    print()
    rich.print('[bold red]Ctrl^C : emergency stop.[/]')
