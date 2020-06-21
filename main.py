import argparse
import sys, os


class Main:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Taichi GLSL CLI Tools')
        self.parser.add_argument('command', default='test', nargs='?')

    def __call__(self, argv):
        args = self.parser.parse_args(argv[1:2])
        getattr(self, f'cmd_{args.command}')(argv[2:])

    def cmd_test(self, argv):
        pytest = 'pytest -nauto '
        tests = 'tests'
        if len(argv):
            tests = ' '.join(f'tests/test_{a}.py' for a in argv)

        return os.system(pytest + tests)

    def cmd_coverage(self, argv):
        return os.system('coverage run -m pytest tests')

    def cmd_report(self, argv):
        return os.system('coverage report && coverage html')

    def cmd_format(self, argv):
        return os.system(f'yapf -ir .')

    def cmd_doc(self, argv):
        return os.system(f'make -C docs ' + ' '.join(argv))

    def cmd_dist(self, argv):
        return os.system(f'{sys.executable} setup.py bdist_wheel')

    def cmd_install(self, argv):
        return os.system(f'{sys.executable} setup.py bdist_wheel && '
                'pip install --user --upgrade dist/*.whl')


if __name__ == '__main__':
    cli = Main()
    exit(cli(sys.argv))
