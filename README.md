# Amelia The Brave
## Chapter 1: Save Ruffles

A magical island adventure about Amelia, her dad, Adeline the doll, and thirty rescued puppies.

### Play on Windows

Download the Windows ZIP from **Releases**, extract the whole ZIP, then double-click **Play Amelia.cmd**. Keep the `Windows` folder beside the launcher. Unreal Engine does not need to be installed. If Windows asks for Unreal prerequisites, install the prerequisite package included under `Windows/Engine/Extras/Redist/en-us`.

Use the cog menu for pause, save, exit, sound levels, screenshots/reports, and fullscreen/windowed mode. The game automatically saves adventure items and wizard victory. Exiting without saving discards changes since the last save. Start over is a separate confirmed action.

Existing progress uses `%LOCALAPPDATA%/ameliasadventure1/Saved/SaveGames/AmeliaChapter1.sav`. Updating the game files keeps that save. Back it up before choosing Start over.

### Controls

- Move: WASD or left stick. Look: mouse or right stick.
- Jump: Space or controller A. Run: stick click.
- Wand: right trigger / left click to shoot; left trigger / right click to aim. Crosshairs appear while aiming.
- Adventure bag: X. Scroll/map and interactions also display their controls in game.
- Cog: click the upper-right cog, or use the settings shortcut shown in game.

### Report a bug

Launch through **Play Amelia.cmd**, open the cog, and select **Screenshot + report**. A matching PNG and TXT appear on your Windows desktop. Add what happened and what you expected to the text file, then attach both to your report. Nothing uploads automatically. Avoid screenshots containing personal information before posting publicly.

### Source and asset setup

This repository contains the original game Blueprints, level layout, original material graphs, configuration, and maintenance tools. It deliberately excludes licensed Fab/Epic source art, character meshes, animation clips, audio, local saves, private reference images, and generated build files. The Windows release includes the complete playable game with cooked assets.

Editing or rebuilding the source requires Unreal Engine **5.8**, the licensed dependencies and their original `/Game/` paths, plus the locally authored derivatives described in [THIRD_PARTY_ASSETS.md](THIRD_PARTY_ASSETS.md). A bare clone is not a self-contained art source distribution. Public availability does not grant a separate license to redistribute third-party source assets.

The current saved Blueprints are authoritative. The tools are maintenance scripts, not a command to rebuild the entire historical project. Run only the specific tool needed, after backing up the level.

### Build

After restoring the licensed dependencies, package `/Game/AmeliasAdventure/Lvl_AmeliasAdventure` for Windows Shipping using Unreal 5.8. Blueprint-only projects can use Epic's installed prebuilt Windows game binaries. See [Docs/TESTING.md](Docs/TESTING.md) for release validation.

No general open-source license is granted by this repository. Original project content remains copyright its owner; third-party assets retain their respective licenses.
