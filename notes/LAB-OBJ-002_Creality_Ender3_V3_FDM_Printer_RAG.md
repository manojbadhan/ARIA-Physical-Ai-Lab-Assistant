# Lab Object Knowledge Record: Creality Ender-3 V3 Series FDM 3D Printer

**Record ID:** LAB-OBJ-002  
**Object category:** Filament (FDM/FFF) 3D printer  
**Visual identification:** A black Creality-branded open-frame 3D printer. It has a moving bed ("bed-slinger" style) with a flexible, magnetic PEI-type build plate marked "220 x 220 mm" and "Warning hot surface", a black direct-drive print head with the Creality logo and a round fan on the front, a gantry frame with a filament spool holder arm on top, a small sensor box with an arrow icon on the top crossbar, and a separate flat touchscreen unit sitting on the bench to the right of the base. A sticker reading "Integrity, Innovation, Responsibility, Teamwork, Win-Win" is on the top-right of the frame.  
**Identification confidence:** High for "Creality Ender-3 V3 family FDM printer". **Likely Ender-3 V3 KE, with Ender-3 V3 SE as the main alternative. The exact model is not confirmed from the photos alone.** Check the label on the base/rear and the touchscreen/boot screen before treating model-specific specifications as certain.

> **Disambiguation for the robot:** This object (LAB-OBJ-002) is a **filament 3D printer** that melts plastic filament. It is **not** the Creality Wash and Cure machine (LAB-OBJ-001), which post-processes **resin** prints. The orange translucent object partly visible at the left edge of the photos is most likely LAB-OBJ-001. The two machines are not interchangeable, and printed filament parts do **not** go into the wash/cure machine.

## 1. Short answer for the robot

This is most likely a **Creality Ender-3 V3 KE** (possibly an **Ender-3 V3 SE**), a compact desktop **FDM (Fused Deposition Modeling) 3D printer**. It builds a physical object layer by layer by heating plastic filament and extruding it through a nozzle onto a heated build plate, following a sliced digital model (G-code).

It is not a resin printer, a laser cutter, or a CNC machine. It needs a slicer program on a computer to prepare files, and a spool of 1.75 mm filament to print.

## 2. What is it used for?

- Printing prototypes, models, brackets, enclosures, jigs and fixtures, and teaching/demo parts.
- Learning the 3D-printing workflow: design → slice → print → remove and finish.
- Everyday functional parts in materials such as PLA and PETG (the KE also lists higher-speed PLA, ABS, ASA, and TPU 95A support; check the filament and settings for your unit).

Maximum object size is about **220 × 220 mm on the bed**, with a height of about **240 mm (KE)** or **250 mm (SE)**.

## 3. How does it work?

1. **Slicing (on a computer):** A model file (STL, OBJ, 3MF, or AMF) is opened in a slicer such as Creality Print or another compatible slicer. The slicer cuts the model into layers and produces G-code.
2. **Transfer:** The G-code reaches the printer by USB drive. The KE also supports Wi-Fi/LAN and the Creality Cloud app; the SE is mainly USB/SD-based. Confirm for the exact model.
3. **Heating:** The nozzle and the heated bed warm to the temperatures set for the filament.
4. **Auto-levelling:** A probe measures the bed surface at several points so the printer can compensate for slight tilt or unevenness. Bed levelling and Z-offset are largely automatic on this family.
5. **Printing:** The direct-drive extruder pushes filament into the hot nozzle. The print head moves left and right (X axis) and up and down (Z axis, on the frame). The bed moves forward and backward (Y axis). The model is built from the bottom layer upward.
6. **Cooling and removal:** The cooling fans on the print head solidify the plastic. After printing, the bed cools and the part is removed.

## 4. Visible parts in the photographs

| Visible part | Name | Function |
|---|---|---|
| Large black base with "CREALITY" in front | Base / housing | Holds the Y-axis mechanism, mainboard and power supply (power supply integrated on this family). |
| Flat bed with "220 x 220 mm" and "Warning hot surface" marks | Heated build plate (flexible PEI-type spring-steel sheet on a magnetic heated bed) | The surface the print sticks to. It is hot during use and can be flexed or lifted off after cooling to release the part. |
| Black print head with "CREALITY" logo | Direct-drive "Sprite" extruder and hotend assembly | Grips and pushes filament, melts it in the hotend and deposits it through the nozzle. |
| Round fan grille on the front of the print head | Part-cooling fan | Cools freshly deposited plastic. |
| Yellow "Caution hot" labels near the print head | Hot-surface warnings | The hotend and nozzle can be extremely hot. |
| Black horizontal beam with row of holes | X-axis beam | Carries the print head left and right. |
| Vertical frame posts with a threaded rod visible on one side | Z-axis frame and lead screw | Moves the X beam up and down to set the layer height. |
| Black rectangular top frame | Gantry top crossbar | Gives the frame rigidity; supports the spool holder. |
| Slotted black arm rising from the top | Filament spool holder | Holds the filament spool above the printer so the filament feeds down to the print head. |
| Small box with arrow icon on the top crossbar | Probable filament runout/filament sensor | Detects when filament is missing or runs out (its exact function should be confirmed on the unit). |
| Black braided sleeve | Cable sleeve | Protects the wiring to the print head and bed. |
| Flat black rectangular unit to the right | Touchscreen / display | The printer's user interface. Appears detached or placed on the bench beside the printer in the photo. |
| Yellow triangle label near the front of the base | Moving-parts / pinch-point warning | Warns that the bed and axes can move and trap fingers. |
| Sticker on the frame | Company/lab sticker | Decorative; not a machine component. |

**Other items visible in the photos (not part of the printer):**
- An aerosol can with an orange/black label partially visible on the left. This looks like a hair-spray-type product. Some users spray adhesive products on the bed to help prints stick, but this is **not required or recommended by Creality for the PEI plate**. It is a **flammable aerosol**, so it should be kept away from the hot printer and stored properly.
- A red fire extinguisher at the left of the photo (lab safety equipment).
- Wooden or cardboard filament spool cores (an eSUN-branded spool core is visible) and cables on the bench.
- A second printer is partly visible at the right edge of image 2.
- Some faint smudges or residue are visible on the bed surface in image 1. This is likely adhesive or oil residue and may need cleaning (see maintenance).

## 5. Controls and interface

The touchscreen (KE: 4.3-inch colour touchscreen) is the main control. The SE uses a 3.2-inch colour knob screen instead. Exact menu names vary with firmware version. Typical functions:

- **Print / Files:** choose a G-code file from USB (or cloud/network on the KE) and start it.
- **Prepare / Control:** home axes, move axes, preheat, extrude/retract filament, turn fans on or off.
- **Auto-levelling / Self-test:** runs automatic bed measurement and Z-offset calibration. On the KE there is a one-tap self-test calibration.
- **Temperature:** set the nozzle and bed target temperatures.
- **Speed/Flow:** adjust print speed during a print.
- **Pause / Resume / Stop:** control a running job.
- **Settings:** Wi-Fi, language, firmware, power-loss recovery and similar.

There is a power switch on the base or rear. Check the actual unit for its position.

## 6. General operating guide

This is a **general guide for the Ender-3 V3 family (likely KE)**. It is not a substitute for the exact model's manual. Confirm the model first.

### Before starting
1. Place the printer on a stable, level, non-flammable surface with space around it for the moving bed (about 40 cm of clearance front and back is a sensible rule).
2. Keep it away from curtains, paper piles, aerosols, solvents and other flammable items.
3. Check that the power cable, spool holder, filament sensor cable and touchscreen cable are connected and undamaged.
4. Check the voltage selector (if fitted) matches local mains supply. The family is rated for roughly 100–240 V and 350 W; confirm on the unit.
5. Make sure the bed is clean and nothing is on or under the print area.

### A. Loading filament
1. Hang a 1.75 mm filament spool on the top holder so it unwinds freely without tangling.
2. Cut the filament tip at an angle with scissors or a cutter.
3. From the touchscreen, preheat the nozzle to the temperature printed on the filament spool.
4. Use the screen's **Extrude / Load** function (one-tap loading is available on this family). Feed the filament in until it flows from the nozzle.
5. Clean off any extruded blob with tweezers or a cloth. **Do not touch the nozzle with bare fingers.**

### B. Preparing and starting a print
1. Slice the model in a compatible slicer. Choose the correct printer profile, nozzle (0.4 mm default), filament type, and layer height (supported range about 0.1–0.35 mm).
2. Save the G-code to a USB drive. On the KE, send it over Wi-Fi or the Creality app instead if configured.
3. Insert the USB drive and choose the file on the touchscreen.
4. Run **auto-levelling/self-test** if starting a new setup, after moving the printer, after changing the nozzle or build plate, or if the first layer looks wrong.
5. Start the print. Watch the **first layer**, as most failures start here. It should be a smooth, slightly squished, continuous line without gaps or curling.

### C. During printing
- Do not reach into the print area while axes are moving.
- Do not touch the nozzle, heated bed, or heater block (both can exceed 60 °C on the bed and 200 °C on the nozzle).
- Do not leave the printer running unattended in an unsupervised lab. Follow the lab supervisor's rules.
- Use **Pause** if you need to stop to change filament. Use **Stop** only if the print has failed or there is danger.

### D. After printing
1. Let the bed cool. A cooled bed helps the part release.
2. Remove the flexible plate (if it is the magnetic type) and bend it gently, or lift the part off carefully. Do not pry the part off with a metal blade against the PEI surface.
3. Remove supports and clean up the part with side cutters or a deburring tool.
4. Switch off and unplug the printer if it will not be used soon. Leave the spool dry and sealed.

### E. Changing filament
1. Heat the nozzle to the temperature of the filament currently loaded.
2. Use the **Retract/Unload** function. Pull the old filament out once it releases.
3. Load the new filament as in section A.

## 7. Safety precautions

- **Burns:** The hotend (up to 300 °C on the KE, 260 °C on the SE) and the bed (up to 100 °C) can cause serious burns. Wait for them to cool before touching them.
- **Moving parts and pinch points:** Keep hands, hair, and loose clothing away from the axes and the moving bed during printing and homing.
- **Fire safety:** Never leave a printer running unattended without lab approval. Keep flammables away, including aerosols, solvents, and alcohol. Know the location of the fire extinguisher (a red extinguisher is visible in the lab photo). Do not spray aerosols near the printer while it is hot or powered.
- **Electrical:** Use the supplied power cable, plug into a grounded socket, and do not open the base or touch internal electronics while powered. Disconnect power before inspecting or changing electrical parts. Do not use if cable or plug is damaged.
- **Fumes:** Heated plastics release fine particles and fumes. Use in a ventilated area. ABS and ASA need extra ventilation, and an enclosure is recommended for them, which this open-frame printer lacks.
- **Sharp tools:** Use scrapers, cutters, and nozzle-cleaning needles carefully, and away from your body.
- **Do not bypass safety features** such as thermal protection or the filament sensor.
- **Eyes:** Wear safety glasses when trimming supports or clipping filament.
- **Wi-Fi/Cloud:** Do not leave a remotely started print unattended.

## 8. Maintenance

| Task | Suggested frequency | Notes |
|---|---|---|
| Wipe build plate with isopropyl alcohol (IPA) | Before each print or when prints stop sticking | Use a lint-free cloth, with the bed cool and the printer unplugged or idle. Keep IPA away from the hot bed and from ignition sources. Fingerprints and oils reduce adhesion. |
| Remove adhesive/hairspray residue from the plate | When visible | Wash with warm water and mild dish soap or follow the manufacturer's guidance, then dry fully. |
| Check/clean nozzle | When under-extruding or oozing | Heat the nozzle, then clean with a brass brush or cleaning needle (carefully). |
| Replace nozzle | When worn or clogged | Do this only when the nozzle is hot or following the manual's procedure. Tighten as directed. Use the proper spanner. |
| Check belts, wheels/rails and screws | Monthly or if prints show layer shifts or ringing | Belts should be taut and not loose. Don't over-tighten. |
| Lubricate Z lead screw and rails | Every few months or when noisy | Use a light machine/PTFE-based lubricant sparingly as recommended by Creality. |
| Clean fans and cooling ducts | Monthly | Disconnect power first. |
| Store filament | Always | Keep PLA/PETG/TPU dry in a sealed bag with desiccant. |
| Update firmware | As needed | Use only firmware published by Creality for the exact model. A wrong firmware file can disable the printer. |

## 9. Basic troubleshooting

| Symptom | Possible checks |
|---|---|
| Printer will not power on | Check the wall outlet, power cable, power switch, and the voltage selector (if present). Do not open the housing. |
| Touchscreen is blank or unresponsive | Check the screen cable at both ends and power-cycle the printer. If damaged, report it to the supervisor. |
| First layer does not stick | Clean the plate with IPA. Run auto-levelling. Check the Z-offset, bed temperature, and the filament profile. Make sure the printing nozzle isn't too far from the bed. |
| Print detaches mid-print or warps | Raise the bed temperature in line with the filament guidance, clean the plate, use a brim, avoid draughts, and avoid printing ABS/ASA on an open frame. |
| Nozzle clogged / no filament comes out | Preheat, then try unload and reload. Cut the filament tip. If it persists, clear it with a cleaning needle or replace the nozzle. |
| Under-extrusion or gaps in layers | Check the spool for tangles, nozzle temperature, filament wetness, and partial clogs. Make sure the extruder gear is gripping the filament. |
| Stringing or oozing | Lower the nozzle temperature, dry the filament, and adjust retraction in the slicer. |
| Layer shifts | Check the belts, loose screws or wheels, cable snags, and speed settings. Slow down the print. |
| Ringing/ghosting (ripples near edges) | Reduce speed or acceleration. Check the printer is on a stable surface and its screws are tight. On the KE, input shaping/self-test can help. |
| Print stops with "filament" message | The runout sensor may have detected no filament. Check the spool, tangles, and sensor cable, and reload. |
| Temperature error / thermal runaway message | Power off at once and unplug. Check the thermistor/heater wiring only when cool. Don't continue to use it. Tell the supervisor. |
| Print starts then the nozzle digs into the bed | Re-run auto-levelling and check the Z-offset. Check the bed is seated properly and free of debris. |
| File not found or won't start | Use a correctly formatted USB drive (commonly FAT32) and put the G-code in the root or a simple folder. Avoid unusual characters in file names. |
| Strange smell, smoke, or sparks | Stop immediately, disconnect power if safe, and tell the supervisor. Do not use again until inspected. |

Do not dismantle the electronics or attempt internal repairs as a student operator.

## 10. Specifications — verify before using as exact facts

### Ender-3 V3 KE (most likely model)
| Item | Value |
|---|---|
| Technology | FDM |
| Build volume | 220 × 220 × 240 mm |
| Product dimensions | about 433 × 366 × 490 mm |
| Net / gross weight | about 7.8 kg / 9.9 kg |
| Typical / max print speed | 300 mm/s / up to 500 mm/s (tested with Hyper PLA) |
| Max acceleration | 8000 mm/s² |
| Layer height | 0.1–0.35 mm |
| Print accuracy | about ±0.1 mm |
| Filament diameter | 1.75 mm |
| Nozzle | 0.4 mm default |
| Max nozzle temperature | up to 300 °C |
| Max bed temperature | up to 100 °C |
| Extruder | "Sprite" direct-drive |
| Build surface | Flexible, removable PEI-type plate on a magnetic heated bed |
| Levelling | Automatic, with one-tap self-test |
| Display | 4.3-inch colour touchscreen |
| Connectivity | USB drive, Wi-Fi, LAN, Creality Cloud app |
| Filament runout sensor | Reported as included |
| Supported materials | Hyper PLA/PLA, PETG, ABS, TPU (95A), ASA |
| Slicer file formats | STL, OBJ, 3MF, AMF |
| Power | about 350 W, 100–240 V~, 50/60 Hz |

### Ender-3 V3 SE (alternative)
| Item | Value |
|---|---|
| Build volume | 220 × 220 × 250 mm |
| Product dimensions | about 349–420 × 366 × 490 mm (sources differ) |
| Net weight | about 7.1–7.3 kg (sources differ) |
| Typical / max print speed | 180 mm/s / 250 mm/s |
| Max acceleration | 2500 mm/s² |
| Max nozzle temperature | about 260 °C |
| Display | 3.2-inch colour knob screen |
| Extruder | "Sprite" direct-drive |
| Levelling | CR-Touch probe plus strain sensor for automatic Z-offset |
| Filament runout sensor | Listed as optional on Creality's page; confirm on the unit |
| Supported materials | PLA, PETG, TPU |

### How to tell the KE and SE apart on the physical unit
- **Screen:** a flat 4.3-inch touchscreen suggests the KE. A smaller screen with a rotary knob suggests the SE. The screen in the photo looks like a flat touchscreen.
- **Boot screen/menu:** the model name and firmware are usually shown in Settings → About.
- **Label:** check the rating label on the base or the packaging for the model name and serial number.
- **Top crossbar sensor:** a filament sensor fitted as standard points to the KE, but this may also be added to an SE.

## 11. User manual and software resources

- Creality supplies a printed quick-start guide in the box and a full user manual on its support/download page for the exact model.
- **Slicer:** Creality Print (free) is the usual choice. Other slicers can be used with the correct printer profile and nozzle/filament settings.
- **Mobile/cloud:** the Creality Cloud app is used for remote monitoring and starting prints on supported models (KE).
- **Firmware:** download only from Creality's official support page for the exact model and follow the update procedure in the manual.
- **Recommended first-run checklist for new lab users:**
  1. Check the printer is clean, level, and safe to run.
  2. Check the filament loaded matches the profile in the slicer.
  3. Run auto-levelling and confirm the first layer.
  4. Stay nearby for the first 10 minutes of a new job.
  5. Wait for cooling before removing the print.
  6. Log the job and tidy the area.

## 12. RAG-ready question and answer pairs

**Q: What is this object?**  
A: It appears to be a Creality Ender-3 V3 series FDM 3D printer, most likely the Ender-3 V3 KE (possibly the V3 SE). It melts plastic filament and builds objects layer by layer. The exact model needs confirmation from its label or the touchscreen's About page.

**Q: Is it the same as the wash and cure machine?**  
A: No. The wash and cure machine (LAB-OBJ-001) post-processes resin prints. This one is a filament printer, and its parts do not need washing or UV-curing.

**Q: What materials can it print?**  
A: PLA and PETG are the usual choices. The Ender-3 V3 KE also lists support for Hyper PLA, ABS, TPU (95A), and ASA. The SE lists PLA, PETG, and TPU. Always follow the filament manufacturer's temperature guidance. ABS and ASA need good ventilation.

**Q: How big can a print be?**  
A: About 220 × 220 mm on the bed and 240 mm tall on the KE (250 mm on the SE).

**Q: What is the little box with an arrow on the top crossbar?**  
A: It is most likely the filament runout/filament sensor, which detects when filament is missing. Confirm on the unit.

**Q: What is the black plate with "Warning hot surface" on it?**  
A: It is the heated, flexible build plate. It can reach up to about 100 °C, so do not touch it during or just after printing.

**Q: Why is there a screen next to the printer instead of on it?**  
A: In the photos the touchscreen appears to be detached or resting on the bench. It normally attaches to the printer base. Confirm that its cable is connected and that it is mounted safely.

**Q: What is the spray can beside the printer?**  
A: It looks like a hair-spray-type aerosol can. People sometimes use such products as bed adhesive, but they are flammable aerosols. Keep them away from the hot printer and never spray near a heated bed or hotend.

**Q: How do I start a print?**  
A: Slice a model into G-code, save it to a USB drive, insert it, load filament, run auto-levelling if needed, choose the file on the touchscreen, and start. Watch the first layer.

**Q: How do I load filament?**  
A: Preheat the nozzle to the filament's recommended temperature, feed the angled filament tip into the extruder, and use the Extrude/Load function until filament flows steadily from the nozzle.

**Q: How do I remove a finished print?**  
A: Wait for the bed to cool, then flex or lift off the plate and release the part. Do not scrape the PEI surface with a sharp metal tool.

**Q: Why won't my print stick?**  
A: Common causes are a dirty or oily plate, wrong Z-offset or levelling, wrong bed temperature, or damp filament. Clean the plate with IPA, rerun auto-levelling, and check settings.

**Q: Can I leave it running overnight?**  
A: Only if the lab rules allow it. 3D printers have heaters and moving parts, so supervised operation is the safe default.

**Q: What should I do if it smells of burning or shows a temperature error?**  
A: Stop the print, power off and unplug if safe, let it cool, and report it to the lab supervisor. Do not restart it until inspected.

**Q: What is its exact model?**  
A: The photos do not confirm it. The 220 × 220 mm bed, Sprite-style direct-drive head, top spool holder, runout-type sensor, and flat touchscreen suggest the Ender-3 V3 KE. The SE is a close alternative. Check the label or the About screen.

## 13. Suggested RAG metadata

```json
{
  "record_id": "LAB-OBJ-002",
  "object_name": "Creality Ender-3 V3 Series FDM 3D Printer",
  "possible_model": "Ender-3 V3 KE (alternative: Ender-3 V3 SE)",
  "model_verified": false,
  "category": "fdm_3d_printer",
  "functions": ["print 3D objects from filament", "auto bed levelling", "heated bed printing"],
  "build_volume_mm": "220x220x240 (KE) / 220x220x250 (SE)",
  "materials": ["PLA", "PETG", "TPU", "ABS (KE)", "ASA (KE)"],
  "related_objects": ["LAB-OBJ-001 (resin wash/cure machine - NOT for filament parts)"],
  "safety_critical": true,
  "hazards": ["hot nozzle", "hot bed", "moving parts", "fumes", "flammable aerosol nearby"],
  "source_images": ["image_2.jpeg", "image3.jpeg"],
  "verification_needed": [
    "base/rear model label",
    "touchscreen About page (model and firmware)",
    "whether the filament runout sensor is standard or added",
    "exact manual version"
  ]
}
```

## 14. Source references

1. **Creality Ender-3 V3 SE support/parameters page:** https://www.creality.com/support/creality-ender-3-v3-se
2. **Creality Ender-3 V3 KE specs (MatterHackers):** https://www.matterhackers.com/store/l/creality3d-ender-3-v3-ke-3d-printer
3. **Ender-3 V3 KE specs and features (3DJake):** https://www.3djake.com/creality-3d-printers-spare-parts/ender-3-v3-ke
4. **Ender-3 V3 SE specs and features (3DJake):** https://www.3djake.com/creality-3d-printers-spare-parts/ender-3-v3-se
5. **Ender-3 V3 family comparison (SainSmart):** https://www.sainsmart.com/products/creality-ender-3-v3-ke
6. **SE vs KE vs Plus differences:** https://printer-hub.ru/en/posts/creality-ender-3-v3-se-vs-ke-vs-plus

Use the actual printer's label, the supplied quick-start guide, and Creality's official manual for the exact model as the final authority, especially for power, dimensions, temperature limits, firmware, and operating steps. Product pages and retailers disagree on some figures.
