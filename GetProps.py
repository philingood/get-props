from CoolProp.CoolProp import PropsSI
import numpy as np
import pandas as pd
import os

# -- SETTINGS ----------------------------------------------------------------
ACCURACY = 6  # decimal places
FOLDER_PATH = 'Tables'
NAME_PROP = 'Hydrogen'
# ----------------------------------------------------------------------------


def save_tables(tables, filenames, folder_path=FOLDER_PATH):
    """
    Saves tables to text files with spaces as delimiters.

    Options:
    tables - a list of Pandas tables
    filenames - list of filenames
    folder_path - path to the folder for outputting files
    """
    # If the folder does not exist, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Saving tables to text files 
    filenames = [filename + '.txt' for filename in filenames]
    for table, filename in zip(tables, filenames):
        file_path = os.path.join(folder_path, filename)
        table.to_csv(file_path, index=True, sep=' ',
                     float_format=f'%.{ACCURACY}f')
    
    # Save tables to excel file
    salary_sheets = {'Den': DF_den, 'Cp': DF_Cp, 'Vis': DF_Vis,
                    'Cond': DF_Cond, 'z': DF_z, 'phase': DF_phase}
    excel_file_path = os.path.join(folder_path, f'prop_{NAME_PROP}.xlsx')
    writer = pd.ExcelWriter(excel_file_path, engine=None)
    for sheet_name in salary_sheets.keys():
        salary_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name)
    writer.save()


if __name__ == '__main__':
    Press_array = np.arange(0.1, 30.5, 0.5)
    Temp_array = np.arange(14, 301, 1)
    den_array = np.array([])
    Cp_array = np.array([])
    Vis_array = np.array([])
    Cond_array = np.array([])
    phase_array = np.array([])
    z_array = np.array([])
    i = 0
    j = 0
    den_array_last = np.array([])
    Cp_array_last = np.array([])
    Vis_array_last = np.array([])
    Cond_array_last = np.array([])
    z_array_last = np.array([])
    phase_array_last = np.array([])
    for press in range(len(Press_array)):
        press = Press_array[i]
        for temp in range(len(Temp_array)):
            temp = Temp_array[j]
            den = PropsSI('D', 'T', temp, 'P', press*1E6, NAME_PROP)
            den_array = np.append(den_array, den)
            Cp = PropsSI('CPMASS', 'T', temp, 'P', press*1E6, NAME_PROP)
            Cp_array = np.append(Cp_array, Cp)
            Vis = PropsSI('VISCOSITY', 'T', temp, 'P', press*1E6, NAME_PROP)
            Vis_array = np.append(Vis_array, Vis)
            Cond = PropsSI('CONDUCTIVITY', 'T', temp, 'P', press*1E6, NAME_PROP)
            Cond_array = np.append(Cond_array, Cond)
            phase = PropsSI('PHASE', 'T', temp, 'P', press*1E6, NAME_PROP)
            phase_array = np.append(phase_array, phase)
            z = PropsSI('Z', 'T', temp, 'P', press*1E6, NAME_PROP)
            z_array = np.append(z_array, z)
            j = j+1
        i = i+1
        j = 0
        den_array_last = np.append(den_array_last, den_array)
        den_array = np.array([])
        Cp_array_last = np.append(Cp_array_last, Cp_array)
        Cp_array = np.array([])
        Vis_array_last = np.append(Vis_array_last, Vis_array)
        Vis_array = np.array([])
        Cond_array_last = np.append(Cond_array_last, Cond_array)
        Cond_array = np.array([])
        z_array_last = np.append(z_array_last, z_array)
        z_array = np.array([])
        phase_array_last = np.append(phase_array_last, phase_array)
        phase_array = np.array([])


    res_den = den_array_last.reshape(len(Press_array), len(Temp_array)).transpose()
    res_Cp = Cp_array_last.reshape(len(Press_array), len(Temp_array)).transpose()
    res_Vis = Vis_array_last.reshape(len(Press_array), len(Temp_array)).transpose()
    res_Cond = Cond_array_last.reshape(len(Press_array), len(Temp_array)).transpose()
    res_z = z_array_last.reshape(len(Press_array), len(Temp_array)).transpose()
    res_phase = phase_array_last.reshape(len(Press_array), len(Temp_array)).transpose()

    DF_den = pd.DataFrame(res_den, index=Temp_array, columns=Press_array)
    DF_Cp = pd.DataFrame(res_Cp, index=Temp_array, columns=Press_array)
    DF_Vis = pd.DataFrame(res_Vis, index=Temp_array, columns=Press_array)
    DF_Cond = pd.DataFrame(res_Cond, index=Temp_array, columns=Press_array)
    DF_z = pd.DataFrame(res_z, index=Temp_array, columns=Press_array)
    DF_phase = pd.DataFrame(res_phase, index=Temp_array, columns=Press_array)

    tables = [DF_den, DF_Cp, DF_Vis, DF_Cond, DF_z, DF_phase]
    filenames = ['Den', 'Cp', 'Vis', 'Cond', 'z', 'phase']

    save_tables(tables, filenames)
    