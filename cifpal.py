#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script uses a lot of utf-8 characters
# mostly in proper_chem_formula and proper_space_group
# replace in case of problems, but c'mon it's 2021
# overline numbers are not possible with Win10 
# had to be partially commented

import sys                        #sys
import argparse                   #argument parser
import re                         #regular expressions
from gemmi import cif             #CIF processing
import gemmi                      #symmetry handling
import pandas as pd               #data analysis
from tabulate import tabulate     #nice table output	

sys.stdout.reconfigure(encoding='utf-8')  #for windows console

splitstr='' #for proper_chem_formula

#sym-op denotation
sym_dict = {
	 1: "'",
	 2: "''",
	 3: "'''",
	 4: "(IV)",
	 5: "(V)",
	 6: "(VI)",
	 7: "(VII)",
	 8: "(VIII)",
	 9: "(IX)",
	10: "(X)",
	11: "(XI)",
	12: "(XII)",
	13: "(XIII)",
	14: "(XIV)",
	15: "(XV)",
	16: "(XVI)",
	17: "(XVII)",
	18: "(XVIII)",
	19: "(XIX)",
	20: "(XX)",
	21: "(XXI)",
	22: "(XXII)",
	23: "(XXII)",
	24: "(XXIV)",
	25: "(XXV)",
	26: "(XXVI)",
	27: "(XXVII)",
	28: "(XXVIII)",
	29: "(XXIX)",
	30: "(XXX)",
	31: "(XXXI)", 
	32: "(XXXII)", 
	33: "(XXXIII)", 
	34: "(XXXIV)", 
	35: "(XXXV)", 
	36: "(XXXVI)", 
	37: "(XXXVII)", 
	38: "(XXXVIII)", 
	39: "(XXXIX)", 
	40: "(XL)", 
}

#for sym code denotation
number_of_calls = 0
sym_code_dict=dict()

def code_to_sym(symcode): 
	#transforms 3_666 to 1-x,1-y,1-z if 3 is -x,-y,-z
	#needs the table of sym ops from CIF
	if '.' in symcode:
		sym='.'
	else:
		regex_symcode = re.compile(r'(\d{1,})_?(\d)?(\d)?(\d)?') 
		sym_trans_str = regex_symcode.findall(str(symcode))
		#if only sym num is given, e.g. 17 instead of 17_555 -> transform to 17_555
		sym_trans_str=['5' if x=='' else x for x in sym_trans_str[0]]
		sym_trans_int = list(map(int,sym_trans_str)) #str to int
		#sym = gemmi.Op(list(sym_table)[sym_trans_int[0]-1][0].strip("'")) \
		sym = gemmi.Op(list(sym_table)[sym_trans_int[0]-1].str(0)) \
		.translated([24*(sym_trans_int[1]-5),24*(sym_trans_int[2]-5),24*(sym_trans_int[3]-5)]).triplet()
	return(sym)


def code_to_symbol(symcode):
	#for sym code denotation
	#sym code denotation depends on how often this function was called
	#return the symbol: ', '', ... etc.
	# A B 1_666
	# A C .
	# A D 2_666
	# C G 1_666
	# gives
	# A-B', A-C, A-B'', C-G' 
	if '.' in symcode:
		#no sym op (='.') returns ''
		sym_symbol=''
	else:
		#number of calls of the functions
		global number_of_calls
		#reset number of calls
		if number_of_calls < 40:
			number_of_calls += 1
		else:
			number_of_calls = 1
		#sym symbols from sym_dict
		sym_symbol_call=sym_dict[number_of_calls]
		
		try:
			#check if symcode is already in sym_code_dict
			sym_code_dict[symcode]
		except KeyError:
			#if not, take symcode in dict, sym_symbol_call is the symbol (e.g. ')
			sym_code_dict[symcode]=sym_symbol_call
		
		#sym_symbol from sym_dict is equal to sym_symbol_call?
		#was this symbol already used for a symmetry operation?
		#e.g. if 1_666 is ' and a second, 2_777 is '' and 1_666 is present again,
		#five or more bond entries later, than ' will be the symbol for 1_666 again
		if sym_symbol_call == sym_code_dict[symcode]:
			sym_symbol=sym_symbol_call
		else:
			sym_symbol=sym_code_dict[symcode]
			
	return(sym_symbol)

def proper_chem_formula(formula):
	#2(C12H12N12 3+) --> 2(C₁₂H₁₂N₁₂³⁺)
	
	global splitstr 
	splitstr = ''
	
	#dict for replacement subscript
	utf_sub_dict = {
		"0" : "₀",
		"1" : "₁",
		"2" : "₂",
		"3" : "₃",
		"4" : "₄",
		"5" : "₅",
		"6" : "₆",
		"7" : "₇",
		"8" : "₈",
		"9" : "₉",
	}
	#dict for replacement superscript
	utf_sup_dict = {
		"0" : "⁰",
		"1" : "¹",
		"2" : "²",
		"3" : "³",
		"4" : "⁴",
		"5" : "⁵",
		"6" : "⁶",
		"7" : "⁷",
		"8" : "⁸",
		"9" : "⁹",
	}

	#first supscript C111 --> C₁₁₁
	pattern=re.split(r"([A-Z][a-z]?)(\d+\.?\d{0,})",formula.strip("'"))
	for split in pattern:
		if re.match('\d', split):
			p=re.compile(r"([0|1|2|3|4|5|6|7|8|9])")
			split=p.sub(lambda x: utf_sub_dict[x.group()],split)
		splitstr=splitstr+split.strip()
	
	#2nd superscript 2+ --> ²+
	pattern=re.split(r"(\d+)([+|-])",splitstr)
	splitstr=''
	for split in pattern:
		if re.match('\d', split):
			p=re.compile(r"([0|1|2|3|4|5|6|7|8|9])")
			split=p.sub(lambda x: utf_sup_dict[x.group()],split)
		splitstr=splitstr+split
		
	#3rd superscript + and - --> ⁺ and ⁻
	proper_formula=splitstr.replace(" -","⁻")
	proper_formula=proper_formula.replace(" +","⁺")
	proper_formula=proper_formula.replace("-","⁻")
	proper_formula=proper_formula.replace("+","⁺")
	proper_formula=proper_formula.replace(", ",",")
	proper_formula=proper_formula.replace(",",", ")
	return(proper_formula)

def proper_space_group(space_group):
	#P21/c --> P2₁/c
	#
	#unicode overline ('-1' --> '1'+ u'\u0305') works, but tabulate has a unicode bug
	#pandoc transformation of overline unicode to MS Word gives strange characters
	#commented because  of problems
	#Win10 is not able to show overlined unicode characters (pathetic)
	#
	#too lazy to think about a proper regex
	#
	#space_group=space_group.replace('-1','1'+ u'\u0305')
	#space_group=space_group.replace('-2','2'+ u'\u0305')
	#space_group=space_group.replace('-3','3'+ u'\u0305')
	#space_group=space_group.replace('-4','4'+ u'\u0305')
	#space_group=space_group.replace('-6','6'+ u'\u0305')
	#
	space_group=space_group.replace('21','2₁')
	space_group=space_group.replace('31','3₁')
	space_group=space_group.replace('41','4₁')
	space_group=space_group.replace('61','6₁')
	space_group=space_group.replace('32','3₂')
	space_group=space_group.replace('42','4₂')
	space_group=space_group.replace('62','6₂')
	space_group=space_group.replace('32','3₂')
	space_group=space_group.replace('42','4₂')
	space_group=space_group.replace('62','6₂')
	space_group=space_group.replace('43','4₃')
	space_group=space_group.replace('63','6₃')
	space_group=space_group.replace('64','6₄')
	space_group=space_group.replace('65','6₅')
	proper_space_group = space_group
	return(proper_space_group)

#argument parser
parser = argparse.ArgumentParser(prog='cifpal', 
		description = "Print selected bond lengths, angles and more from CIF.")

#filename is required
parser.add_argument("filename", 
	help = "filename, CIF; e.g. mystructure.cif")

#atoms for tables and calculations (required)
parser.add_argument("atom_names", 
	nargs="+",
	type=str,
	help = "atom names; e.g. Co1 or Co1 Fe1")

#exclude atoms
parser.add_argument('-ea','--excludeAt',
	nargs="+",
	type=str,
	help='exclude bonds and angles to specified atoms; e.g. -ea N1 or -ea N1 N2')

#exclude elements
parser.add_argument('-ee','--excludeEl',
	nargs="+",
	type=str,
	help='exclude bonds and angles to specified elements; e.g. -ee C or -ee C N')

#sort by value
parser.add_argument('-sa','--sortasc',
	default=0, action='store_true',
	help='sort values for bond lengths and angles ascending')

#sort by value
parser.add_argument('-sd','--sortdes',
	default=0, action='store_true',
	help='sort values for bond lengths and angles descending')

#sort by name
parser.add_argument('-sae','--sortascEl',
	default=0, action='store_true',
	help='ascending alphabetical sort of elements')

#sort by name
parser.add_argument('-sde','--sortdesEl',
	default=0, action='store_true',
	help='descending alphabetical sort of elements')

#contact search
parser.add_argument('-f','--findcontact',
	type=float,
	help='find contacts of named atoms within d Å, e.g. -f 4, find contacts of Co1 Fe1 in a radius of 4 Å each') 

#parse arguments
args = parser.parse_args()

#load cif
try:
	doc = cif.read_file(args.filename)
#file not found
except IOError:
	print(f"'{args.filename}'" + " not found")
	sys.exit(1)
#not a valid cif
except ValueError:
	print(f"'{args.filename}'" + " is not a valid CIF. Exit.\n")
	sys.exit(1)
	
#more than one or no data_block --> exit
if len(doc) != 1:
	print("CIF should contain one structure or one 'data_' block. Exit.")
	sys.exit(1)
	
#get the block
block = doc.sole_block()

#check if selected atoms are in the CIF)
if args.atom_names:
	if set(args.atom_names).issubset(list(block.find_loop('_atom_site_label'))) is False:
		print("One or more atoms are not part of the CIF. Exit.")
		sys.exit(1)


#check if selected elements are in the CIF
if args.excludeEl:
	elements=list(block.find_loop('_atom_type_symbol'))
	elements=[element.strip("'") for element in elements]
	if set(args.excludeEl).issubset(elements) is False:
		print("One or more excluded elements are not part of the CIF. Exit.")
		sys.exit(1)

#check if selected atoms are in the CIF
if args.excludeAt:
	if set(args.excludeAt).issubset(list(block.find_loop('_atom_site_label'))) is False:
		print("One or more excluded atoms are not part of the CIF. Exit.")
		sys.exit(1)
		

#build a sym op table
sym_table=block.find(['_space_group_symop_operation_xyz'])

#build a bond table atom1-atom2 bond-length symmetry_2
bond_table=block.find(['_geom_bond_atom_site_label_1', 
				       '_geom_bond_atom_site_label_2',
				       '_geom_bond_distance',
				       '_geom_bond_site_symmetry_2'])

#build an angle table atom1-atom2-atom3 angle symmetry_1 symmetry_3
angle_table=block.find(['_geom_angle_atom_site_label_1',
	                    '_geom_angle_atom_site_label_2',
						'_geom_angle_atom_site_label_3',
						'_geom_angle',
						'_geom_angle_site_symmetry_1',
						'_geom_angle_site_symmetry_3'])

#summary table
summary_list = [
	['compound',block.name],
	['empirical formula',proper_chem_formula(block.find_value('_chemical_formula_sum').strip("'"))],
	['moiety formula',proper_chem_formula(block.find_value('_chemical_formula_moiety').strip("'"))],
	['formula weight',block.find_value('_chemical_formula_weight')],
	['T /K',block.find_value('_diffrn_ambient_temperature')],
	['crystal size /mm³',block.find_value('_exptl_crystal_size_max') + " x " + \
		block.find_value('_exptl_crystal_size_mid') + " x " + \
	    block.find_value('_exptl_crystal_size_min')],
	['crystal system',block.find_value('_space_group_crystal_system')],
	#function 'proper_space_group' not applied in the next two lines
	#['space group',block.find_value('_space_group_name_H-M_alt').strip("'").replace('-','–') + " (No. " + \
	#	block.find_value('_space_group_IT_number') + ")"],
	#function 'proper_space_group' applied
	['space group',proper_space_group(block.find_value('_space_group_name_H-M_alt')).strip("'").replace(" ","") + " (No. " + \
		block.find_value('_space_group_IT_number') + ")"],
	['a /Å',block.find_value('_cell_length_a')],
	['b /Å',block.find_value('_cell_length_b')],
	['c /Å',block.find_value('_cell_length_c')],
	['α /°',block.find_value('_cell_angle_alpha')],
	['β /°',block.find_value('_cell_angle_beta')],
	['γ /°',block.find_value('_cell_angle_gamma')],
	['V /Å³',block.find_value('_cell_volume')],
	['Z',block.find_value('_cell_formula_units_Z')],
	['ρ /g·cm⁻³',block.find_value('_exptl_crystal_density_diffrn')],
	['F(000)',block.find_value('_exptl_crystal_F_000')],
	['µ /mm⁻¹',block.find_value('_exptl_absorpt_coefficient_mu')],
	['Tmin / Tmax',block.find_value('_exptl_absorpt_correction_T_min') + " / " + \
		block.find_value('_exptl_absorpt_correction_T_max')],
	['θ-range /°',block.find_value('_diffrn_reflns_theta_min') + " - " + \
		block.find_value('_diffrn_reflns_theta_max')],
	['hkl-range',(block.find_value('_diffrn_reflns_limit_h_min')).replace('-','–') + " ≤ h ≤ " + \
		block.find_value('_diffrn_reflns_limit_h_max') +", " + \
	    block.find_value('_diffrn_reflns_limit_k_min').replace('-','–') + " ≤ k ≤ " + \
		block.find_value('_diffrn_reflns_limit_k_max') +", " + \
	    block.find_value('_diffrn_reflns_limit_l_min').replace('-','–') + " ≤ l ≤ " + \
	    block.find_value('_diffrn_reflns_limit_l_max')],
	['measured refl.',block.find_value('_diffrn_reflns_number')],
	['unique refl. [Rint]',block.find_value('_reflns_number_total') + " [" + \
		block.find_value('_diffrn_reflns_av_R_equivalents') + "]"],
	['observed refl. (I > 2σ(I))',block.find_value('_reflns_number_gt')],
	['data / restr. / param.',block.find_value('_refine_ls_number_reflns') + " / " + \
		block.find_value('_refine_ls_number_restraints') +" / " + \
	    block.find_value('_refine_ls_number_parameters')],
	['goodness-of-fit (F²)',block.find_value('_refine_ls_goodness_of_fit_ref')],
	['R1, wR2 (I > 2σ(I))',block.find_value('_refine_ls_R_factor_gt') + " / " + \
		block.find_value('_refine_ls_wR_factor_gt')],
	['R1, wR2 (all data)',block.find_value('_refine_ls_R_factor_all') + " / " + \
		block.find_value('_refine_ls_wR_factor_ref')],
	['res. el. dens. /e·Å⁻³',block.find_value('_refine_diff_density_min').replace('-','–') + " / " + \
		block.find_value('_refine_diff_density_max')]
]

#for unicode bug with overlined numbers (e.g. -1, '\u0305') in tabulate
#remove space from 'No. ' --> 'No.' if overline (e.g. -1, '\u0305') is found
#commented because of Win10 problems, see also line for 'space group' above
#MS Word is not able to display it correctly after pandoc transformation of the output
#Win10 is not able to show overlined unicode characters (in 2021!)
#
#if any(u'\u0305' in string for string in summary_list[7]):
#	summary_list[7]=[sub.replace('No. ', 'No.') for sub in summary_list[7]]

#create table
#sum_table=tabulate(summary_list,headers='firstrow',tablefmt='github')

#insert space in 'No.' --> 'No. ' if overline (e.g. -1, '\u0305') is found
#if u'\u0305' in sum_table:
#	sum_table=sum_table.replace('No.', 'No. ')

#print table
#print(sum_table)

print('')
print(tabulate(summary_list,headers='firstrow',tablefmt='github'))


############ Data Frame
#bond table to pandas data frame
all_bonds=pd.DataFrame(data=bond_table)
#rename headers
all_bonds.rename(columns={0:'Atom1', 1:'Atom2',2:'Bond_length',3:'Sym_Code'}, inplace=True)
#set fusion char A B --> A-B (fused by '-')
all_bonds['Fusion_Char']='–'

#search for contacts with gemmi functions
#limited to cell boundaries
#no s.u. on bond lengths
#mainly taken from the example in the gemmi documentation
if args.findcontact:
	#prepare for search
	small = gemmi.read_small_structure(args.filename)
	ns = gemmi.NeighborSearch(small,args.findcontact*2).populate()
	#iter through all atoms
	for atom in small.sites:
		#continue if atom name was in arguments args.atom_names
		if atom.label in args.atom_names:
			for mark in ns.find_site_neighbors(atom, min_dist=0.1, max_dist=args.findcontact):
				site = mark.to_site(small)
				dist = ns.dist(mark.pos(), small.cell.orthogonalize(atom.fract))
				#limit to 4 decimals
				dist = '%.4f' % dist 
				#continue if atom name was in arguments args.atom_names
				#only add distances from atom names in input
				if site.label in args.atom_names:
						#get symmetry op an translation
						nim = small.cell.find_nearest_image(mark.pos(), small.cell.orthogonalize(atom.fract))
						#extract sym code from nearest image
						code = str(nim.symmetry_code())
						#replace 1_555 with '.'
						if code == '1_555':
							code='.'
						#avoid double entries, e.g. Cu1 Cu2 1_555 3.956 and Cu2 Cu1 1_555 3.956
						#maybe erroneous
						if not ((all_bonds['Atom1'] == atom.label) & (all_bonds['Atom2'] == site.label) & \
							(all_bonds['Sym_Code'] == code)).any() and not ((all_bonds['Atom2'] == atom.label) & \
								(all_bonds['Atom1'] == site.label) & (all_bonds['Sym_Code'] == code)).any():
							#append all new contacts to all_bonds data frame 
							#set fusion char A B --> A…B (fused by '…')
							all_bonds = all_bonds.append({'Atom1':atom.label, 'Atom2':site.label, 'Bond_length':dist, \
								'Sym_Code':code, 'Fusion_Char':'…'}, ignore_index=True)

#add A-B column from atom names, e.g. Co1 N1 --> Co1-N1
#all_bonds['A-B']=all_bonds['Atom1']+"-"+ all_bonds['Atom2']

#add element column from atom1 name, e.g. Co1 --> Co
all_bonds['El_1']=all_bonds['Atom1'].str.extract('(\D*)')
#add element column from atom2 name, e.g. Co1 --> Co
all_bonds['El_2']=all_bonds['Atom2'].str.extract('(\D*)')
#add bond length value column from bond length, e.g. 1.334(16) --> 1.334
all_bonds['B_value']=all_bonds['Bond_length'].str.extract('(\d+[.]?\d+)')
#add s.u. / e.s.d. value column from bond length, e.g. 1.334(16) --> 16
all_bonds['B_s.u.']=all_bonds['Bond_length'].str.extract('.*\((.*)\).*')
#add sym op column from sym code, e.g. 2_666 --> 1-x,1-y,1-z if 2 is -x,-y,-z
all_bonds['Sym_Op']=all_bonds.apply(lambda row: code_to_sym(row['Sym_Code']),axis=1)
#bond length value to numeric (float)
all_bonds['B_value']=pd.to_numeric(all_bonds['B_value'])

#reorder data frame
#all_bonds=all_bonds[['Atom1','El_1','Atom2','El_2','A-B','Bond_length','B_value','B_s.u.','Sym_Code','Sym_Op']]

#reorder data frame
all_bonds=all_bonds[['Atom1','El_1','Atom2','El_2','Bond_length','B_value','B_s.u.','Sym_Code','Sym_Op','Fusion_Char']]


############ Exclude
#select only bonds where atoms from input are present (in Atom1 and Atom2)
sel_bonds=pd.DataFrame(all_bonds[(all_bonds.Atom1.isin(args.atom_names)) | (all_bonds.Atom2.isin(args.atom_names))])

#exclude named atoms from input (in Atom1 and Atom2)
if args.excludeAt:
	sel_bonds=sel_bonds[~sel_bonds.Atom1.isin(args.excludeAt) & ~sel_bonds.Atom2.isin(args.excludeAt)]
	
#exclude named elements from input (in Element1 and Element2)
if args.excludeEl:
	sel_bonds=sel_bonds[~sel_bonds.El_1.isin(args.excludeEl) & ~sel_bonds.El_2.isin(args.excludeEl)]

############ Sort
#sort bond length values ascending
if args.sortasc:
	sel_bonds=sel_bonds.sort_values(by=['B_value'])

#sort bond length values descending
if args.sortdes:
	sel_bonds=sel_bonds.sort_values(by=['B_value'],ascending=False)

#sort by elements ascending, A --> Z (not PSE like)
if args.sortascEl:
	sel_bonds=sel_bonds.sort_values(by=['El_1','El_2','B_value','Atom1','Atom2'])

#sort by elements descending, A --> Z (not PSE like)
if args.sortdesEl:
	sel_bonds=sel_bonds.sort_values(by=['El_1','El_2','B_value','Atom1','Atom2'],ascending=False)

#exit if no bond lenghts are present
if len(sel_bonds) == 0:
	print("To many excluded atoms or no-bonded atom. Exit.")
	sys.exit(1)

############ Print
# generate the sym symbol from sym code
# e.g. A B 1666 --> A-B'
sel_bonds['Sym_Symbol'] = sel_bonds.apply(lambda row: code_to_symbol(row['Sym_Code']),axis=1)
sel_bonds['A-B']=sel_bonds['Atom1']+sel_bonds['Fusion_Char']+sel_bonds['Atom2']+sel_bonds['Sym_Symbol']

#select columns from data frame for printing
pr_sel_bonds=sel_bonds[['A-B','Bond_length']]

#print bond length table, Atoms | Bond length, e.g. Co-N | 1.9563(13) Å
print('')
print(tabulate(pr_sel_bonds, headers=['Atoms','Bond length /Å'], tablefmt='github', showindex=False))

#generate and insert El1-El2 from El1 El2, e.g. C-N from C N
sel_bonds['El1-El2']=sel_bonds['El_1']+ sel_bonds['Fusion_Char'] + sel_bonds['El_2']

#lists for printed tables
summary_bond_table_1 = list()
summary_bond_table_2 = list()
summary_bond_table_3 = list()

#generate verbose table Element1-Element2 | Bond length, 
#sort by Bond length value 'B_value' (float), not 'Bond_length' (str)
for groups in sel_bonds[['Bond_length','B_value']].groupby(sel_bonds['El1-El2']):
	summary_bond_table_1.append([groups[0],', '.join(groups[1].sort_values(by=['B_value'])['Bond_length'].tolist())])
	#print(groups[0] + ': ' + ', '.join(groups[1].sort_values(by=['B_value'])['Bond_length'].tolist()))

#print verbose table El1-El2 | bond length, e.g. Co-N 1.945(3), 2.004(3)
print('')
print(tabulate(summary_bond_table_1,headers=['Atoms','Bonds lengths /Å'], tablefmt='github'))

#generate short table Element1-Element2 | Bond length, e.g. C-N 1.323(3) - 1.434(3) (more than two bonds),
#C-N 1.323(3) / 1.434(3) (two bonds), C-N 1.323(3) (one bond)
for groups in sel_bonds[['Bond_length','B_value']].groupby(sel_bonds['El1-El2']):
	if len(groups[1]) == 1:
		#print(groups[0] + ': ' + groups[1].sort_values(by=['B_value'])['Bond_length'].tolist()[0])
		summary_bond_table_2.append([groups[0], groups[1].sort_values(by=['B_value'])['Bond_length'].tolist()[0]])
	elif len(groups[1]) == 2:
		summary_bond_table_2.append([groups[0], groups[1].sort_values(by=['B_value'])['Bond_length'].tolist()[0] + 
				" / " + groups[1].sort_values(by=['B_value'])['Bond_length'].tolist()[-1]])
		#print(groups[0] + ': ' + groups[1].sort_values(by=['B_value'])['Bond_length'].tolist()[0] + 
		#		" / " + groups[1].sort_values(by=['B_value'])['Bond_length'].tolist()[-1])
	else:
		summary_bond_table_2.append([groups[0], groups[1].sort_values(by=['B_value'])['Bond_length'].tolist()[0] + 
				" - " + groups[1].sort_values(by=['B_value'])['Bond_length'].tolist()[-1]])
		#print(groups[0] + ': ' + groups[1].sort_values(by=['B_value'])['Bond_length'].tolist()[0] + 
		#		" - " + groups[1].sort_values(by=['B_value'])['Bond_length'].tolist()[-1])

#print short table
print('')
print(tabulate(summary_bond_table_2,headers=['Atoms','Bond lengths /Å'], tablefmt='github'))

#generate table with statistics, | El1-El2 | Count | Mean | Median | Sam. std. dev. | Pop. std. dev. | Std. error |
for groups in sel_bonds['B_value'].groupby(sel_bonds['El1-El2']):
	summary_bond_table_3.append([groups[0], groups[1].count(), f'{groups[1].mean():.4f}', f'{groups[1].median():.4f}', \
		f'{groups[1].std():.4f}', f'{groups[1].std(ddof=0):.4f}', f'{groups[1].sem():.4f}',f'{groups[1].skew():.4f}'])
	#print(groups[0] + ': ' + f'{groups[1].mean():.4f}' + " " + f'{groups[1].std():.4f}')
	
#print statistics table
print('')
print(tabulate(summary_bond_table_3,headers=['Atoms','Count','Mean /Å', 'Median /Å','Sam. std. dev.',\
	'Pop. std. dev.','Std. error','Skewness'], tablefmt='github'))

############ Data Frame
#angle table to pandas data frame
all_angles=pd.DataFrame(data=angle_table)
#rename headers
all_angles.rename(columns={0:'Atom1', 1:'Atom2',2:'Atom3',3:'Angle',4:'Sym_Code_1',5:'Sym_Code_3'}, inplace=True)
#set fusion char A B C --> A-B-C (fused by '-')
all_angles['Fusion_Char']='–'

#add element column from atom1 name, e.g. Co1 --> Co
all_angles['El_1']=all_angles['Atom1'].str.extract('(\D*)')
#add element column from atom2 name, e.g. Co1 --> Co
all_angles['El_2']=all_angles['Atom2'].str.extract('(\D*)')
#add element column from atom3 name, e.g. Co1 --> Co
all_angles['El_3']=all_angles['Atom3'].str.extract('(\D*)')
#add angle value column from angle, e.g. 123.45(16) --> 123.45
all_angles['A_value']=all_angles['Angle'].str.extract('(\d+[.]?\d+)')
#add s.u. / e.s.d. value column from angle, e.g. 123.45(16) --> 16
all_angles['A_s.u.']=all_angles['Angle'].str.extract('.*\((.*)\).*')
#add sym op column from sym code, e.g. 2_666 --> 1-x,1-y,1-z if 2 is -x,-y,-z
all_angles['Sym_Op_1']=all_angles.apply(lambda row: code_to_sym(row['Sym_Code_1']),axis=1)
#add sym op column from sym code, e.g. 2_666 --> 1-x,1-y,1-z if 2 is -x,-y,-z
all_angles['Sym_Op_3']=all_angles.apply(lambda row: code_to_sym(row['Sym_Code_3']),axis=1)
#angle value to numeric (float)
all_angles['A_value']=pd.to_numeric(all_angles['A_value'])
#reorder data frame
all_angles=all_angles[['Atom1','El_1','Atom2','El_2','Atom3','El_3','Angle','A_value','A_s.u.',
	'Sym_Code_1','Sym_Op_1','Sym_Code_3','Sym_Op_3','Fusion_Char']]

############ Exclude
#select only angles where atoms from input are present (in Atom1, Atom2 and Atom3)
sel_angles=pd.DataFrame(all_angles[(all_angles.Atom1.isin(args.atom_names)) | \
	(all_angles.Atom2.isin(args.atom_names)) | \
	(all_angles.Atom3.isin(args.atom_names))])

#exclude named atoms from input (in Atom1, Atom2 and Atom3)
if args.excludeAt:
	sel_angles=sel_angles[~sel_angles.Atom1.isin(args.excludeAt) & \
		~sel_angles.Atom2.isin(args.excludeAt) & \
		~sel_angles.Atom3.isin(args.excludeAt)] 

#exclude named elements from input (in Element1, Element2 and Element3)
if args.excludeEl:
	sel_angles=sel_angles[~sel_angles.El_1.isin(args.excludeEl) & \
		~sel_angles.El_2.isin(args.excludeEl) & \
		~sel_angles.El_3.isin(args.excludeEl)] 

############ Sort
#sort angle values ascending
if args.sortasc:
	sel_angles=sel_angles.sort_values(by=['A_value'])
	
#sort angle values descending
if args.sortdes:
	sel_angles=sel_angles.sort_values(by=['A_value'],ascending=False)

#sort by elements ascending, A --> Z (not PSE like)
if args.sortascEl:
	sel_angles=sel_angles.sort_values(by=['El_2','El_1','El_3','A_value','Atom2','Atom1','Atom3'])

#sort by elements descending, A --> Z (not PSE like)	
if args.sortdesEl:
	sel_angles=sel_angles.sort_values(by=['El_2','El_1','El_3','A_value','Atom2','Atom1','Atom3'],ascending=False)

#reset number_of_call in sym symbol function (sym symbol: ','',''', etc.)
number_of_calls = 0

#exit if no angles are present
if len(sel_angles) == 0:
	print("No angles found for the selected atom(s). Exit.")
	sys.exit(1)
	
############ Print
# generate the sym symbol from sym code
# e.g. A B 1666 --> A-B'
sel_angles['Sym_Symbol_1'] = sel_angles.apply(lambda row: code_to_symbol(row['Sym_Code_1']),axis=1)
sel_angles['Sym_Symbol_3'] = sel_angles.apply(lambda row: code_to_symbol(row['Sym_Code_3']),axis=1)
sel_angles['A-B-C'] = sel_angles['Atom1'] + sel_angles['Sym_Symbol_1'] + sel_angles['Fusion_Char'] + \
                      sel_angles['Atom2'] + sel_angles['Fusion_Char'] + sel_angles['Atom3'] + sel_angles['Sym_Symbol_3']

#select columns from data frame for printing
pr_sel_angles=sel_angles[['A-B-C','Angle']]

#print angle table, Atoms | Angle, e.g. N1-Co1-N2 | 179.95(14) Å
print('')
print(tabulate(pr_sel_angles, headers=['Atoms','Angle /°'], tablefmt='github', showindex=False))

#generate and insert El1-El2-El3 from El1 El2 El3, e.g. O-C-N from O C N
sel_angles['El1-El2-El3'] = sel_angles['El_1']+ sel_angles['Fusion_Char'] + \
                            sel_angles['El_2'] +sel_angles['Fusion_Char'] + sel_angles['El_3']

#lists for printed tables
summary_angle_table_1 = list()
summary_angle_table_2 = list()
summary_angle_table_3 = list()

#generate verbose table Element1-Element2-Element3 | Angle, 
#sort by Bond length value 'B_value' (float), not 'Bond_length' (str)
for groups in sel_angles[['Angle','A_value']].groupby(sel_angles['El1-El2-El3']):
	summary_angle_table_1.append([groups[0],', '.join(groups[1].sort_values(by=['A_value'])['Angle'].tolist())])
	#print(groups[0] + ': ' + ', '.join(groups[1].sort_values(by=['A_value'])['Angle'].tolist()))

#print verbose table El1-El2-El3 | Angle, e.g. O-Co-N 187.22(3), 189.20(3)
print('')
print(tabulate(summary_angle_table_1,headers=['Atoms','Angles /°'], tablefmt='github'))


#generate short table Element1-Element2-Element3 | Angle, e.g. Co-N 92.3(1) - 179.4(1) (more than two angles),
#Co-N  92.3(1) / 179.4(1)  (two angles), C-N  92.3(1) (one angle)
for groups in sel_angles[['Angle','A_value']].groupby(sel_angles['El1-El2-El3']):
	if len(groups[1]) == 1:
		#print(groups[0] + ': ' + groups[1].sort_values(by=['A_value'])['Angle'].tolist()[0])
		summary_angle_table_2.append([groups[0], groups[1].sort_values(by=['A_value'])['Angle'].tolist()[0]])
	elif len(groups[1]) == 2:
		summary_angle_table_2.append([groups[0], groups[1].sort_values(by=['A_value'])['Angle'].tolist()[0] + 
				" / " + groups[1].sort_values(by=['A_value'])['Angle'].tolist()[-1]])
		#print(groups[0] + ': ' + groups[1].sort_values(by=['A_value'])['Angle'].tolist()[0] + 
		#		" / " + groups[1].sort_values(by=['A_value'])['Angle'].tolist()[-1])
	else:
		summary_angle_table_2.append([groups[0], groups[1].sort_values(by=['A_value'])['Angle'].tolist()[0] + 
				" - " + groups[1].sort_values(by=['A_value'])['Angle'].tolist()[-1]])
		#print(groups[0] + ': ' + groups[1].sort_values(by=['A_value'])['Angle'].tolist()[0] + 
		#		" - " + groups[1].sort_values(by=['A_value'])['Angle'].tolist()[-1])

#print short table
print('')
print(tabulate(summary_angle_table_2,headers=['Atoms','Angles /°'], tablefmt='github'))

#generate table with statistics, | El1-El2-El3 | Count | Mean | Median | Sam. std. dev. | Pop. std. dev. | Std. error |
for groups in sel_angles['A_value'].groupby(sel_angles['El1-El2-El3']):
	summary_angle_table_3.append([groups[0], groups[1].count(), f'{groups[1].mean():.4f}', f'{groups[1].median():.4f}', \
		f'{groups[1].std():.4f}', f'{groups[1].std(ddof=0):.4f}', f'{groups[1].sem():.4f}',f'{groups[1].skew():.4f}'])
	#print(groups[0] + ': ' + str(groups[1].mean()) + " " + str(groups[1].std()))

#print statistics table
print('')
print(tabulate(summary_angle_table_3,headers=['Atoms','Count','Mean /°', 'Median /°','Sam. std. dev.',\
	'Pop. std. dev.','Std. error','Skewness'], tablefmt='github'))

#####################################################
#Figure caption
#####################################################
#columns (A-B / A-B-C & Bond length / Angle) from data frames into lists / large strings
fig_capture_bonds=' '.join(sel_bonds['A-B'] + " " + sel_bonds['Bond_length'].tolist()+",")
fig_capture_angles=' '.join(sel_angles['A-B-C'] + " " + sel_angles['Angle'].tolist()+",")


#print string
print('')
print(f'Selected distances /Å and angles /° for {block.name}: ' + fig_capture_bonds[:-1]+ "; " + fig_capture_angles[:-1] + '.')

#symmetry dict into string
fig_capture_sym = '; '.join('{} {}'.format(value,code_to_sym(key)) for key, value in sym_code_dict.items())
fig_capture_sym  = fig_capture_sym.replace("''","('')")
fig_capture_sym  = fig_capture_sym.replace("('')'","(''')")
fig_capture_sym  = fig_capture_sym.replace("'","(')",1)

#print symmetry string (if not empty)
if len(sym_code_dict) != 0:
	fig_caption_sym_ops = "Symmetry operation(s) used to generate equivalent atoms: " + fig_capture_sym +"."
	#change '-' to '—'
	print(fig_caption_sym_ops.replace('-','–'))

	
