import os
import subprocess
from rich import print as cprint
from shutil import rmtree


"""
@Copyright 2023 MRX

license: XOSL - X Open Software License ('unknown')

You are granted free permission to work with the Software without restrictions, including not 
limited to, the rights to use, copy, modify, merge, publish, distribute.
All your developments using this software must also be open source and in the public domain.
You may not, however, sell copies of this software.
"""


user_login = os.getlogin()

pah_directory = f'/home/{user_login}/.pah'

aur_pkgs: list = []

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


def remove_pkg(package_name, del_deps: bool, ask: bool = True) -> int | None:
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


def init_confdir():
    if not confdir_exist():
        return os.mkdir(pah_directory)


def confdir_exist() -> bool:
    return os.path.exists(pah_directory)


def chdir_to_config():
    return os.chdir(pah_directory)


def remove_pkgs_list():
    os.remove(f'{pah_directory}/pkgs.list')


def args_error():
    cprint('[bold red]Error while parsing arguments[/]')


def continue_ask(ask='[bold]Do you want to continue? [Y/n]:') -> bool:
    cprint(ask, end=' ')
    if input() in ['n', 'no', 'N', 'NO', 'not', 'NOT', 'No']:
        return False

    return True


def init_aur_pkgs():
    global aur_pkgs
    aur_pkgs = subprocess.getoutput('pacman -Qqm').split('\n')
