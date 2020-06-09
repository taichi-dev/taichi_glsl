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
        return os.system(f'{sys.executable} -m pytest tests -n 4')

    def cmd_coverage(self, argv):
        return os.system('coverage run -m pytest tests')

    def cmd_report(self, argv):
        return os.system('coverage report && coverage html')

    def cmd_format(self, argv):
        return os.system(f'{sys.executable} -m yapf --style style.yapf -ir .')

    def cmd_dist(self, argv):
        return os.system(f'{sys.executable} setup.py bdist_wheel')


if __name__ == '__main__':
    cli = Main()
    exit(cli(sys.argv))
