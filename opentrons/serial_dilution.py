"""
Phase 2 golden-fixture protocol — serial dilution across two mounts.

Exercises:
- 8-channel pipette (left mount) doing transfers across a 96-well plate.
- Single-channel pipette (right mount) doing a final spike addition.
- ``instrument.distribute(...)`` helper expansion (one asp, N dispenses).
- Two-mount protocol: builder produces two parallel tracks.
"""

metadata = {
    'protocolName': '8-step serial dilution + single-channel spike',
    'apiLevel': '2.13',
}


def run(protocol):
    tips_300 = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
    tips_20 = protocol.load_labware('opentrons_96_tiprack_20ul', 4)
    diluent = protocol.load_labware('nest_12_reservoir_15ml', 2)
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 3)

    p300m = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tips_300])
    p20s = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[tips_20])

    # Left mount: fill columns 2-8 with diluent via one distribute call,
    # then run a 7-step serial 1:2 dilution down the rows.
    p300m.distribute(100, diluent['A1'], [plate.columns()[i] for i in range(1, 8)])
    for col in range(1, 8):
        p300m.pick_up_tip()
        p300m.aspirate(100, plate.columns()[col - 1])
        p300m.dispense(100, plate.columns()[col])
        p300m.mix(3, 80, plate.columns()[col])
        p300m.drop_tip()

    # Right mount: spike a small volume into the first column.
    p20s.transfer(5, diluent['A1'], plate.columns()[0])
