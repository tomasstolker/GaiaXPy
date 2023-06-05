import unittest

import numpy.testing as npt
import pandas as pd
import pandas.testing as pdt

from gaiaxpy import calibrate
from gaiaxpy.core.generic_functions import str_to_array
from gaiaxpy.input_reader.input_reader import InputReader
from tests.files.paths import *
from tests.utils.utils import pos_file_to_array, missing_bp_source_id

# Load solution
solution_path = join(files_path, 'calibrator_solution')
solution_converters = dict([(column, lambda x: str_to_array(x)) for column in ['flux', 'flux_error']])
with_missing_solution_df = pd.read_csv(join(solution_path, 'with_missing_calibrator_solution.csv'),
                                       converters=solution_converters)
solution_sampling = pos_file_to_array(join(solution_path, 'with_missing_calibrator_solution_sampling.csv'))

missing_solution_df = with_missing_solution_df[with_missing_solution_df['source_id'] ==
                                               missing_bp_source_id].reset_index(drop=True)

_atol = 1e-10
_rtol = 1e-10


class TestCalibratorMissingBPFileInput(unittest.TestCase):

    def test_missing_bp_csv_file(self):
        output_df, sampling = calibrate(with_missing_bp_csv_file, save_file=False)
        pdt.assert_frame_equal(output_df, with_missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_ecsv_file(self):
        output_df, sampling = calibrate(with_missing_bp_ecsv_file, save_file=False)
        pdt.assert_frame_equal(output_df, with_missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_fits_file(self):
        output_df, sampling = calibrate(with_missing_bp_fits_file, save_file=False)
        pdt.assert_frame_equal(output_df, with_missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_xml_file(self):
        output_df, sampling = calibrate(with_missing_bp_xml_file, save_file=False)
        pdt.assert_frame_equal(output_df, with_missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_xml_plain_file(self):
        output_df, sampling = calibrate(with_missing_bp_xml_plain_file, save_file=False)
        pdt.assert_frame_equal(output_df, with_missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_csv_file_isolated(self):
        output_df, sampling = calibrate(missing_bp_csv_file, save_file=False)
        pdt.assert_frame_equal(output_df, missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_ecsv_file_isolated(self):
        output_df, sampling = calibrate(missing_bp_ecsv_file, save_file=False)
        pdt.assert_frame_equal(output_df, missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_fits_file_isolated(self):
        output_df, sampling = calibrate(missing_bp_fits_file, save_file=False)
        pdt.assert_frame_equal(output_df, missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_xml_file_isolated(self):
        output_df, sampling = calibrate(missing_bp_xml_file, save_file=False)
        pdt.assert_frame_equal(output_df, missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_xml_plain_file_isolated(self):
        output_df, sampling = calibrate(missing_bp_xml_plain_file, save_file=False)
        pdt.assert_frame_equal(output_df, missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)


class TestCalibratorMissingBPDataFrameInput(unittest.TestCase):

    def test_missing_bp_simple_dataframe(self):
        # Test dataframe containing strings instead of arrays
        df = pd.read_csv(with_missing_bp_csv_file)
        output_df, sampling = calibrate(df, save_file=False)
        pdt.assert_frame_equal(output_df, with_missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_simple_dataframe_isolated(self):
        # Test dataframe containing strings instead of arrays
        df = pd.read_csv(missing_bp_csv_file)
        output_df, sampling = calibrate(df, save_file=False)
        pdt.assert_frame_equal(output_df, missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_array_dataframe(self):
        # Convert columns in the dataframe to arrays (but not to matrices)
        array_columns = ['bp_coefficients', 'bp_coefficient_errors', 'bp_coefficient_correlations', 'rp_coefficients',
                         'rp_coefficient_errors', 'rp_coefficient_correlations']
        converters = dict([(column, lambda x: str_to_array(x)) for column in array_columns])
        df = pd.read_csv(with_missing_bp_csv_file, converters=converters)
        output_df, sampling = calibrate(df, save_file=False)
        pdt.assert_frame_equal(output_df, with_missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_array_dataframe_isolated(self):
        # Convert columns in the dataframe to arrays (but not to matrices)
        array_columns = ['bp_coefficients', 'bp_coefficient_errors', 'bp_coefficient_correlations', 'rp_coefficients',
                         'rp_coefficient_errors', 'rp_coefficient_correlations']
        converters = dict([(column, lambda x: str_to_array(x)) for column in array_columns])
        df = pd.read_csv(missing_bp_csv_file, converters=converters)
        output_df, sampling = calibrate(df, save_file=False)
        pdt.assert_frame_equal(output_df, missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_parsed_dataframe(self):
        # Test completely parsed (arrays + matrices) dataframe
        df, _ = InputReader(with_missing_bp_csv_file, calibrate).read()
        output_df, sampling = calibrate(df, save_file=False)
        pdt.assert_frame_equal(output_df, with_missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_parsed_dataframe_isolated(self):
        # Test completely parsed (arrays + matrices) dataframe
        df, _ = InputReader(missing_bp_csv_file, calibrate).read()
        output_df, sampling = calibrate(df, save_file=False)
        pdt.assert_frame_equal(output_df, missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)


class TestCalibratorMissingBPQueryInput(unittest.TestCase):

    def test_missing_bp_query(self):
        query = f"SELECT * FROM gaiadr3.gaia_source WHERE source_id IN ('5853498713190525696', " \
                f"{missing_bp_source_id}, '5762406957886626816')"
        output_df, sampling = calibrate(query, save_file=False)
        sorted_output_df = output_df.sort_values('source_id', ignore_index=True)
        sorted_solution_df = with_missing_solution_df.sort_values('source_id', ignore_index=True)
        pdt.assert_frame_equal(sorted_output_df, sorted_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_query_isolated(self):
        query = f"SELECT * FROM gaiadr3.gaia_source WHERE source_id IN ({missing_bp_source_id})"
        output_df, sampling = calibrate(query, save_file=False)
        pdt.assert_frame_equal(output_df, missing_solution_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)


class TestCalibratorMissingBPListInput(unittest.TestCase):

    def test_missing_bp_list(self):
        src_list = ['5853498713190525696', str(missing_bp_source_id), '5762406957886626816']
        output_df, sampling = calibrate(src_list, save_file=False)
        sorted_output_df = output_df.sort_values('source_id', ignore_index=True)
        sorted_solution_df = with_missing_solution_df.sort_values('source_id', ignore_index=True)
        pdt.assert_frame_equal(sorted_output_df, sorted_solution_df, check_dtype=False, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)

    def test_missing_bp_isolated(self):
        src_list = [missing_bp_source_id]
        output_df, sampling = calibrate(src_list, save_file=False)
        pdt.assert_frame_equal(output_df, missing_solution_df, check_dtype=False, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, solution_sampling)
