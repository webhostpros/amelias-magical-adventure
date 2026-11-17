# Third-party assets and source boundaries

The playable Windows release incorporates licensed assets in cooked Unreal containers. Raw licensed meshes, animations, textures, music, and sound libraries are not included in this public source repository. Obtain them through the appropriate Fab/Epic license before editing or rebuilding.

Principal content dependencies:

| Content path | Dependency |
|---|---|
| `/Game/Animals_Free` | ithappy, **Animals FREE - Low Poly 3D Models Pack**. Dog, cat, horse, chicken, deer, and matching animations. [Fab listing](https://www.fab.com/listings/0c8f3917-2461-4775-a853-b995bb93bac5) |
| `/Game/Medieval_Castle` | **Stylized Medieval Castle**, castle architecture, interior furniture, foliage and textures |
| `/Game/Fab` | Licensed Amelia and father character packs |
| `/Game/Wizard*` and related imported character paths | **Wizard for Battle Polyart** |
| `/Game/Free_Fantasy_Music_Pack` | **Free Fantasy Music Pack** |
| `/Game/Interface_And_Item_Sounds` | **Interface & Item Sounds Pack** |
| Sea/wave content paths | **Procedural Sea Waves** |
| `/Game/Characters`, template content | Epic Unreal template skeletons, locomotion and animation assets |

`Docs/asset-dependencies.json` records external package paths referenced by the published game assets. Names and paths are for setup, not a substitute for acquiring the correct license.

The local project also contains derived licensed character, dog, castle and audio assets under `/Game/AmeliasAdventure/Characters`, `Living`, `Interior`, `Rescue`, `Audio`, and related art folders. These stay outside public Git. Original Blueprints and material graphs retain references to them. Restore those derived assets from an authorized private project backup when rebuilding this exact release. Public consumers should use the complete packaged release to play.

Ruffles' coat treatment, Adeline naming, the adventure game logic, level arrangement and restoration behavior are project customizations. The underlying character and animal artwork retains its original rights. Fab's governing terms are available at [fab.com/eula](https://www.fab.com/eula). Unreal Engine licensing remains governed by Epic.

No personal reference photographs, saved-game files, downloaded authoring applications, credentials, editor logs or QA profiles are intentionally distributed.
