from CoolProp.CoolProp import PropsSI
import numpy as np
import pandas as pd
import os

# -- SETTINGS ----------------------------------------------------------------
FLUID_NAME = 'Hydrogen'

# Decimal places
ACCURACY = 6  

# Output format
FOLDER_PATH = FLUID_NAME  # Output folder name
EXCEL = 0
TXT = 0
TXT_1_COLUMN = 1
# ----------------------------------------------------------------------------


def save_tables(tables, filenames, folder_path):
    """Saves tables to text files with spaces as delimiters."""
    # If the folder does not exist, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Saving tables to text files 
    filenames = [filename + '.txt' for filename in filenames]
    for table, filename in zip(tables, filenames):
        file_path = os.path.join(folder_path, filename)
        table.to_csv(file_path, index=True, sep=' ',
                     float_format=f'%.{ACCURACY}f')
    

def save_excel(folder_path=FOLDER_PATH):
    """Save tables to excel file"""
    salary_sheets = {'Den': DF_den, 'Cp': DF_Cp, 'Vis': DF_Vis,
                    'Cond': DF_Cond, 'z': DF_z, 'phase': DF_phase}
    excel_file_path = os.path.join(folder_path, f'prop_{FLUID_NAME}.xlsx')
    writer = pd.ExcelWriter(excel_file_path, engine=None)
    for sheet_name in salary_sheets.keys():
        salary_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name)
    writer.save()


def save_special_format(tables, filenames, folder_path):
    """Save tables to text files with special formatting"""
    # If the folder does not exist, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Save tables to text files with special formatting
    filenames = [filename + '.txt' for filename in filenames]
    for table, filename in zip(tables, filenames):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w') as f:
            for i in range(len(Press_array)):
                f.write(f"P={format(Press_array[i], '.2f')}" + "\n")
                f.write(table[Press_array[i]].to_csv(sep=' ', float_format=f'%.{ACCURACY}f', header=False))


def save_cp_spec_format(table, filename, folder_path):
    """Save Cp table to text file with special formatting"""
    # If the folder does not exist, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Save table to text file with special formatting
    filename = filename + '.txt'
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as f:
        for i in range(len(Press_array)):
            f.write(f"P={format(Press_array[i], '.2f')}" + "\n")
            f.write("2 5" + "\n" "3 17.4" + "\n" "4 43" + "\n" "5 89" + "\n" "8 450" + "\n" "10 1030" + "\n")
            f.write(table[Press_array[i]].to_csv(sep=' ', float_format=f'%.{ACCURACY}f', header=False))


if __name__ == '__main__':
    if EXCEL or TXT or TXT_1_COLUMN == 1:
        Press_array = np.arange(0.01, 1.01, 0.01) * 1e6
        Press_array = np.append(Press_array, np.arange(1.1, 60.1, 0.1) * 1e6)
        Temp_array = np.arange(14, 501, 1)
        # Temp_array = np.arange(14, 25, 1)
        temp_array = np.array([])  # Index array

        den_array = np.array([])
        Cp_array = np.array([])
        Vis_array = np.array([])
        Cond_array = np.array([])
        phase_array = np.array([])
        z_array = np.array([])

        den_array_last = np.array([])
        Cp_array_last = np.array([])
        Vis_array_last = np.array([])
        Cond_array_last = np.array([])
        z_array_last = np.array([])
        phase_array_last = np.array([])

        i = 0
        j = 0
        for press in range(len(Press_array)):
            press = Press_array[i]
            np.append(temp_array, Temp_array)
            for temp in range(len(Temp_array)):
                temp = Temp_array[j]
                den_array = np.append(den_array, PropsSI('D', 'T', temp, 'P', press, FLUID_NAME))
                Cp_array = np.append(Cp_array, PropsSI('CPMASS', 'T', temp, 'P', press, FLUID_NAME))
                Vis_array = np.append(Vis_array, PropsSI('VISCOSITY', 'T', temp, 'P', press, FLUID_NAME))
                Cond_array = np.append(Cond_array, PropsSI('CONDUCTIVITY', 'T', temp, 'P', press, FLUID_NAME))
                phase_array = np.append(phase_array, PropsSI('PHASE', 'T', temp, 'P', press, FLUID_NAME))
                z_array = np.append(z_array, PropsSI('Z', 'T', temp, 'P', press, FLUID_NAME))
                j = j+1
            i = i+1
            j = 0

            # Append the press[i] arrays to the general arrays
            den_array_last = np.append(den_array_last, den_array)
            Cp_array_last = np.append(Cp_array_last, Cp_array)
            Vis_array_last = np.append(Vis_array_last, Vis_array)
            Cond_array_last = np.append(Cond_array_last, Cond_array)
            z_array_last = np.append(z_array_last, z_array)
            phase_array_last = np.append(phase_array_last, phase_array)

            # Empty the press[i] arrays
            den_array = np.array([])
            Cp_array = np.array([])
            Vis_array = np.array([])
            Cond_array = np.array([])
            z_array = np.array([])
            phase_array = np.array([])


        res_den = den_array_last.reshape(len(Press_array), len(Temp_array)).transpose()
        res_Cp = Cp_array_last.reshape(len(Press_array), len(Temp_array)).transpose()
        res_Vis = Vis_array_last.reshape(len(Press_array), len(Temp_array)).transpose()
        res_Cond = Cond_array_last.reshape(len(Press_array), len(Temp_array)).transpose()
        res_z = z_array_last.reshape(len(Press_array), len(Temp_array)).transpose()
        res_phase = phase_array_last.reshape(len(Press_array), len(Temp_array)).transpose()

        # Press_array = [f'p={Press_array[i]}' for i in range(len(Press_array))]
        DF_den = pd.DataFrame(res_den, index=Temp_array, columns=Press_array)
        DF_Cp = pd.DataFrame(res_Cp, index=Temp_array, columns=Press_array)
        DF_Vis = pd.DataFrame(res_Vis, index=Temp_array, columns=Press_array)
        DF_Cond = pd.DataFrame(res_Cond, index=Temp_array, columns=Press_array)
        DF_z = pd.DataFrame(res_z, index=Temp_array, columns=Press_array)
        DF_phase = pd.DataFrame(res_phase, index=Temp_array, columns=Press_array)

        if not os.path.exists(FOLDER_PATH):
            os.makedirs(FOLDER_PATH)

        # tables = [DF_den, DF_Cp, DF_Vis, DF_Cond, DF_z, DF_phase]
        # filenames = ['Den', 'Cp', 'Vis', 'Cond', 'z', 'phase']
        
        tables = [DF_den, DF_Vis, DF_Cond, DF_z, DF_phase]
        filenames = ['Den', 'Vis', 'Cond', 'z', 'phase']

        if EXCEL == 1:
            save_excel()
        if TXT == 1:
            TXT_FOLDER_PATH = os.path.join(FOLDER_PATH, "txt")
            save_tables(tables, filenames, TXT_FOLDER_PATH)
        if TXT_1_COLUMN == 1:
            TXT_1_COL_FOLDER_PATH = os.path.join(FOLDER_PATH, "txt_1_column")
            save_special_format(tables, filenames, TXT_1_COL_FOLDER_PATH)
            save_cp_spec_format(DF_Cp, "Cp", TXT_1_COL_FOLDER_PATH)
    else:
        raise ValueError("select type of output file in the settings section")
        