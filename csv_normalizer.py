import numpy as np


def normalize_csvs(source: np, target: np, source_csv_header: set, target_csv_header: set,
                   source_csv_record_identifier: set, target_csv_record_identifier: set) -> tuple[
    np, np, set, set, set, set]:
    """
     Normalize two CSV arrays by ensuring they have consistent headers and row identifiers.

     This function takes two CSV arrays as input along with their corresponding sets of headers and record identifiers.
     It ensures that both arrays have the same headers and row identifiers by adding missing headers/identifiers and
     filling in missing records.

     Parameters:
     - source: np.ndarray: The source CSV array.
     - target: np.ndarray: The target CSV array.
     - source_csv_header: set: Set of headers in the source CSV array.
     - target_csv_header: set: Set of headers in the target CSV array.
     - source_csv_record_identifier: set: Set of row identifiers in the source CSV array.
     - target_csv_record_identifier: set: Set of row identifiers in the target CSV array.
     """

    # get headers in source set but not in target
    headers_not_in_target = source_csv_header.difference(target_csv_header)
    headers_not_in_source = target_csv_header.difference(source_csv_header)
    # we want to get the number of rows in source, so
    # we know the dimension of the source set(n) so
    # we know the dimensions n X 1 column
    # we are adding to the source array
    number_of_rows_in_source = source.shape[0]
    # no point putting this in the loop because its always going to be the same
    # we are using np.nan to fill up the column that is in source but not in
    # because it is not equal to anything, you would see why then we compare the numpys
    missing_header_column_values = np.full((number_of_rows_in_source, 1), np.nan, dtype=object)
    for header in headers_not_in_source:
        # we counted the header value when creating the
        # missing_header_column_values, so we want to replace the nan in that column with the header
        missing_header_column_values.put((0, 0), header)
        source = np.hstack((source, missing_header_column_values))
    # it is possible there is a row mismatch between the number of rows in
    # source and target because we have not regularized the rows yet
    number_of_rows_in_target = target.shape[0]
    missing_header_column_values = np.full((number_of_rows_in_target, 1), np.nan, dtype=object)
    for header in headers_not_in_target:
        # we counted the header value when creating the
        # missing_header_column_values, so we want to replace the nan in that column with the header
        missing_header_column_values.put((0, 0), header)
        target = np.hstack((target, missing_header_column_values))

    records_not_in_source = target_csv_record_identifier.difference(source_csv_record_identifier)
    records_not_in_target = source_csv_record_identifier.difference(target_csv_record_identifier)

    number_of_columns_in_source = source.shape[1]

    missing_record_row_values = np.full((1, number_of_columns_in_source), np.nan, dtype=object)

    for record in records_not_in_source:
        missing_record_row_values.put((0, 0), record)
        source = np.vstack((source, missing_record_row_values))

    for record in records_not_in_target:
        missing_record_row_values.put((0, 0), record)
        target = np.vstack((target, missing_record_row_values))

    return source, target, headers_not_in_source, headers_not_in_target, records_not_in_source, records_not_in_target
