# Results

Every run the team reports ends up here, following the Day 1 rule that the run log is the Friday presentation:

- **[`runs.csv`](runs.csv)** has one row per run: task, run number, label, model, observation, grounding, steps against the budget, time, the official verifier result, the failure class and where the evidence is. Add a row for every run, including failures and infrastructure errors.
- **[`development/`](development/)** holds development attempts. They show progress but never count towards a success rate.
- **[`formal/`](formal/)** holds the nine formal runs (three tasks × three runs). They start only after the code, model, device settings, seeds and step budgets are frozen.

Each run folder keeps the files the harness writes: `result.json`, `trajectory.jsonl`, the final screenshot and, when it is small enough, `recording.mp4`. Larger videos go to shared storage and are linked from the row.

Use one of the five failure classes from the course, and only these: `grounding`, `too_early`, `lost_value`, `wrong_app`, `false_done`. Leave the column empty when the verifier says PASS.
