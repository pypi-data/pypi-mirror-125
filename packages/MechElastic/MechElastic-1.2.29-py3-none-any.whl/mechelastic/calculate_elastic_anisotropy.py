from .comms import printer
from .parsers import VaspOutcar
from .parsers import AbinitOutput
from .parsers import QE_ElaStic_Parser
from .parsers import QE_thermo_pw_Parser

from .core import ELATE


def calculate_elastic_anisotropy(
    infile="OUTCAR",
    code="vasp",
    plot=None,
    elastic_calc=None,
    anaddbfile=None,
    outfile=None,
    adjust_pressure=True,
    npoints=100,
    show=True,
    
    #keywords for plot_3D_slice
    normal = (1,0,0), 
    origin =(0,0,0)
    
):
    """
    This method calculates the elastic properties
    of a material from a DFT calculation.
    """

    # welcome message
    printer.print_mechelastic()

    elastic_tensor = None

    rowsList = []
    # calling parser
    if code == "vasp":

        output = VaspOutcar(infile=infile, adjust_pressure=adjust_pressure)
        elastic_tensor = output.elastic_tensor
        elastic_tensor = output.elastic_tensor
        density = output.density

        row = elastic_tensor.shape[0]
        col = elastic_tensor.shape[1]
        rowsList = []
        for i in range(row):
            columnsList = []
            for j in range(col):
                columnsList.append(round(elastic_tensor[i, j], 3))
            rowsList.append(columnsList)

    elif code == "abinit":
        output = AbinitOutput(infile=infile, anaddbfile=anaddbfile)
        elastic_tensor = output.elastic_tensor
        density = output.density

        row = elastic_tensor.shape[0]
        col = elastic_tensor.shape[1]
        rowsList = []
        for i in range(row):
            columnsList = []
            for j in range(col):
                columnsList.append(round(elastic_tensor[i, j], 3))
            rowsList.append(columnsList)

    elif code == "qe_ElaStic":
        output = QE_ElaStic_Parser(outfile=outfile, infile=infile)
        elastic_tensor = output.elastic_tensor
        density = output.density

        row = elastic_tensor.shape[0]
        col = elastic_tensor.shape[1]
        rowsList = []
        for i in range(row):
            columnsList = []
            for j in range(col):
                columnsList.append(round(elastic_tensor[i, j], 3))
            rowsList.append(columnsList)

    elif code == "qe_thermo_pw":
        output = QE_thermo_pw_Parser(outfile=outfile, infile=infile)
        elastic_tensor = output.elastic_tensor
        density = output.density

        row = elastic_tensor.shape[0]
        col = elastic_tensor.shape[1]
        rowsList = []
        for i in range(row):
            columnsList = []
            for j in range(col):
                columnsList.append(round(elastic_tensor[i, j], 3))
            rowsList.append(columnsList)

    
    elastic_tensor = ELATE(rowsList, density)

    if plot == "2D":
        fig = elastic_tensor.plot_2D(
            elastic_calc=elastic_calc, npoints=npoints, apply_to_plot=None, show=show)
    elif plot == "3D":
        meshes = elastic_tensor.plot_3D(
            elastic_calc=elastic_calc, npoints=npoints, show=show)
    elif plot == "3D_slice":
        meshes = elastic_tensor.plot_3D_slice(
            elastic_calc=elastic_calc, npoints=npoints, normal = normal, show=show)

    elastic_tensor.print_properties()

    print("\nThanks! See you later. ")
    if plot == "2D":
        return output, fig
    elif plot == "3D":
        return output, meshes
    else:
        return output
