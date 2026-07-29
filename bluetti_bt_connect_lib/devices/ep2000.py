from ..base_devices import BaseDeviceV2
from ..enums import WorkingMode
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
    WriteableUIntField,
    SelectField,
)


class EP2000(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                # These are plain 16-bit fields, not 32-bit - treating them
                # as 32-bit previously produced nonsensical values in the
                # tens of millions.
                SIntField(FieldName.CONSUMPTION_POWER_ALL, 142),
                UIntField(FieldName.PV_INPUT_POWER_ALL, 144),
                SIntField(FieldName.GRID_POWER_ALL, 146),
                DecimalField(FieldName.TOTAL_AC_CONSUMPTION, 152, 1),
                DecimalField(FieldName.TOTAL_GRID_FEED, 158, 1),
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
                # Register from an EP2000-specific contributor source; enum
                # values cross-referenced from a related device (AP300,
                # register 2005 there) - the set of names matches exactly
                # what's shown in the app's Working Mode dropdown.
                SelectField(FieldName.WORKING_MODE, 2013, WorkingMode),
                UIntField(FieldName.BATTERY_SOC_RANGE_START, 2022),
                UIntField(FieldName.BATTERY_SOC_RANGE_END, 2023),
                SwitchField(FieldName.CHARGE_FROM_GRID_ENABLED, 2207),
                SwitchField(FieldName.GRID_EXPORT_ENABLED, 2208),
                WriteableUIntField(FieldName.MAX_GRID_EXPORT_POWER, 2215, min=0, max=6666),
                # Restored: live-tested and confirmed working in an earlier
                # build (37A raw read correctly, no scaling needed) before
                # being lost from the codebase during restructuring. Bound
                # is the last value you confirmed - 35A for wiring
                # headroom, since the 6666W power limit above is the true
                # constraint anyway.
                WriteableUIntField(FieldName.MAX_GRID_EXPORT_CURRENT, 2216, min=0, max=35),
                # Cross-referenced from two independent sources (a related
                # device's register map and the original bluetti_mqtt/EP600
                # reference, which both agree on this register/purpose).
                # Fixed: min was 1, but if the device legitimately reports
                # 0 (e.g. no active import limit set), the old min=1 bound
                # made in_range() silently discard every reading with no
                # error - which is exactly what was happening. Changed to
                # min=0 so real 0 readings actually surface instead of
                # vanishing. Max raised 30 -> 40: the Bluetti app's own
                # Energy Buying/Selling screen shows 40A as a real,
                # currently-configured value on this exact unit, so our
                # old 30A ceiling was simply wrong, not just conservative.
                # Confirmed directly from a raw register dump: 2213 reads
                # 6600, exactly matching "Single-phase Grid Max. Input
                # Power: 6600 W" in the Bluetti app. Bound set to that
                # confirmed real value.
                WriteableUIntField(FieldName.MAX_GRID_IMPORT_POWER, 2213, min=0, max=6600),
                WriteableUIntField(FieldName.CTRL_GRID_MAX_CURRENT, 2214, min=0, max=40),
                # Single-source, unverified for EP2000 specifically. Same
                # min=1 -> min=0 fix applied as above, for the same reason.
                # Possibly a duplicate of CTRL_GRID_MAX_CURRENT above -
                # worth comparing live values from both once they surface,
                # and removing whichever one turns out to be wrong/unused.
                WriteableUIntField(FieldName.CTRL_GRID_INPUT_CURRENT, 2272, min=0, max=30),
                BoolField(FieldName.CTRL_GENERATOR, 2246),
                DecimalField(FieldName.GRID_VOLT_MIN_VAL, 2435, 1),
                DecimalField(FieldName.GRID_VOLT_MAX_VAL, 2436, 1),
                DecimalField(FieldName.GRID_FREQ_MIN_VALUE, 2437, 2),
                DecimalField(FieldName.GRID_FREQ_MAX_VALUE, 2438, 2),
                SwapStringField(FieldName.WIFI_NAME, 12002, 16),
                # Read directly here rather than via the pack_fields/
                # max_packs mechanism below, which is dormant (max_packs=0)
                # and untested for multi-pack selection.
                SwapStringField(FieldName.BMS_CONTROLLER_MODEL, 6101, 6),
                DecimalField(FieldName.PACK_VOLTAGE, 6111, 1),
                UIntField(FieldName.PACK_BATTERY_SOC, 6113, min=0, max=100),
                UIntField(FieldName.PACK_SOH, 6114, min=0, max=100),
                UIntField(FieldName.ACTIVE_CELL_COUNT, 6153),
                UIntField(FieldName.BATTERY_STACK_COUNT, 6154),
                # Exploratory, unverified: "Total Node Count", documented
                # alongside a separate write-only discovery-trigger register.
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
