# Release validation

Version 1.0.0 is validated with isolated QA profiles. Production saved progress is kept outside the build and is never replaced by QA fixtures.

- 52 integration checks cover a visible 30-dog jail, pack idle animation, real wand impacts, cage removal, dog release, victory lighting, 30-orb completion, fireworks, restoration, disk saves, continued exploration, all puppies reaching the island, and Dad returning to normal.
- Projectile accuracy is isolated against a stationary wizard so rendering/frame throttling does not change the target between scripted aim samples. The packaged desktop game is also reviewed with normal game behavior.
- Six petting checks cover contact and control recovery for Ruffles and short/tall dogs. Hand height follows the new pack rig rather than the former dog mesh.
- Twelve saved-world checks verify enclosure geometry, hidden legacy anatomy, furniture clearance, restoration visibility, animal pairing compilation of all 20 custom gameplay Blueprints, normal save defaults and the shipping game mode.
- Four maze clearance checks verify the ordinary maze cannot reach the wizard, the secret path can, the components are separate, and wall spans do not overlap.
- Windows Shipping cooking/packaging must finish successfully, without puppy material compilation failures.
- The desktop smoke test covers loading the restored world, pause/options, confirmation buttons, screenshot/report files, display mode changes and save/exit.
- The public Git allowlist is scanned for credentials, private keys, oversized files, licensed raw art folders, and generated/private runtime data before publication.

Physical gamepad testing is not represented by the keyboard/mouse desktop checks. Developer QA artifacts and saves stay outside the public source and downloadable game.
