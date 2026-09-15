# Gold set for agent-authored programs

Expert-authored programs paired with the text they were extracted from.
`rhylthyme eval-prompts` scores a model's program against these, component
by component (steps, durations, resources, actors, relationships, tracks,
end-to-end), so a change to the `plan_schedule` prompt or the extraction
guide is measured rather than eyeballed. Background: the PRD
`prd/prd-agent-prompt-structure.md` and the plan
`plans/agent-prompt-structure.md` in the monorepo root.

## Layout

```
gold/
  README.md               this file
  context.schema.json     JSON Schema for context.json
  <slug>/
    source.txt            the recipe / protocol / run sheet, plain UTF-8 text
    context.json          what the author knew besides the text
    program.json          the gold program (0.2.0-alpha schema)
```

The slug is `<domain>-<short-name>` in kebab case. It is the key the
scorer uses to pair a predicted program with its gold program
(`--predicted <dir>/<slug>.json` or `<dir>/<slug>/program.json`).

24 programs in the mix the PRD asks for (§5.1): 10 kitchen, 6 laboratory,
4 event, 4 fitness. `tests/test_gold.py` asserts those counts and that each
slug's prefix matches its domain (`laboratory` is spelled `lab` in slugs).

| Slug | Domain | Tracks | Steps | What it exercises |
|---|---|---|---|---|
| `kitchen-thanksgiving-one-oven` | kitchen | 8 | 24 | One oven shared by five dishes; everything joins at a serve step; holds with variable durations |
| `kitchen-weeknight-stir-fry` | kitchen | 4 | 15 | Two burners; wok work anchored to the rice coming off the heat; passive marinade on its own track |
| `kitchen-weekend-brunch` | kitchen | 5 | 13 | An inferred step (`preheat-oven`, `sourceSpan: null`); batter rest anchored to the bacon going in |
| `kitchen-backyard-barbecue-smoker-grill` | kitchen | 6 | 18 | An all-day smoker with a paper wrap partway and a variable cooler hold; the whole second half hangs off the hold's start; indefinite beans and a `manual` "cooks say it's ready" gate |
| `kitchen-country-loaf-bread-bake` | kitchen | 5 | 24 | A fermentation clock: variable levain ripen, bulk ferment and overnight retard; the dutch oven heats from a point inside the retard (`event: "start"` plus offset) and two boules bake in sequence |
| `kitchen-griddle-breakfast-for-six` | kitchen | 5 | 19 | One griddle as a strict queue (bacon, scrape, three pancake passes, heat drop, eggs); a warming oven held by a variable duration; three-way compound `all` at the serve |
| `kitchen-holiday-cookie-batch` | kitchen | 6 | 20 | Two queues at once, one oven and two pans that must cool before reloading, so the last bake carries a three-way compound trigger; an inferred tempering step borrowing the rolling sentence as its span |
| `kitchen-sheet-pan-chicken-dinner` | kitchen | 5 | 14 | Staggered sheet pans in one oven with a mid-roast rotate anchored twenty minutes into the chicken (`event: "start"` plus offset), and a salad dressed on an `afterStepWithBuffer` |
| `kitchen-soup-and-salad-lunch` | kitchen | 4 | 15 | Everything anchored on the moment the soup starts simmering (`event: "start"`); a variable "until the lentils are soft" simmer; salad dressed on a buffer off the reheat |
| `kitchen-two-burner-three-course-dinner` | kitchen | 4 | 20 | One oven booked twice (braise, then tart); service is a `manual` gate on the guests being seated, the main course is `indefinite`, and dessert is an `afterStepWithBuffer` on it |
| `lab-plasmid-miniprep-digest` | laboratory | 3 | 22 | Incubations, a shared microcentrifuge and gel rig, a gel cast in parallel, an inferred heat-block warm-up that borrows its span |
| `lab-cell-passaging-hood-incubator` | laboratory | 5 | 21 | Two flasks queueing for one biosafety cabinet, centrifuge and microscope; an inferred reagent warm-up borrowing a sentence span; overnight settle as a variable duration |
| `lab-elisa-plate-wash` | laboratory | 3 | 22 | Two plates staggered by `programStartOffset` through one plate washer; `indefinite` overnight coat; three identical wash sentences told apart by `occurrence` |
| `lab-microbiology-streak-and-incubate` | laboratory | 6 | 18 | A two-plate incubator shelf forcing the third plate to wait for the first to come out; two steps sharing one span; a `manual` supervisor sign-off before subculture |
| `lab-pcr-and-gel` | laboratory | 4 | 16 | A gel cast and set inside the cycling window (`event: "start"` plus offset into the thermocycler run); loading is a compound `all` on products, rig and ladder |
| `lab-western-blot-transfer-block` | laboratory | 5 | 21 | A single transfer tank and single-tray rocker serialising every stage; `afterStepWithBuffer` nested inside a compound `all` for the transfer sandwich; a 12-18 h variable primary |
| `event-product-launch-run-of-show` | event | 4 | 18 | Three `manual` gates (doors, keynote cue, host close), bounded Q&A as a variable duration |
| `event-conference-session-av-checks` | event | 4 | 20 | Three chair-called `manual` speaker gates; slide loads contending with the talks for one projector; one lapel pack forcing real changeover steps; variable Q&A |
| `event-theater-load-in-soundcheck` | event | 6 | 20 | Two trucks through one dock and one stage; a compound `all` soundcheck across PA, monitors and an inferred stage sweep (`sourceSpan: null`); doors on the house manager's call; indefinite show |
| `event-wedding-reception-timeline` | event | 5 | 19 | Two `manual` gates (the planner's room call, the MC's speech cue); three courses serialised on one kitchen pass; clearing anchored with `event: "start"` buffers; dancing indefinite |
| `fitness-partner-upper-body-supersets` | fitness | 2 | 28 | Two lifters handing off one bench, one pair of dumbbells and one bar; rest intervals; round 2 reuses round 1's span |
| `fitness-hiit-circuit-intervals` | fitness | 3 | 27 | Three athletes, four maxConcurrent-1 stations; every station entry a compound `all` on the athlete's own rest plus the athlete ahead leaving; per-round spans from the rotation table |
| `fitness-rowing-erg-interval-session` | fitness | 5 | 28 | Four rowers alternating on two ergs; the first pair's rests are `afterStepWithBuffer` gaps, the second pair's are the first pair's pieces; late entry via `programStartOffset` |
| `fitness-swim-practice-lane-assignments` | fitness | 4 | 20 | Three lanes as three tracks against one `lane` resource of 3; per-lane variable main sets joined by an `all` before a sprint set that serialises on one set of blocks; a coach's whiteboard `manual` gate |

## `source.txt`

150-600 words of plain text in the author's own words (no copyrighted
recipes or protocols). Write it the way such a text is actually written:
prose with headings, or numbered protocol steps. State durations the way a
person would ("about 20 minutes", "until it smokes, about 3 minutes",
"no less than 15 and no more than 25"). Leave some things implicit; that
is what the relationship-inference turn is for.

Do not edit `source.txt` after `program.json` is written without
re-checking every span: the spans are exact substrings.

## Source spans

Every step in `program.json` carries

```json
"metadata": {
  "sourceSpan": { "quote": "Roast the turkey for 3 hours", "occurrence": 1 }
}
```

* `quote` is an exact, case-sensitive substring of `source.txt`,
  including punctuation and the degree sign, micro sign and multiplication
  sign exactly as typed there.
* `occurrence` is the 1-based index of that substring in the text,
  counting non-overlapping matches left to right (the same way Python's
  `str.count` counts). It disambiguates repeated phrases such as
  "spin for 1 minute".
* Choose the shortest quote that identifies the activity **and** its
  duration or trigger cue. Two steps may share a span when one sentence
  yields two activities (the fitness gold does this for round 2).

Steps the author added that the text does not state are tagged

```json
"metadata": { "inferred": true, "sourceSpan": null }
```

or, where the inference is tied to a sentence (a heat block must be warm
before "Incubate at 37 °C"), `inferred: true` with that sentence as the
span. The scorer counts a *predicted* step with no gold match and no
locatable span as *unsupported* (a rate, not an error); gold inferred
steps are ordinary steps for scoring.

## `context.json`

Validated by `context.schema.json`:

| Field | Required | Meaning |
|---|---|---|
| `environmentType` | yes | Value for `program.environmentType`; fills the scenario slot of the T3 prompt |
| `domain` | yes | `kitchen`, `laboratory`, `event`, `fitness` or `other` (reporting category) |
| `constraints` | yes | Resource limits as a prompt would state them: `["one oven", "four burners", "two cooks"]` |
| `deadline` | no | Wall-clock `HH:MM`, ISO-8601, or a short phrase; omit when the source states none |
| `title`, `servesOrScale`, `notes` | no | Title, scale ("8 people", "2 lifters"), and authoring notes (judgement calls, why a step is inferred) |

## Authoring rules

1. **Validate with both validators.** `rhylthyme validate gold/<slug>/program.json`
   (schema + logic, including in-track overlaps) and the JavaScript
   validator in `rhylthyme-server/mcp-api/schedule.js`. `tests/test_gold.py`
   runs both (the JS one when `node` is on the path).
2. **Every step has `metadata.sourceSpan`** (or `inferred: true` with a
   `null` span). `tests/test_gold.py` locates every quote at its stated
   occurrence.
3. **Use tracks for parallel lines of work** and `afterStep` across tracks
   wherever the text implies a dependency ("as soon as the turkey comes
   out", "B takes the bench as soon as A racks the bar"). Joins that wait on
   several tracks use a compound trigger `{"logic": "all", "triggers": [...]}`.
4. **Respect the declared resources.** With `oven: maxConcurrent 1` no two
   oven steps may overlap in the resolved timeline. Check the timeline
   (`rhylthyme plan`, or the MCP `analyze_schedule` tool) before committing.
5. **Durations follow the text.** Fixed when the text gives one number;
   `variable` with `minSeconds`/`maxSeconds`/`defaultSeconds` when it gives
   a range or a hold "until everything else is ready"; `indefinite` only
   for true open-ended waits. Give every variable duration a
   `defaultSeconds`: the resolvers use it for the makespan.
6. **Manual gates are `{"type": "manual"}`** on the step that waits for a
   human call; the resolvers place it after its in-track predecessor, so
   put it in the track whose previous step is what it really waits for.
7. **Step ids are global, kebab-case, and stable.** Predicted programs are
   matched by span and name, not by id, but the ids appear in reports.
8. **No `replicates`, `trackTemplates` or `environment` references.** Gold
   programs are fully expanded and self-contained
   (`environmentType` + `resourceConstraints`).

## Adding a program

1. Create `gold/<domain>-<short-name>/` with `source.txt` and
   `context.json`.
2. Write `program.json` by hand (a small Python script that builds the
   dict is fine; commit only the JSON). Give every step a span.
3. Run, from the monorepo root:
   ```bash
   source .venv/bin/activate
   cd rhylthyme-examples && python -m pytest -q tests/test_gold.py
   cd ../rhylthyme-cli-runner && python -m pytest -q tests/test_eval_scorer.py -k self
   ```
   The second command scores every gold program against itself and must
   report 1.0 on every component.
4. Add the row to the table above, and update `REQUIRED_DOMAINS` in
   `tests/test_gold.py`: the domain counts are asserted exactly, so a new
   program is also a decision about the mix.
