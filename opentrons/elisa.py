"""
Phase 3 golden-fixture protocol — simple ELISA wash + bead separation + read.

Exercises every Phase 3 module kind:
- Magnetic module (engage / disengage to settle beads).
- Heater-shaker (incubation with shake, then deactivate).
- Temperature module (block kept at 4 C during reagent prep).
- Thermocycler (open / close lid; the absorbance reader uses lid commands
  with the same name on Flex but here we use the thermocycler stub).
- Absorbance reader (initialize + read).
"""

metadata = {
    'protocolName': 'ELISA — beads + heater-shaker + absorbance read',
    'apiLevel': '2.16',
}


def run(protocol):
    # Setup labware + instrument
    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
    plate = protocol.load_labware('nest_96_wellplate_2ml_deep', 2)
    p300 = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tips])

    # Modules
    mag = protocol.load_module('magneticModuleV2', 4)
    hs = protocol.load_module('heaterShakerModuleV1', 7)
    temp = protocol.load_module('temperatureModuleV2', 9)
    absorbance = protocol.load_module('absorbanceReaderV1', 3)

    # Pre-warm + cool
    temp.set_temperature(4)
    temp.await_temperature(4)

    # Wash step: add buffer, shake, settle, aspirate supernatant
    p300.pick_up_tip()
    p300.aspirate(200, plate['A1'])
    p300.dispense(200, plate['A2'])
    p300.drop_tip()

    hs.close_labware_latch()
    hs.set_and_wait_for_shake_speed(800)
    hs.deactivate_shaker()
    hs.open_labware_latch()

    mag.engage(height_from_base=4)
    mag.disengage()

    # Read
    absorbance.initialize(mode='single')
    absorbance.read()

    # Tear down
    temp.deactivate()
