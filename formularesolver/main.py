import cmd
import csv
import sys
from collections import UserDict
from pathlib import Path
from typing import Generator

from interpreter import formula_resolver
from utils import alphabetical_generator, arange


class Variables(UserDict):
    "evaluate a cell variable when getitem is called"

    def __getitem__(self, key):
        cell = super().__getitem__(key)
        cell = cell.lstrip("=")
        return formula_resolver(cell, variables=self) if cell else ""

    def __missing__(self, key):
        return ""

    def __repr__(self) -> str:
        cells = [list(line) for line in get_bounds(self)]

        # gen header with col names from the first line
        header = ["|      |"]
        for cell in cells[0]:
            cell = "".join(c for c in cell if not c.isnumeric())  # remove numbers
            header.append(f"{cell:^6}|")
        header.append("\n")

        # construct and add table divisor / spacer
        len_header = len("".join(header)) - 1
        div = "-" * len_header + "\n"
        repr = [div] + header + [div]

        # iter all cells and add then to the table representation
        for line in cells:
            # add line number
            n = "".join(c for c in line[0] if c.isnumeric())  # remove letters
            repr.append(f"|{n:^6}|")
            # add cells
            for cell in line:
                repr.append(f"{self[cell]:>6}|")
            repr.append("\n")

        repr.append(div)
        return "".join(repr)


def csv2variables(filename: str) -> Variables:
    "parse a CSV file into a Variables dict"
    variables = Variables()
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)
        for line_num, row in enumerate(reader, 1):
            for col_char, cell in zip(alphabetical_generator(), row):
                variables[col_char + str(line_num)] = cell.strip()
    return variables


def variables2csv(variables: Variables) -> Generator:
    "evaluates the cell variables and format then into a csv"
    lines = get_bounds(variables)
    first = True
    for line in lines:
        for cell in line:
            if first:
                yield f"{variables[cell]}"
                first = False
            else:
                yield f",{variables[cell]}"
        yield "\n"
        first = True


def get_bounds(variables: Variables) -> Generator:
    "returns a list of excel cells where the indices are the csv positions"
    only_nums = lambda s: int("".join(c for c in s if c.isnumeric()))
    only_chars = lambda s: "".join(c for c in s if not c.isnumeric())
    max_line = max(map(only_nums, variables.keys()))
    max_col = max(map(only_chars, variables.keys()), key=lambda s: (len(s), s))

    return ((c + str(j) for c in arange("A", max_col)) for j in range(1, max_line + 1))


class PyParseExcelShell(cmd.Cmd):
    intro = "Welcome to the PyParseExcel shell.\nType help or ? to list commands.\n"
    prompt = "(sheet) "
    file = None

    def __init__(self, variables: Variables) -> None:
        self.variables = variables
        super().__init__()

    def do_set(self, arg: str) -> None:
        "attribute a value to a given cell in the sheet\n\t$ set [cell] [formula / value]"
        cell, formula, *_ = arg.split(maxsplit=1)
        self.variables[cell] = formula
        print(f">>> {cell} = {self.variables[cell]}")

    def do_get(self, arg: str) -> None:
        "print the value of a cell to the terminal\n\t$ get [cell]"
        cell, *_ = arg.split()
        formula = self.variables.__dict__["data"].get(cell)
        print(f">>> {cell} = {self.variables[cell]}  (formula: {formula!r})")

    def do_view(self, arg) -> None:
        "print the sheet to the terminal"
        print(self.variables)

    def do_dump(self, arg) -> None:
        "convert sheet to csv and print output to the terminal"
        csv_out = "".join(variables2csv(self.variables))
        print(csv_out)

    def do_exit(self, arg: str) -> bool:
        "exit the shell"
        return True


def main() -> None:
    # argument checks
    assert len(sys.argv) in (2, 3), ValueError(
        "wrong number of args, must pass a filename as an argument"
    )
    filename, path = sys.argv[-1], Path(sys.argv[-1])
    assert path.exists(), FileNotFoundError(f"file {filename} doesn't exist")
    assert path.is_file(), FileNotFoundError(f"argument {filename} is not a file")

    # read and parse file
    try:
        variables = csv2variables(filename)
    except Exception as e:
        raise Exception(f"Could not parse CSV file: {e}")

    # on interactve flag, enter REPL mode
    if "-i" in sys.argv:
        PyParseExcelShell(variables).cmdloop()
        return

    # evaluates cells and print to stdout
    try:
        csv_out = "".join(variables2csv(variables))
        print(csv_out.rstrip(), end="")
    except Exception as e:
        raise Exception(f"Interpreter Error: {e}")


if __name__ == "__main__":
    main()
