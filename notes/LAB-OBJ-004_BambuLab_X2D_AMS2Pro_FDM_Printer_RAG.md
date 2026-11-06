# Lab Object Knowledge Record: Bambu Lab X2D Dual-Nozzle 3D Printer with AMS 2 Pro

**Record ID:** LAB-OBJ-004  
**Object category:** Enclosed dual-nozzle filament (FDM/FFF) 3D printer with automatic multi-material filament system  
**Visual identification:** A grey-and-black Bambu Lab printer with a glossy black top surface and a dark tinted lid. The lower-right front panel carries the badge **"Bambu Lab X2D"**. A separate unit sitting on top of the printer carries the badge **"Bambu Lab AMS 2 PRO"**. The AMS 2 Pro has a clear front window showing several grey/white spool positions with orange spring-loaded feed mechanisms. A round silver button with a four-square logo sits on the top surface, a dark touchscreen is partly visible at the lower left, and clear plastic packaging is visible at the right of the photo.  
**Identification confidence:** **High** for both "Bambu Lab X2D" and "AMS 2 Pro", because both names are printed on the badges. Whether this is the printer-only X2D or the "X2D AMS Combo" cannot be told from the photo, but the AMS 2 Pro is present, so it is functionally a combo setup.

> **Disambiguation for the robot:**
> - This is a **filament printer**. It is **not** a resin printer (LAB-OBJ-003) and its parts do **not** go into the wash/cure machine (LAB-OBJ-001).
> - It is a different brand and a different machine from the Creality Ender-3 V3 filament printer (LAB-OBJ-002). The two use different software (Bambu Studio versus Creality Print or other slicers), different screens, and different procedures. **Do not give Ender-3 instructions for this machine or the reverse.**
> - The "AMS 2 Pro" is an accessory unit **for** the printer, not a separate printer.

## 1. Short answer for the robot

This is a **Bambu Lab X2D**, an enclosed, high-speed **FDM 3D printer** with a **dual-nozzle** system, paired with a **Bambu Lab AMS 2 Pro** (Automatic Material System). The X2D prints by melting plastic filament and depositing it layer by layer. The AMS 2 Pro holds several filament spools, feeds the right filament automatically, switches colours and materials during a print, and can **dry** the filament while it is stored.

The dual-nozzle design is meant for multi-colour printing, multi-material printing, and **cleaner support removal**, where the second nozzle can handle support material.

## 2. What is it used for?

- Multi-colour and multi-material prints, with the AMS 2 Pro swapping filaments automatically.
- Parts with easy-to-remove supports (model material on one nozzle, support or second material on the other).
- Functional and engineering parts using materials that benefit from an enclosed, heated chamber (for example ABS or ASA).
- Larger prototypes, with a build volume of about 256 × 256 × 260 mm.
- Learning and demonstrating advanced FDM printing in the lab.

## 3. How does it work?

1. **Slicing:** The model is prepared in **Bambu Studio** (Bambu Lab's own slicer) or another compatible slicer. Filament types, colours, and supports are assigned there.
2. **Sending the job:** The print is sent over **Wi-Fi/network** (Bambu Studio, Bambu Handy app) or loaded from a **USB drive**. A Bambu Lab account is normally used for cloud features.
3. **Filament feeding:** The AMS 2 Pro automatically recognises the loaded filaments, feeds the right one to the printer, and changes between filaments as the job requires. It also dries up to four spools.
4. **Printing:** The enclosed printer heats the bed and (when needed) the chamber (up to about 65 °C). The main nozzle prints the model and the second nozzle can print support or another material. The printer switches between the two nozzles mechanically.
5. **Monitoring:** The printer has many built-in sensors and AI monitoring (the manufacturer's listing mentions about 31 monitoring points and dynamic flow control) to detect problems such as jams or failed prints.
6. **Finish:** After cooling, the part is removed from the build plate.

## 4. Visible parts in the photograph

| Visible part | Name | Function |
|---|---|---|
| Badge "Bambu Lab X2D" at the lower right of the front | Model badge | Identifies the printer as an X2D. |
| Unit with the clear front window and "AMS 2 PRO" badge | AMS 2 Pro (Automatic Material System) | Holds up to 4 spools, feeds filament to the printer, and dries the filament. |
| Orange spring-loaded mechanisms visible in the AMS window | Feed/retract mechanisms | Grip and move the filament for each spool slot. |
| Grey/white cylinders in the AMS window | Spools or spool hubs in the AMS slots | Hold the filament spools. Several slots appear to hold grey/white spools. Some dust or speckling is visible on the right-hand spool. |
| Dark tinted lid over the top | Top lid / cover | Encloses the top of the printer and helps retain heat in the chamber. |
| Glossy black top surface with a round silver button | Top panel and button | The function of this round button/logo is not confirmed from the photo. It may be a magnetic cap, handle, or logo plug. Check the manual. |
| Dark rectangular screen at the lower left, partly visible | Touchscreen (about 5-inch) | Main on-printer control. It is off or dark in the photo. |
| Glossy dark panel at the bottom edge | Front door / glass panel | Encloses the build chamber. |
| Clear plastic bag at the right | Packaging | Suggests the printer may be newly unpacked. It is not part of the machine. |

## 5. Controls and interface

- **5-inch touchscreen** on the front: file selection, start, pause, stop, temperature, filament loading/unloading, calibration and settings. Exact menus depend on firmware.
- **Bambu Studio** (PC/Mac/Linux) and **Bambu Handy** (phone app) for slicing, sending prints, and remote monitoring.
- **AMS 2 Pro:** assignment of filament type and colour to each slot, loading/unloading, and drying settings. These are done on the printer screen and in the slicer.
- **Power switch and ports:** Check the rear and side for the power switch, USB, and exhaust-fan connection.

## 6. General operating guide

This is a **general guide for the X2D with AMS 2 Pro**. It is not a substitute for the official Bambu Lab manual and wiki. Follow the lab supervisor's rules.

### Before starting
1. Put the printer on a **stable, level, non-flammable surface** with space around it, and leave room for the AMS 2 Pro and the exhaust fan.
2. Keep it away from flammable items. Keep aerosols, solvents, and paper away from the printer.
3. Check that the **power cable, AMS cable, PTFE tubes, and exhaust-fan cable** are connected properly and undamaged.
4. Make sure all **transport screws, foam, and packaging** have been removed (new printers have red transport screws and parts that must be removed before powering on; see the official quick start guide).
5. Confirm the unit is the correct **mains-voltage variant** for the lab's power supply. Some listings show a 100–120 V version, so check the label on the unit before powering on.
6. Install the **textured PEI build plate** correctly and make sure the plate is clean and free of debris.

### A. Loading filament in the AMS 2 Pro
1. Select a 1.75 mm filament spool within the supported spool size (about 50–68 mm wide and 197–202 mm in diameter).
2. Place the spool in a slot and insert the filament end into the AMS feeder as instructed on the screen or in the manual.
3. Set the filament **type and colour** if it is not recognised automatically (Bambu-branded spools with an RFID tag are read automatically).
4. Use the printer's load/unload functions from the screen. Do not force the filament.
5. Keep filament dry. Use the AMS 2 Pro's drying function as recommended. Materials such as ABS and PC need higher temperatures to dry than the AMS may reach, so they may not dry fully there.

### B. Starting a print
1. Open **Bambu Studio**, choose the **Bambu Lab X2D** printer profile, add the model, and assign the filaments to the AMS slots.
2. Choose whether to use one or both nozzles. Use Bambu's default filament profiles where possible.
3. Slice and send the job, or save it to a USB drive.
4. On the first run or after changing the nozzle or plate, allow the printer's **automatic calibration** to complete.
5. Close the lid and the front door. Watch the first layer.

### C. During printing
- Do not reach into the chamber while the printer is running.
- Do not touch the nozzles, heated bed, or heated chamber walls. The nozzles can reach 300 °C and the chamber about 65 °C.
- Do not leave the printer unattended unless the lab rules allow it. Use the monitoring features only as an aid.

### D. After printing
1. Let the bed and chamber cool.
2. Remove the build plate and flex it gently, or remove the part with care. Do not scrape the PEI surface with sharp metal tools.
3. Remove supports. With a dual-nozzle setup, support material can often be peeled away easily.
4. Remove waste filament and purge material from the printer.
5. If the printer will not be used soon, keep filament dry and switch off the printer.

## 7. Safety precautions

- **Burns:** Nozzles up to 300 °C, bed up to about 120 °C and an active chamber heated to about 65 °C. Wait until everything has cooled before touching hot parts.
- **Moving parts:** Keep hands, hair, and loose clothing clear of the toolhead, the nozzle-switching mechanism, and the moving bed. Do not defeat the door or lid sensors.
- **Fumes and ventilation:** Printing ABS, ASA, and other engineering plastics produces fumes. Use the supplied **external exhaust fan** and a ventilated room.
- **Fire safety:** Never leave flammable materials near the printer. Know where the fire extinguisher is. Do not use unapproved power supplies or adapters.
- **Electrical:** Do not open the housing or touch internal electronics while connected to power. Use the supplied cable in a grounded socket. Do not use if the cable or plug is damaged.
- **Heated filament dryer:** The AMS 2 Pro heats the filament during drying. Do not block its vents, and do not put non-filament items inside it.
- **Cutters and tools:** The printer has a filament cutter. Use hand tools carefully and wear eye protection when trimming supports.
- **Network/cloud:** The printer connects to Wi-Fi and the Bambu cloud. Follow the lab's network and account rules.
- **Heavy equipment:** The printer weighs about 16 kg without the AMS. Lift it with care, and with help.

## 8. Maintenance

How to maintain the Bambu Lab X2D: regular upkeep and care of the printer. Tasks include cleaning the build plate, checking and cleaning the nozzle, and caring for the AMS 2 Pro filament system. The table below lists each maintenance task and how often to do it.

## Filament storage

How should filament be stored for the Ender 3: keep PLA, PETG and TPU filament dry in a sealed bag with desiccant.

| Task | Suggested frequency | Notes |
|---|---|---|
| Wash the build plate with warm water and mild dish soap, then dry with a clean towel | When prints stop sticking, or regularly | Avoid touching the surface with bare hands. |
| Check and clean the purge wiper | As needed | The wiper cleans the nozzle during filament changes. Replace per the wiki. |
| Vacuum dust from the chamber | Regularly | Especially after printing ASA or ABS. |
| Check the nozzle for clogs or wear | When under-extruding, or per the manual | Use only genuine or compatible nozzles. Use a hardened nozzle for abrasive filaments. |
| Check PTFE tubes and AMS connections | Periodically | Look for kinks, wear, or loose fittings. |
| Check the exhaust fan | Periodically | Make sure it is connected and clear. |
| Keep spools dry | Always | Use the AMS drying function or sealed storage with desiccant. |
| Update firmware (printer and AMS) | When a stable release is available | Use only official Bambu Lab firmware. |
| Lubricate rods or rails | As in the official guide | Use the recommended lubricant only. |

## 9. Basic troubleshooting

| Symptom | Possible checks |
|---|---|
| Printer does not power on | Check the wall outlet, cable, power switch, and voltage variant. Do not open the housing. |
| Touchscreen is dark | Check power and wait for boot. The screen in the photo appears off. |
| AMS does not recognise filament | Check that the filament is inserted properly, the RFID tag is readable, the PTFE tube is seated, and the AMS cable is connected. Set the filament type manually if needed. |
| Filament jam or tangle | Check the spool for tangles, the PTFE tube path, and the filament cutter. Unload, cut the tip, and reload. |
| Print does not stick | Wash the plate, check the plate is a compatible 256 mm plate, check bed temperature, and run calibration. |
| Poor support removal or mixed material | Check the filament pairing in Bambu Studio, and use Bambu's recommended profiles. |
| Warping with ABS/ASA | Use the enclosed chamber, keep the door and lid closed, use the heated chamber, and use the right plate. |
| Nozzle clog | Run the printer's guided procedure. Replace the nozzle if needed. |
| Print stops or reports a sensor error | Read the on-screen message. Check the filament path and sensors. Follow the wiki for the error code. |
| Burning smell, smoke, or sparks | Stop, disconnect power if safe, let it cool, and report it to the supervisor. |

Do not dismantle the printer or attempt internal electrical repairs as a student operator.

## 10. Specifications — verify before using as exact facts

These figures come from reseller and retailer pages, since I could not open an official Bambu Lab specification sheet. **Check the official manual and label before recording exact values.**

### Bambu Lab X2D
| Item | Value |
|---|---|
| Technology | FDM / FFF, enclosed CoreXY |
| Nozzle system | Dual nozzle with mechanical switching. The main nozzle is direct-drive. The auxiliary nozzle is often described as the support nozzle. |
| Build volume, main nozzle | 256 × 256 × 260 mm |
| Build volume, auxiliary or dual-nozzle printing | about 235.5 × 256 × 256 mm |
| Max nozzle temperature | about 300 °C |
| Max bed temperature | about 120 °C |
| Active chamber heating | up to about 65 °C |
| Max speed | up to about 1000 mm/s (manufacturer/retailer figure) |
| Printer dimensions | about 392 × 406 × 478 mm |
| Net weight | about 16.25 kg |
| Display | about 5-inch touchscreen |
| Build plate | Textured PEI plate. Compatible with current Bambu 256 mm plates (not first-generation plates). |
| Connectivity | Wi-Fi, USB |
| Slicers | Bambu Studio. Third-party G-code slicers with some features limited. |
| Model number (one retailer) | PF004-P |
| Power | Listings show a 100–120 V version. **Verify voltage and power on the unit's label.** |
| Discrepancy | One reseller lists a 330 × 330 × 320 mm build volume. This disagrees with most sources and is probably an error. |

### Bambu Lab AMS 2 Pro
| Item | Value |
|---|---|
| Capacity | 4 spools per unit |
| Functions | Automatic filament feeding, filament switching, and integrated drying |
| Spool size | about 50–68 mm wide, 197–202 mm diameter |
| Dimensions / weight | about 372 × 280 × 226 mm / about 2.5 kg (one retailer listing) |
| Expansion | Up to 4 AMS 2 Pro and 8 AMS HT units, for up to 24 filaments in parallel (single-nozzle setups) |
| More than two AMS units | A 4-in-1 PTFE adapter (FAZ013-N) is needed. |
| AMS hub | Not compatible with the X2D |
| Drying limits | Materials needing very high drying temperatures (for example ABS, PC) may not dry completely |

### In-the-box items listed for the X2D
Textured PEI build plate, external exhaust fan bundle, accessory box, spool holder. The AMS 2 Pro is included only in the "AMS Combo" version. Filament is not included.

## 11. User manual and software resources

**Official**
- **Bambu Lab Wiki (home):** https://wiki.bambulab.com/en/home  
  This is where Bambu Lab publishes manuals, setup guides, maintenance guides, and error-code help for its printers. I could not confirm a direct link to the X2D page, so search for "X2D" or "AMS 2 Pro" on the wiki.
- **Quick Start Guide:** supplied in the printer box (in the toolbox).
- **Software:** Bambu Studio (slicer) and Bambu Handy (phone app) from Bambu Lab's official download page.

**Third-party guides (not official; use for orientation only)**
- X2D unboxing and first-print setup guide: https://makers101.com/bambu-lab-x2d-unboxing-first-print-setup-guide/
- X2D user guide and tips: https://bikmantech.com/blogs/blogs/bambu-lab-x2d-complete-user-guide-and-tips
- X2D compatibility and filament guide: https://simplyprint.io/compatibility/bambu-lab-x2d

**Note:** The older Bambu Lab X1 manual at https://wiki.bambulab.com/x1/manual is for a different printer. Do not use it for X2D-specific steps.

## 12. RAG-ready question and answer pairs

**Q: What is this object?**  
A: It is a Bambu Lab X2D, an enclosed dual-nozzle FDM 3D printer, with a Bambu Lab AMS 2 Pro filament system on top. The badges on the machine show both names.

**Q: What is the unit on top of the printer?**  
A: It is the AMS 2 Pro (Automatic Material System). It holds up to four filament spools, feeds the filament automatically, enables multi-colour printing, and dries the filament.

**Q: Is it a resin printer?**  
A: No. It uses plastic filament. The resin printer in the lab is the HALOT-MAGE S 14K (LAB-OBJ-003).

**Q: Is it the same as the Creality Ender-3 printer?**  
A: No. The Ender-3 V3 (LAB-OBJ-002) is a different brand, single-nozzle, open-frame printer. The X2D is enclosed and dual-nozzle, and it uses the Bambu Studio ecosystem.

**Q: What is special about the X2D?**  
A: It has two nozzles, so it can print model and support materials (or two materials) without as much filament waste, and with easier support removal. It also has an enclosed, actively heated chamber and many sensors.

**Q: How big can a print be?**  
A: About 256 × 256 × 260 mm with the main nozzle, and about 235.5 × 256 × 256 mm when printing with both nozzles.

**Q: What materials can it print?**  
A: Common materials such as PLA, PETG, TPU, ABS, and ASA, and with the right setup engineering filaments. Always check the filament's own temperature guidance, and use ventilation for ABS and ASA.

**Q: How many colours can it print?**  
A: A single AMS 2 Pro holds four spools. With more AMS units, a setup can reach up to about 24 filaments in parallel.

**Q: What software does it use?**  
A: Bambu Studio for slicing and Bambu Handy for phone monitoring. Other G-code slicers can be used with limited features.

**Q: What is the round silver button on top?**  
A: Its function is not confirmed from the photo. Check the manual or the printer itself before assuming it has a specific function.

**Q: How should I handle ABS or ASA?**  
A: Keep the lid and door closed, use the enclosed chamber and the external exhaust fan, ventilate the room, and do not stay near the printer for long periods. Note that the AMS 2 Pro may not dry such filaments completely.

**Q: Can I leave it printing unattended?**  
A: Only if the lab rules permit it. The printer has monitoring features, but heaters and moving parts mean supervised use is the safe default.

**Q: Where is the manual?**  
A: The Quick Start Guide is in the printer's box, and the official manuals and guides are on the Bambu Lab Wiki (https://wiki.bambulab.com/en/home).

**Q: What is its exact version?**  
A: The badges confirm "X2D" and "AMS 2 Pro". The exact variant (printer only or AMS Combo), regional voltage version, and firmware are not visible in the photo. Check the label and the touchscreen's settings.

## 13. Suggested RAG metadata

```json
{
  "record_id": "LAB-OBJ-004",
  "object_name": "Bambu Lab X2D Dual-Nozzle 3D Printer with AMS 2 Pro",
  "brand": "Bambu Lab",
  "model": "X2D",
  "accessory": "AMS 2 Pro",
  "model_verified": true,
  "model_verification_source": "badges visible on printer and AMS",
  "category": "fdm_3d_printer_enclosed_dual_nozzle",
  "functions": ["multi-colour printing", "multi-material printing", "dual-nozzle support printing", "filament drying (AMS 2 Pro)"],
  "build_volume_mm": "256x256x260 (main nozzle); 235.5x256x256 (dual nozzle)",
  "software": ["Bambu Studio", "Bambu Handy"],
  "not_to_be_confused_with": ["LAB-OBJ-002 (Creality Ender-3 V3 FDM printer)", "LAB-OBJ-003 (resin printer)", "LAB-OBJ-001 (wash/cure machine)"],
  "safety_critical": true,
  "hazards": ["hot nozzles up to 300 C", "heated chamber up to 65 C", "moving parts", "fumes from ABS/ASA", "heated filament dryer"],
  "source_images": ["image_6.jpeg"],
  "verification_needed": ["power/voltage label", "printer-only or AMS Combo variant", "firmware version", "function of the round top button", "official X2D manual link"]
}
```

## 14. Source references

1. **X2D specifications and features (3DJake):** https://www.3djake.com/bambu-lab/x2d-combo
2. **X2D specifications, build volumes, FAQ (Spool3D):** https://spool3d.ca/bambu-lab-x2d-dual-extruder-3d-printer/
3. **X2D AMS Combo specifications (Shop3D Universe):** https://shop3duniverse.com/products/bambu-lab-x2d
4. **X2D features and box contents (MatterHackers):** https://www.matterhackers.com/store/l/bambu-lab-x2d-3d-printer/
5. **X2D listing with model number and chamber/nozzle figures (LDLC):** https://www.ldlc.com/en/product/PB00751825.html
6. **X2D unboxing and setup guide (third-party):** https://makers101.com/bambu-lab-x2d-unboxing-first-print-setup-guide/
7. **X2D user guide and tips (third-party):** https://bikmantech.com/blogs/blogs/bambu-lab-x2d-complete-user-guide-and-tips
8. **X2D filament compatibility (SimplyPrint):** https://simplyprint.io/compatibility/bambu-lab-x2d
9. **Bambu Lab Wiki:** https://wiki.bambulab.com/en/home

The X2D is a recent product and details such as firmware behaviour and accessories may change. Use the printer's label, the supplied Quick Start Guide, and the official Bambu Lab Wiki as the final authority, especially for power, safety, and setup.
