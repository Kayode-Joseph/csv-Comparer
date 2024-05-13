import time

import csv
import os

import numpy as np


# file file kind, Source or Target
def read_csv_into_numpy(csv_file_kind: str):
    try:
        # Get the path to the 'csv' folder from the current directory
        csv_folder_path = os.path.join(os.getcwd(), 'csv')

        # Prompt the user to enter the CSV file name with its extension
        file_name = input(
            f"\n\n\033[93mEnter the {csv_file_kind} CSV file name with its extension \n"
            f"(The csv file has to be in the '{csv_folder_path}'): \033[0m")
        file_path = os.path.join(csv_folder_path, file_name)

        # Check if the file exists within the 'csv' folder
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"\033[91m{csv_file_kind} CSV File '{file_name}' not found in the 'csv' folder.\033[0m")

        # Read the CSV file into a 2D NumPy array
        numpy_array = np.genfromtxt(file_path, delimiter=',', dtype=str)

        return file_name, numpy_array
    except FileNotFoundError as e:
        print(e)
        # Call the function again recursively
        return read_csv_into_numpy(csv_file_kind)
    except ValueError as e:
        print(f"\033[91m{e}\033[0m")
        # Call the function again recursively
        return read_csv_into_numpy(csv_file_kind)


def process_report_csv_numpy(sorted_source: np,
                             sorted_target: np,
                             header_row: list,
                             record_identifier_column: list,
                             coordinates_where_source_is_not_equals_to_target: np,
                             headers_in_source_but_not_target: set,
                             headers_in_target_but_not_source: set,
                             row_identifiers_in_source_but_not_target: set,
                             row_identifiers_in_target_but_not_source: set,
                             ) -> np:
    report_csv_numpy = [['Record Identifier', 'Header', 'Description']]

    missing_records_already_reported_in_result = set()

    missing_headers_already_reported_in_result = set()

    for record_identifier_coordinate, header_coordinate in coordinates_where_source_is_not_equals_to_target:

        record_identifier = record_identifier_column[record_identifier_coordinate]

        header = header_row[header_coordinate]

        mismatched_coordinates_already_reported = False

        if record_identifier in row_identifiers_in_source_but_not_target:
            mismatched_coordinates_already_reported = True
            if record_identifier not in missing_records_already_reported_in_result:
                report_csv_numpy.append([record_identifier, "ALL",
                                         f"Record with Identifier: {record_identifier}, is missing from target CSV"])
                missing_records_already_reported_in_result.add(record_identifier)

        elif record_identifier in row_identifiers_in_target_but_not_source:
            mismatched_coordinates_already_reported = True
            if record_identifier not in missing_records_already_reported_in_result:
                report_csv_numpy.append([record_identifier, "ALL",
                                         f"Record with Identifier: {record_identifier}, is missing from source CSV"])
                missing_records_already_reported_in_result.add(record_identifier)

        if header in headers_in_source_but_not_target:
            mismatched_coordinates_already_reported = True
            if header not in missing_headers_already_reported_in_result:
                report_csv_numpy.append(["ALL", header, f"Header column: {header}, is missing from target CSV"])
                missing_headers_already_reported_in_result.add(header)

        elif header in headers_in_target_but_not_source:
            mismatched_coordinates_already_reported = True
            if header not in missing_headers_already_reported_in_result:
                report_csv_numpy.append(["ALL", header, f"Header column: {header}, is missing from source CSV"])
                missing_headers_already_reported_in_result.add(header)

        # if the mismatched rows have already been reported we don't need to do anything more
        if mismatched_coordinates_already_reported:
            continue

        report_csv_numpy.append([record_identifier, header,
                                 f"There is a mismatch between source value:"
                                 f"{sorted_source[record_identifier_coordinate, header_coordinate]} "
                                 f"and target value:{sorted_target[record_identifier_coordinate, header_coordinate]} "])

    return report_csv_numpy


def write_numpy_to_csv_file(numpy_array, file_name):
    """
    Write a NumPy array to a CSV file.

    Parameters:
    - numpy_array: NumPy array to be written to CSV.
    - file_name: Name of the CSV file.

    Returns:
    - None
    """
    result_folder = os.path.join(os.getcwd(), 'csv', 'reports')
    os.makedirs(result_folder, exist_ok=True)
    result_csv_path = os.path.join(result_folder, f"{file_name}{time.time()}")

    with open(result_csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(numpy_array)
        print(f"CSV Report has been saved at {result_csv_path}")


