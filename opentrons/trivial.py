"""
Phase 1 golden-fixture protocol — exercises every command the tracer
bullet recognises: load_labware / load_instrument (setup, no events),
then pickup_tip → aspirate → dispense → drop_tip on the left mount.

Stored alongside the expected CommandEvent stream so CI can assert the
simulator emits exactly four events in this order.
"""

metadata = {
    'protocolName': 'Trivial single-aspirate-and-dispense',
    'description': 'Tracer-bullet protocol for the Rhylthyme Opentrons importer.',
    'apiLevel': '2.13',
}


def run(protocol):
    tips = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 2)
    pipette = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tips])

    pipette.pick_up_tip()
    pipette.aspirate(100, plate['A1'])
    pipette.dispense(100, plate['B1'])
    pipette.drop_tip()
