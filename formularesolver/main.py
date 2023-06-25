import csv
import sys
from collections import UserDict
from pathlib import Path
from typing import Iterator

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


def csv2variables(filename: str) -> Variables:
    "parse a CSV file into a Variables dict"
    variables = Variables()
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)
        for line_num, row in enumerate(reader, 1):
            for col_char, cell in zip(alphabetical_generator(), row):
                variables[col_char + str(line_num)] = cell.strip()
    return variables


def get_bounds(variables: Variables) -> Iterator[str]:
    "returns a list of excel cells where the indices are the csv positions"
    only_nums = lambda s: int("".join(c for c in s if c.isnumeric()))
    only_chars = lambda s: "".join(c for c in s if not c.isnumeric())
    max_line = max(map(only_nums, variables.keys()))
    max_col = max(map(only_chars, variables.keys()), key=lambda s: (len(s), s))

    return ((c + str(j) for c in arange("A", max_col)) for j in range(1, max_line + 1))


def variables2csv(variables: Variables) -> str:
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


def main() -> None:
    # argument checks
    assert len(sys.argv) == 2, ValueError(
        "wrong number of args, must pass a filename as the first argument"
    )
    filename, path = sys.argv[1], Path(sys.argv[1])
    assert path.exists(), FileNotFoundError(f"file {filename} doesn't exist")
    assert path.is_file(), FileNotFoundError(f"argument {filename} is not a file")

    # read and parse file
    try:
        variables = csv2variables(filename)
    except Exception as e:
        raise Exception(f"Could not parse CSV file: {e}")

    # evaluates cells and print to stdout
    try:
        csv_out = "".join(variables2csv(variables))
        print(csv_out.rstrip(), end="")
    except Exception as e:
        raise Exception(f"Interpreter Error: {e}")


if __name__ == "__main__":
    main()
