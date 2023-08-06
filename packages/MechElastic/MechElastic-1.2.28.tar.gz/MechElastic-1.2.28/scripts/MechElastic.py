#!/usr/bin/env python

"""This script reads elastic constants from DFT output files, calculates elastic moduli, and performs mechanical stability test:
   Authors: Sobhit Singh (1,2) Logan Lang (2), Viviana Dovale-Farelo (2), Uthpala Herath(2), Pedram Tavadze(2), François-Xavier Coudert(3), Aldo Romero (2)
   Email: smsingh@mix.wvu.edu, alromero@mail.wvu.edu
   (1) Rutgers University, Piscataway, NJ, USA
   (2) West Virginia University, Morgantown, WV, USA
   (3) Chimie ParisTech, PSL University, CNRS, Institut de Recherche de Chimie Paris, 75005, Paris, France
Version: 12.2019   #Dec. 2019

Please cite the below paper if you use this code for your research:
    - Sobhit Singh, Irais Valencia-Jaime, Olivia Pavlic, and Aldo H. Romero; Phys. Rev. B 97, 054108 (2018).
    - Sobhit Singh, Logan Lang, Viviana Dovale-Farelo, Uthpala Herath, Pedram Tavadze, François-Xavier Coudert, Aldo H. Romero; arXiv:2012.04758 [cond-mat.mtrl-sci].


To RUN this code for a 3D system assuming you know the crystal type before hand:
 >> python MechElastic.py -i OUTCAR-file -c hexagonal --dim 3D

Note: The crystal type is needed only to perform the elastic stabilty test.
      This test is not yet implemented for 2D systems, so you can ignore the crystal type for 2D systems.

If the crystal symmetry is not provided by user, then the code will rely on spglib to find it
 >> python MechElastic.py -i OUTCAR-file --dim 3D

To RUN this code for a 2D monolayer system
 >> python MechElastic.py -i OUTCAR-file --dim 2D
      (please pay attention to the warning for 2D systems)

OUTCAR file, if present in the current directory, is read as default unless a filename is specified by the user.


Disclaimer: Please check the authenticity of your results before publishing.
            AUTHORS of this script do not guarantee the quality and/or accuracy
            of results generated using this script.

"""

import argparse
import sys
import mechelastic

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--input",
    type=str,
    help="Output file of the DFT calculation.",
    default=None,
)
parser.add_argument(
    "-anaddb",
    "--anaddbfile",
    type=str,
    help="DDB file of the Abinit anaddb calculation.",
    default=None,
)
parser.add_argument(
    "-qe_outfile",
    type=str,
    help="Quantum Espresso output file.",
    default=None,
)

parser.add_argument(
    "-c",
    "--crystal",
    type=str,
    default=None,
    help="Provide the crystal family. Otherwise it would be determined from the DFT output.",
)

parser.add_argument(
    "-l",
    "--lattice_type",
    type=str,
    default=None,
    help="Provide the lattice type for 2D materials. This is required to perform 2D stability tests.",
)

parser.add_argument(
    "-d",
    "--dim",
    type=str,
    help="Enter the dimension, 2D or 3D: For example: '-d 2D' or '--dim 2D'. Default is '3D' ",
    default="3D",
)
parser.add_argument(
    "-co",
    "--code",
    type=str,
    help="DFT code",
    default="vasp",
    choices=["vasp", "abinit", "qe"],
)
parser.add_argument(
    "-ap",
    "--adjust_pressure",
    default=1,
    type=int,
    help="Flag to adjust pressure in Elastic Tensor (VASP). Default: 1 (True)",
    choices=[1, 0],
)

parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Enable verbosity.",
)
parser.add_argument(
    "-o",
    "--outfile",
    type=str,
    default="elastic_properties.txt",
    help="Name of output file. Could be in .txt, .json or .xml formats.",
)


args = parser.parse_args()

print("-----------------------------")
print("List of arguments entered:")
print("Input file name:", args.input)
print("DFT code:", args.code)
print("Crystal type: ", args.crystal)
print("Dimensions:", args.dim)
print("-----------------------------")


# calculate elastic properties
def main():

    if args.adjust_pressure == 1:
        args.adjust_pressure = True
    else:
        args.adjust_pressure = False

    mechelastic.calculate_elastic(
        code=args.code,
        dim=args.dim,
        infile=args.input,
        crystal=args.crystal,
        lattice_type=args.lattice_type,
        anaddbfile=args.anaddbfile,
        adjust_pressure=args.adjust_pressure,
        qe_outfile=args.qe_outfile,
        verbose=args.verbose,
        outfile=args.outfile,
    )


if __name__ == "__main__":
    main()
