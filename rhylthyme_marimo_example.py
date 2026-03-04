import marimo

__generated_with = "0.19.7"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md("# Rhylthyme Timeline in Marimo")
    return


@app.cell
def _():
    import json

    from rhylthyme_web.rhylthyme import load_program_file
    from rhylthyme_web.web.web_visualizer import (
        extract_step_dependencies,
        generate_dag_html,
    )

    return extract_step_dependencies, generate_dag_html, json, load_program_file


@app.cell
def _(extract_step_dependencies, generate_dag_html, mo):
    def show_timeline(program, height="600px"):
        """Render a Rhylthyme program as an interactive timeline."""
        nodes, edges = extract_step_dependencies(program)
        resource_constraints = program.get("resourceConstraints", [])
        html = generate_dag_html(nodes, edges, program, None, resource_constraints)
        return mo.iframe(html, width="100%", height=height)

    return (show_timeline,)


@app.cell
def _(load_program_file, mo, show_timeline):
    program = load_program_file("programs/bakery_program_example.json")
    mo.output.replace(
        mo.vstack(
            [
                mo.md(
                    f"**{program['name']}** — "
                    f"{len(program['tracks'])} tracks, "
                    f"{sum(len(t['steps']) for t in program['tracks'])} steps"
                ),
                show_timeline(program),
            ]
        )
    )
    return (program,)


@app.cell
def _(mo):
    mo.md("## Build a program from scratch")
    return


@app.cell
def _(mo, show_timeline):
    my_program = {
        "programId": "morning-coffee",
        "name": "Morning Coffee",
        "version": "0.1.0",
        "tracks": [
            {
                "trackId": "brew",
                "name": "Brew Coffee",
                "steps": [
                    {
                        "stepId": "grind",
                        "name": "Grind Beans",
                        "task": "grinder",
                        "trigger": {"type": "programStart"},
                        "duration": {"type": "fixed", "seconds": 30},
                    },
                    {
                        "stepId": "pour-over",
                        "name": "Pour Over",
                        "task": "kettle",
                        "trigger": {"on": "grind"},
                        "duration": {"type": "fixed", "seconds": 240},
                    },
                ],
            },
            {
                "trackId": "water",
                "name": "Heat Water",
                "steps": [
                    {
                        "stepId": "boil",
                        "name": "Boil Water",
                        "task": "kettle",
                        "trigger": {"type": "programStart"},
                        "duration": {
                            "type": "variable",
                            "minSeconds": 120,
                            "maxSeconds": 180,
                            "defaultSeconds": 150,
                        },
                    },
                ],
            },
        ],
        "resourceConstraints": [
            {"task": "kettle", "maxConcurrent": 1},
            {"task": "grinder", "maxConcurrent": 1},
        ],
    }

    mo.output.replace(
        mo.vstack(
            [
                mo.md(f"**{my_program['name']}**"),
                show_timeline(my_program),
            ]
        )
    )
    return (my_program,)


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
