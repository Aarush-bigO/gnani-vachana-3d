# ADR 0005: Three.js 60 FPS Blendshapes and Skeletal Kinematics

## Status
Accepted

## Context
Interactive digital humans must maintain 60 FPS render performance on standard consumer laptops and smartphones without requiring high-end dedicated GPUs. Complex bone rigs and heavy morph meshes can drop frame rates below 30 FPS.

## Decision
1. Standardize on GLTF/GLB avatar models with ARKit and Oculus-compatible viseme blendshapes (`viseme_aa`, `viseme_O`, `viseme_PP`, etc.).
2. Couple viseme weights directly to real-time Web Audio RMS energy bands and expressivity tags (`<laugh>`, `<chuckle>`).
3. Isolate secondary hair and cloth dynamics to a lightweight spring-damper simulator (`dynamicbones.mjs`) that runs within the main `requestAnimationFrame` loop.

## Consequences
* **Positive:** Stable 60 FPS rendering across standard web browsers.
* **Positive:** Natural speech lip-sync, procedural breathing, saccadic eye movement, and culturally authentic gestures (**Namaste 🙏**).
