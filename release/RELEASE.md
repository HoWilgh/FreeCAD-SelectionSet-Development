# Releasing the SelectionSet macro for FreeCAD Addon Manager

This document describes how to prepare and share the SelectionSet macro so users can install it via FreeCAD’s **Addon Manager** (tested on FreeCAD 1.0.2 and 1.1). Where available, official FreeCAD documentation is referenced; the rest is a concise guide for this repo.

---

## Official FreeCAD documentation (use these when available)

- **Addon Academy — publishing an addon:** [freecad.github.io/Addon-Academy/Guides/Publishing/](https://freecad.github.io/Addon-Academy/Guides/Publishing/)
- **Installing macros:** [wiki.freecad.org/How_to_install_macros](https://wiki.freecad.org/How_to_install_macros)
- **FreeCAD-macros repo (official macro collection):** [github.com/FreeCAD/FreeCAD-macros](https://github.com/FreeCAD/FreeCAD-macros)
  – README explains how to submit a macro (fork, category folder, metadata, `__Files__`, PR). **Do not** add `package.xml` when submitting to that repo.
- **Package Metadata (own repo with package.xml):** [wiki.freecad.org/Package_Metadata](https://wiki.freecad.org/Package_Metadata)
  – Describes the `package.xml` format for addons (including macros) hosted in your own Git repository so the Addon Manager can install them.
- **Macro documentation on the wiki:** [wiki.freecad.org/Macro_documentation](https://wiki.freecad.org/Macro_documentation)

If the wiki is temporarily unavailable, the [FreeCAD-macros README](https://github.com/FreeCAD/FreeCAD-macros#readme) and the [AddonManager source](https://github.com/FreeCAD/AddonManager) are the main technical references.

---

## Three ways to get the macro into Addon Manager (official options)

From the [FreeCAD-macros README](https://github.com/FreeCAD/FreeCAD-macros#ways-to-submit-a-macro-for-other-freecad-users) (three mutually exclusive options):

1. **Submit to [FreeCAD/FreeCAD-macros](https://github.com/FreeCAD/FreeCAD-macros)**
   Put the macro and auxiliary files in a category folder. Use `__Files__` in the macro to list every file to install. No `package.xml`. Good for single-file or few-file macros.

2. **Add the macro to the [FreeCAD wiki Macros recipes](https://wiki.freecad.org/Macros_recipes)**
   The Addon Manager also indexes macros from the wiki.

3. **Host the macro in your own Git repo with a [package.xml](https://wiki.freecad.org/Package_Metadata)**
   Addon Manager can install from a custom source (user adds your repo URL in Addon Manager preferences). Best when the macro has many files (e.g. multiple `.py`, `icons/`, tests).

**Recommendation for SelectionSet:** Use **option 3** (own GitHub repo + `package.xml`), because the macro has several Python modules, icons, and optional test/script files. The FreeCAD-macros README suggests a separate repository when the file list is long.

---

## Releasing via your own GitHub repo (option 3)

### 1. Repository layout and files not for the addon

**Do not ship these with the addon** (development only): `rules.md`, `TODO.md`. They are listed in `.gitignore` so the repository used as the Addon Manager source does not contain them; installs will not get them. Keep them locally or in a separate dev branch if you need version control for them. If they were already committed, run `git rm --cached rules.md TODO.md` and commit so they stop being tracked in the release repo.

Keep the layout that works when the macro is run from its folder (path in `sys.path`, `icons/` next to the entry point). For example:

- **Entry point:** `SelectionSet.FCMacro`
- **Required:** `selection_set_core.py`, `highlight_subelements.py`, `icons/SelectionSet.svg`, `icons/SelectionSetLink.svg`
- **Optional for users:** `selection_set_tests.py`, `run_macro_and_tests_at_startup.py` / `.FCMacro`, `README.md`, scripts under `run_*.sh` etc.

The Addon Manager will clone or download the repo and run the macro from that directory; the macro already uses `os.path.dirname(os.path.abspath(__file__))` so the folder is on `sys.path` and `icons/` resolve correctly.

### 2. Add `package.xml` in the repo root

Create a `package.xml` that describes the addon for the Addon Manager. The exact schema is on the wiki [Package_Metadata](https://wiki.freecad.org/Package_Metadata); a typical minimal structure for a **Macro** addon is:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<package format="1" xmlns="https://wiki.freecad.org/Package_Metadata">
  <name>SelectionSet</name>
  <description>Volume-based selection of faces or solids. SelectionSet and SelectionSetLink for FEM and other references.</description>
  <version>1.0.1</version>
  <date>2025-03-01</date>
  <maintainer email="your@email.example">Your Name</maintainer>
  <license file="LICENSE">LGPL-2.1-or-later</license>
  <url type="repository" branch="main">https://github.com/YOUR_USERNAME/FreeCAD_macro_SelectionSet</url>
  <icon>icons/SelectionSet.svg</icon>
  <content>
    <macro name="SelectionSet"/>
  </content>
  <dependencies>
    <freecad_min_version>1.0.0</freecad_min_version>
  </dependencies>
</package>
```

- Replace `YOUR_USERNAME`, `your@email.example`, `Your Name`, and `LICENSE` / license text as needed. Do not publish the current template values.
- `content/macro name` must match the entry point filename without extension (`SelectionSet` for `SelectionSet.FCMacro`).
- Adjust `version` and `date` for each release.

If the wiki documents more required or recommended tags (e.g. `tag`, `communication`), add them.

### 3. Add a LICENSE file

Add a `LICENSE` file in the repo root (e.g. LGPL-2.1-or-later) and reference it in `package.xml` as above.

### 4. How users install (custom source)

1. In FreeCAD: **Tools → Addon Manager**.
2. In Addon Manager preferences/settings, add a **custom addon source**: your repo URL (e.g. `https://github.com/YOUR_USERNAME/FreeCAD_macro_SelectionSet`).
3. Refresh the list; **SelectionSet** should appear. Install/update from there.

The Addon Manager will use `package.xml` to know it’s a macro and which file to run.

### 5. Optional: also list on the wiki or FreeCAD-macros

- **Wiki:** Add a short entry or link under [Macros recipes](https://wiki.freecad.org/Macros_recipes) pointing to your repo and README.
- **FreeCAD-macros:** If you later split out a minimal “single macro + few files” version, you can submit that to [FreeCAD/FreeCAD-macros](https://github.com/FreeCAD/FreeCAD-macros) with `__Files__` and no `package.xml`, so it appears in the default Addon Manager catalog without users adding a custom source.

---

## Checklist before release

- [ ] Version and date in `package.xml` and in code (e.g. `selection_set_core.__version__`) match.
- [ ] `README.md` has install instructions (Addon Manager custom source + link to this release doc or wiki).
- [ ] The standalone `src/macro/README.md` contains only macro installation and usage guidance; development commands and release preparation remain in the development repository documentation.
- [ ] The development-root `README.md` documents the development project and is not copied into the standalone macro package.
- [ ] `LICENSE` file present and referenced in `package.xml`.
- [ ] `rules.md` and `TODO.md` are not in the repo (they are in `.gitignore`; do not add them to the addon).
- [ ] Test install from a clean clone (run `SelectionSet.FCMacro` as macro in FreeCAD 1.0.2 and 1.1).
- [ ] Optional: disable or gate debug output by default for end users.

---

## Summary

| Goal | Use |
|------|-----|
| Official docs | [AddonManager](https://wiki.freecad.org/AddonManager), [How_to_install_macros](https://wiki.freecad.org/How_to_install_macros), [Package_Metadata](https://wiki.freecad.org/Package_Metadata), [FreeCAD-macros](https://github.com/FreeCAD/FreeCAD-macros) |
| This macro (many files) | Own GitHub repo + `package.xml`; users add repo as custom source in Addon Manager |
| Single-file macro | Submit to FreeCAD-macros with `__Files__`, or publish on wiki |

If the wiki or links change, the FreeCAD project may publish updated instructions; prefer the official documentation over this file when it exists.
