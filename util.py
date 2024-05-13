import numpy as np


def validate_there_are_no_duplicate_records_or_headers_in_csv(source_csv_header_list_and_set: tuple[list, set],
                                                              target_csv_header_list_and_set: tuple[list, set],
                                                              source_csv_record_identifier_list_and_set: tuple[
                                                                  list, set],
                                                              target_csv_record_identifier_list_and_set: tuple[
                                                                  list, set]
                                                              ) -> tuple[bool, str]:
    source_csv_header_list, source_csv_header_set = source_csv_header_list_and_set

    target_csv_header_list, target_csv_header_set = target_csv_header_list_and_set

    has_duplicate_headers = False

    # this implementation does not support duplicate headers, if the length of the set != length of the
    # original array then there is a duplication
    if len(source_csv_header_set) != len(source_csv_header_list) or len(target_csv_header_set) != len(
            target_csv_header_list):
        has_duplicate_headers = True

    source_csv_row_identifier_list, source_csv_row_identifier_set = source_csv_record_identifier_list_and_set

    target_csv_row_identifier_list, target_csv_row_identifier_set = target_csv_record_identifier_list_and_set

    if len(source_csv_row_identifier_set) != len(source_csv_row_identifier_list) or len(
            target_csv_row_identifier_set) != len(target_csv_row_identifier_list):
        return (False, "Records and Headers") if has_duplicate_headers else (False, "Headers")

    return True, ""


def get_headers(csv_numpy) -> tuple[list, set]:
    """get the first row of the 2d numpy, that would be the headers"""
    csv_headers_set = set(csv_numpy[0])
    return csv_numpy[0], csv_headers_set


def get_row_identifiers(csv_numpy) -> tuple[list, set]:
    """to get each row identifier, the identifier would be on the fist column of the csv
    #the slicing would return a 2d array which we would flatten to a 1d array to get the array of the exact values"""
    row_identifier_list = csv_numpy[:, 0:1].flatten()
    row_identifier_set = set(row_identifier_list)
    return row_identifier_list, row_identifier_set


def sort_numpy_by_record_identifier_column_and_header_row(numpy_array: np) -> tuple[np, np, np]:
    # let slice off the header row and identifier column,
    # we would need this slice to get the header
    # and row identifier of dissimilar record later in the program

    header_row = numpy_array[0, 1:]
    record_identifier_column = numpy_array[1:, 0]

    sorted_record_identifier_column_index = np.argsort(record_identifier_column)
    sorted_header_row_index = np.argsort(header_row)

    # sort header row and record identifier column
    header_row = header_row[sorted_header_row_index]
    record_identifier_column = record_identifier_column[sorted_record_identifier_column_index]

    # we want sort array without headers and record identifier slice
    numpy_array = numpy_array[1:, 1:]

    # this would sort the numpy rows using the order of the record identifier field
    numpy_array = numpy_array[sorted_record_identifier_column_index]
    # this would sort the numpy columns using the order of the header row
    numpy_array = numpy_array[:, sorted_header_row_index]

    # # this would return the indexes of the sorted column
    # sorted_first_column_index = np.argsort(numpy_array[:, 0])
    # numpy_array = numpy_array[sorted_first_column_index]
    #
    # sorted_first_row_index = np.argsort(numpy_array[0])
    # numpy_array = numpy_array[:, sorted_first_row_index]

    return numpy_array, header_row, record_identifier_column


def are_all_csv_numpy_elements_numeric(numpy_array: np) -> bool:
    try:
        # ignore first row and column, because that is header row and record identifier column
        numpy_array[1:, 1:].astype(float)
        return True
    except ValueError:
        print("There are non-numeric values in source or target CSV, so CSV is NOT a candidate for Fuzzy Equals")
        return False


def read_float_from_user(prompt="Enter an Float: "):
    try:
        user_input = input(prompt)
        integer_value = float(user_input)
        return integer_value
    except ValueError:
        print("Invalid input. Please enter an Float.\n")
        read_float_from_user(prompt)


def is_not_fuzzy_equals(source, target, threshold):
    """
    Calculate fuzzy equality between two NumPy arrays.

    Parameters:
    - source: source csv NumPy array.
    - target: target csv NumPy array.
    - threshold: Threshold for fuzzy equality comparison.

    Returns:
    - Boolean NumPy array indicating fuzzy inequality.
    """
    source = source.astype(float)
    target = target.astype(float)
    source_element_that_are_nan = np.isnan(source)
    target_element_that_are_nan = np.isnan(target)
    absolute_difference = np.abs(source - target)
    # we want to return true for values in the numpy that are nan,
    # the absolute_difference > threshold line would be false on nan > x comparisons,
    # and I need it to be true, so the nan column can be recorded in the reports,
    # so I use boolean numpy to get true on elements that are nan in source or target,
    # and then use the logical_or to make the results of nan columns or rows to be true in reports
    return np.logical_or(absolute_difference > threshold, source_element_that_are_nan, target_element_that_are_nan)
