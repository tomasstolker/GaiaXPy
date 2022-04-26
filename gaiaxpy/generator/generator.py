import warnings
from .photometric_system import PhotometricSystem
from .multi_synthetic_photometry_generator import MultiSyntheticPhotometryGenerator
from gaiaxpy.core import _validate_arguments
from gaiaxpy.input_reader import InputReader
from gaiaxpy.output import PhotometryData
from gaiaxpy.colour_equation import apply_colour_equation
from gaiaxpy.error_correction import apply_error_correction

def generate(
        input_object,
        photometric_system,
        save_path='.',
        output_file='output_synthetic_photometry',
        output_format=None,
        save_file=True,
        colour_equation=False,
        error_correction=False):
    """
    Synthetic photometry utility: generates synthetic photometry in a set of
    available systems from the input internally-calibrated
    continuously-represented mean spectra.

    Args:
        input_object (object): Path to the file containing the mean spectra
             as downloaded from the archive in their continuous representation,
             a list of sources ids (string or long), or a pandas DataFrame.
        photometric_system (obj): Desired photometric system or list of photometric systems.
        save_path (str): Path where to save the output data.
        output_file (str): Name of the output file.
        output_format (str): Format to be used for the output file. If no format
                is given, then the output file will be in the same format as the
                input file.
        save_file (bool): Whether to save the output in a file. If false, output_format
            and output_file are ignored.
        with_colour_equation (bool): Whether to return the results with the colour
            equation applied or not.

        Returns:
            DataFrame: A DataFrame of all synthetic photometry results.
    """
    # TODO: merge this statement with _validate_arguments
    if photometric_system in (None, [], ''):
        raise ValueError('At least one photometric system is required as input.')
    _validate_arguments(generate.__defaults__[1], output_file, save_file)
    if isinstance(photometric_system, PhotometricSystem):
        int_photometric_system = [photometric_system].copy()
    elif isinstance(photometric_system, list):
        int_photometric_system = photometric_system.copy()
    else:
        raise ValueError('Parameter photometric_system must be either a PhotometricSystem or a list.')
    # Load data
    parsed_input_data, extension = InputReader(input_object, generate)._read()
    gaia_system = PhotometricSystem.Gaia_DR3_Vega
    # Create multi generator
    gaia_initially_in_systems = bool(gaia_system in int_photometric_system)
    if error_correction:
        if not gaia_initially_in_systems:
            int_photometric_system.append(gaia_system)
    if isinstance(int_photometric_system, list):
        generator = MultiSyntheticPhotometryGenerator(int_photometric_system, bp_model='v375wi', rp_model='v142r')
    else:
        raise ValueError('Photometry generation not implemented for the input type.')
    photometry_df = generator._generate(parsed_input_data, extension, output_file=None, output_format=None, save_file=False)
    if colour_equation:
        photometry_df = apply_colour_equation(photometry_df, photometric_system=int_photometric_system, save_file=False)
    if error_correction:
        photometry_df = apply_error_correction(photometry_df, photometric_system=photometric_system.copy(), save_file=False)
    if not gaia_initially_in_systems:
        # Remove Gaia_DR3_Vega system from the final result
        gaia_label = gaia_system.get_system_label()
        gaia_columns = [column for column in photometry_df if column.startswith(gaia_label)]
        photometry_df = photometry_df.drop(columns=gaia_columns)
    output_data = PhotometryData(photometry_df)
    output_data.save(save_file, save_path, output_file, output_format, extension)
    return photometry_df