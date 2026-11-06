# Lab Object Knowledge Record: Make3D Pratham 3.0 Industrial FDM 3D Printer

**Record ID:** LAB-OBJ-005  
**Object category:** Enclosed industrial-style filament (FDM/FFF) 3D printer, made in India  
**Visual identification:** A box-shaped printer with a white sheet-metal frame and grey painted panels. The name **"Pratham 3.0"** is embossed on the grey top hood. A dark touchscreen is at the top-right of the hood. Two grey-framed glass doors with black hinges and silver handles cover the front. A narrow grey panel on the right carries **four round metal push buttons** stacked vertically. Inside, a black heated bed with binder clips sits on a bed carriage that moves on lead screws and polished rods. A sheet of transparent plastic wrap lies over the top of the machine. A small Iron Man sticker is visible at the bottom centre.  
**Identification confidence:** **High** for "Pratham 3.0", because the model name is embossed on the machine. The Pratham series is made by **Make3D (Make3d.in), Surat, Gujarat, India**. The exact variant (for example the standard 3.0 or the "3.0 Bigger") and its serial number and firmware are not visible in the photo.

> **Disambiguation for the robot:**
> - This is an **Indian-made, industrial-style, enclosed filament printer**. It is **not** a Creality Ender-3 (LAB-OBJ-002), **not** a Bambu Lab X2D (LAB-OBJ-004), and **not** a resin printer (LAB-OBJ-003 and LAB-OBJ-001).
> - Each of these machines has its own software and procedures. **Do not give instructions for another machine's screen, slicer, or menus.**
> - Its manufacturer's documentation is limited online compared with Creality or Bambu Lab. For anything not in this record, ask the lab supervisor or contact the manufacturer.

## 1. Short answer for the robot

This is a **Make3D Pratham 3.0**, a heavy-duty, **industrial-grade FDM 3D printer** with a metal enclosure. It melts plastic filament and builds objects layer by layer on a heated bed. It is designed for long print jobs, engineering plastics (such as ABS, PETG, and HIPS), and rapid prototyping in engineering, education, and small-scale manufacturing.

Its listed build volume is about **300 × 300 × 300 mm**, larger than a typical desktop printer.

## 2. What is it used for?

- Prototypes and functional parts for engineering projects.
- Larger parts that do not fit small desktop printers.
- Engineering materials such as ABS, PETG, HIPS, and (as listed) composites. The enclosure helps hold heat, which helps with materials that warp.
- Long, continuous jobs. The manufacturer describes the machine as built for prolonged, 24/7 operation.
- Education, labs, and industrial demonstration. Pratham printers are reported in use at institutes and in industry in India.

## 3. How does it work?

1. **Slicing:** A model (usually STL) is converted into layers and G-code with a slicer program. The exact slicer for this machine should be confirmed with the supervisor or the supplier.
2. **Transfer:** The G-code is loaded by the method the machine supports (USB or memory card are typical; some listings mention Wi-Fi). Confirm on the unit.
3. **Heating:** The silicone heated bed (listed as reaching up to 120 °C) and the nozzle heat to the filament's temperatures.
4. **Auto-levelling:** The manufacturer lists an automatic **9-point bed-levelling** system with a magnetic touch sensor.
5. **Printing:** The extruder feeds filament into the hot nozzle. In the photo the **bed carriage moves up and down** on vertical lead screws and polished rods, and the print head moves across the bed. Confirm the motion layout in the manual.
6. **Safety functions:** The manufacturer lists a **filament sensor** (warns or pauses when filament runs out) and **power-failure protection** (resumes after power loss).
7. **Finish:** After cooling, the part is removed from the bed (clips visible on the bed hold a plate in place).

## 4. Visible parts in the photograph

| Visible part | Name | Function |
|---|---|---|
| Grey hood with "Pratham 3.0" embossed | Top cover / hood | Encloses the top of the machine and houses the controls and electronics. |
| Dark rectangular screen at the top right | Touchscreen display | The main interface for controlling prints. Its size is not confirmed. The listed 7-inch display belongs to the 5.0 model. |
| Two glass-front doors with silver handles | Front doors | Give access to the print area and help hold heat in the enclosure. Keep closed during printing. |
| Black hinges | Door hinges | Support the doors. One hinge looks repaired or glued near the top right. |
| Four round metal buttons on the right panel | Push buttons | Functions are **not confirmed from the photo**. They may include power or lighting. The supervisor should label each one. |
| Black plate with binder clips | Heated bed with clips | The build surface. The clips appear to hold a glass or other plate on the bed. It is hot during use. |
| Vertical threaded rods and polished rods | Z-axis lead screws and guide rods | Move the bed carriage precisely up and down. |
| White shelf-like panel under the bed | Internal divider/base plate | Part of the frame. The bed moves in the space below and above it, so the lower compartment must stay clear (see safety). |
| Black wires and braided cable inside | Cabling | Power and signal for the bed and print head. |
| Transparent plastic wrap on top | Packaging or protective film | Not a machine component. It should be removed. |
| Small Iron Man sticker | Decoration | Not a machine component. |

**Other items visible in the photo (not part of the printer):**
- **Two aerosol cans** in the lower compartment: a red "ENZO"-labelled hair-spray-type can and a black "GATSBY"-labelled can. These are flammable pressurised aerosols (see safety).
- A **plastic box** with tools or accessories, a **yellow-and-black scraper/knife**, a **white printed part**, white printed discs or rings, and loose **filament strings and plastic waste** inside the machine.
- A red board on a wooden pallet at the right, and a bench surface at the left.

## 5. Controls and interface

- **Touchscreen** on the top hood: used for file selection, starting, pausing, and stopping prints, temperature control, moving axes, loading and unloading filament, and settings. Exact menus depend on the firmware.
- **Four push buttons** on the right panel: functions need to be confirmed and labelled.
- The manufacturer lists a **filament sensor** and **power-failure resume**. Check how they are enabled in the machine's settings.

## 6. General operating guide

This is a **general guide**. It is not the Make3D manual, which I could not find online. Confirm each step with the lab supervisor or Make3D.

### Before starting
1. Check the machine is on a **stable, level surface**, with clearance around it and good ventilation, especially for ABS.
2. **Remove the plastic wrap from the top of the machine** and any loose packaging.
3. **Clear the inside of the machine.** Remove aerosol cans, tools, boxes, loose parts, and filament scraps from the print area and from the lower compartment. Nothing should be in the path of the bed, print head, or lead screws.
4. Check the power cable, plug, and wiring for damage. Confirm the power rating on the machine's label (the reseller lists about 550 W).
5. Check the bed plate and clips are secure and the bed surface is clean.

### A. Loading filament
1. Use 1.75 mm filament unless the label says otherwise (the filament diameter is **not confirmed**).
2. Mount the spool so it unwinds freely.
3. Preheat the nozzle to the filament's recommended temperature on the touchscreen, then use the load function. Do not force filament in.
4. Wait until the filament flows steadily from the nozzle. Remove the extruded blob with tweezers, not bare fingers.

### B. Starting a print
1. Prepare and slice the model for this printer, matching the filament type.
2. Transfer the file by the supported method and select it on the touchscreen.
3. Run or confirm **auto bed levelling** if needed.
4. **Close the doors.** Start the print and watch the first layer.
5. Stay nearby for the first part of every new job.

### C. During printing
- Do not reach into the machine while it is running.
- Do not touch the nozzle, bed, or enclosure interior when hot.
- Do not open the doors for long periods when printing temperature-sensitive materials such as ABS.

### D. After printing
1. Let the bed cool.
2. Remove the part with the proper tool. Use scrapers away from your body, and do not damage the bed plate.
3. Clean the bed and remove waste plastic.
4. Switch off the machine and keep the inside tidy.

## 7. Safety precautions

- **Aerosols and flammables:** Pressurised aerosol cans (hair spray and similar products) are **flammable** and may burst or ignite if stored in or near a heated enclosure. **Do not store them inside the printer, near the heated bed, or on top of it.** Spray adhesive only when the machine is switched off and cool, away from ignition sources, and with the machine empty of loose items.
- **Loose items in the machine:** The bed moves vertically. Tools, boxes, or parts in the path can jam the bed, bend the rods, or damage the lead screws. Keep the interior clear.
- **Burns:** The nozzle and silicone heated bed (up to 120 °C as listed) can burn skin. Wait for cooling.
- **Moving parts and pinch points:** Keep fingers, hair, and clothing clear of the bed carriage, print head, and lead screws. Do not bypass any door or safety switch.
- **Electrical:** Do not open the electrical housing while connected to power. Do not use if wiring or plug is damaged. Plastic wrap or other coverings should not sit on top of the electronics or ventilation.
- **Fumes:** ABS, HIPS, and composites release fumes. Print in a ventilated room.
- **Fire safety:** Know where the extinguisher is. Do not leave the printer unattended unless the lab rules allow it.
- **Sharp tools:** Use scrapers and knives carefully, and wear eye protection when trimming supports.
- **Damaged hinge:** One door hinge looks repaired. Check that the doors close properly and report any damage.

## 8. Maintenance

How to maintain the Pratham 3.0: regular upkeep and care of the printer. Tasks include cleaning the bed plate, removing loose filament and debris, and lubricating the lead screws and guide rods. The table below lists each maintenance task and how often to do it.

| Task | Suggested frequency | Notes |
|---|---|---|
| Clean the bed plate | Before each print, or as needed | Remove oils and old adhesive residue. Follow the supervisor's guidance on cleaning liquids. |
| Remove loose filament and debris from the enclosure | After each job | Debris can jam the bed travel or fall into mechanisms. |
| Check lead screws and guide rods | Monthly, or if noisy | Wipe clean and lubricate lightly, only as the manufacturer advises. |
| Check the nozzle and extruder | When under-extruding | Clean or replace using the correct procedure, with the machine hot or as instructed. |
| Check bed levelling and the touch sensor | When first layers fail | Run the auto-levelling routine. |
| Check the filament sensor | Periodically | Confirm it triggers when filament is removed. |
| Check doors, hinges, and seals | Monthly | Repair or replace damaged hinges. |
| Store filament dry | Always | Seal spools with desiccant. |
| Firmware | Only as directed by Make3D | Do not install unofficial firmware without approval. |

## 9. Basic troubleshooting

| Symptom | Possible checks |
|---|---|
| Machine does not power on | Check the wall outlet, cable, and the correct push button or switch. Do not open the housing. |
| Touchscreen is dark | Check power and the correct button. Wait for boot. |
| First layer does not stick | Clean the bed, run auto-levelling, check bed temperature and clips, and check the filament profile. |
| Filament runout warning | Check the spool, tangles, sensor, and filament path, then reload. |
| Nozzle clog or under-extrusion | Check temperature, try unload and reload, and clear or replace the nozzle. |
| Warping (ABS/HIPS) | Keep the doors closed, raise the bed temperature in line with filament guidance, clean the bed, and use a brim. |
| Bed jams or grinds | Stop the machine. Check for loose items or debris in the lower compartment and on the lead screws and rods. |
| Print stops after a power cut | Use the power-failure resume function, if available. |
| Burning smell, smoke, or sparks | Stop, disconnect power if safe, let it cool, and tell the supervisor. |

Do not dismantle the machine or attempt internal electrical repairs as a student operator.

## 10. Specifications — verify before using as exact facts

These figures come from reseller and listing pages (Robu.in, IndiaMART), which I could not cross-check against an official Make3D manual. **Treat them as unconfirmed.**

| Item | Value |
|---|---|
| Manufacturer | Make3D (Make3d.in), Surat, Gujarat, India |
| Series | Pratham (Desktop, Mini, 3.0, 5.0 "Monster", 6.0 "Mega", X) |
| Technology | FDM / FFF |
| Build volume | about 300 × 300 × 300 mm |
| Heated bed | Silicone heated bed, listed as reaching 120 °C in about 30 seconds |
| Bed levelling | Automatic, 9-point magnetic touch sensor |
| Filament sensor | Yes |
| Power-failure protection | Yes (auto-resume) |
| Listed materials | ABS, PETG, HIPS, composites (one listing also includes PLA, TPU, PP, PVA, carbon-fibre and glass-fibre filled) |
| Body | Mild steel / metal frame |
| Power consumption | about 550 W (IndiaMART listing) |
| Operation | Marketed as low-vibration and capable of 24/7 running |
| Supported file format | STL (reseller listing) |
| Connectivity | Listings vary (USB, Wi-Fi). Confirm on the unit. |
| Display | Touchscreen. Size not confirmed. |
| Max nozzle temperature | **Not found** in the sources I could open |
| Nozzle diameter, filament diameter | **Not confirmed** |
| Weight and dimensions | **Not found** |

## 11. User manual, datasheets and support

I could not find an official Pratham 3.0 user manual online. These are the best available resources:

- **Manufacturer's website:** https://www.make3d.in  
  Email: info@make3d.in or support@make3d.in. Phone: +91 8866710006 (as printed on Make3D's datasheet). Address on the datasheet: Plot 36/A, Nilkanth Industrial Society, Ved Road, Katargam, Surat, Gujarat 395004.
- **Robu.in product page for the Pratham 3.0 Bigger (300 × 300 × 300 mm), with a "DataSheet" tab:** https://stgaws.robu.in/product/pratham-3-0-bigger-3d-printer-300x300x300-mm
- **IndiaMART listing for Pratham 3.0, with a product brochure download:** https://m.indiamart.com/proddetail/rapid-prototype-machine-2851121728673.html
- **Related datasheets (other models in the same series, for reference only):**
  - Pratham Desktop: https://stgaws.robu.in/wp-content/uploads/2024/12/2-Pratham-Desktop-3D-Printer.pdf
  - Pratham 5.0 Monster: https://stgaws.robu.in/wp-content/uploads/2024/12/3-Pratham-5.0-Monster-3D-Printer.pdf
- **News coverage (Pratham 3.0 installed at Indian Railways, with 300 × 300 × 300 mm build volume):** https://manufactur3dmag.com/make3d-installs-pratham-3-0-fdm-3d-printer-at-northeast-frontier-railway-zone-assam/

**Recommendation:** Ask the lab supervisor whether a printed manual or USB drive came with the machine, and contact Make3D for the official user manual and slicer profile.

## 12. RAG-ready question and answer pairs

**Q: What is this object?**  
A: It is a Make3D Pratham 3.0, an Indian-made, enclosed, industrial-style FDM 3D printer. The name is embossed on its top hood.

**Q: Who makes it?**  
A: Make3D (Make3d.in), a company based in Surat, Gujarat, India.

**Q: Is it a Creality or Bambu Lab printer?**  
A: No. It is a different brand with a different interface and software. The Creality Ender-3 V3 is LAB-OBJ-002 and the Bambu Lab X2D is LAB-OBJ-004.

**Q: Is it a resin printer?**  
A: No. It melts plastic filament. The resin printer is LAB-OBJ-003.

**Q: How big can a print be?**  
A: The listings give about 300 × 300 × 300 mm.

**Q: What materials can it print?**  
A: Listings mention ABS, PETG, HIPS and composites. Some also list PLA, TPU, PP, and PVA. Check the manufacturer's guidance for the exact material and temperature limits.

**Q: What are the four buttons on the right?**  
A: Their functions are not confirmed from the photo. Ask the supervisor and label them. Do not press them without knowing what they do.

**Q: Why are there aerosol cans inside the printer?**  
A: Spray cans are sometimes used as bed adhesive, but they should not be stored inside or next to a heated machine. They are flammable and pressurised. Remove them.

**Q: Why should the inside of the machine be kept clear?**  
A: The bed carriage moves vertically on lead screws, so loose items in the lower compartment can jam it or cause damage.

**Q: What is the plastic sheet on top of the printer?**  
A: It looks like packaging or protective wrap. It is not part of the machine and should be removed so it does not cover vents or electronics.

**Q: What happens if the power fails during a print?**  
A: The manufacturer lists a power-failure protection feature that resumes the print. Confirm how it works on this machine.

**Q: Where can I find the manual?**  
A: I could not find an official online manual. Ask the supervisor for the supplied documents, or contact Make3D through https://www.make3d.in.

**Q: What is the exact variant?**  
A: The embossed name shows "Pratham 3.0". The variant (standard or "Bigger"), serial number, and firmware are not visible. Check the label and the touchscreen.

## 13. Suggested RAG metadata

```json
{
  "record_id": "LAB-OBJ-005",
  "object_name": "Make3D Pratham 3.0 Industrial FDM 3D Printer",
  "brand": "Make3D (Make3d.in), Surat, India",
  "model": "Pratham 3.0",
  "model_verified": true,
  "model_verification_source": "name embossed on the top hood",
  "category": "fdm_3d_printer_enclosed_industrial",
  "functions": ["print engineering plastics", "large-format prototyping", "auto bed levelling", "power-failure resume"],
  "build_volume_mm": "about 300x300x300 (unconfirmed)",
  "not_to_be_confused_with": ["LAB-OBJ-002 (Creality Ender-3 V3)", "LAB-OBJ-004 (Bambu Lab X2D)", "LAB-OBJ-003 (resin printer)", "LAB-OBJ-001 (wash/cure machine)"],
  "safety_critical": true,
  "hazards": ["hot nozzle", "hot bed up to 120 C", "moving bed and lead screws", "fumes (ABS)", "flammable aerosol cans stored inside", "loose items in bed travel path", "plastic wrap on top"],
  "source_images": ["image_7.jpeg"],
  "verification_needed": [
    "function of the four push buttons",
    "touchscreen size and firmware",
    "slicer and file transfer method",
    "max nozzle temperature",
    "power rating label",
    "official manual"
  ]
}
```

## 14. Source references

1. **Robu.in product page, Pratham 3.0 Bigger (300 × 300 × 300 mm):** https://stgaws.robu.in/product/pratham-3-0-bigger-3d-printer-300x300x300-mm
2. **Robu.in Pratham series category:** https://st.robu.in/product-category/3d-printer-parts/full-3d-printer-kit/pratham-3d-printers
3. **IndiaMART listing, Pratham 3.0 (materials, power, features):** https://m.indiamart.com/proddetail/rapid-prototype-machine-2851121728673.html
4. **Make3D Pratham 3.0 at Northeast Frontier Railway (news):** https://manufactur3dmag.com/make3d-installs-pratham-3-0-fdm-3d-printer-at-northeast-frontier-railway-zone-assam/
5. **Make3D at ENGIMACH 2021 (series overview):** https://themachinemaker.com/?p=7886
6. **Pratham Desktop datasheet (company contact details):** https://stgaws.robu.in/wp-content/uploads/2024/12/2-Pratham-Desktop-3D-Printer.pdf
7. **iStem equipment listing (Pratham 3.0 at an Indian institute):** https://www.istem.gov.in/equipment-info/29329/Pratham-3-0-3D-Printer

Use the machine's own label, any supplied documents, and the manufacturer's guidance as the final authority, especially for power, temperature limits, and operating procedures.
