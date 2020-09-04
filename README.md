# An Automatic Schematic Generation Tool
This tool generates schematics from a SPICE netlist, usually of output from
[qflow](https://github.com/RTimothyEdwards/qflow). It was initially developed
during Summer 2020 under the mentorship of Tim Edwards. The schematic entry
tools currently supported are Xschem and EESchema.

# Usage
asg can be installed using PIP by running `pip install asg`.

Once installed, it can be run with `asg [netlist] [library]`

Full usage:
```
usage: asg [-h] [-f FORMAT] [-d DEPTH] [--vcc VCC] [--vss VSS] [-l] [-e] [-D] input library

positional arguments:
  input
  library

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        output format - one of xschem, eeschema
  -d DEPTH, --depth DEPTH
                        depth to unpack subcircuits
  --vcc VCC             vcc net name
  --vss VSS             vss net name
  -l, --include-library-name
                        include the library name in xschem output. should be used if xschem library env var is a directory instead of a list
  -e, --no-embed-symbols
                        don't embed symbols in xschem schematic output
  -D, --debug           output intermediate steps of the ASG to ./out/
```

# Contributing
To run in a development environment, run `python -m asg.main`, with appropriate
arguments as seen above

The program is organized into a few different submodules under `asg/`:
- `generation`: Constraint classes and the algorithm which optimizes them
- `grammar`: Generic classes for parsing and writing files (currently only used
for s-expressions for EESchema)
- `input`: Reading a netlist from qflow or other synthesis tool
- `library_source`: Reads symbols and parses out metadata and pin locations
- `output`: Writes a schematic from an internal representation to a schematic file
- `entities.py`: A collection of geometry classes and representations of
schematic components
- `intermediate_lang.py`: Representations of schematics and netlists as
collections of components and connections
