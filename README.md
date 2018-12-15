# Parser for a Small Programming Language

## cc3102-tarea2

---

This project corresponds to the second homework of Universidad de Chile's cc3102 course, a small Python implementation using [Python's PLY](http://github.com/dabeaz/ply)

## Installation Instructions

---

The project was implemented to run on [Python 3.7](https://www.python.org/), installation instructions for the language in each system can be found in their [down load's page](https://www.python.org/downloads/).

For the project depends heavily on the [Python's PLY](http://github.com/dabeaz/ply) package, specifically version **`3.11`** of it.

This can be installed using `Python`'s package manager `pip` with the command:

```bash
pip install ply
```

## Execution Examples

---

To execute the code, simply run the command:

```bash
python program.py
```

The program will then ask for an executable to run, four tests are included with the project, these are `test_1`, `test_2`, `test_3` and `test_4`.

* `test_1` simply tests some simple variable assignment, usage and a loop.

* `test_2` is a simple implementation of fibonacci calculation.

```bash
Enter filename to execute (or press enter to end):
>> test_2
#> 20
6765
Enter filename to execute (or press enter to end):
>> 
```

* `test_3` is a simple implementation of factorial calculation.

```bash
Enter filename to execute (or press enter to end):
>> test_3
#> 12
479001600
Enter filename to execute (or press enter to end):
>> 
```

* Finally, `test_4` tests single line programs and should display an error when attempting to print a non-existent variable.
