import os
import subprocess
from rich import print as cprint
from shutil import rmtree


user_login = os.getlogin()

pah_directory = f'/home/{user_login}/.pah'

user_uid = os.getuid()


def clone_pkg(pkg_git) -> int | None:
    clone = subprocess.run(['git', 'clone', pkg_git])

    return clone.returncode


def install_pkg(package_name, AUR_URL, ask: bool = True) -> int | list:
    pkg_git = f'{AUR_URL}{package_name}.git'
    clone_pkg(pkg_git)
    if ask:
        if not continue_ask():
            print('Exiting...')
            rmtree(package_name)
            exit()
    print()
    cprint('[bold]Installing package...[/]')
    os.chdir(package_name)
    makepkg = subprocess.run(['makepkg', '-si'])
    os.chdir(pah_directory)
    rmtree(package_name)

    return makepkg.returncode

    # else:
    #     cprint(f'[bold red]Package "{package_name}" not found![/]')


def remove_pkg(package_name, del_deps: bool = False, ask: bool = True) -> int | None:
    pacman_key = '-R'
    if ask:
        if not continue_ask(f'[bold]Do you want to delete package "{package_name}"? [Y/n]:'):
            print('Exiting...')
            exit()
    if del_deps:
        pacman_key = '-Rs'
    pacman = ['sudo', 'pacman', pacman_key, package_name]
    pacman_run = subprocess.run(pacman)
    return pacman_run.returncode


def create_confdir():
    if not confdir_exist():
        return os.mkdir(pah_directory)


def confdir_exist() -> bool:
    return os.path.exists(pah_directory)


def chdir_to_config():
    return os.chdir(pah_directory)


def change_pkgs_list(to_write, type_of_changing: str):
    chdir_to_config()
    with open(f'{pah_directory}/pkgs.list', type_of_changing) as f:
        if f'{to_write}' not in get_pkgs_list():
            f.write(f'{to_write}')
            f.write('\n')


def remove_pkgs_list():
    os.remove(f'{pah_directory}/pkgs.list')


def get_pkgs_list() -> list | None:
    if confdir_exist():
        pkgs = None
        try:
            with open(f'{pah_directory}/pkgs.list', 'r') as f:
                pkgs = f.read().split('\n')
                del pkgs[-1]
        except FileNotFoundError:
            with open(f'{pah_directory}/pkgs.list', 'w') as f:
                pkgs = []
        return pkgs


def args_error():
    cprint('[bold red]Error while parsing arguments[/]')


def continue_ask(ask='[bold]Do you want to continue? [Y/n]:') -> bool:
    cprint(ask, end=' ')
    if input() in ['n', 'no', 'N', 'NO', 'not', 'NOT', 'No']:
        return False

    return True
