#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 9 13:29:32 2020

@author: grat05
"""

import numpy as np
import pandas as pd

from ._PyLongQt import DataReader

def readAsDataFrame(folder, exclude_trials=set()):
    """
    Read a folder in the same manner as :py:meth:`DataReader.readDir`
    but return a DataFrame instead of a :py:class:`SimData` object
    :folder: The directory which contains the simulation save files
    :exclude_trials: Trials to exclude
    
    returns
      traces_by_cell, measured_by_cell A list of the traces and a list of the
      measures
    """
    data = DataReader.readDir(folder, exclude_trials)
    traces_by_cell = []
    for trial in range(len(data.trace)):
        traces = data.trace[trial]
        trace_data = np.array(traces.data).T
        if trace_data.size == 0:
            trace_data = None
        trace_names = []
        cell_positions = []
        for head in traces.header:
            trace_names.append(head.var_name)
            if len(head.cell_info_parsed) > 0:
                cell_positions.append(tuple(head.cell_info_parsed))
        if len(cell_positions) != 0:
            col_index = pd.MultiIndex.from_arrays(
                [cell_positions, trace_names],
                names=['Cell', 'Variable'])
        else:
            col_index = pd.Index(data=trace_names, name='Variable')

        traces_by_cell.append(pd.DataFrame(data=trace_data, 
                                               columns=col_index))
            
    measured_by_cell = []
    for trial in range(len(data.meas)):
        meases = data.meas[trial]
        meas_data = np.array(meases.data).T
        if meas_data.size == 0:
            meas_data = None
        meas_names = []
        prop_names = []
        cell_positions = []
        for head in meases.header:
            meas_names.append(head.var_name)
            prop_names.append(head.prop_name)
            if len(head.cell_info_parsed) > 0:
                cell_positions.append(tuple(head.cell_info_parsed))
        if len(cell_positions) != 0:
            col_index = pd.MultiIndex.from_arrays(
                [cell_positions, meas_names, prop_names],
                names=['Cell', 'Variable', 'Property'])
        else:
            col_index = pd.MultiIndex.from_arrays(
                [meas_names, prop_names],
                names=['Variable', 'Property'])
        measured_by_cell.append(pd.DataFrame(data=meas_data, 
                                             columns=col_index))
    return traces_by_cell, measured_by_cell

def convertDataToExcel(fname_trace, fname_meas,\
               data_folder = None,\
               traces_by_cell=None, measured_by_cell=None):
    """
    Convert simulation data into an excel sheet for traces and an excel sheet
    for measures
    
    :fname_trace: The excel sheet for traces
    :fname_meas: The excel sheet for measures
    :data_folder: (optional) The data directory to be read
    :traces_by_cell: (optional) A list of trace DataFrames
    :measured_by_cell: (optional) A list of measure DataFrames
    
    .. note::
       Either the data_folder or the lists of DataFrames must be supplied
    """
    if not data_folder is None:
        traces_by_cell, measured_by_cell = readAsDataFrame(data_folder)
    elif (traces_by_cell is None) or (measured_by_cell is None):
        print("Data must be specified by data_folder or BOTH traces_by_cell AND measured_by_cell")
        return

    with pd.ExcelWriter(fname_trace) as writer:
        for trial in range(len(traces_by_cell)):
            df = traces_by_cell[trial]
            df.to_excel(excel_writer=writer,\
                        sheet_name='Trial '+str(trial))
    with pd.ExcelWriter(fname_meas) as writer:
        for trial in range(len(measured_by_cell)):
            df = measured_by_cell[trial]
            df.to_excel(excel_writer=writer,\
                        sheet_name='Trial '+str(trial))

def convertDataToHDF(outfile, data_folder = None,\
             traces_by_cell=None, measured_by_cell=None):
    '''
    Convert simulation data into a Hierarchical Data Format (HDF) file which 
    can be read by :py:func:`readHDF`
    
    :outfile: The HDF file to be written
    :data_folder: (optional) The data directory to be read
    :traces_by_cell: (optional) A list of trace DataFrames
    :measured_by_cell: (optional) A list of measure DataFrames
    
    .. note::
       Either the data_folder or the lists of DataFrames must be supplied
       
    .. note::
        The HDF format was designed for the storage of large amounts of data.
        As such, it is much more efficient to read HDF files than a datadir,
        so for large simulations it is recommended to convert them to HDF
    '''
    if not data_folder is None:
        traces_by_cell, measured_by_cell = readAsDataFrame(data_folder)
    elif (traces_by_cell is None) or (measured_by_cell is None):
        print("Data must be specified by data_folder or BOTH traces_by_cell AND measured_by_cell")
        return

    with pd.HDFStore(outfile) as store:
        for trial in range(len(traces_by_cell)):
            df = traces_by_cell[trial]
            df.to_hdf(path_or_buf=outfile,
                      key='Trace_'+str(trial))
        for trial in range(len(measured_by_cell)):
            df = measured_by_cell[trial]
            df.to_hdf(path_or_buf=outfile,
                      key='Measure_'+str(trial))
            
def readHDF(file):
    '''
    Read a saved Hierarchical Data Format (HDF) file and return the lists
    of DataFrames for traces and measures
    
    :file: The HDF file to read
    '''
    traces_by_cell = []
    measured_by_cell = []
    with pd.HDFStore(file, mode='r') as store:
         for key in sorted(store.keys(), 
                           key=lambda x: int(x.split('_')[-1])):
            if 'Measure' in key:
                measured_by_cell.append(store[key])
            elif 'Trace' in key:
                traces_by_cell.append(store[key])
            else:
                print("Key not trace or meansure with name: "+key)
    return traces_by_cell, measured_by_cell
                

#Add functions to DataReader
DataReader.readAsDataFrame = readAsDataFrame
DataReader.convertDataToExcel = convertDataToExcel
DataReader.convertDataToHDF = convertDataToHDF
DataReader.readHDF = readHDF
