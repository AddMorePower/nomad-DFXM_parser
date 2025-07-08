from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

import h5py
import numpy as np

from nomad.config import config
from nomad.datamodel.results import Cell, Material, Results, Symmetry, System
from nomad.parsing.parser import MatchingParser

import nomad_dfxm_parser.schema_packages.schema_package as dfxm

configuration = config.get_plugin_entry_point(
    'nomad_dfxm_parser.parsers:parser_entry_point'
)


class NewParser(MatchingParser):
    def extract_string(self, dataset, key):
        try:
            return dataset[key][()].decode('UTF-8')
        except KeyError:
            self.logger.warning(f"Value was not found for {key}")
            pass

    def safe_extract(self, dataset, key):
        try:
            return dataset[key][()]
        except KeyError:
            self.logger.warning(f"Value was not found for {key}")
            pass

    def parse_output(self):
        self.output_data.definition = self.extract_string(self.datafile, 'definition')
        self.output_data.start_time = self.extract_string(self.datafile, 'start_time')
        self.output_data.end_time = self.extract_string(self.datafile, 'end_time')

    def parse_sample(self):
        sample = self.output_data.m_create(dfxm.Sample)
        sampleH5 = self.datafile['sample']
        sample.chemical_formula = self.extract_string(sampleH5, 'chemical_formula')
        sample.manufacturer = self.extract_string(sampleH5, 'manufacturer')
        sample.name = self.extract_string(sampleH5, 'name')
        sample.space_group = self.extract_string(sampleH5, 'space_group')
        sample.structure = self.extract_string(sampleH5, 'structure')
        sample.thickness = self.safe_extract(sampleH5, 'thickness')
        sample.unit_cell_abc = self.safe_extract(sampleH5, 'unit_cell_abc')
        sample.unit_cell_alphabetagamma = self.safe_extract(sampleH5, 'unit_cell_alphabetagamma')
        sample.unit_cell_volume = self.safe_extract(sampleH5, 'unit_cell_volume')

    def parse_process(self):
        process = self.output_data.m_create(dfxm.Process)
        processH5 = self.datafile['process']
        process.date = self.extract_string(processH5, 'date')
        process.doi_raw_data = self.extract_string(processH5, 'doi_raw_data')
        process.link_raw_data = self.extract_string(processH5, 'link_raw_data')
        process.program = self.extract_string(processH5, 'program')
        process.program_repo = self.extract_string(processH5, 'program_repo')
        process.version = self.extract_string(processH5, 'version')

    def parse_beam(self, instrument, instrumentH5):
        beam = instrument.m_create(dfxm.Beam)
        beamH5 = instrumentH5['beam']
        beam.extent = self.safe_extract(beamH5, 'extent')

    def parse_condenser(self, instrument, instrumentH5):
        condenser = instrument.m_create(dfxm.Condenser)
        condenserH5 = instrumentH5['condenser']
        condenser.nature = self.extract_string(condenserH5, 'nature')
        condenser.number = self.safe_extract(condenserH5, 'number')
        condenser.radius = self.safe_extract(condenserH5, 'radius')

    def parse_detector(self, instrument, instrumentH5):
        detector = instrument.m_create(dfxm.Detector)
        detectorH5 = instrumentH5['detector']
        detector.magnification = self.extract_string(detectorH5, 'magnification')
        detector.nature = self.extract_string(detectorH5, 'nature')
        detector.position = self.extract_string(detectorH5, 'position')
        detector.x_pixel_size = self.safe_extract(detectorH5, 'x_pixel_size')
        detector.y_pixel_size = self.safe_extract(detectorH5, 'y_pixel_size')

    def parse_goniometer(self, instrument, instrumentH5):
        goniometer = instrument.m_create(dfxm.Goniometer)
        goniometerH5 = instrumentH5['goniometer']
        goniometer.chi = self.safe_extract(goniometerH5, 'chi')
        goniometer.mu = self.safe_extract(goniometerH5, 'mu')
        goniometer.omega = self.safe_extract(goniometerH5, 'omega')
        goniometer.phi = self.safe_extract(goniometerH5, 'phi')

    def parse_monochromator(self, instrument, instrumentH5):
        monochromator = instrument.m_create(dfxm.Monochromator)
        monochromatorH5 = instrumentH5['monochromator']
        monochromator.bandwidth = self.safe_extract(monochromatorH5, 'bandwidth')
        monochromator.energy = self.safe_extract(monochromatorH5, 'energy')
        monochromator.angle = self.safe_extract(monochromatorH5, 'angle')
        monochromator.name = self.extract_string(monochromatorH5, 'name')

    def parse_objective(self, instrument, instrumentH5):
        objective = instrument.m_create(dfxm.Objective)
        objectiveH5 = instrumentH5['objective']
        objective.nature = self.extract_string(objectiveH5, 'nature')
        objective.number = self.safe_extract(objectiveH5, 'number')
        objective.pitch = self.safe_extract(objectiveH5, 'pitch')
        objective.position_x = self.safe_extract(objectiveH5, 'position_x')
        objective.position_y = self.safe_extract(objectiveH5, 'position_y')
        objective.position_z = self.safe_extract(objectiveH5, 'position_z')
        objective.radius = self.safe_extract(objectiveH5, 'radius')
        objective.yaw = self.safe_extract(objectiveH5, 'yaw')

    def parse_devices(self, source, sourceH5):
        devicesH5 = sourceH5['devices']
        for deviceH5 in devicesH5.values():
            device = source.m_create(dfxm.Device)
            device.gap = self.extract_string(deviceH5, 'gap')
            device.name = self.extract_string(deviceH5, 'name')

    def parse_source(self, instrument, instrumentH5):
        source = instrument.m_create(dfxm.Source)
        sourceH5 = instrumentH5['source']
        source.name = self.extract_string(sourceH5, 'name')
        source.nature = self.extract_string(sourceH5, 'nature')
        source.probe = self.extract_string(sourceH5, 'probe')
        self.parse_devices(source, sourceH5)

    def parse_transfocator(self, instrument, instrumentH5):
        transfocator = instrument.m_create(dfxm.Transfocator)
        transfocatorH5 = instrumentH5['transfocator']
        actuatorsH5 = transfocatorH5['actuators']
        for actuatorH5 in actuatorsH5.values():
            actuator = transfocator.m_create(dfxm.Actuator)
            actuator.nature = self.extract_string(actuatorH5, 'nature')
            actuator.number = self.safe_extract(actuatorH5, 'number')
            actuator.radius = self.safe_extract(actuatorH5, 'radius')

    def parse_instrument(self):
        instrument = self.output_data.m_create(dfxm.Instrument)
        instrumentH5 = self.datafile['instrument']
        instrument.citation = self.extract_string(instrumentH5, 'citation')
        instrument.name = self.extract_string(instrumentH5, 'name')
        self.parse_beam(instrument, instrumentH5)
        self.parse_condenser(instrument, instrumentH5)
        self.parse_detector(instrument, instrumentH5)
        self.parse_goniometer(instrument, instrumentH5)
        self.parse_monochromator(instrument, instrumentH5)
        self.parse_objective(instrument, instrumentH5)
        self.parse_source(instrument, instrumentH5)
        self.parse_transfocator(instrument, instrumentH5)

    def store_results(self):
        sampleH5 = self.datafile['sample']

        cell = Cell()
        cell.a, cell.b, cell.c = sampleH5['unit_cell_abc']
        cell.alpha, cell.beta, cell.gamma = sampleH5['unit_cell_alphabetagamma']
        cell.volume = self.safe_extract(sampleH5, 'unit_cell_volume')

        topology = System()
        topology.cell = cell

        symmetry = Symmetry()
        symmetry.space_group_symbol = self.extract_string(sampleH5, 'space_group')

        material = Material()
        material.elements = [self.extract_string(sampleH5, 'chemical_formula')]
        material.symmetry = symmetry
        material.topology.append(topology)
        results = Results()
        results.material = material
        return results


    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        self.mainfile = mainfile
        self.archive = archive
        self.logger = logging.getLogger(__name__) if logger is None else logger

        self.output_data = dfxm.DFXMOutput()
        archive.data = self.output_data

        try:
            self.datah5 = h5py.File(self.mainfile)
        except Exception as err:
            self.logger.error(f'Error opening h5 file.\n{err}')
            return

        self.datafile = self.datah5['entry']

        self.parse_output()
        self.parse_instrument()
        self.parse_process()
        self.parse_sample()
        results = self.store_results()
        archive.results = results