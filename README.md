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

Sam. std. dev. = Sample standard deviation, Pop. std. dev. = Population standard deviation, Std. error = Standard error or standard error of mean. Please refer to literature or Wikipedia for the meaning of these terms. The population standard deviation is probably the value you are looking for.

## Remarks
The format of the tabular output can be easily changed in the script using another formatting option of the `tabulate` module.

## Known Issues
- The script makes extensive use of Unicode characters, which can cause problems with output or conversion.
- Overline numbers N̅ (e.g. 1̅) will be displayed as -N, because of Windows Unicode issues. 

## Examples

### Example 1:
```console
python3 cifpal.py 2103396.cif Cu1
```
Open `2103396.cif` and show tables for `Cu1`.

![show](/examples/example1a.gif)

### Example 2:
```console
python3 cifpal.py 2103396.cif Cu1 Cu2 -ee K -f 12
```

Open `2103396.cif` and show tables for `Cu1` and `Cu2`, exclude bonds to potassium (`-ee K`) and search for copper copper contacs within a range of 12 Å (`-f 12`).   

| compound                   | 1K-kd25                                      |
|----------------------------|----------------------------------------------|
| empirical formula          | C₆₈H₁₂₆Cu₄F₁₂K₂N₁₆O₁₈.₅₀S₄                   |
| moiety formula             | C₆₆H₁₂₆Cu₄F₆K₂N₁₆O₁₂S₂²⁺, 2(CF₃O₃S⁻), 0.5(O) |
| formula weight             | 2152.44                                      |
| T /K                       | 133(2)                                       |
| crystal size /mm³          | 0.500 x 0.210 x 0.090                        |
| crystal system             | triclinic                                    |
| space group                | P-1 (No. 2)                                  |
| a /Å                       | 10.8272(5)                                   |
| b /Å                       | 12.8073(6)                                   |
| c /Å                       | 17.8554(8)                                   |
| α /°                       | 72.844(4)                                    |
| β /°                       | 81.765(4)                                    |
| γ /°                       | 86.531(4)                                    |
| V /Å³                      | 2340.96(19)                                  |
| Z                          | 1                                            |
| ρ /g·cm⁻³                  | 1.527                                        |
| F(000)                     | 1120                                         |
| µ /mm⁻¹                    | 1.168                                        |
| Tmin / Tmax                | 0.6301 / 0.9058                              |
| θ-range /°                 | 1.204 - 25.677                               |
| hkl-range                  | –13 ≤ h ≤ 12, –15 ≤ k ≤ 15, –21 ≤ l ≤ 21     |
| measured refl.             | 29369                                        |
| unique refl. [Rint]        | 8834 [0.0535]                                |
| observed refl. (I > 2σ(I)) | 7043                                         |
| data / restr. / param.     | 8834 / 70 / 614                              |
| goodness-of-fit (F²)       | 1.049                                        |
| R1, wR2 (I > 2σ(I))        | 0.0518 / 0.1201                              |
| R1, wR2 (all data)         | 0.0682 / 0.1267                              |
| res. el. dens. /e·Å⁻³      | –0.800 / 0.761                               |

| Atoms    | Bond length /Å   |
|----------|------------------|
| Cu1–O1   | 1.907(2)         |
| Cu1–N1   | 1.911(3)         |
| Cu1–N3   | 2.154(3)         |
| Cu1–N5   | 2.170(3)         |
| Cu1–N4   | 2.187(3)         |
| Cu2–O2   | 1.908(3)         |
| Cu2–N2   | 1.909(3)         |
| Cu2–N6   | 2.136(3)         |
| Cu2–N7   | 2.178(3)         |
| Cu2–N8   | 2.192(3)         |
| Cu1…Cu1' | 7.5543           |
| Cu1…Cu2' | 8.2313           |
| Cu1…Cu2  | 3.7978           |

| Atoms   | Bonds lengths /Å                                                               |
|---------|--------------------------------------------------------------------------------|
| Cu–N    | 1.909(3), 1.911(3), 2.136(3), 2.154(3), 2.170(3), 2.178(3), 2.187(3), 2.192(3) |
| Cu–O    | 1.907(2), 1.908(3)                                                             |
| Cu…Cu   | 3.7978, 7.5543, 8.2313                                                         |

| Atoms   | Bond lengths /Å     |
|---------|---------------------|
| Cu–N    | 1.909(3) - 2.192(3) |
| Cu–O    | 1.907(2) / 1.908(3) |
| Cu…Cu   | 3.7978 - 8.2313     |

| Atoms   |   Count |   Mean /Å |   Median /Å |   Sam. std. dev. |   Pop. std. dev. |   Std. error |   Skewness |
|---------|---------|-----------|-------------|------------------|------------------|--------------|------------|
| Cu–N    |       8 |    2.1046 |      2.162  |           0.1215 |           0.1136 |       0.0429 |    -1.3495 |
| Cu–O    |       2 |    1.9075 |      1.9075 |           0.0007 |           0.0005 |       0.0005 |   nan      |
| Cu…Cu   |       3 |    6.5278 |      7.5543 |           2.3884 |           1.9501 |       1.3789 |    -1.5768 |

| Atoms      | Angle /°   |
|------------|------------|
| O1–Cu1–N1  | 98.68(12)  |
| O1–Cu1–N3  | 171.94(12) |
| N1–Cu1–N3  | 80.09(13)  |
| O1–Cu1–N5  | 103.92(12) |
| N1–Cu1–N5  | 137.78(13) |
| N3–Cu1–N5  | 81.87(12)  |
| O1–Cu1–N4  | 91.77(11)  |
| N1–Cu1–N4  | 130.58(13) |
| N3–Cu1–N4  | 83.17(12)  |
| N5–Cu1–N4  | 84.14(13)  |
| O2–Cu2–N2  | 97.51(12)  |
| O2–Cu2–N6  | 171.47(12) |
| N2–Cu2–N6  | 80.00(12)  |
| O2–Cu2–N7  | 104.64(11) |
| N2–Cu2–N7  | 138.96(13) |
| N6–Cu2–N7  | 82.17(12)  |
| O2–Cu2–N8  | 91.96(11)  |
| N2–Cu2–N8  | 129.27(12) |
| N6–Cu2–N8  | 83.51(12)  |
| N7–Cu2–N8  | 84.47(11)  |
| C2–N1–Cu1  | 120.8(3)   |
| N2–N1–Cu1  | 127.3(2)   |
| C3–N2–Cu2  | 121.1(3)   |
| N1–N2–Cu2  | 128.7(2)   |
| C5–N3–Cu1  | 101.9(2)   |
| C10–N3–Cu1 | 110.2(2)   |
| C4–N3–Cu1  | 108.7(2)   |
| C7–N4–Cu1  | 100.7(2)   |
| C6–N4–Cu1  | 107.8(2)   |
| C11–N4–Cu1 | 110.2(2)   |
| C9–N5–Cu1  | 103.1(2)   |
| C8–N5–Cu1  | 106.9(2)   |
| C14–N5–Cu1 | 110.8(2)   |
| C23–N6–Cu2 | 102.1(2)   |
| C18–N6–Cu2 | 110.5(2)   |
| C17–N6–Cu2 | 109.3(2)   |
| C20–N7–Cu2 | 106.6(2)   |
| C24–N7–Cu2 | 111.6(2)   |
| C19–N7–Cu2 | 103.0(2)   |
| C21–N8–Cu2 | 100.4(2)   |
| C27–N8–Cu2 | 111.1(2)   |
| C22–N8–Cu2 | 107.1(2)   |
| O2–O1–Cu1  | 118.71(17) |
| O1–O2–Cu2  | 118.98(18) |

| Atoms   | Angles /°                                                                                                                                                                                              |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| C–N–Cu  | 100.4(2), 100.7(2), 101.9(2), 102.1(2), 103.0(2), 103.1(2), 106.6(2), 106.9(2), 107.1(2), 107.8(2), 108.7(2), 109.3(2), 110.2(2), 110.2(2), 110.5(2), 110.8(2), 111.1(2), 111.6(2), 120.8(3), 121.1(3) |
| N–Cu–N  | 80.00(12), 80.09(13), 81.87(12), 82.17(12), 83.17(12), 83.51(12), 84.14(13), 84.47(11), 129.27(12), 130.58(13), 137.78(13), 138.96(13)                                                                 |
| N–N–Cu  | 127.3(2), 128.7(2)                                                                                                                                                                                     |
| O–Cu–N  | 91.77(11), 91.96(11), 97.51(12), 98.68(12), 103.92(12), 104.64(11), 171.47(12), 171.94(12)                                                                                                             |
| O–O–Cu  | 118.71(17), 118.98(18)                                                                                                                                                                                 |

| Atoms   | Angles /°               |
|---------|-------------------------|
| C–N–Cu  | 100.4(2) - 121.1(3)     |
| N–Cu–N  | 80.00(12) - 138.96(13)  |
| N–N–Cu  | 127.3(2) / 128.7(2)     |
| O–Cu–N  | 91.77(11) - 171.94(12)  |
| O–O–Cu  | 118.71(17) / 118.98(18) |

| Atoms   |   Count |   Mean /° |   Median /° |   Sam. std. dev. |   Pop. std. dev. |   Std. error |   Skewness |
|---------|---------|-----------|-------------|------------------|------------------|--------------|------------|
| C–N–Cu  |      20 |  108.195  |     108.25  |           5.7092 |           5.5647 |       1.2766 |     0.8211 |
| N–Cu–N  |      12 |   99.6675 |      83.825 |          25.6314 |          24.5402 |       7.3991 |     0.8386 |
| N–N–Cu  |       2 |  128      |     128     |           0.9899 |           0.7    |       0.7    |   nan      |
| O–Cu–N  |       8 |  116.486  |     101.3   |          34.4055 |          32.1834 |      12.1642 |     1.3599 |
| O–O–Cu  |       2 |  118.845  |     118.845 |           0.1909 |           0.135  |       0.135  |   nan      |

Selected distances /Å and angles /° for 1K-kd25: Cu1–O1 1.907(2), Cu1–N1 1.911(3), Cu1–N3 2.154(3), Cu1–N5 2.170(3), Cu1–N4 2.187(3), Cu2–O2 1.908(3), Cu2–N2 1.909(3), Cu2–N6 2.136(3), Cu2–N7 2.178(3), Cu2–N8 2.192(3), Cu1…Cu1' 7.5543, Cu1…Cu2' 8.2313, Cu1…Cu2 3.7978; O1–Cu1–N1 98.68(12), O1–Cu1–N3 171.94(12), N1–Cu1–N3 80.09(13), O1–Cu1–N5 103.92(12), N1–Cu1–N5 137.78(13), N3–Cu1–N5 81.87(12), O1–Cu1–N4 91.77(11), N1–Cu1–N4 130.58(13), N3–Cu1–N4 83.17(12), N5–Cu1–N4 84.14(13), O2–Cu2–N2 97.51(12), O2–Cu2–N6 171.47(12), N2–Cu2–N6 80.00(12), O2–Cu2–N7 104.64(11), N2–Cu2–N7 138.96(13), N6–Cu2–N7 82.17(12), O2–Cu2–N8 91.96(11), N2–Cu2–N8 129.27(12), N6–Cu2–N8 83.51(12), N7–Cu2–N8 84.47(11), C2–N1–Cu1 120.8(3), N2–N1–Cu1 127.3(2), C3–N2–Cu2 121.1(3), N1–N2–Cu2 128.7(2), C5–N3–Cu1 101.9(2), C10–N3–Cu1 110.2(2), C4–N3–Cu1 108.7(2), C7–N4–Cu1 100.7(2), C6–N4–Cu1 107.8(2), C11–N4–Cu1 110.2(2), C9–N5–Cu1 103.1(2), C8–N5–Cu1 106.9(2), C14–N5–Cu1 110.8(2), C23–N6–Cu2 102.1(2), C18–N6–Cu2 110.5(2), C17–N6–Cu2 109.3(2), C20–N7–Cu2 106.6(2), C24–N7–Cu2 111.6(2), C19–N7–Cu2 103.0(2), C21–N8–Cu2 100.4(2), C27–N8–Cu2 111.1(2), C22–N8–Cu2 107.1(2), O2–O1–Cu1 118.71(17), O1–O2–Cu2 118.98(18).
Symmetry operation(s) used to generate equivalent atoms: (') –x+1,–y+1,–z+1.
