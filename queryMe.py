import pandas as pd

# Reading the Excel file
df = pd.read_excel(r'C:\Users\Kyle\Downloads\12182023-Kyle_Phan-Finding_student_IDs.xlsx')

# Function handling 'Student Name' column
def split_name(name):
    parts = name.split(', ')
    if len(parts) == 2:
        last_name, rest_of_name = parts
        first_name = rest_of_name.split(' ')[0]  # Take only the first name, ignore middle names
        return last_name, first_name
    else:
        return name, ''  # In case the format is not as expected

df['Last Name'], df['First Name'] = zip(*df['Student Name'].apply(split_name))

# Function to convert academic year to a range of semesters
def academic_year_to_term_range(ay):
    # Extract the first two digits of the start year and the last two digits of the end year
    start_year_prefix = ay[0]  # e.g., '1' from '1992-1993'#
    start_year_suffix = ay[2:4]  # e.g., '92' from '1992-1993'
    end_year_prefix = ay[5]   # e.g., '1' from '1992-1993'
    end_year_suffix = ay[7:9]   # e.g., '93' from '1992-1993'
    
    # Construct the full term codes
    fall_term_code = start_year_prefix + start_year_suffix + '7'  # e.g., '1927'
    # The spring term code will be the year following the fall term, so we increment the year
    spring_term_code = end_year_prefix  + end_year_suffix + '1'  # e.g., '1931'
    
    return fall_term_code, spring_term_code



# Function to generate a single SQL query for a batch of names
def generate_query(batch, term_range):
    conditions = ["(padpv.first_nm = '{}' AND padpv.last_nm = '{}')".format(first.strip(), last.strip()) for last, first in batch]
    condition_str = " OR \n".join(conditions)
    fall_term, spring_term = term_range
    query = (
        "SELECT \n"
        "   distinct padpv.person_id, padpv.last_nm, padpv.first_nm, padpv.middle_nm\n"
        "FROM\n"
        "   asu_student.asu_stdnt_profile_maj_term aspmt\n"
        "INNER JOIN\n"
        "   asu_global.ps_asu_d_person_vw padpv\n"
        "ON\n"
        "   aspmt.emplid = padpv.person_id\n"
        "WHERE\n"
        f"   (aspmt.strm BETWEEN {fall_term} AND {spring_term}) AND \n"
        f"   ({condition_str})\n"
        "ORDER BY\n"
        f"   padpv.last_nm ASC \n"
    )
    return query

# Directory where you want to save the files
output_directory = r'C:\Users\Kyle\Documents\BTO\queryscriptOutput'

# Iterate over each academic year group in the DataFrame
for ay, group_df in df.groupby('AY'):
    term_range = academic_year_to_term_range(ay)
    names = list(zip(group_df['Last Name'], group_df['First Name']))
    query = generate_query(names, term_range)
    file_name = f'{output_directory}\\query_{ay.replace("-", "to")}.sql'  # Use 'to' for the filename to represent the range
    with open(file_name, 'w') as file:
        file.write(query)