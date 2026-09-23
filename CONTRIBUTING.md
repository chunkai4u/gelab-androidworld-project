# Team workflow

1. Pick an issue and agree on its owner.
2. Create a branch such as `fix/emulator-stability` or `fix/text-input`.
3. Keep each pull request focused and describe the change, evidence, and remaining limitations.
4. Work that only reviews code, logs, or documentation does not require AndroidWorld locally. Use one reference experiment machine until the environment is stable.
5. Do not run competing experiments on the same emulator or change its settings during another run.
6. Before formal evaluation, freeze the code revision, model, device settings, task seeds, and step budgets. Record every run, including failures.

The current Wi-Fi example is a historical development success. The current graphics and text-input candidate is still unverified. Keep these distinctions in reports and pull requests.

Never commit private keys, credentials, model weights, virtual environments, emulator disks, or videos. Use your own authorized cloud access; store videos separately and link them from result summaries.
