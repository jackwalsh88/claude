# Answer 5 of 7 — `claude-fable-5.1-max`

- **Source page:** Arena2 (Battle)
- **Model label shown by Arena:** `claude-fable-5.1-max`

## Prompt

> would you go about putting together a real time rendered (frame rate) photorealistic avatar with generated voice. What would be your options and their requirements

## Response (verbatim, converted from HTML to Markdown)

Here's how I'd approach it, structured as the decisions you have to make, the pipeline, the four fundamentally different ways to produce the pixels, voice options, and the glue that actually makes it feel real.

---

## 1. Decide these first — they determine everything

| Question | Why it matters |
| --- | --- |
| **Specific real person, or a synthetic person?** | Real likeness needs capture data + consent; synthetic can be built from tools |
| **Framing: head-and-shoulders "video call", or full body in a 3D scene with a moving camera?** | 2D neural methods only do the former well; only 3D does the latter |
| **Interactive conversation, or driven from text/script?** | Conversation makes latency the hardest problem (voice-to-voice < ~1 s) |
| **Where does it render — server (one GPU per session) or client (browser/device)?** | Photoreal in a browser is basically server-render + WebRTC, or Gaussian splats |
| **Scale: one kiosk, or 1,000 concurrent web users?** | Per-session GPU cost dominates at scale |
| **Build vs. buy, and commercial use?** | Many open models have non-commercial weights or dependencies |

---

## 2. The reference pipeline (everything must stream)

```
[user mic] → VAD/endpointing → streaming STT ─┐
                                              ├─► LLM (token stream) → sentence/clause chunker
[scripted text] ──────────────────────────────┘                 │
                                                                ▼
                                                     streaming TTS (PCM chunks)
                                                       │                 │
                                                       ▼                 ▼
                                      audio → facial motion         audio to client
                                      (blendshapes / expression     (delayed to match video)
                                       codes / pixels directly)
                                                       │
                                                       ▼
                  renderer (UE5 | Gaussian splats | 2D neural) → NVENC H.264/AV1 → WebRTC → browser/app
```

The rule: never wait for a full response at any stage. First audio should start on the first clause, first frames on the first ~100–200 ms of audio.

---

## 3. The four ways to produce the pixels

### Option A — Game-engine 3D (Unreal Engine 5 + MetaHuman)

**How:** A rigged photoreal character rasterized in real time (Lumen GI, Nanite, strand-based groom hair, subsurface-scattering skin, refractive eyes). The face is driven by ARKit-52 blendshapes or the full MetaHuman rig; body from a mocap library.

**Face driver options:**

- **NVIDIA Audio2Face-3D** (now open-source; ONNX/TensorRT; UE5 plugin; outputs ARKit blendshapes + emotion, works on any audio incl. TTS output)
- **MetaHuman Animator audio-driven animation** (UE 5.5+, with a runtime/real-time mode in 5.6 — verify for your version)
- **Azure TTS viseme/blendshape events** (TTS emits 55 blendshapes at 60 fps alongside audio — no separate model)

**Requirements:**

- *Skills:* UE5 (Blueprint/C++), a tech artist for lighting/look-dev/rig tuning, animation sensibility
- *Hardware:* RTX 4080/4090 or better for 1080p60 at LOD0 with groom hair; server-side L40S/A10G per stream; L4 only with card hair and LOD1. Pixel Streaming (WebRTC) for browsers.
- *Data:* none for a synthetic human. For a real likeness: head scan (iPhone TrueDepth via MetaHuman Animator identity capture, or photogrammetry) → Mesh to MetaHuman → **custom skin textures** (this is where the real artist work lives)
- *Animation library:* idle/listening/gesture clips (capture a real actor with MetaHuman Animator + body mocap), procedural blinks/saccades/breathing/look-at
- *Licensing:* UE's non-game licensing terms; MetaHuman license was relaxed in 2025 to allow use outside Unreal — check current terms

**Pros:** full body, free camera, scenes, lighting, outfits, deterministic, no per-person GPU "model", consistent identity, can run natively on a kiosk/device.  
**Cons:** hardest to make truly *photo*-real in motion. The uncanny valley comes from animation (dead eyes, generic co-articulation, no micro-expressions), not from the shader. Budget more for animation than rendering.

### Option B — 2D audio-driven neural video (talking-head models)

**How:** A model takes a reference image or video of the person plus audio and generates frames directly (either inpainting the mouth region onto a looping base video, or generating the whole head's motion).

**Real-time-capable open models:**

- **MuseTalk** — lip-region inpainting over a driving video loop; ~30 fps on a 4090; MIT. Robust, mouth-only.
- **Ditto** — motion-space diffusion with TensorRT, streaming/online mode, whole-head motion from audio
- **LivePortrait family** — ~12 ms/frame retargeting on a 4090; needs an audio→motion front-end (e.g., JoyVASA). *Gotcha:* depends on InsightFace (non-commercial).
- **Per-person NeRF talking heads** (SyncTalk, ER-NeRF, GeneFace++) — train on 3–5 min of the person, then real-time inference
- Hosted/closed: NVIDIA Maxine Audio2Face-2D, Microsoft VASA-1 (unreleased)
- *Not* real-time: Hallo3, OmniHuman, EchoMimic, Sonic, LatentSync (close)

**Requirements:**

- *Data:* a portrait photo (low fidelity) or 2–5 min of the person recorded with a static camera, neutral background, gentle idle motion (becomes the base loop)
- *Hardware:* RTX 4090 / L4 / A10G → 1–3 concurrent sessions at 25–30 fps, 512–768 px face region; 4–10 GB VRAM per session
- *Skills:* Python/CUDA/TensorRT, a compositing step to paste the face back into a higher-res frame, WebRTC publishing (LiveKit/Daily SDK, aiortc, GStreamer)

**Pros:** most photoreal per dollar and per week of effort; it *is* video of a person.  
**Cons:** fixed head-and-shoulders framing, limited head rotation, no camera moves, gestures only what's in the base loop, teeth/tongue/occlusion artifacts, identity drift in long sessions, per-session GPU cost, model licenses.

### Option C — Neural 3D (3D Gaussian Splatting head avatars)

**How:** Capture a real person → optimize a cloud of Gaussians rigged to a FLAME head mesh → animate with expression/pose parameters → rasterize at 100+ fps. This is the Codec-Avatars / Vision Pro Persona direction, in open form.

**Methods:** GaussianAvatars (multi-view rig), FlashAvatar / SplattingAvatar / MonoGaussianAvatar (monocular video), GaussianTalker / TalkingGaussian (audio-driven end-to-end), **LAM** (one-shot from a single image, renders in a browser via WebGL — used in OpenAvatarChat), ExAvatar for full body.

**Requirements:**

- *Data:* 1–3 min monocular video at 30 fps (head turns ±45°, varied expressions, speech, flat lighting) — or a multi-camera rig for best quality; FLAME tracking (e.g., VHAP/metrical tracker)
- *Compute:* minutes to a few hours of training on a 4090; inference trivially real-time, even on modest GPUs or in-browser
- *Driver:* audio → FLAME expression (Audio2Face → ARKit → FLAME mapping, UniTalker/EMOTE, or learned per-subject from the same footage)
- *Skills:* PyTorch, CUDA, tolerance for research code, writing your own glue

**Pros:** true photorealism *with* 3D consistency (head turns, partial relighting), extremely cheap to render, can run client-side.  
**Cons:** research maturity; mostly bust-only; hair/torso/hands/mouth-interior are weak spots; expressions limited to what was captured.

### Option D — Buy it (hosted real-time avatar APIs)

**Vendors:** Tavus (Phoenix-3, CVI), HeyGen Interactive Avatar, D-ID Agents, Simli, Anam, Hedra Live, Beyond Presence, Azure TTS Avatar (real-time, prebuilt or custom with consent), Soul Machines / UneeQ (3D, enterprise).  
**Orchestration:** LiveKit Agents or Pipecat (both have avatar integrations), ElevenLabs/Vapi/Retell for the voice-agent layer.

**Requirements:** API keys, a WebRTC client, 2–5 min consent video for a custom likeness, per-minute budget (typically tens of cents per conversation-minute).  
**Pros:** working in days; they own GPUs, sync, scaling. **Cons:** cost scales linearly with usage, limited framing/control, lock-in, data residency.

### Comparison

|  | A. UE5 / MetaHuman | B. 2D neural | C. Gaussian splat | D. Hosted |
| --- | --- | --- | --- | --- |
| Face realism | good (stills) / risky in motion | excellent | excellent | excellent |
| Body / camera / scene | yes | no | bust only | no |
| Specific real person | hard (textures) | easy | moderate (capture+train) | easy |
| Frame rate | 60 fps | 25–30 fps | 100+ fps | 25–30 fps |
| GPU per session | high | medium | low | n/a |
| Time to first demo | weeks | days | weeks | hours |
| Maturity | production | production-ish | research | production |

---

## 4. Voice options

|  | Examples | TTFB / latency | Requirements | Notes |
| --- | --- | --- | --- | --- |
| Hosted streaming TTS | ElevenLabs Flash, Cartesia Sonic, Deepgram Aura, OpenAI TTS, Azure Neural (viseme output), Google Chirp 3, Rime, Hume, Inworld | ~40–250 ms + network | API key; WebSocket streaming; consent for cloning | Best quality/latency ratio; Azure/Polly give visemes for free |
| Self-hosted, fast & small | Kokoro (82M, Apache-2, even CPU), Piper (MIT) | <100 ms | CPU or tiny GPU | No/limited cloning, less expressive |
| Self-hosted, cloning + streaming | CosyVoice 2 (Apache-2), Orpheus (Apache-2, 3B), Chatterbox (MIT), Kyutai TTS, Sesame CSM, Zonos (Apache-2) | 150–400 ms | 4–12 GB VRAM, vLLM/TensorRT helps | Check licenses: XTTS-v2, F5-TTS weights, Fish Speech are non-commercial |
| Speech-to-speech (no STT/LLM/TTS split) | OpenAI Realtime, Gemini Live, Amazon Nova Sonic, Kyutai Moshi | ~300–500 ms voice-to-voice | API | Lowest latency; you still need audio→face; less control over text |

Voice cloning data: 5–30 s for zero-shot; 30 min–3 h clean studio audio for a professional clone.

---

## 5. Audio → face (the glue for 3D paths)

- **Audio2Face-3D** (open, best general option) — tens of ms per frame; configurable lookahead (more future context = better co-articulation = more latency; ~100 ms is a good compromise, delay audio playout to match)
- **TTS visemes/blendshapes** (Azure, Polly) — zero extra inference, text-timing-derived, slightly mechanical
- **Meta/Oculus Lipsync SDK, uLipSync** — cheap viseme classifiers, "good enough" tier
- **Research:** UniTalker, CodeTalker, EMOTE, DiffPoseTalk (face); EMAGE, TalkSHOW, Audio2Gesture (body) — body gesture generation is still not production-ready; use a curated mocap library triggered by LLM tags (`<nod>`, `<smile>`) or prosody

---

## 6. Latency and sync budget (conversational case)

| Stage | Typical | Notes |
| --- | --- | --- |
| Endpointing (silence after user stops) | 200–400 ms | Silero VAD + semantic endpointing to cut this |
| STT final | 50–150 ms | streaming partials already available |
| LLM first clause | 250–600 ms | small/fast model, TTFT-optimized |
| TTS first audio | 80–250 ms | split on clause boundaries, keep context for prosody |
| Audio→face + render + encode | 40–120 ms (+ lookahead 0–200) | NVENC low-latency preset |
| Network + jitter buffer + decode | 80–200 ms | WebRTC |
| **Voice-to-voice total** | **0.7–1.5 s typical; ~0.5 s excellent** | S2S models collapse STT+LLM+TTS |

Hard requirements that bite people:

- **A/V sync:** keep audio within roughly −45 ms / +100 ms of lips (detectability thresholds); timestamp from one clock, delay audio by the animation latency. UE Pixel Streaming handles this if audio plays through the engine; custom pipelines must do it via RTP timestamps.
- **Barge-in:** detect user speech during avatar speech (client echo cancellation), then cancel the LLM stream, flush TTS, clear animation/audio queues, blend to a listening pose — all consistently.
- **Liveness layer:** blinks (every 3–6 s), saccades, breathing, head sway, listening nods/backchannels. This contributes more to "alive" than skin shaders. In 2D methods the base-video loop provides it — pick loop points carefully.

---

## 7. Sizing cheat sheet

| Deployment | GPU | What it carries |
| --- | --- | --- |
| Dev workstation | RTX 4090/5090 | UE5 + Audio2Face + small TTS; push LLM to API or a second GPU |
| Kiosk / installation | RTX 4070–4090 PC | UE5 locally, voice via API; 60 fps 1080p |
| Cloud, UE5 per session | L40S or A10G (L4 at reduced LOD) | 1 session/GPU, NVENC encode |
| Cloud, 2D neural | L4 / A10G / 4090 | 1–3 sessions per 24 GB GPU at 30 fps |
| Cloud, Gaussian splat | L4 or smaller, or client-side | many sessions/GPU |
| Self-hosted TTS | shared GPU 4–12 GB (Kokoro: CPU) | several concurrent streams |

---

## 8. What I'd actually do, by scenario

**Web product, need it live fast, head-and-shoulders:** LiveKit Agents or Pipecat → Deepgram STT → fast LLM → Cartesia/ElevenLabs → Tavus/HeyGen/Simli/Anam avatar. Swap the avatar vendor later; the orchestration is the durable part.

**Own IP, full control, body + scene, kiosk or installation:** UE5 + MetaHuman + Audio2Face-3D + streaming TTS (Azure if you want free visemes) + Pixel Streaming for remote clients. Spend the budget on captured idle/listening/gesture performance from a real actor, not on more shader work.

**A specific real person, maximum realism, self-hosted and cheap to run:** capture 3 min of video, train a Gaussian-splat head avatar (or a per-person 2D model like MuseTalk/Ditto over a base loop) and drive it from Audio2Face/FLAME. More engineering, lowest per-minute cost, best realism — accept research-grade tooling.

**Lowest possible latency:** speech-to-speech model (OpenAI Realtime / Gemini Live) → Audio2Face-3D → any renderer, with ~100 ms lookahead and matched audio delay.

---

## 9. Gotchas checklist

- Model licenses (non-commercial weights; LivePortrait's InsightFace dependency; UE non-game terms)
- Consent for likeness and voice; disclosure obligations (EU AI Act transparency rules for AI interaction/deepfakes); biometric data rules (GDPR, BIPA)
- Test on the failure points: teeth/tongue, eye contact and blinks, hair edges, neck/clothing seam, large head turns, long sessions (drift)
- Chunking TTS too aggressively ruins prosody; too lazily ruins latency — clause-level with context carry-over is the sweet spot
- Per-session GPU cost is the business model; design the quality tiers (resolution, LOD, frame rate) before you scale

If you tell me which of the six framing questions you lean toward (real person vs synthetic, framing, scale), I can narrow this to a concrete stack and bill of materials.
