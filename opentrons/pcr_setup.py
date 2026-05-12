"""
Phase 2 golden-fixture protocol — PCR setup.

Exercises:
- ``protocol.delay(seconds=N)`` → fixed-duration step on the Protocol track.
- ``protocol.pause(...)`` → indefinite-duration / manual-trigger step.
- ``instrument.mix(reps, vol, location)`` with explicit repetitions.
- ``instrument.transfer(...)`` helper expansion to pickup + asp + disp + drop.
- The OT-2 single-channel pipette on the right mount.
"""

metadata = {
    'protocolName': 'PCR setup',
    'description': 'Combine master mix + template + primers across a 12-well strip, with a brief incubation pause.',
    'apiLevel': '2.13',
}


def run(protocol):
    tips = protocol.load_labware('opentrons_96_tiprack_20ul', 1)
    mm = protocol.load_labware('nest_12_reservoir_15ml', 2)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 3)
    p20 = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[tips])

    # Aliquot 15 uL master mix into 8 reaction wells, with a mix at the end of each.
    p20.pick_up_tip()
    p20.aspirate(120, mm['A1'])
    for col in range(8):
        p20.dispense(15, plate['A%d' % (col + 1)])
        p20.mix(3, 10, plate['A%d' % (col + 1)])
    p20.drop_tip()

    # Pause for the user to load template, then resume with a brief
    # equilibration delay before the thermocycler step would begin.
    protocol.pause('Load template strip and confirm')
    protocol.delay(seconds=30, msg='Equilibration')
