from ..base_devices import BaseDeviceV2
from ..fields import (
    FieldName,
    UIntField,
    WriteableUIntField,
    WriteableStringField,
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
                # Total instantaneous PV power (all strings combined),
                # genuinely 32-bit per register debug data.
                SInt32Field(FieldName.TOTAL_PV_POWER, 1200),
                # Fixed: was reading only the first 16 bits of this 32-bit
                # energy total, and without the correct 0.1 scale factor.
                # Register debug data confirms 1202 is "Total PV Energy"
                # (kWh, scale 1 = one decimal place), 32-bit, not power.
                SInt32Field(FieldName.POWER_GENERATION, 1202, 0.1),
                UIntField(FieldName.PV_S1_POWER, 1212),
                DecimalField(FieldName.PV_S1_VOLTAGE, 1213, 1),
                DecimalField(FieldName.PV_S1_CURRENT, 1214, 1),
                UIntField(FieldName.PV_S2_POWER, 1220),
                DecimalField(FieldName.PV_S2_VOLTAGE, 1221, 1),
                DecimalField(FieldName.PV_S2_CURRENT, 1222, 1),
                # Registers 1228/1236/1244 were previously mislabeled as
                # "smart meter" (SM_P) fields. Debugger data confirms these
                # are actually PV Strings 3, 4, and 5 (String 5 may be
                # AC-coupled PV specifically) - renamed accordingly.
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
                # Combined "GRID consumption + PV-AC generation" total.
                # Debugger data flagged this as a 32-bit value, but live
                # testing showed the raw 16-bit value at 1301 alone (355)
                # is the correct power reading - the 32-bit combination was
                # producing implausible numbers in the millions of watts.
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
                # Possible inverter self-consumption / overhead figure -
                # unverified, worth testing against known baseline draw.
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
                # New: "Load Phase Power" block - distinct from both AC
                # output and Grid. Unverified but potentially represents
                # true home-load-only power. Worth validating against the
                # already-confirmed Net Battery Power formula before
                # relying on it.
                UIntField(FieldName.LOAD_P1_POWER, 1430),
                UIntField(FieldName.LOAD_P2_POWER, 1436),
                UIntField(FieldName.LOAD_P3_POWER, 1442),
                # Unlocks writes to the protected 2200-2280 "Advanced
                # Settings" block (which includes grid export and export
                # power limit). Write this BEFORE writing to those
                # registers, in a separate action - not yet automated
                # into a single combined write. 8 characters = 4 registers.
                # Unverified byte order - see WriteableStringField notes.
                WriteableStringField(FieldName.ADV_LOGIN_PASSWORD, 2200, 4),
                SwitchField(FieldName.CTRL_AC, 2011),
                UIntField(FieldName.BATTERY_SOC_RANGE_START, 2022),
                UIntField(FieldName.BATTERY_SOC_RANGE_END, 2023),
                # --- Read-only diagnostics below: values only, no write ---
                # capability yet. Purpose is to observe real values first
                # and confirm meaning against known device state before
                # ever considering write access.
                #
                # Confirmed via live testing: 1=export enabled, 0=disabled.
                SwitchField(FieldName.GRID_EXPORT_ENABLED, 2208),
                DecimalField(FieldName.MAX_BULK_CHARGE_VOLTAGE, 2211, 1),
                DecimalField(FieldName.MAX_SOLAR_CHARGE_CURRENT, 2212, 1),
                # Writeable, per-phase. Bounds set from the confirmed real
                # safety ceiling: 20kW total export across 3 phases =
                # ~6666W/phase max. Previous placeholder (10000W) would
                # have allowed 30kW total if set to max on all 3 phases -
                # corrected here.
                WriteableUIntField(FieldName.MAX_GRID_EXPORT_POWER, 2215, 0, 6666),
                # Fixed: debugger data said scale=1 (divide by 10), but live
                # testing showed 37A displaying as 3.7A - the raw register
                # value is the real value with no scaling needed.
                # Bound raised to 35A: watts (6666W cap above) is the true
                # limiting factor per user confirmation, and physical
                # wiring has sufficient headroom above 29A.
                WriteableUIntField(FieldName.MAX_GRID_EXPORT_CURRENT, 2216, 0, 35),
                UIntField(FieldName.GENERATOR_AUTO_START_SOC, 2248),
                UIntField(FieldName.GENERATOR_AUTO_STOP_SOC, 2249),
                BoolField(FieldName.CTRL_GENERATOR, 2246),
                DecimalField(FieldName.GRID_VOLT_MIN_VAL, 2435, 1),
                DecimalField(FieldName.GRID_VOLT_MAX_VAL, 2436, 1),
                DecimalField(FieldName.GRID_FREQ_MIN_VALUE, 2437, 2),
                DecimalField(FieldName.GRID_FREQ_MAX_VALUE, 2438, 2),
                # Reverted: debugger data suggested 12003 was the correct
                # start register, but this broke a previously-working
                # reading. 12002 reported correctly before that change.
                SwapStringField(FieldName.WIFI_NAME, 12002, 16),
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
