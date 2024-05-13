import os

import numpy as np
import sys

from util import (get_headers, get_row_identifiers,
                  validate_there_are_no_duplicate_records_or_headers_in_csv,
                  sort_numpy_by_record_identifier_column_and_header_row,
                  are_all_csv_numpy_elements_numeric, read_float_from_user, is_not_fuzzy_equals)

from csv_service import read_csv_into_numpy, process_report_csv_numpy, write_numpy_to_csv_file

from csv_normalizer import normalize_csvs


source_csv_file_name, source = read_csv_into_numpy(csv_file_kind="source")
target_csv_file_name, target = read_csv_into_numpy(csv_file_kind="target")

is_csv_fuzzy_equals_candidate, fuzzy_equals_threshold = False, 0.00

if are_all_csv_numpy_elements_numeric(source) and are_all_csv_numpy_elements_numeric(target):
    is_csv_fuzzy_equals_candidate = True
    print("All values in the source and target CSV files are numeric.\n"
          "You can compare these values using fuzzy equality with a specified error threshold, \n"
          "set error threshold 0 to compare exact equality.\n\n")
    fuzzy_equals_threshold = read_float_from_user(
        "\033[93mPlease set the error threshold for fuzzy equality comparison, AND hit ENTER: \033[0m")

source_csv_header_list_and_set: tuple[list, set] = get_headers(source)
target_csv_header_list_and_set: tuple[list, set] = get_headers(target)

source_csv_record_identifier_list_and_set: tuple[list, set] = get_row_identifiers(source)
target_csv_record_identifier_list_and_set: tuple[list, set] = get_row_identifiers(target)

"""for optimal performance, this impl does not support duplicate records or headers
Every record is expected to have a unique identifier in its first column"""
are_csvs_valid: tuple[bool, str] = validate_there_are_no_duplicate_records_or_headers_in_csv(
    source_csv_header_list_and_set,
    target_csv_header_list_and_set,
    source_csv_record_identifier_list_and_set,
    target_csv_record_identifier_list_and_set)

if not are_csvs_valid[0]:
    print(f"\033[91mThere are duplicate {are_csvs_valid[1]} in Source or Target CSV files.\033[0m Terminating program")
    sys.exit(1)

# we want to make source and target csv the same shape,
# so we can leverage numpy's performant element-wise functions and we don't have to loop
source, target, headers_not_in_source, headers_not_in_target, records_not_in_source, records_not_in_target = (
    normalize_csvs(source, target, source_csv_header_list_and_set[1],
                   target_csv_header_list_and_set[1],
                   source_csv_record_identifier_list_and_set[1],
                   target_csv_record_identifier_list_and_set[1]))

sorted_source, header_row, record_identifier_column = sort_numpy_by_record_identifier_column_and_header_row(source)
sorted_target, *_ = sort_numpy_by_record_identifier_column_and_header_row(target)

# Compare arrays element-wise
comparison = (sorted_source != sorted_target) if not is_csv_fuzzy_equals_candidate else is_not_fuzzy_equals(
    sorted_source,
    sorted_target,
    fuzzy_equals_threshold)
# Get coordinates of dissimilar elements
coordinates_where_source_is_not_equals_to_target = np.argwhere(comparison)

report_csv_numpy = process_report_csv_numpy(sorted_source,
                                            sorted_target,
                                            header_row,
                                            record_identifier_column,
                                            coordinates_where_source_is_not_equals_to_target,
                                            headers_not_in_target,
                                            headers_not_in_source,
                                            records_not_in_target,
                                            records_not_in_source
                                            )

write_numpy_to_csv_file(report_csv_numpy,
                        os.path.splitext(source_csv_file_name)[0] + os.path.splitext(target_csv_file_name)[0])

