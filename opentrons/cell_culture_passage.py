"""
Phase 4 golden-fixture protocol — Flex cell-culture passage.

Exercises every Phase 4 hardware addition:
- Flex 96-channel pipette (its own track + shared gantry resource constraint).
- Flex 1-channel pipette on the right mount.
- Flex gripper moving a plate between two deck positions.

Mirrors a real cell-culture passage workflow:
1. Move the source plate onto the temperature module (gripper).
2. Aspirate spent media from every well with the 96-channel pipette.
3. Dispense fresh media with the 96-channel pipette.
4. Move the plate back to its starting position (gripper).
5. Spike one well with a single-channel pipette.
"""

metadata = {
    'protocolName': 'Flex cell-culture passage',
    'apiLevel': '2.16',
}


def run(protocol):
    tips_96 = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 1)
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 2)
    media = protocol.load_labware('nest_12_reservoir_15ml', 3)
    waste = protocol.load_labware('nest_1_reservoir_195ml', 4)
    temp = protocol.load_module('temperatureModuleV2', 9)

    p96 = protocol.load_instrument('flex_96channel_1000', 'left', tip_racks=[tips_96])
    p50 = protocol.load_instrument('flex_1channel_50', 'right')

    # 1. Gripper moves the plate onto the temperature module
    protocol.move_labware(plate, temp, use_gripper=True)

    # 2. 96-channel aspirates spent media from every well into the waste reservoir
    p96.pick_up_tip()
    p96.aspirate(150, plate['A1'])
    p96.dispense(150, waste['A1'])
    p96.drop_tip()

    # 3. 96-channel dispenses fresh media from the reservoir back into every well
    p96.pick_up_tip()
    p96.aspirate(150, media['A1'])
    p96.dispense(150, plate['A1'])
    p96.drop_tip()

    # 4. Gripper moves the plate back off the temperature module
    protocol.move_labware(plate, 2, use_gripper=True)

    # 5. Right-mount single-channel spikes a small treatment volume
    p50.transfer(5, media['A2'], plate['A1'])
