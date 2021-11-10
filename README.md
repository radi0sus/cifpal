# cifpal
A Python 3 script for printing the summary table and tables of bond lengths and angles to the console. The script furthermore calculates average values, including a variety of statistical parameters, and is able to group bonding parameters. Contacts within a defined radius can be printed as well. The output should result in nicely rendered mark down tables. 

The script uses the Gemmi library for CIF processing:

https://gemmi.readthedocs.io/en/latest/

https://github.com/project-gemmi/gemmi

## External modules
 `gemmi`,  `pandas`,  `tabulate`
 
## Quick start
 Start the script with:
```console
python3 cifpal.py filename.cif atom1_name (atom2_name ...)
```
to open the CIF. It gives the following output:

A table with general information.

```
| compound                   | 1K-kd25                                      |
|----------------------------|----------------------------------------------|
| empirical formula          | C₆₈H₁₂₆Cu₄F₁₂K₂N₁₆O₁₈.₅₀S₄                   |
| moiety formula             | C₆₆H₁₂₆Cu₄F₆K₂N₁₆O₁₂S₂²⁺, 2(CF₃O₃S⁻), 0.5(O) |
| formula weight             | 2152.44                                      |
| T /K                       | 133(2)                                       |
| ...                        | ...                                          |
```
A table of bond lengths with atoms from the input, `atom1_name (atom2_name ...)`, Cu1 for example.
```
| Atoms   | Bond length /Å   |
|---------|------------------|
| Cu1–O1  | 1.907(2)         |
| Cu1–N1  | 1.911(3)         |
| ...     | ....             |
```
A table with general bond lengths.
```
| Atoms   | Bonds lengths /Å                       |
|---------|----------------------------------------|
| Cu–N    | 1.911(3), 2.154(3), 2.170(3), 2.187(3) |
| Cu–O    | 1.907(2)                               |
```
A table with summarized general bond lengths.
```
| Atoms   | Bond lengths /Å     |
|---------|---------------------|
| Cu–N    | 1.911(3) - 2.187(3) |
| Cu–O    | 1.907(2)            |
```
A table with statistical parameters.
```
| Atoms   |   Count |   Mean /Å |   Median /Å |   Sam. std. dev. |   Pop. std. dev. |   Std. error |   Skewness |
|---------|---------|-----------|-------------|------------------|------------------|--------------|------------|
| Cu–N    |       4 |    2.1055 |       2.162 |           0.1304 |           0.1129 |       0.0652 |    -1.9361 |
| Cu–O    |       1 |    1.907  |       1.907 |         nan      |           0      |     nan      |   nan      |
```
Four tables with angles in the same manner.

A figure caption with bond lengths and angles.
```
Selected distances /Å and angles /° for 1K-kd25: Cu1–O1 1.907(2), Cu1–N1 1.911(3), 
Cu1–N3 2.154(3), Cu1–N5 2.170(3), Cu1–N4 2.187(3); O1–Cu1–N1 98.68(12), ...
```

Start the script with:
```console
python3 cifpal.py filename.cif atom1_name (atom2_name ...) > filename.md
```
will save the output in markdown format.

Convert markdown to docx (install [PANDOC](https://pandoc.org) first):
```console
pandoc filename.md -o filename.docx
```
This will convert the markdown file to a docx file. Open it with your favorite
word processor. Convert the file to even more formats such as HTML, PDF or TeX with PANDOC.

## Command-line options
- `filename` , required: filename, e.g. `my_structure.cif`
- `atom_name(s)`, required: atom names, e.g. `Cu1` or `Cu1 Cu2`
- `-ea` `atom(s)`, optional: exclude atoms, e.g. `-ea K1` exclude bonds to K1, `-ea K1 N2` exclude bonds K1 and N1
- `-ee` `elements(s)`,  optional: exlude elements,  e.g. `-ee K` exclude bonds to potassium, `-ea K N` exclude bonds to potassium and nitrogen
- `-sa`, optional: sort values for bond lengths and angles ascending
- `-sd`, optional: sort values for bond lengths and angles descending
- `-sae`, optional: ascending alphabetical sort of elements
- `-sde`, optional:  descending alphabetical sort of elements
- `-f` `N`, optional: find contacts of named atoms within d Å, e.g. `-f 4.5`, find contacts of Cu1 and Cu2 (Cu1…Cu1, Cu2…Cu2, Cu1…Cu2) in a radius of 4 Å each within the cell boundary

## Statistics
Statistics are derived from the values of the bonding parameters. The individual e.s.d.'s or s.u.'s of the bond lengths or angles (usually given in parentheses, e.g. 1.234(5) Å) are not taken into account.

Sam. std. dev. = Sample standard deviation, Pop. std. dev. = population standard deviation, Std. error = Standard Error or Standard Error of Mean. Please refer to literature or Wikipedia for the meaning of these terms. The population standard deviation is probably the value you're looking for.

## Remarks
The format of the tabular output can be easily changed in the script using another formatting option of the `tabulate` module.

## Known Issues
The script makes extensive use of Unicode characters, which can cause problems with output or conversion.

## Examples

### Example 1:
 Start the script with:
```console
python3 cifpal.py 2103396.cif Cu1
```
![show](/examples/example1a.gif)

