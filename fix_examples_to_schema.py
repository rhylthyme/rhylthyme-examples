import os
import json
import yaml
from glob import glob
from copy import deepcopy

SCHEMA_PATH = '../rhylthyme-spec/schemas/program_schema_0.2.0-alpha.json'
EXAMPLES_DIR = '../rhylthyme-examples/programs/'

# Helper: load JSON or YAML
def load_program(path):
    with open(path, 'r') as f:
        if path.endswith('.json'):
            return json.load(f)
        else:
            return yaml.safe_load(f)

def save_program(path, data):
    with open(path, 'w') as f:
        if path.endswith('.json'):
            json.dump(data, f, indent=2)
        else:
            yaml.dump(data, f, default_flow_style=False)

def fix_resource_constraints(rcs):
    fixed = []
    for rc in rcs:
        rc = deepcopy(rc)
        # Remove deprecated fields
        rc.pop('type', None)
        rc.pop('capacity', None)
        # Ensure required fields
        if 'task' not in rc:
            rc['task'] = 'unknown-task'
        if 'maxConcurrent' not in rc:
            rc['maxConcurrent'] = 1
        fixed.append(rc)
    return fixed

def fix_step_trigger(trigger):
    # Convert old trigger types to schema-compliant
    if isinstance(trigger, dict):
        t = trigger.get('type')
        if t == 'stepComplete':
            return {'type': 'afterStep', 'stepId': trigger.get('stepId')}
        if t == 'stepStart':
            return {'type': 'afterStep', 'stepId': trigger.get('stepId'), 'event': 'start'}
        if t == 'programStartOffset':
            return {'type': 'programStartOffset', 'offsetSeconds': trigger.get('offsetSeconds', 0)}
        if t == 'manual':
            return {'type': 'manual', 'triggerName': trigger.get('triggerName', 'manual')}
        if t == 'programStart':
            return {'type': 'programStart'}
        if t == 'afterStep':
            return trigger
        if t == 'afterStepWithBuffer':
            return trigger
        if t == 'absolute':
            return trigger
        if t == 'offset':
            return trigger
        # Multi-trigger logic
        if 'logic' in trigger and 'triggers' in trigger:
            return {
                'logic': trigger['logic'],
                'triggers': [fix_step_trigger(tr) for tr in trigger['triggers']]
            }
    return trigger

def fix_step(step):
    step = deepcopy(step)
    # Ensure required fields
    if 'stepId' not in step:
        step['stepId'] = 'step-' + step.get('name', 'unnamed').replace(' ', '-').lower()
    if 'name' not in step:
        step['name'] = step['stepId']
    # Fix trigger
    if 'startTrigger' in step:
        step['startTrigger'] = fix_step_trigger(step['startTrigger'])
    # Fix duration
    if 'duration' in step and isinstance(step['duration'], (int, float)):
        step['duration'] = {'type': 'fixed', 'seconds': step['duration']}
    # Ensure task
    if 'task' not in step:
        # Try to infer from preBuffer or tasks
        if 'tasks' in step and step['tasks']:
            step['task'] = step['tasks'][0]
        elif 'preBuffer' in step and 'tasks' in step['preBuffer'] and step['preBuffer']['tasks']:
            step['task'] = step['preBuffer']['tasks'][0]
        else:
            step['task'] = 'unknown-task'
    return step

def fix_program(prog):
    prog = deepcopy(prog)
    changed = False
    # Top-level required fields
    if 'programId' not in prog:
        prog['programId'] = 'unknown-program'
        changed = True
    if 'name' not in prog:
        prog['name'] = prog['programId']
        changed = True
    if 'tracks' not in prog:
        prog['tracks'] = []
        changed = True
    # Environment or resourceConstraints
    if 'environmentType' not in prog and 'environment' not in prog and 'resourceConstraints' not in prog:
        prog['environmentType'] = 'test'
        changed = True
    # Fix resourceConstraints
    if 'resourceConstraints' in prog:
        orig = json.dumps(prog['resourceConstraints'], sort_keys=True)
        prog['resourceConstraints'] = fix_resource_constraints(prog['resourceConstraints'])
        if json.dumps(prog['resourceConstraints'], sort_keys=True) != orig:
            changed = True
    # Fix tracks/steps
    for track in prog.get('tracks', []):
        if 'steps' in track:
            for i, step in enumerate(track['steps']):
                fixed = fix_step(step)
                if fixed != step:
                    track['steps'][i] = fixed
                    changed = True
    return prog, changed

def main():
    files = glob(os.path.join(EXAMPLES_DIR, '*.json')) + glob(os.path.join(EXAMPLES_DIR, '*.yaml')) + glob(os.path.join(EXAMPLES_DIR, '*.yml'))
    print(f"Found {len(files)} example files.")
    for path in files:
        try:
            orig = load_program(path)
            fixed, changed = fix_program(orig)
            if changed:
                save_program(path, fixed)
                print(f"[FIXED] {os.path.basename(path)}")
            else:
                print(f"[OK]    {os.path.basename(path)}")
        except Exception as e:
            print(f"[ERROR]  {os.path.basename(path)}: {e}")

if __name__ == '__main__':
    main()