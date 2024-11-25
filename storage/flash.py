from enum import Enum

BITS_PER_B = 8
HZ_PER_MHZ = 1000 * 1000
BYTES_PER_MB = 1024 * 1024


class OpType(Enum):
    """
    Defines the types of flash operations
    """

    READ = 0
    WRITE = 1
    ERASE = 2


class Mode(Enum):
    """
    Defines the mode of operation
    """

    MIN = 0
    TYP = 1
    MAX = 2


class Flash:

    def __init__(
        self,
        name: str,
        channel_is_ddr: bool,
        channel_frequency_mhz: int,
        channel_width_bits: int,
        nvsim: bool,
        synchronous: bool,
        channels_per_nvm: int,
        chips_per_channel: int,
        dies_per_chip: int,
        planes_per_die: int,
        blocks_per_plane: int,
        pages_per_block: int,
        page_size_b: int,
        **kwargs,
    ):
        self.name: str = name
        self.channel_is_ddr = channel_is_ddr
        self.channel_frequency_mhz = channel_frequency_mhz
        self.channel_width_bits = channel_width_bits

        self.nvsim: bool = nvsim
        self.synchronous: bool = synchronous

        self.channels_per_nvm = channels_per_nvm
        self.chips_per_channel = chips_per_channel
        self.dies_per_chip = dies_per_chip
        self.planes_per_die = planes_per_die
        self.blocks_per_plane = blocks_per_plane
        self.pages_per_block = pages_per_block

        self.planes_per_chip = self.planes_per_die * self.dies_per_chip
        self.planes_per_channel = self.planes_per_chip * self.chips_per_channel
        self.chips_per_nvm = self.chips_per_channel * self.channels_per_nvm

        self.page_size_b = page_size_b
        self.page_size_mb = self.page_size_b / BYTES_PER_MB
        self.block_size_b = self.page_size_b * self.pages_per_block
        self.plane_size_b = self.block_size_b * self.blocks_per_plane
        self.die_size_b = self.plane_size_b * self.planes_per_die
        self.chip_size_b = self.die_size_b * self.dies_per_chip
        self.nvm_size_b = (self.chip_size_b * self.chips_per_channel *
                           self.channels_per_nvm)

        self.context = kwargs

        self.mode: Mode = Mode.TYP  # Default Mode

    def set_mode(self, mode: Mode):
        self.mode = mode

    def get_mode_name(self):
        match self.mode:
            case Mode.MIN:
                return "min"
            case Mode.TYP:
                return "typ"
            case Mode.MAX:
                return "max"

    def get_next_mode(self, mode: Mode):
        match mode:
            case Mode.MIN:
                return "typ"
            case Mode.TYP:
                return "max"
            case Mode.MAX:
                assert False

    def get_context(self, key: str):
        if self.nvsim:
            new_key = key
        else:
            new_key = key + "_" + self.get_mode_name()
            if new_key not in self.context:
                new_key = key + "_" + self.get_next_mode(self.mode)
                if new_key not in self.context:
                    new_key = (
                        key + "_" +
                        self.get_next_mode(self.get_next_mode(self.mode)))
                    if new_key not in self.context:
                        print("Key does not exist!", new_key)
                        assert False
        return self.context[new_key]

    # Plane Bandwidth
    def plane_bandwidth_bits_s(self, op: OpType):
        if op == OpType.ERASE:
            return 1 / self.plane_op_latency_s(
                op) * self.block_size_b * BITS_PER_B
        return 1 / self.plane_op_latency_s(op) * self.page_size_b * BITS_PER_B

    def plane_bandwidth_b_s(self, op: OpType):
        return self.plane_bandwidth_bits_s(op) / BITS_PER_B

    def plane_bandwidth_pages_s(self, op: OpType):
        return self.plane_bandwidth_b_s(op) / self.page_size_b

    def plane_bandwidth_mb_s(self, op: OpType):
        return self.plane_bandwidth_b_s(op) / BYTES_PER_MB

    # Plane Latency
    def plane_op_latency_ms(self, op: OpType):
        match op:
            case OpType.READ:
                return self.get_context("page_read_latency_ms")
            case OpType.WRITE:
                return self.get_context("page_write_latency_ms")
            case OpType.ERASE:
                return self.get_context("block_erase_latency_ms")
        assert False

    def plane_op_latency_s(self, op: OpType):
        return self.plane_op_latency_ms(op) / 1000

    def plane_page_latency_s(self, op: OpType):
        return 1 / self.plane_bandwidth_pages_s(op)

    def plane_page_latency_ms(self, op: OpType):
        return 1000 / self.plane_bandwidth_pages_s(op)

    def plane_byte_latency_s(self, op: OpType):
        return 1 / self.plane_bandwidth_b_s(op)

    def plane_byte_latency_ms(self, op: OpType):
        return 1000 / self.plane_bandwidth_b_s(op)

    # Plane Energy
    def plane_op_energy_j(self, op: OpType):
        match op:
            case OpType.READ:
                return self.get_context("page_read_energy_nj") / 1e9
            case OpType.WRITE:
                return self.get_context("page_write_energy_nj") / 1e9
            case OpType.ERASE:
                return self.get_context("block_erase_energy_nj") / 1e9
        assert False

    # Chip Power
    def chip_supply_voltage_v(self):
        return self.get_context("vdd_v")

    def chip_op_power_w(self, op: OpType):
        """
        Assumes a single die is operational and the other dies are idle
        """
        return (self.die_io_idle_power_w() + self.die_array_op_power_w(op) +
                (self.dies_per_chip - 1) *
                (self.die_io_idle_power_w() + self.die_array_idle_power_w()))

    def chip_io_power_w(self):
        """
        Assumes a single die is performing I/O and the other dies are idle
        """
        return (self.die_array_idle_power_w() + self.die_io_burst_power_w() +
                (self.dies_per_chip - 1) *
                (self.die_io_idle_power_w() + self.die_array_idle_power_w()))

    def chip_idle_power_w(self):
        return (self.die_io_idle_power_w() +
                self.die_array_idle_power_w()) * self.dies_per_chip

    def chip_standby_power_w(self):
        """
        Adds up the standby power (from both supply voltages) for all dies in a chip
        """
        return (self.die_io_standby_power_w() +
                self.die_array_standby_power_w()) * self.dies_per_chip

    def chip_leakage_power_w(self):
        """
        Adds up the leakage power (from both supply voltages) for all dies in a chip
        """
        return (self.die_io_leakage_power_w() +
                self.die_array_leakage_power_w()) * self.dies_per_chip

    # Die Power
    def die_array_op_current_a(self, op: OpType):
        match op:
            case OpType.READ:
                return self.get_context("die_array_read_current_ma") / 1000
            case OpType.WRITE:
                return self.get_context("die_array_write_current_ma") / 1000
            case OpType.ERASE:
                return self.get_context("die_array_erase_current_ma") / 1000
        assert False

    def die_array_op_power_w(self, op: OpType):
        if self.nvsim:
            return self.plane_op_energy_j(op) / self.plane_op_latency_s(op)
        vdd_v = self.chip_supply_voltage_v()
        return self.die_array_op_current_a(op) * vdd_v

    def die_array_idle_current_a(self):
        return self.get_context("die_array_idle_current_ma") / 1000

    def die_array_idle_power_w(self):
        if self.nvsim:
            return 0
        vdd_v = self.chip_supply_voltage_v()
        return self.die_array_idle_current_a() * vdd_v

    def die_array_standby_current_a(self):
        return self.get_context("die_array_standby_current_ma") / 1000

    def die_array_standby_power_w(self):
        if self.nvsim:
            return 0
        vdd_v = self.chip_supply_voltage_v()
        return self.die_array_standby_current_a() * vdd_v

    def die_array_leakage_current_a(self):
        return self.get_context("die_array_leakage_current_ma") / 1000

    def die_array_leakage_power_w(self):
        if self.nvsim:
            return self.get_context("leakage_power_mw") / 1000
        vdd_v = self.chip_supply_voltage_v()
        return self.die_array_leakage_current_a() * vdd_v

    def die_io_burst_current_a(self):
        return self.get_context("die_io_burst_current_ma") / 1000

    def die_io_burst_power_w(self):
        if self.nvsim:
            return self.get_context("die_io_power_ratio_to_read"
                                    ) * self.die_array_op_power_w(OpType.READ)
        vdd_io_v = self.channel_supply_voltage_v()
        return self.die_io_burst_current_a() * vdd_io_v

    def die_io_idle_current_a(self):
        return self.get_context("die_io_idle_current_ma") / 1000

    def die_io_idle_power_w(self):
        if self.nvsim:
            return 0
        vdd_io_v = self.channel_supply_voltage_v()
        return self.die_io_idle_current_a() * vdd_io_v

    def die_io_standby_current_a(self):
        return self.get_context("die_io_standby_current_ma") / 1000

    def die_io_standby_power_w(self):
        if self.nvsim:
            return 0
        vdd_io_v = self.channel_supply_voltage_v()
        return self.die_io_standby_current_a() * vdd_io_v

    def die_io_leakage_current_a(self):
        return self.get_context("die_io_leakage_current_ma") / 1000

    def die_io_leakage_power_w(self):
        if self.nvsim:
            return 0
        vdd_io_v = self.channel_supply_voltage_v()
        return self.die_io_leakage_current_a() * vdd_io_v

    # Channel Bandwidth
    def channel_bandwidth_bits_s(self):
        if self.channel_is_ddr:
            return (2 * (self.channel_frequency_mhz * HZ_PER_MHZ) *
                    self.channel_width_bits)
        return (self.channel_frequency_mhz *
                HZ_PER_MHZ) * self.channel_width_bits

    def channel_bandwidth_b_s(self):
        return self.channel_bandwidth_bits_s() / BITS_PER_B

    def channel_bandwidth_pages_s(self):
        return self.channel_bandwidth_b_s() / self.page_size_b

    def channel_bandwidth_mb_s(self):
        return self.channel_bandwidth_b_s() / BYTES_PER_MB

    # Channel Latency
    def channel_byte_latency_s(self):
        return 1 / self.channel_bandwidth_b_s()

    def channel_byte_latency_ms(self):
        return 1000 / self.channel_bandwidth_b_s()

    def channel_page_latency_s(self):
        return 1 / self.channel_bandwidth_pages_s()

    def channel_page_latency_ms(self):
        return 1000 / self.channel_bandwidth_pages_s()

    # Channel Power
    def channel_supply_voltage_v(self):
        return self.get_context("vdd_io_v")

    # Total Latency
    def total_op_latency_s(self, op: OpType, parallel: bool = False):
        """
        If parallel=True, assumes using all planes in a single chip.
        """
        if op == OpType.ERASE:
            return self.plane_op_latency_s(op)

        if parallel:
            return (self.plane_page_latency_s(op) +
                    self.channel_page_latency_s() * self.planes_per_channel)
        return self.plane_page_latency_s(op) + self.channel_page_latency_s()

    def total_op_latency_ms(self, op: OpType, parallel: bool = False):
        return self.total_op_latency_s(op, parallel) * 1000

    def total_schedule_latency_s(self,
                                 num_reads: int,
                                 num_writes: int,
                                 parallel: bool = False):
        total_read_latency_s = self.total_op_latency_s(OpType.READ, parallel)
        total_write_latency_s = self.total_op_latency_s(OpType.WRITE, parallel)
        return total_read_latency_s * num_reads + total_write_latency_s * num_writes

    # Total Bandwidth
    def total_op_s(self, op: OpType, parallel: bool = False):
        """
        Total number of read + transfer or write + transfer operations per second
        """
        return 1 / self.total_op_latency_s(op, parallel)

    def total_op_bandwidth_mb_s(self, op: OpType, parallel: bool = False):
        if op == OpType.ERASE:  # TODO
            assert False
        if parallel:
            return (self.total_op_s(op, parallel) * self.page_size_mb *
                    self.planes_per_channel)
        return self.total_op_s(op, parallel) * self.page_size_mb

    # Total Power
    def total_op_power_page_w(self, op: OpType, full_chip: bool = True):
        """
        Includes operation and I/O (if applicable)
        Assumes I/O is for a full page
        """
        if full_chip:
            io_energy_j = self.chip_io_power_w() * self.channel_page_latency_s(
            )
            op_energy_j = self.chip_op_power_w(op) * self.plane_op_latency_s(
                op)
        else:
            io_energy_j = self.die_io_burst_power_w(
            ) * self.channel_page_latency_s()
            op_energy_j = self.die_array_op_power_w(
                op) * self.plane_op_latency_s(op)

        total_latency_s = self.channel_page_latency_s(
        ) + self.plane_op_latency_s(op)
        return (io_energy_j + op_energy_j) / total_latency_s

    def total_op_power_bytes_w(self,
                               op: OpType,
                               bytes_transferred: int,
                               full_chip: bool = True):
        if full_chip:
            io_energy_j = (self.chip_io_power_w() *
                           self.channel_byte_latency_s() * bytes_transferred)
            op_energy_j = self.chip_op_power_w(op) * self.plane_op_latency_s(
                op)
        else:
            io_energy_j = (self.die_io_burst_power_w() *
                           self.channel_byte_latency_s() * bytes_transferred)
            op_energy_j = self.die_array_op_power_w(
                op) * self.plane_op_latency_s(op)

        total_latency_s = (self.channel_byte_latency_s() * bytes_transferred +
                           self.plane_op_latency_s(op))
        return (io_energy_j + op_energy_j) / total_latency_s

    def total_standby_power_w(self):
        """
        Assumes a single chip is active
        """
        return self.chip_standby_power_w() * (self.chips_per_nvm - 1)

    def total_leakage_power_w(self):
        """
        Calculates leakage across a single chip
        """
        # return self.chip_leakage_power_w() * self.chips_per_nvm
        return self.chip_leakage_power_w()

    def total_schedule_power_w(
        self,
        num_reads: int,
        num_writes: int,
        parallel: bool = False,
        full_chip: bool = True,
    ):
        """
        Currently does not include leakage or standby power
        Assumes a sequential schedule on a single chip
        """
        total_read_latency_s = self.total_op_latency_s(OpType.READ, parallel)
        total_write_latency_s = self.total_op_latency_s(OpType.WRITE, parallel)
        total_latency_s = (total_read_latency_s * num_reads +
                           total_write_latency_s * num_writes)

        total_read_energy_j = num_reads * (self.total_op_power_page_w(
            OpType.READ, full_chip) * total_read_latency_s)
        total_write_energy_j = num_writes * (self.total_op_power_page_w(
            OpType.WRITE, full_chip) * total_write_latency_s)
        total_op_power_w = (total_read_energy_j +
                            total_write_energy_j) / total_latency_s
        return total_op_power_w
