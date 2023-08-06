#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name, protected-access

"""
Generates/Patches/Synchronizes a hop Python package with a PostgreSQL database
using the `hop` command.

Initiate a new project and repository with the `hop new <project_name>` command.
The <project_name> directory should not exist when using this command.

In the <project name> directory generated, the hop command helps you patch your
model, keep your Python synced with the PostgreSQL model, test your Python code and
deal with CI.

TODO:
On the 'devel' or any private branch hop applies patches if any, runs tests.
On the 'main' or 'master' branch, hop checks that your git repo is in sync with
the remote origin, synchronizes with devel branch if needed and tags your git
history with the last release applied.
"""

import os
import subprocess
import sys
from getpass import getpass
from configparser import ConfigParser

import click
import psycopg2
from git import Repo, GitCommandError

from half_orm.model import Model, CONF_DIR
from half_orm.model_errors import MissingConfigFile

from half_orm_packager.globals import TEMPLATES_DIR, hop_version
from half_orm_packager.patch import Patch
from half_orm_packager.test import tests
from half_orm_packager.update import update_modules
from half_orm_packager.hgit import HGit

PWD = os.path.abspath(os.path.curdir)

def get_connection_file_name(base_dir=None, ref_dir=None):
    """searches the hop configuration file for the package.
    This method is called when no hop config file is provided.
    It changes to the package base directory if the config file exists.
    """
    config = ConfigParser()

    cur_dir = base_dir
    if not base_dir:
        ref_dir = os.path.abspath(os.path.curdir)
        cur_dir = base_dir = ref_dir
    for base in ['hop', 'halfORM']:
        if os.path.exists('.{}/config'.format(base)):
            config.read('.{}/config'.format(base))
            config_file = config['halfORM']['config_file']
            package_name = config['halfORM']['package_name']
            return config_file, package_name, cur_dir

    if os.path.abspath(os.path.curdir) != '/':
        os.chdir('..')
        cur_dir = os.path.abspath(os.path.curdir)
        return get_connection_file_name(cur_dir, ref_dir)
    # restore reference directory.
    os.chdir(ref_dir or PWD)
    return None, None, None

class Hop:
    "XXX: The hop class doc..."
    __connection_file_name, __package_name, __project_path = get_connection_file_name()
    __model = None

    def __init__(self):
        self.__production = False
        if self.__package_name and self.__model is None:
            self.__model = self.get_model()
            self.__production = self.__model.production

    def get_model(self):
        "Returns the half_orm model"
        # config_file, package_name = get_connection_file_name()

        if not self.package_name:
            sys.stderr.write(
                "You're not in a hop package directory.\n"
                "Try hop new <package directory> or change directory.\n")

        try:
            self.__model = Model(self.package_name)
            model = self.alpha()  # XXX To remove after alpha
            return model
        except psycopg2.OperationalError as exc:
            sys.stderr.write(f'The database {self.package_name} does not exist.\n')
            raise exc
        except MissingConfigFile:
            sys.stderr.write(
                'Cannot find the half_orm config file for this database.\n')
            sys.exit(1)


    @property
    def production(self):
        return self.__production

    @property
    def connection_file_name(self):
        "returns the connection file name"
        return self.__connection_file_name

    @property
    def package_name(self):
        "returns the package name"
        return self.__package_name

    @package_name.setter
    def package_name(self, package_name):
        self.__package_name = package_name

    @property
    def project_path(self):
        return self.__project_path

    @project_path.setter
    def project_path(self, project_path):
        if self.__project_path is None:
            self.__project_path = project_path

    @property
    def package_path(self):
        return f'{self.project_path}/{self.package_name}'

    @property
    def model(self):
        "model getter"
        if self.__model is None and self.__package_name:
            self.model = self.get_model()
        return self.__model

    @model.setter
    def model(self, model):
        "model setter"
        self.__model = model

    def alpha(self):
        """Toutes les modifs à faire durant la mise au point de hop
        """
        if not self.model.has_relation('half_orm_meta.hop_release'):
            if self.model.has_relation('meta.release'):
                click.echo(
                    "ALPHA: Renaming meta.release to half_orm_meta.hop_release, ...")
                self.model.execute_query("""
                create schema half_orm_meta;
                create schema "half_orm_meta.view";
                alter table meta.release set schema half_orm_meta;
                alter table meta.release_issue set schema half_orm_meta ;
                alter table half_orm_meta.release rename TO hop_release ;
                alter table half_orm_meta.release_issue rename TO hop_release_issue ;
                alter view "meta.view".last_release set schema "half_orm_meta.view" ;
                alter view "meta.view".penultimate_release set schema "half_orm_meta.view" ;
                alter view "half_orm_meta.view".last_release rename TO hop_last_release ;
                alter view "half_orm_meta.view".penultimate_release rename TO hop_penultimate_release ;
                """)
                click.echo("Please re-run the command.")
                sys.exit()
        # if not model.has_relation('half_orm_meta.view.hop_penultimate_release'):
        #     TODO: fix missing penultimate_release on some databases.
        return Model(self.package_name)

    def __str__(self):
        return f"""
        connection_file_name: {self.connection_file_name}
        package_name: {self.package_name}
        """


# print(HOP)

BASE_DIR = os.getcwd()

TMPL_CONF_FILE = """[database]
name = {name}
user = {user}
password = {password}
host = {host}
port = {port}
production = {production}
"""


def status():
    """Prints the status"""
    print('STATUS')
    print(HOP)
    next_release = Patch(HOP).get_next_release()
    while next_release:
        next_release = Patch(HOP).get_next_release(next_release)
    print('hop --help to get help.')


def read_template(file_path):
    "helper"
    with open(file_path, encoding='utf-8') as file_:
        return file_.read()

def write_file(file_path, content):
    "helper"
    with open(file_path, 'w', encoding='utf-8') as file_:
        file_.write(content)

def init_package(model, project_name: str):
    """Initialises the package directory.

    model (Model): The loaded model instance
    project_name (str): The project name (hop create argument)
    """
    curdir = os.path.abspath(os.curdir)
    project_path = os.path.join(curdir, project_name)
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    else:
        sys.stderr.write(f"ERROR! The path '{project_path}' already exists!\n")
        sys.exit(1)
    README = read_template(f'{TEMPLATES_DIR}/README')
    CONFIG_TEMPLATE = read_template(f'{TEMPLATES_DIR}/config')
    SETUP_TEMPLATE = read_template(f'{TEMPLATES_DIR}/setup.py')
    GIT_IGNORE = read_template(f'{TEMPLATES_DIR}/.gitignore')
    PIPFILE = read_template(f'{TEMPLATES_DIR}/Pipfile')

    dbname = model._dbname
    setup = SETUP_TEMPLATE.format(dbname=dbname, package_name=project_name)
    write_file(f'{project_path}/setup.py', setup)
    write_file(f'{project_path}/Pipfile', PIPFILE)
    os.mkdir(f'{project_path}/.hop')
    write_file(f'{project_path}/.hop/config',
        CONFIG_TEMPLATE.format(
            config_file=project_name, package_name=project_name))
    cmd = " ".join(sys.argv)
    readme = README.format(cmd=cmd, dbname=dbname, package_name=project_name)
    write_file(f'{project_path}/README.md', readme)
    write_file(f'{project_path}/.gitignore', GIT_IGNORE)
    os.mkdir(f'{project_path}/{project_name}')
    HOP.project_path = project_path
    HGit(HOP).init()
    print(f"\nThe hop project '{project_name}' has been created.")

def set_config_file(project_name: str):
    """ Asks for the connection parameters. Returns a dictionary with the params.
    """
    print(f'HALFORM_CONF_DIR: {CONF_DIR}')
    HOP.package_name = project_name
    conf_path = os.path.join(CONF_DIR, project_name)
    if not os.path.isfile(conf_path):
        if not os.access(CONF_DIR, os.W_OK):
            sys.stderr.write(f"You don't have write acces to {CONF_DIR}.\n")
            if CONF_DIR == '/etc/half_orm':
                sys.stderr.write(
                    "Set the HALFORM_CONF_DIR environment variable if you want to use a\n"
                    "different directory.\n")
            sys.exit(1)
        print('Connection parameters to the database:')
        dbname = input(f'. database name ({project_name}): ') or project_name
        user = os.environ['USER']
        user = input(f'. user ({user}): ') or user
        password = getpass('. password: ')
        if password == '' and \
                (input(
                    '. is it an ident login with a local account? [Y/n] ') or 'Y').upper() == 'Y':
            host = port = ''
        else:
            host = input('. host (localhost): ') or 'localhost'
            port = input('. port (5432): ') or 5432

        production = input('Production (False): ') or False

        res = {
            'name': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port,
            'production': production
        }
        open(f'{CONF_DIR}/{project_name}',
             'w', encoding='utf-8').write(TMPL_CONF_FILE.format(**res))
    else:
        print(f"Using '{CONF_DIR}/{project_name}' file for connexion.")

    try:
        return Model(project_name)
    except psycopg2.OperationalError:
        config = ConfigParser()
        config.read([conf_path])
        dbname = config.get('database', 'name')

        sys.stderr.write(f"The database '{dbname}' does not exist.\n")
        create = input('Do you want to create it (Y/n): ') or "y"
        if create.upper() == 'Y':
            subprocess.run(['createdb', dbname], check=True)
            return Model(project_name)
        print(f'Please create the database an rerun hop new {project_name}')
        sys.exit(1)

@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-v', '--version', is_flag=True)
def main(ctx, version):
    """
    Generates/Synchronises/Patches a python package from a PostgreSQL database
    """
    if HOP.model:
        if ctx.invoked_subcommand is None:
            status()
        if version:
            click.echo(f'hop {hop_version()}')
            sys.exit()
    else:
        sys.stderr.write(
            "You're not in a hop package directory.\n"
            "Try hop new <package directory> or change directory.\n")
        sys.exit()

    sys.path.insert(0, '.')

@click.command()
@click.argument('package_name')
def new(package_name):
    """ Creates a new hop project named <package_name>.

    It adds to your database a patch system (by creating the relations:
    * half_orm_meta.hop_release
    * half_orm_meta.hop_release_issue
    and the views
    * "half_orm_meta.view".hop_last_release
    * "half_orm_meta.view".hop_penultimate_release
    """
    # click.echo(f'hop new {package_name}')
    # on cherche un fichier de conf .hop/config dans l'arbre.
    conf_file, _, _ = get_connection_file_name('.')
    if conf_file is not None:
        sys.stderr.write("ERROR! Can't run hop new in a hop project.\n")
        sys.exit(1)
    model = set_config_file(package_name)

    init_package(model, package_name)


@click.command()
@click.option('-f', '--force', is_flag=True, help="Don't check if git repo is clean.")
@click.option('-r', '--revert', is_flag=True, help="Revert to the previous release.")
@click.option('-p', '--prep-next', type=click.Choice(['patch', 'minor', 'major']))
def patch(force, revert, prep_next):
    """ Applies the next patch.
    """
    if not prep_next:
        Patch(HOP).patch(force, revert)
    else:
        Patch(HOP).prep_next_release(prep_next)

    sys.exit()


@click.command()
# @click.option('-d', '--dry-run', is_flag=True, help='Do nothing')
# @click.option('-l', '--loop', is_flag=True, help='Run every patches to apply')
def upgrade():
    """Apply one or many patches.

    switches to hop_main, pulls should check the tags
    """
    Patch(HOP).patch()

@click.command()
def test():
    """ Tests some common pitfalls.
    """
    if tests(HOP.model, HOP.package_name):
        click.echo('Tests OK')
    else:
        click.echo('Tests failed')

HOP = Hop()
if not HOP.model:
    main.add_command(new)
elif not HOP.production:
    # commands only available in dev
    main.add_command(patch)
    main.add_command(test)
    # main.add_command(update)
else:
    # in prod
    main.add_command(upgrade)

if __name__ == '__main__':
    main({}, None)
