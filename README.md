# cifpal
A Python 3 script for printing the summary table and tables of bond lengths and angles to the console. The script furthermore calculates average values, including a variety of statistical parameters, and is able to group bonding parameters. Contacts within a defined radius can be printed as well.

## External modules
 `gemmi`,  `pandas`,  `tabulate`
 
## Quick start
 Start the script with:
```console
python3 cifpal.py filename.cif atom1_name (atom2_name ...)
```
to open the CIF. It gives the following output:

A table with general informations.

| compound                   | 1K-kd25                                      |
|----------------------------|----------------------------------------------|
| empirical formula          | C₆₈H₁₂₆Cu₄F₁₂K₂N₁₆O₁₈.₅₀S₄                   |
| moiety formula             | C₆₆H₁₂₆Cu₄F₆K₂N₁₆O₁₂S₂²⁺, 2(CF₃O₃S⁻), 0.5(O) |
| formula weight             | 2152.44                                      |
| T /K                       | 133(2)                                       |
| ...                        | ...                                          |

A table of bond lengths with atoms from the input, `atom1_name (atom2_name ...)`, Cu1 in that example.

| Atoms   | Bond length /Å   |
|---------|------------------|
| Cu1–O1  | 1.907(2)         |
| Cu1–N1  | 1.911(3)         |
| ...     | ....             |

## Command-line options
