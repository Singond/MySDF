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

def OpenReadFile(filename):

    atom_counts = list()
    bond_counts = list()
    atoms_all = list()
    coordinates_all = list()
    bond_data = list()
    
    #n = 1
    with open(filename) as file:
        while True:
            
            try:
                for i in range(3):
                    file.readline()                
                info = file.readline()

                atom_counts.append(int(info[0:3]))  # atom_count: position '012' in line
                bond_counts.append(int(info[3:6]))  # bond_count: position '345' in line
                
                coordinates = list()
                atoms = list()
                for i in range(int(info[0:3])):  # atom_count
                    line = file.readline()                
                    atoms.append(line[31:34].strip())
                    x, y, z = (float(line[l: r]) for l, r in [(3,10), (13,20), (23,30)])
                    coordinates.append((x, y, z))
                    
                atoms_all.append(atoms)
                coordinates_all.append(coordinates)
                
                molecule_data = list()
                for i in range(int(info[3:6])):   # bond_count
                    line = file.readline()
                    molecule_data.append(tuple(int(line[l: r]) for l, r in [(0,3), (3,6), (6,9)]))
                                         # first atom, second atom, bond type
                bond_data.append(molecule_data)
                    
            except ValueError:
                break

            while True:
                line = file.readline()
                if '$$$$' in line:
                    #n += 1
                    break
    
    A = {}
    A['atom_counts'] = atom_counts
    A['bond_counts'] = bond_counts
    A['atoms_all'] = atoms_all
    A['coordinates'] = coordinates_all
    A['bond_data'] = bond_data
    return A   # class tuple

allinone = OpenReadFile('example.txt')
print(allinone['bond_data'])
#print(OpenReadFile('example.txt')[4])
#all_data = OpenReadFile('example.txt')
#print(all_data)

"""def DistanceVol2(somelist):
    maxdist = 0
    for i in range(len(somelist)):
        for j in range(i+1, len(somelist)):
            distance = math.sqrt(sum( (somelist[i][k] - somelist[j][k])**2 for k in range(3) ))
            
            if distance > maxdist:
                maxdist = distance
                
    return maxdist

Coor = [[(0.2906, 0.4933, -0.7757), (2.6311, 2.3748, 0.9594), (0.0654, 2.7426, -0.4648), (-4.1329, -0.679, 1.1295), (-3.8923, 0.6333, 0.7679), (-3.3366, -1.6914, 0.6276), (-2.8565, 0.9331, -0.097), (-2.3011, -1.3916, -0.2377), (-2.061, -0.0794, -0.6), (1.2351, -1.8577, -0.6863), (2.2827, -2.6336, -0.2269), (1.2127, -0.4925, -0.4318), (2.2676, 0.0816, 0.2961), (3.3223, -2.0648, 0.49), (3.3202, -0.7104, 0.7545), (1.9694, 1.5217, 0.4053), (0.6678, 1.6999, -0.3186), (-0.9324, 0.2473, -1.5437), (-4.9394, -0.9128, 1.8088), (-4.5147, 1.4242, 1.1597), (-3.5244, -2.7166, 0.9104), (-2.6689, 1.9584, -0.3801), (-1.6794, -2.1826, -0.6304), (0.4311, -2.3145, -1.2443), (2.2909, -3.6944, -0.4296), (4.1347, -2.6822, 0.8438), (4.1301, -0.2656, 1.3137), (-1.1858, 1.1381, -2.1185), (-0.7727, -0.5901, -2.2229)], [(-0.1476, -0.3625, 0.0287), (2.5819, -2.4968, 0.1779), (-0.3716, -2.6249, 0.2231), (-4.1811, 0.6822, -0.0197), (-3.2763, 1.4564, 0.6833), (-3.7503, -0.4383, -0.7062), (-2.4141, -0.7871, -0.6924), (-1.9387, 1.113, 0.7011), (-1.5028, -0.0114, 0.0123), (0.9076, 1.9361, -0.1648), (2.105, 2.6239, -0.2296), (0.9022, 0.5521, -0.0536), (2.1277, -0.1322, -0.0085), (3.3123, 1.9467, -0.1858), (1.8052, -1.5669, 0.1097), (0.3069, -1.6234, 0.1316), (3.3299, 0.571, -0.0751), (-5.2273, 0.9503, -0.0284), (-3.6159, 2.3308, 1.2184), (-4.4595, -1.0411, -1.254), (-2.0782, -1.6623, -1.2287), (-1.2324, 1.7184, 1.2497), (-0.0266, 2.4771, -0.1993), (2.099, 3.7004, -0.3159), (4.2409, 2.4957, -0.237), (4.2707, 0.0417, -0.0398)], [(1.338, -2.0234, -0.0879), (3.182, -0.6097, 0.4669), (3.6777, 0.6519, 0.5906), (1.854, -0.7986, 0.0438), (1.0587, 0.3374, -0.2454), (2.891, 1.7651, 0.3038), (-0.3224, 0.1289, -0.6851), (0.1059, -2.2285, -0.48), (-0.7643, -1.1898, -0.7898), (1.5993, 1.6198, -0.1083), (-1.2054, 1.2608, -1.002), (-2.4772, 1.2715, -0.5508), (-2.9186, 0.2666, 0.4182), (-2.1111, -0.4944, 0.9156), (-4.2212, 0.1851, 0.7594), (3.8055, -1.462, 0.6934), (4.6979, 0.7922, 0.9161), (3.3088, 2.7553, 0.4102), (-0.2485, -3.2451, -0.5659), (-1.7739, -1.4021, -1.1091), (0.9977, 2.4895, -0.3278), (-0.8362, 2.0838, -1.596), (-3.1694, 2.0212, -0.9046), (-4.4647, -0.4942, 1.4031)], [(0.2759, 1.1637, -0.4738), (0.1106, 0.643, -1.8374), (-0.1051, -0.7686, -1.7855), (-1.4403, -1.1402, -1.4371), (-1.5307, -2.6627, -1.3155), (-2.9845, -3.0689, -1.0656), (-3.0579, -4.5777, -0.8228), (1.6731, 1.5395, -0.2196), (2.497, 0.281, 0.06), (2.7302, -0.477, -1.2484), (3.5325, 0.4014, -2.2106), (3.8444, 0.6779, 0.6667), (4.6069, -0.5815, 1.0831), (5.9954, -0.1914, 1.5938), (6.758, -1.4508, 2.0103), (-4.9097, -1.0358, 2.9831), (-3.531, -0.3929, 2.8197), (-3.4612, 0.3287, 1.4724), (-2.0824, 0.9716, 1.309), (-2.0457, 1.7761, 0.0081), (-3.0118, 2.9579, 0.1119), (-3.0903, 3.6726, -1.2387), (-0.6268, 2.2966, -0.2297), (-0.7463, 1.1244, -2.3087), (1.0093, 0.8522, -2.4176), (-1.7078, -0.6831, -0.4844), (-2.1267, -0.7961, -2.2107), (-1.1785, -3.1225, -2.2388), (-0.9116, -2.9981, -0.4834), (-3.3639, -2.5411, -0.1906), (-3.5884, -2.8111, -1.9356), (-2.6784, -5.1054, -1.6978), (-2.454, -4.8355, 0.0472), (-4.0936, -4.8671, -0.6448), (2.0764, 2.0512, -1.0934), (1.7194, 2.2034, 0.6437), (1.9579, -0.3583, 0.7592), (3.285, -1.3926, -1.0439), (1.77, -0.727, -1.6996), (3.6323, -0.1073, -3.1695), (3.0147, 1.3497, -2.3544), (4.5222, 0.5874, -1.7933), (4.4274, 1.2281, -0.0718), (3.6779, 1.3076, 1.5407), (4.0591, -1.0929, 1.8746), (4.7088, -1.2451, 0.2245), (6.5432, 0.3199, 0.8023), (5.8935, 0.4722, 2.4525), (7.7472, -1.1729, 2.3741), (6.2101, -1.9622, 2.8018), (6.8599, -2.1145, 1.1516), (-4.9595, -1.5499, 3.9429), (-5.6777, -0.2633, 2.9445), (-5.0743, -1.7522, 2.1782), (-3.3665, 0.3235, 3.6246), (-2.763, -1.1655, 2.8583), (-3.6257, -0.3877, 0.6675), (-4.2292, 1.1013, 1.4338), (-1.8886, 1.6349, 2.152), (-1.3201, 0.1932, 1.2765), (-2.3422, 1.1364, -0.8231), (-4.0016, 2.5949, 0.389), (-2.6544, 3.6538, 0.871), (-2.0898, 3.9734, -1.5492), (-3.5142, 2.998, -1.9826), (-3.7229, 4.5554, -1.1463), (-0.2897, 2.8471, 0.6486), (-0.6228, 2.9576, -1.0965)], [(2.6906, -1.5521, -0.3192), (3.387, 0.7325, -0.318), (3.0637, 2.0425, -0.142), (2.4025, -0.2574, -0.1525), (1.0857, 0.1325, 0.1963), (1.7677, 2.4237, 0.2002), (0.1011, -0.8598, 0.3615), (1.7761, -2.4788, -0.1665), (0.463, -2.1638, 0.1766), (0.7879, 1.4939, 0.3694), (-1.3129, -0.4937, 0.7326), (-2.0981, -0.1441, -0.5331), (-3.5121, 0.222, -0.162), (-3.8564, 0.2051, 0.996), (-4.389, 0.5669, -1.118), (4.3963, 0.4542, -0.5831), (3.8236, 2.7992, -0.2703), (1.538, 3.4704, 0.3346), (2.0478, -3.5142, -0.3103), (-0.2681, -2.9497, 0.2956), (-0.2128, 1.8014, 0.635), (-1.7874, -1.3378, 1.2331), (-1.3017, 0.3662, 1.4023), (-1.6236, 0.7, -1.0336), (-2.1093, -1.0041, -1.2028), (-5.2842, 0.7936, -0.8314)]]

for i in Coor:
    print(DistanceVol2(i))"""

def MaxDistance(coordinates):
    n = 1
    for molecule in coordinates:
        maxdist = 0
        atom1 = 1
        atom2 = 1
        
        for i in range(len(molecule)):
            for j in range(i+1, len(molecule)):
                distance = math.sqrt(sum( (molecule[i][k] - molecule[j][k])**2 for k in range(3) ))
                
                if distance > maxdist:
                    maxdist = distance
                    atom1 = i+1
                    atom2 = j+1
                    
        if args.verbose:
            print('{}: Maxdist between atms {a1} {a2}; {dist:.4f}'.format(n, a1=atom1, a2=atom2, dist=maxdist))
        n += 1

#MaxDistance(OpenReadFile())

def MaxBond(bond_tuples, atom_counts):   # add counters you must
    for i, count in zip(bond_tuples, atom_counts):
        maxbonds = [0] * count
        for j in i:
            if j[2] > maxbonds[j[0]-1]:
                maxbonds[j[0]-1] = j[2]
            if j[2]  > maxbonds[j[1]-1]:
                maxbonds[j[1]-1] = j[2]
        
        if args.verbose:
            print(maxbonds)

MaxBond(allinone['bond_data'], allinone['atom_counts'])

def MolecularMass():
    pass
    # with open(nanjb) as f:
    # csv.reader created blablabla...


def main():
    #if args.verbose:
        ## call MaxDistance, MolecularMass, delete args.verbose in them
    pass

main()