# pubpdf
Produce a PDF for a set of publications.

pubpdf currently only handles publication metadata in mods or bib format, and mods records can be fetched via OAI-PMH.

Conversion of records is performed using bibutils, which must be installed separately.

# Installation

## Installing bibutils
On Unix platforms, it is often found in the package management system.

If you need to compile it from source, such as on Windows:

1. Fetch the latest tarball from https://sourceforge.net/projects/bibutils/files/

2. Unpack it using `tar` and, in the new directory, run: `./configure; make; make install`

## Installing pubpdf
```sh
$ pip install "git+https://github.com/jayvdb/pubpdf"
```

# Usage

```
pubpdf [options] pid [pid]

pubpdf produces a publications list. Args that start with '--' (eg. --oai-api)
can also be set in a config file (~/.pubpdfrc or .pubpdfrc or ~/.pubrc or
.pubrc or specified via -c). Config file syntax allows: key=value, flag=true,
stuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi). If an arg is
specified in more than one place, then commandline values override config file
values which override defaults.

positional arguments:
  pids                  pids (identifiers)

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config file path
  --oai-api OAI_API     OAI API URL
  --oai-format OAI_FORMAT
                        OAI format
  --oai-identifier-prefix OAI_IDENTIFIER_PREFIX
                        OAI identifier prefix
  --check-oai-repo      Iterate over all publications in repository
  --csl-style CSL_STYLE
                        CSL style name
  --csl-style-dir CSL_STYLE_DIR
                        Directory containing CSL style files
  --group-by-type       Group types of publicatons together
  --html-preamble HTML_PREAMBLE
  --output-file OUTPUT_FILE
                        Output filename
```

## Targets

The publications to be included in the PDF may be specified as:

1. A list of OAI PIDs, such as `une:1 une:5 une:6`.

2. A list of filenames to mods files.

3. A single filename ending with `.bib`, which should be a complete set of publications .

While processing the specified target MODS records, a file `pubs.pdf.bib` will be written into the current directory.

If there is a problem parsing a BibTeX records, manually modify the generated .bib file to simplify the LaTeX as appropriate.
A list of potential parsing problems can be seen at https://github.com/brechtm/citeproc-py/issues/55 .

The option `--check-oai-repo` is primarily intended to be used as a way to verify that all publications
in the repository are sucessfully parsed by bibutils and citeproc.

When using the `--check-oai-repo` mode, one or two pids may be provided as command arguments to indicate the
start and end range that should be checked.
