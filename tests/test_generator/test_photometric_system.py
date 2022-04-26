import unittest
import numpy as np
import numpy.testing as npt
import pandas as pd
from configparser import ConfigParser
from numpy import ndarray
from os import path
from gaiaxpy.generator import PhotometricSystem
from gaiaxpy.config import config_path
from tests.files import files_path

def get_system_by_name(lst, name):
    return [item[1] for item in lst if item[0] == name][0]

# Photometric systems specifications to compare with objects generated by the package 'converters' is used to parse bands and zero_points
phot_systems_specs = pd.read_csv(path.join(files_path, 'PhotometricSystemSpecs.csv'), \
                                           converters={'bands': lambda x: x[1:-1].split(','), \
                                           'zero_points': lambda y: np.array(y[1:-1].split(',')).astype(float)}, \
                                           float_precision='round_trip')
available_systems = list(phot_systems_specs['name'])


class TestPhotometricSystem(unittest.TestCase):

    def setUp(self):
        self.phot_system_names = [phot_system.name for phot_system in PhotometricSystem]
        self.phot_systems = [(name, PhotometricSystem[name]) for name in self.phot_system_names]

    def test_init(self):
        for name, phot_system in self.phot_systems:
            self.assertIsInstance(phot_system, PhotometricSystem)

    def test_get_system_label(self):
        for name in available_systems:
            # Photometric systems created by the package
            system = get_system_by_name(self.phot_systems, name)
            system_label = system.get_system_label()
            test_label = phot_systems_specs.loc[phot_systems_specs['name'] == name]['label'].iloc[0]
            self.assertIsInstance(system_label, str)
            self.assertEqual(system_label, test_label)

    def test_bands(self):
        for name in available_systems:
            # Photometric systems created by the package
            system = get_system_by_name(self.phot_systems, name)
            test_bands = phot_systems_specs.loc[phot_systems_specs['name'] == name]['bands'].iloc[0]
            system_bands = system.get_bands()
            self.assertIsInstance(system_bands, list)
            self.assertEqual(system_bands, test_bands)

    def test_get_set_zero_points(self):
        for name in available_systems:
            # Photometric systems created by the package
            system = get_system_by_name(self.phot_systems, name)
            test_zero_points = phot_systems_specs.loc[phot_systems_specs['name'] == name]['zero_points'].iloc[0]
            system_zero_points = system.get_zero_points()
            self.assertIsInstance(system_zero_points, ndarray)
            npt.assert_array_equal(system_zero_points, test_zero_points)

    def tearDown(self):
        del self.phot_system_names
        del self.phot_systems