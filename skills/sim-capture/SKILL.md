---
name: sim-capture
description: Capture fresh iOS simulator screenshots of an app while the user drives it, then crop and pad them to a target aspect ratio.
disable-model-invocation: true
---

# Sim capture

## 1. Agree the shot list

Ask which screens are needed and where the images should go (existing asset paths or a new folder).
Record each target by the screen name the user navigates to. If replacing an asset, open it and
describe its current screen so the user can confirm it.

Read the layout that consumes the images and record its enforced aspect ratio. A fixed
`aspectRatio` with `resizeMode="contain"` makes that ratio a hard output constraint.

Done when every target, destination, and output ratio is recorded.

## 2. Stage the app

Make the app look like the product:

- **Seed data.** Write directly to the app's store (SQLite in the data container or an AsyncStorage
  manifest) instead of tapping through creation flows. Back up the store first, relaunch after
  changing it, and tell the user what changed so it can be restored.
- **Hide dev chrome.** Have the user disable the Expo dev-client floating gear in dev-client
  settings; it appears in screenshots and cannot be hidden by the capture tools.
- **Set appearance.** Run `xcrun simctl ui booted appearance light|dark` for the intended theme.

Done when the app is staged, the backup path is recorded, and the intended appearance is set.

## 3. Run the loop while the user drives

Start the poller in the background, then give the user the exact navigation path and ask them to
reply when finished:

```bash
bash <skill>/scripts/capture_loop.sh <out-dir> 1.5 120 &
```

The arguments are output directory, poll interval, and duration in seconds. The poller saves only
frames with an md5 not seen earlier in that run.

Identify the frames with contact sheets:

```bash
python3 <skill>/scripts/contact_sheet.py <out-dir> <out-dir>/sheet 12 6
```

Use the filename labels to identify frames; open any candidate at full size. Repeat the loop for
missing targets.

Done when every target has a confirmed source frame identified by filename.

## 4. Crop and pad

Crop below the status bar and above any floating tab bar. Set `bottom` as a y coordinate from the
top edge; use `0` to crop to the frame's bottom. Pad to the exact ratio from step 1 with the
frame's background color:

```bash
python3 <skill>/scripts/crop_pad.py <frame.png> <asset.jpeg> <top> <bottom> 9:16
```

Done when every output's printed dimensions match the required ratio exactly.

## 5. Verify in the app

Render the state that displays the new images (for example, reset the onboarding flag or navigate
to the relevant screen), capture a frame, and inspect it. Check that the copy beside each image
still describes what it shows; report drift instead of editing it silently.

List every simulator state change you made, including seeded rows, appearance, cleared flags, and
backup paths, so the user can restore the desired state.

Done when each asset has been checked in its consuming UI, copy drift is reported, and all state
changes are documented.
