from ..base_devices import BaseDeviceV2
from ..fields import (
    FieldName,
    UIntField,
    SIntField,
    SInt32Field,
    DecimalField,
    SwapStringField,
    SerialNumberField,
    VersionField,
    SwitchField,
    BoolField,
)


class EP2000(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                SInt32Field(FieldName.TOTAL_PV_POWER, 1200),
                SInt32Field(FieldName.POWER_GENERATION, 1202, 0.1),
                UIntField(FieldName.PV_S1_POWER, 1212),
                DecimalField(FieldName.PV_S1_VOLTAGE, 1213, 1),
                DecimalField(FieldName.PV_S1_CURRENT, 1214, 1),
                UIntField(FieldName.PV_S2_POWER, 1220),
                DecimalField(FieldName.PV_S2_VOLTAGE, 1221, 1),
                DecimalField(FieldName.PV_S2_CURRENT, 1222, 1),
                UIntField(FieldName.PV_S3_POWER, 1228),
                DecimalField(FieldName.PV_S3_VOLTAGE, 1229, 1),
                DecimalField(FieldName.PV_S3_CURRENT, 1230, 1),
                UIntField(FieldName.PV_S4_POWER, 1236),
                DecimalField(FieldName.PV_S4_VOLTAGE, 1237, 1),
                DecimalField(FieldName.PV_S4_CURRENT, 1238, 1),
                UIntField(FieldName.PV_S5_POWER, 1244),
                DecimalField(FieldName.PV_S5_VOLTAGE, 1245, 1),
                DecimalField(FieldName.PV_S5_CURRENT, 1246, 1),
                DecimalField(FieldName.GRID_FREQUENCY, 1300, 1),
                SIntField(FieldName.TOTAL_AC_POWER, 1301),
                SIntField(FieldName.GRID_P1_POWER, 1313),
                DecimalField(FieldName.GRID_P1_VOLTAGE, 1314, 1),
                DecimalField(FieldName.GRID_P1_CURRENT, 1315, 1),
                SIntField(FieldName.GRID_P2_POWER, 1319),
                DecimalField(FieldName.GRID_P2_VOLTAGE, 1320, 1),
                DecimalField(FieldName.GRID_P2_CURRENT, 1321, 1),
                SIntField(FieldName.GRID_P3_POWER, 1325),
                DecimalField(FieldName.GRID_P3_VOLTAGE, 1326, 1),
                DecimalField(FieldName.GRID_P3_CURRENT, 1327, 1),
                UIntField(FieldName.TOTAL_SELF_CONSUMPTION, 1290),
                DecimalField(FieldName.AC_OUTPUT_FREQUENCY, 1500, 1),
                SIntField(FieldName.AC_P1_POWER, 1510),
                DecimalField(FieldName.AC_P1_VOLTAGE, 1511, 1),
                DecimalField(FieldName.AC_P1_CURRENT, 1512, 1),
                SIntField(FieldName.AC_P2_POWER, 1517),
                DecimalField(FieldName.AC_P2_VOLTAGE, 1518, 1),
                DecimalField(FieldName.AC_P2_CURRENT, 1519, 1),
                SIntField(FieldName.AC_P3_POWER, 1524),
                DecimalField(FieldName.AC_P3_VOLTAGE, 1525, 1),
                DecimalField(FieldName.AC_P3_CURRENT, 1526, 1),
                UIntField(FieldName.LOAD_P1_POWER, 1430),
                UIntField(FieldName.LOAD_P2_POWER, 1436),
                UIntField(FieldName.LOAD_P3_POWER, 1442),
                SwitchField(FieldName.CTRL_AC, 2011),
                UIntField(FieldName.BATTERY_SOC_RANGE_START, 2022),
                UIntField(FieldName.BATTERY_SOC_RANGE_END, 2023),
                SwitchField(FieldName.GRID_EXPORT_ENABLED, 2208),
                BoolField(FieldName.CTRL_GENERATOR, 2246),
                DecimalField(FieldName.GRID_VOLT_MIN_VAL, 2435, 1),
                DecimalField(FieldName.GRID_VOLT_MAX_VAL, 2436, 1),
                DecimalField(FieldName.GRID_FREQ_MIN_VALUE, 2437, 2),
                DecimalField(FieldName.GRID_FREQ_MAX_VALUE, 2438, 2),
                SwapStringField(FieldName.WIFI_NAME, 12002, 16),
                # Battery pack detail block (register 6100+). Read directly
                # here rather than via the pack_fields/max_packs mechanism
                # below, since that's currently dormant (max_packs=0) and
                # untested for multi-pack selection - this matches what was
                # actually observed in the official app's own traffic: a
                # single direct read, no per-pack selection write involved.
                # Validated July 27-28 against a real capture: battery
                # voltage, SOC, and SOH all read as physically sensible
                # values, and active cell count (112) and stack count (7)
                # both matched independently-known reference values exactly
                # (the stack count confirmed directly against the owner's
                # own real hardware: 7 physical battery stacks attached).
                SwapStringField(FieldName.BMS_CONTROLLER_MODEL, 6101, 6),
                DecimalField(FieldName.PACK_VOLTAGE, 6111, 1),
                UIntField(FieldName.PACK_BATTERY_SOC, 6113, min=0, max=100),
                UIntField(FieldName.PACK_SOH, 6114, min=0, max=100),
                UIntField(FieldName.ACTIVE_CELL_COUNT, 6153),
                UIntField(FieldName.BATTERY_STACK_COUNT, 6154),
                # Read-only, purely exploratory: register 21000 was
                # documented as a "NODE_INFO" discovery trigger (write-only,
                # never observed being read back in any captured traffic).
                # 21001 is documented as "Total Node Count" - added here as
                # a read to see what it actually reports; unverified
                # whether it requires the 21000 trigger to have run first,
                # or reports a live value regardless.
                UIntField(FieldName.TOTAL_NODE_COUNT, 21001),
            ],
            [
                SwapStringField(FieldName.PACK_TYPE, 6101, 6),
                SerialNumberField(FieldName.PACK_SN, 6107),
                VersionField(FieldName.PACK_VER_BCU, 6175),
                VersionField(FieldName.PACK_VER_BMU, 6178),
                VersionField(FieldName.PACK_VER_SAFETY_MOD, 6181),
                VersionField(FieldName.PACK_VER_HV_MOD, 6184),
            ],
            # max_packs=2,
        )
