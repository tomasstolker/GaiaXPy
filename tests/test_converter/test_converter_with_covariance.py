import unittest
from os.path import join

import numpy.testing as npt
import pandas as pd
import pandas.testing as pdt

from gaiaxpy import convert
from gaiaxpy.core.generic_functions import str_to_array, correlation_to_covariance
from tests.files.paths import files_path
from tests.test_converter.converter_paths import mean_spectrum_csv_file_with_missing, mean_spectrum_csv_with_cov_sol_df

# Load sampling
sampling_solution = join(files_path, 'converter_solution', 'converter_with_covariance_missing_bp_solution_sampling.csv')
converters = {'pos': (lambda x: str_to_array(x))}
sampling_solution_array = pd.read_csv(sampling_solution, float_precision='high', converters=converters).iloc[0]['pos']

_atol, _rtol = 1e-10, 1e-10


class TestConverterWithCovariance(unittest.TestCase):

    def test_with_covariance(self):
        output_spectra, sampling = convert(mean_spectrum_csv_file_with_missing, with_correlation=True, save_file=False)
        output_spectra['covariance'] = output_spectra.apply(lambda row: correlation_to_covariance(
            row['correlation'], row['flux_error'], row['standard_deviation']), axis=1)
        output_spectra = output_spectra.drop(columns=['correlation', 'standard_deviation'])
        pdt.assert_frame_equal(output_spectra, mean_spectrum_csv_with_cov_sol_df, atol=_atol, rtol=_rtol)
        npt.assert_array_equal(sampling, sampling_solution_array)
