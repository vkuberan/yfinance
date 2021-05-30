import os
import glob
import re
import time

nse_file_name_starts_with = ['MW-NIFTY-REALTY-', 'MW-NIFTY-PHARMA-',
                             'MW-NIFTY-METAL-', 'MW-NIFTY-MEDIA-',
                             'MW-NIFTY-IT-', 'MW-NIFTY-FMCG-',
                             'MW-NIFTY-FINANCIAL-SERVICES-',
                             'MW-NIFTY-AUTO-', 'MW-NIFTY-BANK-',
                             'MW-NIFTY-200-', 'MW-NIFTY-100-',
                             'MW-NIFTY-NEXT-50-', 'MW-NIFTY-50-']


# clean the header from nse csv file,
def clean_csv_file_header(file_content):
    number_of_columns_in_the_table = 14
    header = ''
    body = ''
    cnt = 1
    for line in file_content:

        if len(line.split(',')) < number_of_columns_in_the_table:
            encoded_string = line.encode("ascii", "ignore")
            line = encoded_string.decode()

            myString = re.sub(r"[\n\t]*", "", line)
            header += myString.strip()
        else:
            encoded_string = line.encode("ascii", "ignore")
            line = encoded_string.decode()
            body += line

        cnt += 1

    return (header + "\n" + body)


# returns the pattern along with file name
def get_nse_file_by_pattern(full_file_name):
    file_data = {}

    for fname_pattern in nse_file_name_starts_with:
        if fname_pattern in full_file_name:
            mtime = os.path.getmtime(full_file_name)
            modification_time = time.strftime(
                '%Hh-%Mm', time.localtime(mtime))

            new_file_name = fname_pattern[:-1].lower() + '.csv'
            new_file_name_with_time_slot = '{}-{}.csv'.format(
                fname_pattern[:-1].lower(), modification_time)

            start_pos = full_file_name.find(fname_pattern)
            end_pos = full_file_name.find('.csv')
            date_start_pos = start_pos + len(fname_pattern)

            file_name = full_file_name[start_pos:]
            date_of_file = full_file_name[date_start_pos:end_pos]

            # use data's from the filename and other properties of the file
            file_data['pattern'] = fname_pattern
            file_data['file_name'] = file_name
            file_data['new_file_name'] = new_file_name
            file_data['new_file_with_time_slot'] = new_file_name_with_time_slot
            file_data['file_date'] = date_of_file

            break

    return file_data


def clean_nse_data_fetched_from_nse_api():

    # removing old files from the current analysis folder
    files = glob.glob("data/current-analysis/*.csv")
    for file in files:
        os.remove(file)
        print("Old File Deleted: '{}'.".format(
            file
        ))

    files = glob.glob("data/unclean/*.csv")

    for file in files:
        file_data = get_nse_file_by_pattern(file)

        content = ''
        file_name = 'data/unclean/' + file_data['file_name']

        with open(file_name) as inf:
            content = clean_csv_file_header(inf)

        if content is not None:

            current_day_analysis = 'data/current-analysis/' + \
                file_data['new_file_name']

            with open(current_day_analysis, 'w') as writer:
                print("New File Created: '{}'.".format(
                    current_day_analysis))
                writer.write(content)

            # remove the unclean file from unclean folder.
            os.remove(file_name)
            print("Removed all CSV files from 'data/unclean/' folder.")
