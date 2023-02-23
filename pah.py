from sys import argv
import rich
import libimpl


AUR_URL = 'https://aur.archlinux.org/'


if libimpl.user_uid == 0:
    rich.print('[bold red]You run aur helper as super user. It is forbidden![/]')
    exit(1)

libimpl.create_confdir()
libimpl.chdir_to_config()

try:
    if len(argv) > 2:
        if argv[1] in ['in', 'install']:
            ret_code_pkg = libimpl.install_pkg(argv[2], AUR_URL)
            if ret_code_pkg == 0:
                libimpl.change_pkgs_list(f'{argv[2]}', 'a')
                rich.print(f'[bold green]Package "{argv[2]}" installation completed successfully.[/]')

        elif argv[1] in ['rm', 'remove']:
            pkg = ''
            ret_code_pkg = 0
            if argv[2] in ['-rd', '--rm-deps']:
                pkg = argv[3]
                ret_code_pkg = libimpl.remove_pkg(pkg, True)
            else:
                pkg = argv[2]
                ret_code_pkg = libimpl.remove_pkg(pkg, False)

            if ret_code_pkg == 0:
                # print(f'print 1: {pkg}')
                try:
                    pkgs_list_without_rm_pkg = libimpl.get_pkgs_list()
                    pkgs_list_without_rm_pkg.remove(pkg)
                except IndexError:
                    pkgs_list_without_rm_pkg = None
                libimpl.remove_pkgs_list()
                if pkgs_list_without_rm_pkg is not None:
                    for pkg_ in pkgs_list_without_rm_pkg:
                        libimpl.change_pkgs_list(pkg_, 'a')
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
            for pkg in libimpl.get_pkgs_list():
                ret_code_pkg = libimpl.install_pkg(pkg, AUR_URL)
                rich.print(f'[bold green]Package "{pkg}" upgraded successfully.[/]')

        elif argv[1] in ['h', 'help']:
            rich.print('[green]Help for pah:[/]')
            rich.print('[green]pah : python aur helper')
            print('Using:')
            print('\tinstall pkg: pah [in, install] $package')
            print('\tremove pkg: pah [rm, remove] $package')
            print('\t        or: pah [rm, remove] [-rd, --rm-deps] $package')
            print('\tupgrade pkgs: pah [upg, upgrade]')
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
