from pyedb.grpc.edb_core.edb_data.terminals import BundleTerminal
from pyedb.grpc.edb_core.edb_data.terminals import EdgeTerminal
from pyedb.grpc.edb_core.edb_data.terminals import PadstackInstanceTerminal
from pyedb.grpc.edb_core.edb_data.terminals import Terminal
from ansys.edb.utility.value import Value


class GapPort(EdgeTerminal):
    """Manages gap port properties.

    Parameters
    ----------
    pedb : pyaedt.edb.Edb
        EDB object from the ``Edblib`` library.
    edb_object : Ansys.Ansoft.Edb.Cell.Terminal.EdgeTerminal
        Edge terminal instance from EDB.

    Examples
    --------
    This example shows how to access the ``GapPort`` class.
    >>> from pyedb import Edb
    >>> edb = Edb("myaedb.aedb")
    >>> gap_port = edb.ports["gap_port"]
    """

    def __init__(self, pedb, edb_object):
        super().__init__(pedb, edb_object)

    @property
    def magnitude(self):
        """Magnitude."""
        return self._edb_object.source_amplitude.value

    @property
    def phase(self):
        """Phase."""
        return self._edb_object.source_phase.value

    @property
    def renormalize(self):
        """Whether renormalize is active."""
        return self._edb_object.port_post_processing_prop.do_renormalize

    @property
    def deembed(self):
        """Inductance value of the deembed gap port."""
        return self._edb_object.port_post_processing_prop.do_deembed_gap_l

    @property
    def renormalize_z0(self):
        """Renormalize Z0 value (real, imag)."""
        return (
            self._edb_object.port_post_processing_prop.renormalizion_z0.complex[0],
            self._edb_object.port_post_processing_prop.renormalizion_z0.complex[1],
        )


class WavePort(EdgeTerminal):
    """Manages wave port properties.

    Parameters
    ----------
    pedb : pyaedt.edb.Edb
        EDB object from the ``Edblib`` library.
    edb_object : Ansys.Ansoft.Edb.Cell.Terminal.EdgeTerminal
        Edge terminal instance from EDB.

    Examples
    --------
    This example shows how to access the ``WavePort`` class.

    >>> from pyedb import Edb
    >>> edb = Edb("myaedb.aedb")
    >>> exc = edb.ports
    """

    def __init__(self, pedb, edb_terminal):
        super().__init__(pedb, edb_terminal)

    @property
    def horizontal_extent_factor(self):
        """Horizontal extent factor."""
        return self._hfss_port_property["Horizontal Extent Factor"]

    @horizontal_extent_factor.setter
    def horizontal_extent_factor(self, value):
        p = self._hfss_port_property
        p["Horizontal Extent Factor"] = value
        self._hfss_port_property = p

    @property
    def vertical_extent_factor(self):
        """Vertical extent factor."""
        return self._hfss_port_property["Vertical Extent Factor"]

    @vertical_extent_factor.setter
    def vertical_extent_factor(self, value):
        p = self._hfss_port_property
        p["Vertical Extent Factor"] = value
        self._hfss_port_property = p

    @property
    def pec_launch_width(self):
        """Launch width for the printed electronic component (PEC)."""
        return self._hfss_port_property["PEC Launch Width"]

    @pec_launch_width.setter
    def pec_launch_width(self, value):
        p = self._hfss_port_property
        p["PEC Launch Width"] = value
        self._hfss_port_property = p

    @property
    def deembed(self):
        """Whether deembed is active."""
        return self._edb_object.port_post_processing_prop.do_deembed

    @deembed.setter
    def deembed(self, value):
        p = self._edb_object.port_post_processing_prop
        p.do_deembed = value
        self._edb_object.port_post_processing_prop = p

    @property
    def deembed_length(self):
        """Deembed Length."""
        return self._edb_object.port_post_processing_prop.deembed_length.value

    @deembed_length.setter
    def deembed_length(self, value):
        p = self._edb_object.port_post_processing_prop
        p.deembed_length = Value(value)
        self._edb_object.port_post_processing_prop = p


class ExcitationSources(Terminal):
    """Manage sources properties.

    Parameters
    ----------
    pedb : pyaedt.edb.Edb
        Edb object from Edblib.
    edb_terminal : Ansys.Ansoft.Edb.Cell.Terminal.EdgeTerminal
        Edge terminal instance from Edb.



    Examples
    --------
    This example shows how to access this class.
    >>> from pyedb import Edb
    >>> edb = Edb("myaedb.aedb")
    >>> all_sources = edb.sources
    >>> print(all_sources["VSource1"].name)

    """

    def __init__(self, pedb, edb_terminal):
        Terminal.__init__(self, pedb, edb_terminal)

    @property
    def magnitude(self):
        """Get the magnitude of the source."""
        return self._edb_object.source_amplitude.value

    @magnitude.setter
    def magnitude(self, value):
        self._edb_object.source_amplitude = Value(value)

    @property
    def phase(self):
        """Get the phase of the source."""
        return self._edb_object.source_phase.value

    @phase.setter
    def phase(self, value):
        self._edb_object.source_phase = Value(value)


class ExcitationProbes(Terminal):
    """Manage probes properties.

    Parameters
    ----------
    pedb : pyaedt.edb.Edb
        Edb object from Edblib.
    edb_terminal : Ansys.Ansoft.Edb.Cell.Terminal.EdgeTerminal
        Edge terminal instance from Edb.


    Examples
    --------
    This example shows how to access this class.
    >>> from pyedb import Edb
    >>> edb = Edb("myaedb.aedb")
    >>> probes = edb.probes
    >>> print(probes["Probe1"].name)
    """

    def __init__(self, pedb, edb_terminal):
        Terminal.__init__(self, pedb, edb_terminal)


class BundleWavePort(BundleTerminal):
    """Manages bundle wave port properties.

    Parameters
    ----------
    pedb : pyaedt.edb.Edb
        EDB object from the ``Edblib`` library.
    edb_object : Ansys.Ansoft.Edb.Cell.Terminal.BundleTerminal
        BundleTerminal instance from EDB.

    """

    def __init__(self, pedb, edb_object):
        super().__init__(pedb, edb_object)

    @property
    def _wave_port(self):
        return WavePort(self._pedb, self.terminals[0]._edb_object)

    @property
    def horizontal_extent_factor(self):
        """Horizontal extent factor."""
        return self._wave_port.horizontal_extent_factor

    @horizontal_extent_factor.setter
    def horizontal_extent_factor(self, value):
        self._wave_port.horizontal_extent_factor = value

    @property
    def vertical_extent_factor(self):
        """Vertical extent factor."""
        return self._wave_port.vertical_extent_factor

    @vertical_extent_factor.setter
    def vertical_extent_factor(self, value):
        self._wave_port.vertical_extent_factor = value

    @property
    def pec_launch_width(self):
        """Launch width for the printed electronic component (PEC)."""
        return self._wave_port.pec_launch_width

    @pec_launch_width.setter
    def pec_launch_width(self, value):
        self._wave_port.pec_launch_width = value

    @property
    def deembed(self):
        """Whether deembed is active."""
        return self._wave_port.deembed

    @deembed.setter
    def deembed(self, value):
        self._wave_port.deembed = value

    @property
    def deembed_length(self):
        """Deembed Length."""
        return self._wave_port.deembed_length

    @deembed_length.setter
    def deembed_length(self, value):
        self._wave_port.deembed_length = value


class CoaxPort(PadstackInstanceTerminal):
    """Manages bundle wave port properties.

    Parameters
    ----------
    pedb : pyedb.edb.Edb
        EDB object from the ``Edblib`` library.
    edb_object : Ansys.Ansoft.Edb.Cell.Terminal.PadstackInstanceTerminal
        PadstackInstanceTerminal instance from EDB.

    """

    def __init__(self, pedb, edb_object):
        super().__init__(pedb, edb_object)

    @property
    def radial_extent_factor(self):
        """Radial extent factor."""
        return self._hfss_port_property["Radial Extent Factor"]

    @radial_extent_factor.setter
    def radial_extent_factor(self, value):
        p = self._hfss_port_property
        p["Radial Extent Factor"] = value
        self._hfss_port_property = p