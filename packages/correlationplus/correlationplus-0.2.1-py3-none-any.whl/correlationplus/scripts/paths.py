##############################################################################
# correlationplus - A Python package to calculate, visualize and analyze      #
#                   correlation maps of proteins.                             #
# Authors: Mustafa Tekpinar                                                   #
# Copyright (C) Mustafa Tekpinar, 2017-2018                                   #
# Copyright (C) CNRS-UMR3528, 2019                                            #
# Copyright (C) Institut Pasteur Paris, 2020-2021                             #
#                                                                             #
# This file is part of correlationplus.                                       #
#                                                                             #
# correlationplus is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU Lesser General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# correlationplus is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU LESSER General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Lesser General Public License    #
# along with correlationplus.  If not, see <https://www.gnu.org/licenses/>.   #
###############################################################################

import os
import sys
import getopt

import numpy as np
from prody import parsePDB
from prody import buildDistMatrix

from correlationplus.visualize import convertLMIdata2Matrix
from correlationplus.visualize import parseEVcouplingsScores
from correlationplus.visualize import parseSparseCorrData
from correlationplus.visualize import parseElasticityGraph

from correlationplus.centralityAnalysis import buildDynamicsNetwork
from correlationplus.centralityAnalysis import buildSequenceNetwork

from correlationplus.pathAnalysis import pathAnalysis
from correlationplus.pathAnalysis import mapResid2ResIndex
from correlationplus.pathAnalysis import writePath2VMDFile, writePath2PMLFile 

def usage_pathAnalysisApp():
    """
    Show how to use this program!
    """
    print("""
Example usage:
correlationplus paths -i ndcc-6lu7-anm.dat -p 6lu7_dimer_with_N3_protein_sim1_ca.pdb -b A41 -e B41

Arguments: -i: A file containing correlations in matrix format. (Mandatory)

           -p: PDB file of the protein. (Mandatory)
           
           -t: Type of the matrix. It can be dcc, ndcc, lmi, nlmi (normalized lmi), 
               absndcc (absolute values of ndcc) or eg (elasticity graph).
               In addition, coeviz and evcouplings are also some options to analyze sequence
               correlations. 
               If your data is any other coupling data in full matrix format, you can select 'generic'
               as your data type. 
               Default value is ndcc (Optional)

           -o: This will be your output file. Output figures are in png format. 
               (Optional)

           -v: Value filter. The values lower than this value in the map will be 
               considered as zero. Default is 0.3. (Optional)

           -d: Distance filter. The residues with distances higher than this value 
               will be considered as zero. Default is 7.0 Angstrom. (Optional)
                              
           -b: ChainID and residue ID of the beginning (source)  residue (Ex: A41). (Mandatory)

           -e: ChainID and residue ID of the end (sink/target) residue (Ex: B41). (Mandatory)

           -n: Number of shortest paths to write to tcl or pml files. Default is 1. (Optional)
""")


def handle_arguments_pathAnalysisApp():
    inp_file = None
    pdb_file = None
    out_file = None
    sel_type = None
    val_fltr = None
    dis_fltr = None
    src_res = None
    trgt_res = None
    num_path = None

    try:
        opts, args = getopt.getopt(sys.argv[2:], "hi:o:t:p:v:d:b:e:n:", \
            ["help", "inp=", "out=", "type=", "pdb=", "value=", "distance", "beginning=", "end=", "distance=", "npaths"])
    except getopt.GetoptError:
        usage_pathAnalysisApp()
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            usage_pathAnalysisApp()
            sys.exit(-1)
        elif opt in ("-i", "--inp"):
            inp_file = arg
        elif opt in ("-o", "--out"):
            out_file = arg
        elif opt in ("-t", "--type"):
            sel_type = arg
        elif opt in ("-p", "--pdb"):
            pdb_file = arg
        elif opt in ("-v", "--value"):
            val_fltr = arg
        elif opt in ("-d", "--distance"):
            dis_fltr = arg
        elif opt in ("-b", "--beginning"):
            src_res = arg
        elif opt in ("-e", "--end"):
            trgt_res = arg
        elif opt in ("-n", "--npaths"):
            num_path = arg
        else:
            assert False, usage_pathAnalysisApp()

    # Input data matrix and PDB file are mandatory!
    if inp_file is None or pdb_file is None:
        print("@> ERROR: A PDB file and a correlation matrix are mandatory!")
        usage_pathAnalysisApp()
        sys.exit(-1)

    # Assign a default name if the user forgets the output file prefix.
    if out_file is None:
        out_file = "paths"

    # The user may prefer not to submit a title for the output.
    if sel_type is None:
        sel_type = "ndcc"

    if val_fltr is None:
        val_fltr = 0.3

    if dis_fltr is None:
        dis_fltr = 7.0
    
    if num_path is None:
        num_path = 1

    if src_res is None:
        print("@>ERROR: You have to specify a chain ID and source resid!")
        print("@>Example: To specify resid 41 in chain A, use A41.")
        usage_pathAnalysisApp()
        sys.exit(-1)

    if trgt_res is None:
        print("@>ERROR: You have to specify a chain ID and a target resid!")
        print("@>Example: To specify resid 41 in chain B, use B41.")
        usage_pathAnalysisApp()
        sys.exit(-1)

    return inp_file, out_file, sel_type, pdb_file, \
            val_fltr, dis_fltr, src_res, trgt_res, num_path


def pathAnalysisApp():
    inp_file, out_file, sel_type, pdb_file,val_fltr, \
    dis_fltr, src_res, trgt_res, num_paths\
            = handle_arguments_pathAnalysisApp()

    print(f"""
@> Running 'paths' app

@> Input file     : {inp_file}
@> PDB file       : {pdb_file}
@> Data type      : {sel_type}
@> Output         : {out_file}
@> Value filter   : {val_fltr}
@> Distance filter: {dis_fltr}
@> Source residue : {src_res}
@> Target residue : {trgt_res}
@> Number of paths: {num_paths}""")

    if (os.path.isfile(inp_file) == False):
        print("@> ERROR: Could not find the correlation matrix: "+inp_file+"!")
        print("@>        The file does not exist or it is not in the folder!\n")
        sys.exit(-1)

    if (os.path.isfile(pdb_file)  == False):
        print("@> ERROR: Could not find the pdb file: "+pdb_file+"!")
        print("@>        The file does not exist or it is not in the folder!\n")
        sys.exit(-1)

    ##########################################################################
    # Read PDB file
    # TODO: This is the only place where I use Prody.
    # Maybe, I can replace it with a library that only parses
    # PDB files. Prody does a lot more!
    selectedAtoms = parsePDB(pdb_file, subset='ca')

    ##########################################################################
    # Read data file and assign to a numpy array
    if ((sel_type.lower() == "dcc") or (sel_type.lower() == "ndcc")):
        # Check if the data type is sparse matrix
        data_file = open(inp_file, 'r')
        allLines = data_file.readlines()
        data_file.close()
 
        # Read the first line to determine if the matrix is sparse format
        words = allLines[0].split()

        # Read the 1st line and check if it has three columns
        if (len(words) == 3):
            ccMatrix = parseSparseCorrData(inp_file, selectedAtoms, \
                                            Ctype=True, 
                                            symmetric=True,
                                            writeAllOutput=False)
        else:
            ccMatrix = np.loadtxt(inp_file, dtype=float)
    elif sel_type.lower() == "absndcc":
        # Check if the data type is sparse matrix
        data_file = open(inp_file, 'r')
        allLines = data_file.readlines()
        data_file.close()
 
        # Read the first line to determine if the matrix is sparse format
        words = allLines[0].split()

        # Read the 1st line and check if it has three columns
        if (len(words) == 3):
            ccMatrix = np.absolute(parseSparseCorrData(inp_file, selectedAtoms, \
                                                        Ctype=True, 
                                                        symmetric=True,
                                                        writeAllOutput=False))
        else:
            ccMatrix = np.absolute(np.loadtxt(inp_file, dtype=float))
    elif ((sel_type.lower()== "lmi") or (sel_type.lower()== "nlmi")):
        # Check if the data type is sparse matrix
        data_file = open(inp_file, 'r')
        allLines = data_file.readlines()
        data_file.close()
 
        # Read the first line to determine if the matrix is sparse format
        words = allLines[0].split()

        # Read the 1st line and check if it has three columns
        if (len(words) == 3):
            ccMatrix = parseSparseCorrData(inp_file, selectedAtoms, \
                                            Ctype=True, 
                                            symmetric=True,
                                            writeAllOutput=False)
        else:
            ccMatrix = convertLMIdata2Matrix(inp_file, writeAllOutput=False)
    elif sel_type.lower() == "coeviz":
        ccMatrix = np.loadtxt(inp_file, dtype=float) 
    elif sel_type.lower() == "evcouplings":
        ccMatrix = parseEVcouplingsScores(inp_file, selectedAtoms, False)
    elif sel_type.lower() == "generic":
        # Check if the data type is sparse matrix
        data_file = open(inp_file, 'r')
        allLines = data_file.readlines()
        data_file.close()
 
        # Read the first line to determine if the matrix is sparse format
        words = allLines[0].split()

        # Read the 1st line and check if it has three columns
        if (len(words) == 3):
            ccMatrix = parseSparseCorrData(inp_file, selectedAtoms, \
                                            Ctype=True, 
                                            symmetric=True,
                                            writeAllOutput=False)
        else:
            ccMatrix = np.loadtxt(inp_file, dtype=float)
    elif sel_type.lower() == "eg":
        # The data type is elasticity graph
        ccMatrix = parseElasticityGraph(inp_file, selectedAtoms, \
                                            writeAllOutput=False)
    else:
        print("@> ERROR: Unknown data type: Type can only be dcc, ndcc, absndcc, \n")
        print("@>        lmi, nlmi, coeviz or evcouplings. If you have your data in full \n")
        print("@>        matrix format and your data type is none of the options\n")
        print("@>        mentionned, you can set data type as 'generic'.\n")
        sys.exit(-1)

    sourceResid = src_res
    targetResid = trgt_res
    distanceMatrix = buildDistMatrix(selectedAtoms)
    resDict = mapResid2ResIndex(selectedAtoms)

    if ((sel_type.lower() == "ndcc") or \
        (sel_type.lower() == "nlmi")):
        network = buildDynamicsNetwork(ccMatrix, distanceMatrix, \
                                    float(val_fltr), float(dis_fltr),\
                                    selectedAtoms)
    else:
        network = buildSequenceNetwork(ccMatrix, distanceMatrix, \
                                    float(val_fltr), float(dis_fltr),\
                                    selectedAtoms)
                                    
    suboptimalPaths = pathAnalysis(network, \
                                   float(val_fltr), float(dis_fltr),\
                                   resDict[sourceResid], resDict[targetResid], \
                                   selectedAtoms,\
                                   int(num_paths))

    out_file_full_name = out_file+"-source"+sourceResid+"-target"+targetResid+".tcl"
    writePath2VMDFile(suboptimalPaths, selectedAtoms, \
                    resDict[sourceResid], resDict[targetResid], \
                    pdb_file, out_file_full_name)

    out_file_full_name = out_file+"-source"+sourceResid+"-target"+targetResid+".pml"
    writePath2PMLFile(suboptimalPaths, selectedAtoms,\
                    resDict[sourceResid], resDict[targetResid], \
                    pdb_file, out_file_full_name)
    