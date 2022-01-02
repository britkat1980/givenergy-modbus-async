from enum import Enum, auto, unique


class Type(Enum):
    """Type of data register represents."""

    BOOL = auto()
    WORD = auto()  # unsigned single word
    DWORD_HIGH = auto()  # unsigned double word, higher (MSB) address half
    DWORD_LOW = auto()  # unsigned double word, lower (LSB) address half
    SWORD = auto()  # signed single word
    ASCII = auto()

    def render(self, value: int, scaling: float):
        """Convert val to its true representation as determined by the register definition."""
        if self == self.DWORD_HIGH:
            # shift MSB half of the word left by 4 bytes
            return (value << 16) * scaling

        if self == self.SWORD:
            # Subtract 2^n if bit n-1 is set:
            if value & (1 << (16 - 1)):
                value -= 1 << 16
            return value * scaling

        if self == self.ASCII:
            return value.to_bytes(2, byteorder='big').decode(encoding='ascii')

        if self == self.BOOL:  # TODO is this the correct assumption?
            return bool(value & 0x0001)

        # only unsigned WORD left
        return value * scaling


class Scaling(Enum):
    """What scaling factor needs to be applied to a register's value."""

    # KILO = 1000
    # HECTO = 100
    # DECA = 10
    UNIT = 1
    DECI = 0.1
    CENTI = 0.01


@unique
class RegisterBank(bytes, Enum):
    """Mixin to help easier access to register bank structures."""

    def __new__(cls, value: int, type_: Type, scaling: Scaling):
        """Allows indexing by register index."""
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.type = type_  # type: ignore
        obj.scaling = scaling  # type: ignore
        return obj

    def render(self, val):
        """Convert val to its true representation as determined by the register type."""
        return self.type.render(val, self.scaling.value)


class HoldingRegister(RegisterBank):
    """Definitions of what registers in the Holding Bank represent."""

    DEVICE_TYPE_CODE = (0, Type.WORD, Scaling.UNIT)
    INVERTER_MODULE_H = (1, Type.DWORD_HIGH, Scaling.UNIT)
    INVERTER_MODULE_L = (2, Type.DWORD_LOW, Scaling.UNIT)
    INPUT_TRACKER_NUM_AND_OUTPUT_PHASE_NUM = (3, Type.WORD, Scaling.UNIT)
    REG004 = (4, Type.WORD, Scaling.UNIT)
    REG005 = (5, Type.WORD, Scaling.UNIT)
    REG006 = (6, Type.WORD, Scaling.UNIT)
    REG007 = (7, Type.WORD, Scaling.UNIT)
    BATTERY_SERIAL_NUMBER_5 = (8, Type.ASCII, Scaling.UNIT)
    BATTERY_SERIAL_NUMBER_4 = (9, Type.ASCII, Scaling.UNIT)
    BATTERY_SERIAL_NUMBER_3 = (10, Type.ASCII, Scaling.UNIT)
    BATTERY_SERIAL_NUMBER_2 = (11, Type.ASCII, Scaling.UNIT)
    BATTERY_SERIAL_NUMBER_1 = (12, Type.ASCII, Scaling.UNIT)
    INVERTER_SERIAL_NUMBER_5 = (13, Type.ASCII, Scaling.UNIT)
    INVERTER_SERIAL_NUMBER_4 = (14, Type.ASCII, Scaling.UNIT)
    INVERTER_SERIAL_NUMBER_3 = (15, Type.ASCII, Scaling.UNIT)
    INVERTER_SERIAL_NUMBER_2 = (16, Type.ASCII, Scaling.UNIT)
    INVERTER_SERIAL_NUMBER_1 = (17, Type.ASCII, Scaling.UNIT)
    BATTERY_FIRMWARE_VERSION = (18, Type.WORD, Scaling.UNIT)
    DSP_FIRMWARE_VERSION = (19, Type.WORD, Scaling.UNIT)
    WINTER_MODE = (20, Type.BOOL, Scaling.UNIT)
    ARM_FIRMWARE_VERSION = (21, Type.WORD, Scaling.UNIT)
    WIFI_OR_U_DISK = (22, Type.WORD, Scaling.UNIT)  # 2 = wifi?
    SELECT_DSP_OR_ARM = (23, Type.WORD, Scaling.UNIT)
    SET_VARIABLE_ADDRESS = (24, Type.WORD, Scaling.UNIT)
    SET_VARIABLE_VALUE = (25, Type.WORD, Scaling.UNIT)
    GRID_PORT_MAX_OUTPUT_POWER = (26, Type.WORD, Scaling.UNIT)
    BATTERY_POWER_MODE = (27, Type.BOOL, Scaling.UNIT)  # 1 - grid-tie?
    FRE_MODE = (28, Type.WORD, Scaling.UNIT)  # bool?
    SOC_FORCE_ADJUST = (29, Type.WORD, Scaling.UNIT)
    COMMUNICATE_ADDRESS = (30, Type.WORD, Scaling.UNIT)
    CHARGE_SLOT_2_START = (31, Type.WORD, Scaling.UNIT)
    CHARGE_SLOT_2_END = (32, Type.WORD, Scaling.UNIT)
    USER_CODE = (33, Type.WORD, Scaling.UNIT)
    MODBUS_VERSION = (34, Type.WORD, Scaling.CENTI)
    SYSTEM_TIME_YEAR = (35, Type.WORD, Scaling.UNIT)
    SYSTEM_TIME_MONTH = (36, Type.WORD, Scaling.UNIT)
    SYSTEM_TIME_DAY = (37, Type.WORD, Scaling.UNIT)
    SYSTEM_TIME_HOUR = (38, Type.WORD, Scaling.UNIT)
    SYSTEM_TIME_MINUTE = (39, Type.WORD, Scaling.UNIT)
    SYSTEM_TIME_SECOND = (40, Type.WORD, Scaling.UNIT)
    DRM_ENABLE = (41, Type.BOOL, Scaling.UNIT)
    CT_ADJUST = (42, Type.WORD, Scaling.UNIT)
    CHARGE_AND_DISCHARGE_SOC = (43, Type.WORD, Scaling.UNIT)
    DISCHARGE_SLOT_2_START = (44, Type.WORD, Scaling.UNIT)
    DISCHARGE_SLOT_2_END = (45, Type.WORD, Scaling.UNIT)
    BMS_VERSION = (46, Type.WORD, Scaling.UNIT)
    B_METER_TYPE = (47, Type.WORD, Scaling.UNIT)
    B_115_METER_DIRECT = (48, Type.WORD, Scaling.UNIT)
    B_418_METER_DIRECT = (49, Type.WORD, Scaling.UNIT)
    ACTIVE_P_RATE = (50, Type.WORD, Scaling.UNIT)
    REACTIVE_P_RATE = (51, Type.WORD, Scaling.UNIT)
    POWER_FACTOR = (52, Type.WORD, Scaling.UNIT)
    INVERTER_STATE = (53, Type.WORD, Scaling.UNIT)  # 1 = normal?
    BATTERY_TYPE = (54, Type.WORD, Scaling.UNIT)  # 1 = lithium?
    BATTERY_NOMINAL_CAPACITY = (55, Type.WORD, Scaling.UNIT)
    DISCHARGE_SLOT_1_START = (56, Type.WORD, Scaling.UNIT)
    DISCHARGE_SLOT_1_END = (57, Type.WORD, Scaling.UNIT)
    AUTO_JUDGE_BATTERY_TYPE_ENABLE = (58, Type.WORD, Scaling.UNIT)  # bool?
    DISCHARGE_ENABLE = (59, Type.BOOL, Scaling.UNIT)
    INPUT_START_VOLTAGE = (60, Type.WORD, Scaling.UNIT)
    START_TIME = (61, Type.WORD, Scaling.UNIT)
    RESTART_DELAY_TIME = (62, Type.WORD, Scaling.UNIT)
    V_AC_LOW_OUT = (63, Type.WORD, Scaling.DECI)
    V_AC_HIGH_OUT = (64, Type.WORD, Scaling.DECI)
    F_AC_LOW_OUT = (65, Type.WORD, Scaling.CENTI)
    F_AC_HIGH_OUT = (66, Type.WORD, Scaling.CENTI)
    V_AC_LOW_OUT_TIME = (67, Type.WORD, Scaling.UNIT)
    V_AC_HIGH_OUT_TIME = (68, Type.WORD, Scaling.UNIT)
    F_AC_LOW_OUT_TIME = (69, Type.WORD, Scaling.UNIT)
    F_AC_HIGH_OUT_TIME = (70, Type.WORD, Scaling.UNIT)
    V_AC_LOW_IN = (71, Type.WORD, Scaling.DECI)
    V_AC_HIGH_IN = (72, Type.WORD, Scaling.DECI)
    F_AC_LOW_IN = (73, Type.WORD, Scaling.CENTI)
    F_AC_HIGH_IN = (74, Type.WORD, Scaling.CENTI)
    V_AC_LOW_IN_TIME = (75, Type.WORD, Scaling.UNIT)
    V_AC_HIGH_IN_TIME = (76, Type.WORD, Scaling.UNIT)
    F_AC_LOW_TIME_IN = (77, Type.WORD, Scaling.UNIT)
    F_AC_HIGH_TIME_IN = (78, Type.WORD, Scaling.UNIT)
    V_AC_LOW_C = (79, Type.WORD, Scaling.DECI)
    V_AC_HIGH_C = (80, Type.WORD, Scaling.DECI)
    F_AC_LOW_C = (81, Type.WORD, Scaling.CENTI)
    F_AC_HIGH_C = (82, Type.WORD, Scaling.CENTI)
    U_10_MIN = (83, Type.WORD, Scaling.UNIT)
    ISO1 = (84, Type.WORD, Scaling.UNIT)
    ISO2 = (85, Type.WORD, Scaling.UNIT)
    GFCI_I_1 = (86, Type.WORD, Scaling.UNIT)
    GFCI_TIME_1 = (87, Type.WORD, Scaling.UNIT)
    GFCI_I_2 = (88, Type.WORD, Scaling.UNIT)
    GFCI_TIME_2 = (89, Type.WORD, Scaling.UNIT)
    DCI_I_1 = (90, Type.WORD, Scaling.UNIT)
    DCI_TIME_1 = (91, Type.WORD, Scaling.UNIT)
    DCI_I_2 = (92, Type.WORD, Scaling.UNIT)
    DCI_TIME_2 = (93, Type.WORD, Scaling.UNIT)
    CHARGE_SLOT_1_START = (94, Type.WORD, Scaling.UNIT)
    CHARGE_SLOT_1_END = (95, Type.WORD, Scaling.UNIT)
    BATTERY_SMART_CHARGE = (96, Type.BOOL, Scaling.UNIT)
    DISCHARGE_LOW_LIMIT = (97, Type.WORD, Scaling.UNIT)
    CHARGER_HIGH_LIMIT = (98, Type.WORD, Scaling.UNIT)
    PV1_VOLT_ADJUST = (99, Type.WORD, Scaling.UNIT)
    PV2_VOLT_ADJUST = (100, Type.WORD, Scaling.UNIT)
    GRID_R_VOLT_ADJUST = (101, Type.WORD, Scaling.UNIT)
    GRID_S_VOLT_ADJUST = (102, Type.WORD, Scaling.UNIT)
    GRID_T_VOLT_ADJUST = (103, Type.WORD, Scaling.UNIT)
    GRID_POWER_ADJUST = (104, Type.WORD, Scaling.UNIT)
    BATTERY_VOLT_ADJUST = (105, Type.WORD, Scaling.UNIT)
    PV1_POWER_ADJUST = (106, Type.WORD, Scaling.UNIT)
    PV2_POWER_ADJUST = (107, Type.WORD, Scaling.UNIT)
    BATTERY_LOW_FORCE_CHARGE_TIME = (108, Type.WORD, Scaling.UNIT)
    BMS_TYPE = (109, Type.WORD, Scaling.UNIT)
    SHALLOW_CHARGE = (110, Type.WORD, Scaling.UNIT)
    BATTERY_CHARGE_LIMIT = (111, Type.WORD, Scaling.UNIT)
    BATTERY_DISCHARGE_LIMIT = (112, Type.WORD, Scaling.UNIT)
    BUZZER_SW = (113, Type.WORD, Scaling.UNIT)
    BATTERY_POWER_RESERVE = (114, Type.WORD, Scaling.UNIT)
    ISLAND_CHECK_CONTINUE = (115, Type.WORD, Scaling.UNIT)
    TARGET_SOC = (116, Type.WORD, Scaling.UNIT)
    CHG_SOC_STOP2 = (117, Type.WORD, Scaling.UNIT)
    DISCHARGE_SOC_STOP2 = (118, Type.WORD, Scaling.UNIT)
    CHG_SOC_STOP = (119, Type.WORD, Scaling.UNIT)
    DISCHARGE_SOC_STOP = (120, Type.WORD, Scaling.UNIT)


class InputRegister(RegisterBank):
    """Definitions of what registers in the Input Bank represent."""

    INVERTER_STATUS = (0, Type.WORD, Scaling.UNIT)  # 0 waiting (no PV, no bat)? 1 charging?
    V_PV1 = (1, Type.WORD, Scaling.DECI)
    V_PV2 = (2, Type.WORD, Scaling.DECI)
    P_BUS_INSIDE_VOLTAGE = (3, Type.WORD, Scaling.DECI)
    N_BUS_INSIDE_VOLTAGE = (4, Type.WORD, Scaling.DECI)
    V_SINGLE_PHASE_GRID = (5, Type.WORD, Scaling.DECI)
    E_BATTERY_THROUGHPUT_H = (6, Type.DWORD_HIGH, Scaling.DECI)
    E_BATTERY_THROUGHPUT_L = (7, Type.DWORD_LOW, Scaling.DECI)
    I_PV1_INPUT = (8, Type.WORD, Scaling.CENTI)
    I_PV2_INPUT = (9, Type.WORD, Scaling.CENTI)
    I_GRID_OUTPUT_SINGLE_PHASE = (10, Type.WORD, Scaling.CENTI)
    PV_TOTAL_GENERATING_CAPACITY_H = (11, Type.DWORD_HIGH, Scaling.DECI)
    PV_TOTAL_GENERATING_CAPACITY_L = (12, Type.DWORD_LOW, Scaling.DECI)
    F_GRID_THREE_SINGLE_PHASE = (13, Type.WORD, Scaling.CENTI)
    CHARGE_STATUS = (14, Type.WORD, Scaling.UNIT)
    V_HIGHBRIGH_BUS = (15, Type.WORD, Scaling.UNIT)  # high voltage bus?
    PF_INVERTER_OUTPUT_NOW = (16, Type.WORD, Scaling.UNIT)
    E_PV1_DAY = (17, Type.WORD, Scaling.DECI)
    P_PV1_INPUT = (18, Type.WORD, Scaling.UNIT)
    E_PV2_DAY = (19, Type.WORD, Scaling.DECI)
    P_PV2_INPUT = (20, Type.WORD, Scaling.UNIT)
    E_GRID_OUT_TOTAL_H = (21, Type.DWORD_HIGH, Scaling.DECI)
    E_GRID_OUT_TOTAL_L = (22, Type.DWORD_LOW, Scaling.DECI)
    PV_MATE = (23, Type.WORD, Scaling.DECI)
    P_GRID_THREE_SINGLE_PHASE_OUTPUT_L = (24, Type.SWORD, Scaling.UNIT)
    E_GRID_OUT_DAY = (25, Type.WORD, Scaling.DECI)
    E_GRID_IN_DAY = (26, Type.WORD, Scaling.DECI)
    E_INVERTER_IN_TOTAL_H = (27, Type.DWORD_HIGH, Scaling.DECI)
    E_INVERTER_IN_TOTAL_L = (28, Type.DWORD_LOW, Scaling.DECI)
    E_DISCHARGE_YEAR_L = (29, Type.WORD, Scaling.DECI)
    P_GRID_OUTPUT = (30, Type.SWORD, Scaling.UNIT)
    P_BACKUP = (31, Type.WORD, Scaling.UNIT)
    P_GRID_IN_TOTAL_H = (32, Type.DWORD_HIGH, Scaling.DECI)
    P_GRID_IN_TOTAL_L = (33, Type.DWORD_LOW, Scaling.DECI)
    REG034 = (34, Type.WORD, Scaling.UNIT)
    E_TOTAL_LOAD_DAY = (35, Type.WORD, Scaling.DECI)
    E_BATTERY_CHARGE_DAY = (36, Type.WORD, Scaling.DECI)
    E_BATTERY_DISCHARGE_DAY = (37, Type.WORD, Scaling.DECI)
    P_COUNTDOWN = (38, Type.WORD, Scaling.UNIT)
    FAULT_CODE_H = (39, Type.DWORD_HIGH, Scaling.UNIT)
    FAULT_CODE_L = (40, Type.DWORD_LOW, Scaling.UNIT)
    TEMP_INV = (41, Type.WORD, Scaling.DECI)
    P_LOAD_TOTAL = (42, Type.WORD, Scaling.UNIT)
    P_GRID_APPARENT = (43, Type.WORD, Scaling.UNIT)
    E_GENERATED_DAY = (44, Type.WORD, Scaling.DECI)
    E_GENERATED_H = (45, Type.DWORD_HIGH, Scaling.DECI)
    E_GENERATED_L = (46, Type.DWORD_LOW, Scaling.DECI)
    WORK_TIME_TOTAL_H = (47, Type.DWORD_HIGH, Scaling.UNIT)
    WORK_TIME_TOTAL_L = (48, Type.DWORD_LOW, Scaling.UNIT)
    SYSTEM_MODE = (49, Type.WORD, Scaling.UNIT)  # 1 = grid-tie?
    V_BAT = (50, Type.WORD, Scaling.CENTI)
    I_BAT = (51, Type.SWORD, Scaling.CENTI)
    P_BAT = (52, Type.SWORD, Scaling.UNIT)
    V_OUTPUT = (53, Type.WORD, Scaling.DECI)
    F_OUTPUT = (54, Type.WORD, Scaling.CENTI)
    TEMP_CHARGER = (55, Type.WORD, Scaling.DECI)
    TEMP_BAT = (56, Type.WORD, Scaling.DECI)
    CHARGER_WARNING_CODE = (57, Type.WORD, Scaling.UNIT)
    P_GRID_PORT = (58, Type.WORD, Scaling.CENTI)
    BATTERY_PERCENT = (59, Type.WORD, Scaling.UNIT)
    REG060 = (60, Type.WORD, Scaling.UNIT)  # cell voltage? spans to reg 75
    REG061 = (61, Type.WORD, Scaling.UNIT)
    REG062 = (62, Type.WORD, Scaling.UNIT)
    REG063 = (63, Type.WORD, Scaling.UNIT)
    REG064 = (64, Type.WORD, Scaling.UNIT)
    REG065 = (65, Type.WORD, Scaling.UNIT)
    REG066 = (66, Type.WORD, Scaling.UNIT)
    REG067 = (67, Type.WORD, Scaling.UNIT)
    REG068 = (68, Type.WORD, Scaling.UNIT)
    REG069 = (69, Type.WORD, Scaling.UNIT)
    REG070 = (70, Type.WORD, Scaling.UNIT)
    REG071 = (71, Type.WORD, Scaling.UNIT)
    REG072 = (72, Type.WORD, Scaling.UNIT)
    REG073 = (73, Type.WORD, Scaling.UNIT)
    REG074 = (74, Type.WORD, Scaling.UNIT)
    REG075 = (75, Type.WORD, Scaling.UNIT)
    REG076 = (76, Type.WORD, Scaling.UNIT)
    REG077 = (77, Type.WORD, Scaling.UNIT)
    REG078 = (78, Type.WORD, Scaling.UNIT)
    REG079 = (79, Type.WORD, Scaling.UNIT)
    REG080 = (80, Type.WORD, Scaling.UNIT)
    REG081 = (81, Type.WORD, Scaling.UNIT)
    REG082 = (82, Type.WORD, Scaling.UNIT)
    REG083 = (83, Type.WORD, Scaling.UNIT)
    REG084 = (84, Type.WORD, Scaling.UNIT)
    REG085 = (85, Type.WORD, Scaling.UNIT)
    REG086 = (86, Type.WORD, Scaling.UNIT)
    REG087 = (87, Type.WORD, Scaling.UNIT)
    REG088 = (88, Type.WORD, Scaling.UNIT)
    REG089 = (89, Type.WORD, Scaling.UNIT)
    REG090 = (90, Type.WORD, Scaling.UNIT)
    REG091 = (91, Type.WORD, Scaling.UNIT)
    REG092 = (92, Type.WORD, Scaling.UNIT)
    REG093 = (93, Type.WORD, Scaling.UNIT)
    REG094 = (94, Type.WORD, Scaling.UNIT)
    REG095 = (95, Type.WORD, Scaling.UNIT)
    REG096 = (96, Type.WORD, Scaling.UNIT)
    REG097 = (97, Type.WORD, Scaling.UNIT)
    REG098 = (98, Type.WORD, Scaling.UNIT)
    REG099 = (99, Type.WORD, Scaling.UNIT)
    REG100 = (100, Type.WORD, Scaling.UNIT)
    REG101 = (101, Type.WORD, Scaling.UNIT)
    REG102 = (102, Type.WORD, Scaling.UNIT)
    REG103 = (103, Type.WORD, Scaling.UNIT)
    REG104 = (104, Type.WORD, Scaling.UNIT)
    E_BATTERY_DISCHARGE_AC_TOTAL = (105, Type.WORD, Scaling.DECI)
    E_BATTERY_CHARGE_AC_TOTAL = (106, Type.WORD, Scaling.DECI)
    REG107 = (107, Type.WORD, Scaling.UNIT)
    REG108 = (108, Type.WORD, Scaling.UNIT)
    REG109 = (109, Type.WORD, Scaling.UNIT)
    BATTERY_SERIAL_NUMBER_5 = (110, Type.ASCII, Scaling.UNIT)
    BATTERY_SERIAL_NUMBER_4 = (111, Type.ASCII, Scaling.UNIT)
    BATTERY_SERIAL_NUMBER_3 = (112, Type.ASCII, Scaling.UNIT)
    BATTERY_SERIAL_NUMBER_2 = (113, Type.ASCII, Scaling.UNIT)
    BATTERY_SERIAL_NUMBER_1 = (114, Type.ASCII, Scaling.UNIT)
    REG115 = (115, Type.WORD, Scaling.UNIT)
    REG116 = (116, Type.WORD, Scaling.UNIT)
    REG117 = (117, Type.WORD, Scaling.UNIT)
    REG118 = (118, Type.WORD, Scaling.UNIT)
    REG119 = (119, Type.WORD, Scaling.UNIT)
    REG120 = (120, Type.WORD, Scaling.UNIT)
    REG121 = (121, Type.WORD, Scaling.UNIT)
    REG122 = (122, Type.WORD, Scaling.UNIT)
    REG123 = (123, Type.WORD, Scaling.UNIT)
    REG124 = (124, Type.WORD, Scaling.UNIT)
    REG125 = (125, Type.WORD, Scaling.UNIT)
    REG126 = (126, Type.WORD, Scaling.UNIT)
    REG127 = (127, Type.WORD, Scaling.UNIT)
    REG128 = (128, Type.WORD, Scaling.UNIT)
    REG129 = (129, Type.WORD, Scaling.UNIT)
    REG130 = (130, Type.WORD, Scaling.UNIT)
    REG131 = (131, Type.WORD, Scaling.UNIT)
    REG132 = (132, Type.WORD, Scaling.UNIT)
    REG133 = (133, Type.WORD, Scaling.UNIT)
    REG134 = (134, Type.WORD, Scaling.UNIT)
    REG135 = (135, Type.WORD, Scaling.UNIT)
    REG136 = (136, Type.WORD, Scaling.UNIT)
    REG137 = (137, Type.WORD, Scaling.UNIT)
    REG138 = (138, Type.WORD, Scaling.UNIT)
    REG139 = (139, Type.WORD, Scaling.UNIT)
    REG140 = (140, Type.WORD, Scaling.UNIT)
    REG141 = (141, Type.WORD, Scaling.UNIT)
    REG142 = (142, Type.WORD, Scaling.UNIT)
    REG143 = (143, Type.WORD, Scaling.UNIT)
    REG144 = (144, Type.WORD, Scaling.UNIT)
    REG145 = (145, Type.WORD, Scaling.UNIT)
    REG146 = (146, Type.WORD, Scaling.UNIT)
    REG147 = (147, Type.WORD, Scaling.UNIT)
    REG148 = (148, Type.WORD, Scaling.UNIT)
    REG149 = (149, Type.WORD, Scaling.UNIT)
    REG150 = (150, Type.WORD, Scaling.UNIT)
    REG151 = (151, Type.WORD, Scaling.UNIT)
    REG152 = (152, Type.WORD, Scaling.UNIT)
    REG153 = (153, Type.WORD, Scaling.UNIT)
    REG154 = (154, Type.WORD, Scaling.UNIT)
    REG155 = (155, Type.WORD, Scaling.UNIT)
    REG156 = (156, Type.WORD, Scaling.UNIT)
    REG157 = (157, Type.WORD, Scaling.UNIT)
    REG158 = (158, Type.WORD, Scaling.UNIT)
    REG159 = (159, Type.WORD, Scaling.UNIT)
    REG160 = (160, Type.WORD, Scaling.UNIT)
    REG161 = (161, Type.WORD, Scaling.UNIT)
    REG162 = (162, Type.WORD, Scaling.UNIT)
    REG163 = (163, Type.WORD, Scaling.UNIT)
    REG164 = (164, Type.WORD, Scaling.UNIT)
    REG165 = (165, Type.WORD, Scaling.UNIT)
    REG166 = (166, Type.WORD, Scaling.UNIT)
    REG167 = (167, Type.WORD, Scaling.UNIT)
    REG168 = (168, Type.WORD, Scaling.UNIT)
    REG169 = (169, Type.WORD, Scaling.UNIT)
    REG170 = (170, Type.WORD, Scaling.UNIT)
    REG171 = (171, Type.WORD, Scaling.UNIT)
    REG172 = (172, Type.WORD, Scaling.UNIT)
    REG173 = (173, Type.WORD, Scaling.UNIT)
    REG174 = (174, Type.WORD, Scaling.UNIT)
    REG175 = (175, Type.WORD, Scaling.UNIT)
    REG176 = (176, Type.WORD, Scaling.UNIT)
    REG177 = (177, Type.WORD, Scaling.UNIT)
    REG178 = (178, Type.WORD, Scaling.UNIT)
    REG179 = (179, Type.WORD, Scaling.UNIT)
    E_BATTERY_DISCHARGE_TOTAL = (180, Type.WORD, Scaling.DECI)
    E_BATTERY_CHARGE_TOTAL = (181, Type.WORD, Scaling.DECI)
