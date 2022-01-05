from enum import Enum
from pathlib import Path
from cpu.instructions import InstructionSet

import click


INSTRUCTION_SET = InstructionSet()


class Types(Enum):
    DATA = 0
    ADDRESS = 1
    MEMORY = 2
    NUMBER = 3


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def read_lines(lines):
    return [line.strip() for line in lines if not line.strip() == "" and not line.strip().startswith(";")]

def read_instruction(instruction):
    match [s for s in instruction.split(" ") if s]:
        case[label, instruction, args]:
            return label[:-1], INSTRUCTION_SET[instruction.strip()], args.split(",")

        case[instruction, args]:
            if instruction.endswith(":"):
                return instruction.strip()[:-1], INSTRUCTION_SET[args], None

            else:
                return None, INSTRUCTION_SET[instruction.strip()], args.split(",")

        case[instruction]:
            return None, INSTRUCTION_SET[instruction.strip()], [""]


def determine_type(ins):
    """
    Determine if an instruction src or dest is a number, a data register, an address regiser or a memory location
    """

    if ins.startswith("#$"):
        return Types.NUMBER

    elif ins.startswith("0x"):
        return Types.MEMORY

    elif ins.startswith("a"):
        return Types.ADDRESS

    elif ins.startswith("d"):
        return Types.DATA


@click.command()
@click.option("--input", help="The program to compile", required=True)
@click.option("--output", help="The name of the output file", required=True)
def compile(input, output):
    print(f"Compiling: {input} to {output}...")
    code = ""
    offset = 0
    fn_offset = 0
    labels = {}
    instructions = []

    try:
        with Path(input).open() as f:
            code = read_lines(f.readlines())

    except FileNotFoundError as ex:
        error = [
            f"{bcolors.FAIL}\nCompilation failed!",
            f"Input File: '{ex.filename}' does not exist"
        ]

        exit("\n".join(error))

    # First pass to find labels
    try:
        for num, instruction in enumerate(code):
            print("\r", f"Compiling {str(num).zfill(len(str(len(code))))}/{len(code)}...", end="")
            label, parsed_instruction, args = read_instruction(instruction)

            if label:
                labels[label] = offset

            offset += len(parsed_instruction)

    except KeyError as e:
        print(instruction)
        error = [
            f"{bcolors.FAIL}\nCompilation failed!",
            f"Syntax error on line {num+1}: {e} is not a recognized instruction!{bcolors.ENDC}"
        ]

        exit("\n".join(error))

    print("\r", f"{bcolors.OKGREEN}Compiling {str(num+1).zfill(len(str(len(code))))}/{len(code)}... Done!{bcolors.ENDC}")

    # Second pass parsing
    for num, instruction in enumerate(code):
        # Remember to find comments elsewhere in a line (not the beginning) and grab everything before the ";" character, attempt to use that as an instruction
        print("\r", f"Linking {str(num).zfill(len(str(len(code))))}/{len(code)}...", end="")
        label, parsed_instruction, args = read_instruction(instruction)

        if any([
                parsed_instruction == "move.b",
                parsed_instruction == "add.b",
                parsed_instruction == "sub.b",
                parsed_instruction == "div.b",
                parsed_instruction == "mul.b",
        ]):
            parsed_instruction.src_type = determine_type(args[0])
            parsed_instruction.dest_type = determine_type(args[1])

            if parsed_instruction.src_type == Types.DATA or parsed_instruction.src_type == Types.ADDRESS:
                parsed_instruction.src = args[0][1:]

            else:
                parsed_instruction.src = args[0][2:]

            if parsed_instruction.dest_type == Types.DATA or parsed_instruction.dest_type == Types.ADDRESS:
                parsed_instruction.dest = args[1]

            else:
                parsed_instruction.dest = args[1][2:]

            instructions.append(str(parsed_instruction))

        elif parsed_instruction == "inc" or parsed_instruction == "dec":
            parsed_instruction.dest_type = args[0]

            if parsed_instruction.dest_type == Types.DATA or parsed_instruction.dest_type == Types.ADDRESS:
                parsed_instruction.dest = args[0][1:]

            else:
                parsed_instruction.dest = args[0][2:]

            instructions.append(str(parsed_instruction))

        elif parsed_instruction == "halt":
            instructions.append(str(parsed_instruction))

        elif parsed_instruction == "noop":
            instructions.append(str(parsed_instruction))

        elif parsed_instruction == "jmp":
            try:
                parsed_instruction.dest = labels[args[0]]
                parsed_instruction.dest_type = str(Types.MEMORY.value).zfill(2)
                instructions.append(str(parsed_instruction))

            except KeyError as e:
                error = [
                    f"{bcolors.FAIL}\nCompilation failed!",
                    f"Undefined label error on line {num+1}: {e} is not a recognized label, did you forget to define it or misspell it?{bcolors.ENDC}"
                ]
                exit("\n".join(error))

        elif parsed_instruction == "cmp.b":
            parsed_instruction.src_type = determine_type(args[0])
            parsed_instruction.dest_type = determine_type(args[1])

            if parsed_instruction.src_type == Types.NUMBER:
                parsed_instruction.src = args[0][2:].zfill(2)

            else:
                parsed_instruction.src = args[0]

            if parsed_instruction.dest_type == Types.DATA or parsed_instruction.dest_type == Types.ADDRESS:
                parsed_instruction.dest = args[1]

            else:
                parsed_instruction.dest = args[1][2:].zfill(2)

            instructions.append(str(parsed_instruction))

        elif any([
                parsed_instruction == "jnz",
                parsed_instruction == "jng",
                parsed_instruction == "jeq",
                parsed_instruction == "jne",
            ]):
            parsed_instruction.dest = labels[args[0]]
            parsed_instruction.dest_type = str(Types.MEMORY).zfill(2)
            instructions.append(str(parsed_instruction))

        # Update label offset
        fn_offset += len(parsed_instruction)

    print("\r", f"{bcolors.OKGREEN}Linking {str(num+1).zfill(len(str(len(code))))}/{len(code)}... Done!{bcolors.ENDC}")

    with Path(output).open("w+") as f:
        f.write(f".DATA\n")
        f.write(f"START: {labels['start']}\n")
        f.write(f"LENGTH: {len(instructions)}\n\n")
        f.write(".CODE\n")

        for instruction in instructions:
            f.write(f"{instruction}\n")

    print(f"{bcolors.OKGREEN}Done!{bcolors.ENDC}")


if __name__ == '__main__':
    try:
        compile()

    except KeyboardInterrupt:
        exit("Cancelled")
