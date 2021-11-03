import click

from clock import Clock
from vm import VM


@click.command()
@click.option("--load", help="The program to load")
def main(load):
    registers = 8
    clock = Clock(4, "hz")
    memory = 1

    vm = VM(registers, clock, memory)
    vm.boot(load)
    vm.run()


if __name__ == '__main__':
    main()
