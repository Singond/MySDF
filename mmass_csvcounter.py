import argparse
import csv
import math
import pprint
import sys
from collections import Counter
import time

start_time = time.time()

parser = argparse.ArgumentParser(prog = 'SDF4ever', 
                                 description = 'SDF format processing.\n', 
                                 epilog='End of help block. Now try it yourself. Good luck!')
parser.add_argument('--foo', help='This thing serves for nothing.')
parser.add_argument('-v', '--verbose', action='store_true', help='Prints computed data in detail.')
args = parser.parse_args()
if args.verbose:
    print('Chatty output turned on.')

with open('ChI_BI_project.sdf') as file, open('Periodic_Table_Of_Elements.csv') as csvfile:   # sys.argv[1], argv[2]

    final_stat = Counter()
    n = 1
    while True:
        try:
            for i in range(3):   # zahozeni prvnich tri radku souboru
                file.readline()
            info = file.readline()

            """ THE COUNTS LINE
                aaabbblllfffcccsssxxxrrrpppiiimmmvvvvvv

            Where::
            aaa = number of atoms
            bbb = number of bonds """

            atom_count = int(info[0:3])   # prvni pozice ctvrteho radku: pocet atomu
            bond_count = int(info[3:6])   # druha pozice: pocet vazeb

            atoms = list()
            coordinates_all = list()    # list of all atom coordinates created for each molecule in sdf file
            
            for i in range(atom_count):
                line = file.readline()                
                atoms.append(line[31:34].strip())  # vytvoreni seznamu prvku ['N', 'O', ...]
                x, y, z = (float(line[l: r]) for l, r in [(3,10), (13,20), (23,30)])
                coordinates_all.append((x, y, z))   # predavam jako tuple
            
            maxdist = 0
            atom1 = 1
            atom2 = 1
            
            for i in range(len(coordinates_all)):    # creates matrix of distances of atoms
                for j in range(i+1, len(coordinates_all)):
                    distance = math.sqrt(sum( (coordinates_all[i][k] - coordinates_all[j][k])**2 for k in range(3) ))
                        
                    if distance > maxdist:
                        maxdist = distance
                        atom1 = i+1
                        atom2 = j+1
            
            if args.verbose:
                print(str(n) + ': Maxdist between atms ' + str(atom1) + ' ' + str(atom2) + '; ' + ('%.4f' % maxdist))
            #print(str(n) + ': Maxdist between atms ' + str(atom1) + ' ' + str(atom2) + '; ' + ('%.4f' % maxdist))
                
            maxbonds = [0] * atom_count

            for i in range(bond_count):
                line = file.readline()
                
                first, second, bonds = (int(line[l: r]) for l, r in [(0,3), (3,6), (6,9)])

                # hodnota vazby se prepise pouze kdyz je aktualne ctena hodnota vazby je vyssi nez ulozena
                # je treba od pozice 'first' odecist 1, aby pozice atomu odpovidala pozici v 'maxbonds'
                if bonds > maxbonds[first-1]:
                    maxbonds[first-1] = bonds

                if bonds > maxbonds[second-1]:
                    maxbonds[second-1] = bonds

            pairs_tuples = list(zip(atoms, maxbonds))
            mol_counter = Counter()

            for i in pairs_tuples:
                mol_counter[i] += 1
            
            for key in mol_counter:
                final_stat[key] += mol_counter[key]
            
            if args.verbose:
                print(str(n) + ": " + str(mol_counter))
                
            # block calculating real weight of molecule in kgs
            # using data (e.g. molecular mass) from external csv file
            
            reader = csv.DictReader(csvfile, delimiter=',')
            """
            example: mol_counter = Counter({('H', 1): 2, ('C', 1): 7, ('C', 2): 7, ('N', 2): 3,
                                            ('O', 2): 2, ('O', 1): 2, ('N', 1): 1})
            Repetition of elements. The summarizing element_Counter() is created
            in order to reduce opening of the csv file. """
            
            element_sum = Counter()
            for atom_type, count in mol_counter.items():
                element_sum[atom_type[0]] += count   # 'atom_type[0]' represents the element symbol (e.g.'C')
    
            molecular_mass = 0

            for element, count in element_sum.items():
                csvfile.seek(0)   # returns at the beggining of the csvfile
                for row in reader:
                    if element == (row['Symbol']):
                        molecular_mass += float(row['Atomic Weight']) * count

            fin_molecular_mass = molecular_mass * 1.66053904e-27
            
            if args.verbose:
                print(str(n) + ": Weight = " + str("%.3e" % fin_molecular_mass) + " kg\n")
            #print(str(n) + ": Weight = " + str("%.3e" % fin_molecular_mass) + " kg")

        except ValueError:
            break
            
        while True:
            line = file.readline()
            if '$$$$' in line:
                n += 1
                break

    print("\n### FINAL STATISTICS OF ATOM TYPES: ###")    
    PrintFinal = pprint.PrettyPrinter(indent=2)   # fcking awesome
    PrintFinal.pprint(final_stat)
    
print("\n--- %s seconds ---" % (time.time() - start_time))