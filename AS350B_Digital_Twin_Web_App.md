# AS350B Avionics Digital Twin — 3D Web App Plan

## Objectives
- Deliver a web-based, 3D interactive digital twin of the AS350B avionics system for training, analysis, and fault experimentation.
- Simulate electrical, engine, navigation, autopilot, and avionics bus behaviors in real time with deterministic replay.
- Provide realistic cockpit visuals with functional avionics displays plus a technician overlay for faults, charts, and telemetry logs.
- Keep this design self-contained: add new modules without modifying existing project code.

## Tech Stack & Runtime
- **Language:** TypeScript for type safety and predictable data contracts.
- **Rendering:** WebGL via **Three.js** for the 3D cockpit; consider glTF for cockpit assets and instanced meshes for performance.
- **UI Layer:** React or a lightweight reactive UI (e.g., Preact) mounted over the Three.js canvas for overlays (charts, controls, logs).
- **State & Dataflow:** RxJS or a small pub/sub bus for streaming sensor topics; Immer for immutable state snapshots used by replay.
- **Timing:** Simulation tick at 50–100 Hz (engineered to be configurable); rendering decoupled via requestAnimationFrame.
- **Testing:** Jest + Vitest for logic, Playwright for UI smoke; eslint/prettier for consistency.

## High-Level Architecture
```
+---------------------------------------------------------------+
| 3D Cockpit (Three.js)                                         |
|  - Cockpit mesh + clickable switches                          |
|  - Render targets for PFD/EIS/GPS/HeliSAS screens             |
+------------------------------+--------------------------------+
| Overlay UI (React/Preact)    | Technician Panel               |
|  - Fault injection buttons   |  - Charts (engine, electrical) |
|  - Scenario controls         |  - Telemetry log + replay      |
+------------------------------+--------------------------------+
| Simulation Engine (workers / core loop)                       |
|  - Electrical model                                             |
|  - Engine/EIS model                                            |
|  - Navigation model                                            |
|  - Autopilot (HeliSAS)                                         |
|  - Avionics bus simulator (ARINC-429, RS-485, CAN)             |
+------------------------------+--------------------------------+
| Data Services                                                   |
|  - Scenario storage (local IndexedDB/JSON)                     |
|  - Telemetry exporter (CSV/JSON/WebSocket)                     |
+---------------------------------------------------------------+
```

## Simulation Engine Design
- **Deterministic tick:** Fixed-step integrator (e.g., 20 ms) with accumulator for real-time drift correction; random seeds injected via scenario for reproducibility.
- **Units & scaling:** Normalize internally (SI units) and map to cockpit indications per AS350B handbook ranges.
- **Failure injection hooks:** Each subsystem accepts injected faults (e.g., contactor stuck open, GEN offline, GPS lost, ARINC channel noise) with time-based or conditional triggers.
- **Bus abstraction:** Topic-based messages (`electrical.status`, `engine.eis`, `nav.gps`, `autopilot.modes`) that serialize onto virtual buses respecting protocol timing.
- **Data guards:** Clamp to certified limits (e.g., Ng 0–110%, T4 transient logic) and emit exceedances to the alerting layer.

### Electrical Model
- Components: Battery (SoC with Peukert-style discharge), Starter/Generator with contactor logic, main/avionics busbars, essential loads (PFD, GPS, AHRS, lighting).
- Behaviors: cranking voltage sag, GEN takeover on start, bus drop on GEN failure, load shedding, ripple/noise injection for realism.
- Outputs: bus voltage/current, contactor states, fault flags (GEN, BAT, BUS), load table for each avionics unit.

### Engine & EIS Model
- Parameters: Ng, Np, torque, T4, oil P/T.
- Dynamics: first-order lag + rate limits; transient spikes during start and load changes; exceedance timers for caution/warning.
- Outputs: EIS display values, caution/advisory flags, drive torque to rotor load model for autopilot trim.

### Navigation Model
- Sensors: GPS position/velocity, VOR radial/deviation, DME range/closure, Radar Altimeter height.
- Noise & dropouts: configurable Gaussian noise, RA dropout below antenna shadow, VOR signal loss with distance/angle, GPS loss/reacquire timers.
- Outputs: ARINC labels/messages for PFD/HSI, validity flags, update rates (e.g., GPS 10 Hz, VOR/DME 5 Hz, RA 25 Hz).

### Autopilot (HeliSAS) Model
- Modes: SAS (basic stabilization), HDG/NAV, ALT/VRT (vertical speed), IAS/GA (if modeled); discrete state machine with arming/capture.
- Control laws: PID/PI loops referencing attitude/altitude/heading; include authority limits and trim saturation.
- Alerts: mode annunciations, failure flags on AHRS or servo faults, reversion to SAS on nav loss.

### Avionics Bus Simulation
- **ARINC-429:** label scheduling with SDI/SSM, 100 kbps high-speed for attitude/nav; configurable parity errors for fault testing.
- **RS-485:** IFF-style polling with master/slave timing and bus contention handling.
- **CAN (or serial sensors):** periodic engine/electrical data frames with arbitration and dropout simulation.
- Bridge: publish normalized data → encode to bus packets → decode for displays to verify end-to-end integrity.

## 3D Cockpit & UI/UX
- **Cockpit mesh:** Use glTF with baked PBR textures; split interactive meshes (switches, knobs) for event mapping to simulation inputs.
- **Avionics screens:** Render to texture targets feeding cockpit materials; React canvases or Three.js `Scene` layers for PFD, EIS, GPS, HeliSAS.
- **Camera & controls:** Default seated view with limited head movement; inspector mode for technicians with free-fly camera.
- **Interaction mapping:** Switches/knobs fire actions into the simulation bus (e.g., BAT ON closes contactor; GEN RESET cycles field; AP ENG toggles mode).
- **Feedback:** Immediate visual state changes (annunciators, screen dimming on low voltage), tooltips, and contextual warnings to reduce user error.

## Technician / Pilot Overlay
- **Fault injection panel:** One-click triggers + scheduled faults (time-based or condition-based), including GEN offline, AHRS fail, GPS lost, T4 overlimit, bus noise.
- **Charts:** Real-time and replay charts for Ng, Np, T4, torque, bus voltage/current, autopilot mode transitions.
- **Logs:** Structured telemetry log with event markers; export/import JSON or CSV.
- **Scenario replay:** Timeline scrubber tied to deterministic snapshots; overlay ghost traces in 3D for navigation paths.
- **Safety nets:** Undo/redo for injections, reset-to-nominal, and snapshot save/restore.

## Data & Scenario Management
- Scenario schema: metadata (title, seed, weather preset), initial conditions (battery SoC, engine temp, position), scheduled events, and expected outcomes.
- Storage: IndexedDB for local persistence; optional WebSocket uplink for remote observers.
- Telemetry: Rolling buffer with compression (e.g., delta-encoded JSON or CBOR) to keep UI responsive; periodic checkpoints for replay.

## Performance, Quality, and Extensibility
- Run simulation logic in a Web Worker to keep rendering smooth; share state via transferable objects or structured clones.
- Use ECS (entity-component-system) or modular services to keep systems decoupled; each subsystem exposes `update(dt)`, `injectFault`, and `snapshot` methods.
- Include validation tests comparing model outputs against handbook reference tables (e.g., Ng/T4 vs. time during start), plus fuzz tests for bus decoders.
- Telemetry contracts typed via shared interfaces; provide mock providers to support headless testing.
- Avoid touching existing project modules—mount new code under a `digital-twin/` namespace or package to isolate changes.

## Delivery Checklist
- MVP: deterministic simulation loop, basic cockpit render, PFD/EIS data binding, fault injection UI, telemetry log/export.
- Beta: ARINC/RS-485/CAN end-to-end paths, HeliSAS mode logic with annunciations, scenario replay.
- Polish: accessibility (keyboard shortcuts), localization strings, theming, and performance profiling with WebGL inspector.
