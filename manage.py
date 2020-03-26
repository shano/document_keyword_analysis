#!/usr/bin/env python

from flask_script import Manager, Command
from flask_migrate import MigrateCommand

from app import create_app
from tests.command import PytestCommand


manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config_file', required=False)
manager.add_command('test', PytestCommand)

if __name__ == '__main__':
    manager.run()
