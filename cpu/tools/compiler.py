from pathlib import Path
from cpu.instructions import InstructionSet

import click

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
    instruction_set = InstructionSet()

    match instruction.split(" "):
        case[instruction, args]:
            return instruction_set[instruction], args.split(",")

        case[instruction]:
            return instruction_set[instruction], [""]


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

    with Path(input).open() as f:
        code = read_lines(f.readlines())

    # First pass to find labels
    try:
        for num, instruction in enumerate(code):
            print("\r", f"Compiling {str(num).zfill(len(str(len(code))))}/{len(code)}...", end="")
            parsed_instruction, args = read_instruction(instruction)
            offset += parsed_instruction.operands * parsed_instruction.length

            if parsed_instruction == "define":
                labels[args[0]] = offset
                parsed_instruction.label = labels[args[0]]

    except KeyError as e:
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
        parsed_instruction, args = read_instruction(instruction)

        # If this line defines a label
        if parsed_instruction == "define":
            labels[args[0]] = fn_offset
            parsed_instruction.label = labels[args[0]]
            instructions.append(str(parsed_instruction))

        elif parsed_instruction == "move.b":
            if args[0].startswith("#$"):
                parsed_instruction.src = args[0][2:]

            else:
                parsed_instruction.src = args[0]

            parsed_instruction.dest = args[1]
            instructions.append(str(parsed_instruction))

        elif parsed_instruction == "halt":
            instructions.append(str(parsed_instruction))

        elif parsed_instruction == "noop":
            instructions.append(str(parsed_instruction))

        elif parsed_instruction == "jmp":
            parsed_instruction.label = labels[args[0]]
            instructions.append(str(parsed_instruction))

        elif parsed_instruction == "cmp.b":
            if args[0].startswith("#$"):
                parsed_instruction.source = args[0][2:].zfill(2)
                parsed_instruction.destination = args[1][2:].zfill(2)

            else:
                parsed_instruction.source = args[0]
                parsed_instruction.destination = args[1]

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
    compile()
