import argparse
import sys, os


class Main:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Taichi GLSL CLI')
        self.parser.add_argument('command')

    def __call__(self, argv):
        args = self.parser.parse_args(argv[1:2])
        getattr(self, f'cmd_{args.command}')(argv[2:])

    def cmd_test(self, argv):
        os.system('coverage run -m pytest tests')

    def cmd_report(self, argv):
        os.system('coverage report')

    def cmd_format(self, argv):
        os.system('yapf --style style.yapf -ir .')

    def cmd_dist(self, argv):
        os.system(f'{sys.executable} setup.py bdist_wheel')


if __name__ == '__main__':
    cli = Main()
    exit(cli(sys.argv))