# from typing import (
#     TYPE_CHECKING,
# )

# if TYPE_CHECKING:
#     from nomad.datamodel.datamodel import (
#         EntryArchive,
#     )
#     from structlog.stdlib import (
#         BoundLogger,
#     )

from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.metainfo import Datetime, MSection, Quantity, SchemaPackage, SubSection
from numpy import float64

configuration = config.get_plugin_entry_point(
    'nomad_dfxm_parser.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class Beam(MSection):
    extent = Quantity(
        type=float64, shape=[2], unit='mm', description='Dimension of the beam.'
    )


class Condenser(MSection):
    number = Quantity(type=int, description='Amount of lenses in the condenser.')
    radius = Quantity(
        type=float64, description='Radius of the lenses in the condenser.'
    )
    nature = Quantity(
        type=str, description='Nature of the lenses used in the condenser.'
    )


class Detector(MSection):
    magnification = Quantity(
        type=str, description='Magnification used in the detector.'
    )
    position = Quantity(
        type=str, description='Position of the detector in the experimental setup.'
    )
    nature = Quantity(type=str, description='Model of the detector used.')
    x_pixel_size = Quantity(
        type=float64, description='Horizontal dimension of the pixels of the detector.'
    )
    y_pixel_size = Quantity(
        type=float64, description='Vertical dimension of the pixels of the detector.'
    )


class Goniometer(MSection):
    chi = Quantity(type=float64, unit='deg', description='Position of the motor chi.')
    mu = Quantity(
        type=float64, shape=['*'], unit='deg', description='Position of the motor mu.'
    )
    omega = Quantity(
        type=float64, unit='deg', description='Position of the motor omega.'
    )
    phi = Quantity(
        type=float64, shape=['*'], unit='deg', description='Position of the motor phi.'
    )


class Monochromator(MSection):
    name = Quantity(type=str, description='Name of the monochromator.')
    bandwidth = Quantity(
        type=float64, unit='um', description='Spectral bandwidth of the monochromator.'
    )
    energy = Quantity(
        type=float64, unit='keV', description='Energy selected by the monochromator.'
    )
    angle = Quantity(
        type=float64, unit='deg', description='Angle of the monochromator.'
    )


class Objective(MSection):
    number = Quantity(type=int, description='Number of lenses in the objective.')
    radius = Quantity(
        type=float64, description='Radius of the lenses of the objective.'
    )
    nature = Quantity(type=str, description='Nature of the lenses of the objective.')
    pitch = Quantity(type=float64, description='Pitch of the objective.')
    yaw = Quantity(type=float64, description='Yaw of the objective.')
    position_x = Quantity(
        type=float64, description='Position along the x-axis of the objective.'
    )
    position_y = Quantity(
        type=float64, description='Position along the y-axis of the objective.'
    )
    position_z = Quantity(
        type=float64, description='Position along the z-axis of the objective.'
    )


class Device(MSection):
    name = Quantity(type=str, description='Name of the source device.')
    gap = Quantity(type=str, description='Name of the gap of the source device.')


class Source(MSection):
    name = Quantity(type=str, description='Name of the x-ray source.')
    probe = Quantity(type=str, description='Type of probe for the experiment.')
    nature = Quantity(type=str, description='Name of the x-ray source.')
    devices = SubSection(sub_section=Device.m_def, repeats=True)


class Actuator(MSection):
    name = Quantity(type=str, description='Name of the actuator.')
    nature = Quantity(
        type=str, description='Nature of the lenses connected to the actuator.'
    )
    number = Quantity(
        type=int, description='Amount of lenses connected to the actuator.'
    )
    radius = Quantity(
        type=float64,
        unit='um',
        description='Radius of the lenses connected to the actuator.',
    )


class Transfocator(MSection):
    actuators = SubSection(sub_section=Actuator.m_def, repeats=True)


class Instrument(MSection):
    name = Quantity(
        type=str, description='Name of the isntrument used for the measurement.'
    )
    citation = Quantity(
        type=str, description='Publication that describes the instrument.'
    )
    beam = SubSection(sub_section=Beam.m_def, repeats=False)
    condenser = SubSection(sub_section=Condenser.m_def, repeats=False)
    detector = SubSection(sub_section=Detector.m_def, repeats=False)
    goniometer = SubSection(sub_section=Goniometer.m_def, repeats=False)
    monochromator = SubSection(sub_section=Monochromator.m_def, repeats=False)
    objective = SubSection(sub_section=Objective.m_def, repeats=False)
    source = SubSection(sub_section=Source.m_def, repeats=False)
    transfocator = SubSection(sub_section=Transfocator.m_def, repeats=False)


class Process(MSection):
    date = Quantity(
        type=Datetime, description='Date of the processing of the raw files.'
    )
    doi_raw_data = Quantity(type=str, description='DOI of the raw data.')
    link_raw_data = Quantity(type=str, description='Link to the raw data.')
    program = Quantity(type=str, description='Programm used to process the raw files.')
    program_repo = Quantity(
        type=str, description='Online repository of the processing program.'
    )
    version = Quantity(
        type=str, description='Version of the program used to process the raw data.'
    )


class Sample(MSection):
    chemical_formula = Quantity(
        type=str, description='Chemical formula of the sample measured.'
    )
    manufacturer = Quantity(
        type=str, description='Name of the manufacturer of the sample.'
    )
    name = Quantity(type=str, description='Name of the sample.')
    mass = Quantity(type=float64, unit='kg', description="Mass of the sample.")
    space_group = Quantity(type=str, description='Space group of the crystal involved.')
    structure = Quantity(
        type=str, description='Structure of the crystal system of the sample.'
    )
    thickness = Quantity(
        type=float64, unit='um', description='Thickness of the sample.'
    )
    unit_cell_abc = Quantity(
        type=float64,
        shape=[3],
        unit='Å',
        description='Size of the unit cell of the crystal.',
    )
    unit_cell_alphabetagamma = Quantity(
        type=float64,
        shape=[3],
        unit='deg',
        description='Angles of the unit cell of the crystal.',
    )
    unit_cell_volume = Quantity(
        type=float64, unit='Å³', description='Volume of the unit cell of the crystal.'
    )


class DFXMOutput(Schema):
    definition = Quantity(
        type=str, description='Name of the pseudo NeXus application definition.'
    )
    start_time = Quantity(type=str, description='Date at the start of the acquisition.')
    end_time = Quantity(type=str, description='Date at the end of the acquisition.')
    instrument = SubSection(sub_section=Instrument.m_def, repeats=False)
    process = SubSection(sub_section=Process.m_def, repeats=False)
    sample = SubSection(sub_section=Sample.m_def, repeats=False)


m_package.__init_metainfo__()
