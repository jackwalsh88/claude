# Answer 8 of 8 — `space-bunny-alpha`

- **Source page:** OpenRouter Chat Playground (saved HTML), model shown as "Space Bunny Alpha" (`space-bunny-alpha`)
- **Note:** this answer ran live web searches before replying (the search steps are preserved below). It cost $0.0427 for 27,804 tokens per the page footer.

## Prompt

> would you go about putting together a real time rendered (frame rate) photorealistic avatar with generated voice. What would be your options and their requirements

## Response (verbatim, converted from HTML to Markdown)

I'll check what's current in this space before laying out options — this area moves fast.

Retrieved current date & time

Good — I have current data. Let me fill a few gaps.

Good — that's enough current state. Here's how I'd think about it.

## First: the framing question that decides everything

"Photorealistic + real-time" is a solvable problem in maybe three distinct ways, and which one you want depends almost entirely on one question: **does the camera ever move off a locked talking-head framing?**

- **Locked medium close-up, single avatar** → generative 2D is viable, cheaper, better-looking mouth
- **Free camera / turn-around / XR / orbit** → you need actual 3D (mesh or volumetric), no way around it
- **Many avatars, or your own face, at scale** → volumetric capture, but you pay per-subject training

Everything else — TTS choice, GPU tier, license, latency budget — follows from that. I'll assume you're near a locked framing unless you tell me otherwise, but cover both.

Also worth calibrating expectations: **all of these fail at the same place** — teeth and tongue on wide vowels. Every option below has that weakness. It's the reason to be skeptical of any demo that doesn't show you a "th" and an "ah."

---

## The four real options

### Option 1 — Classical 3D render pipeline (mesh + rig + game engine)

**Stack:** MetaHuman in UE5, or Reallusion iClone/Character Creator, or Unity HDRP. Face driven by ARKit-52 blendshapes.

**Where the animation comes from:**

| Method | Latency | Fidelity | Setup cost |
| --- | --- | --- | --- |
| Audio2Face-3D (ACE plugin) | ~50ms | High | **High** — needs per-character training |
| MetaHuman Animator (iPhone/Live Link Face) | ~20ms, optical | Highest | Medium — needs a capture session |
| iClone audio lip-sync (AccuLip etc.) | ~20ms | Medium | Low |
| Viseme timeline from TTS phoneme events | ~0ms | Medium | Low — needs a TTS that emits timestamps |
| Manual/scripted viseme keyframes | 0 | High (if authored) | Manual, no generality |

**Requirements:**

- GPU: RTX 4060 8GB minimum for a single head at 1080p60; 16GB+ if you want hair, a body, and a second pass. Apple Silicon handles this well on Metal.
- Engine knowledge: someone who knows RigLogic, LODs, material setup. This is not a weekend project the first time.
- Per-character asset work: MetaHuman Creator gives you a base head, but shipping-quality takes a groom pass, LOD chain, and texture work. Stock MetaHumans look uncanny in a way that untextured assets don't — you need skin detail, eye wetness, and correct subsurface.

**Two current gotchas I'd flag specifically:**

1. **Audio2Face-3D's diffusion model streams in bursts.** It has a 1s sliding window / 0.5s stride, so you get ~28 frames every ~470ms, not smooth per-frame output. You have to pre-buffer ~500ms to pace it, which kills conversational latency. The older *regression* model streams continuously at 1 frame per chunk — use that for interactive, not the diffusion one. Also, the ACE Unreal plugin's changelog tops out at UE 5.6, so check compatibility if you're on 5.7/5.8.
2. **Animated maps are a CPU bottleneck, not GPU.** MetaHuman's material curve transfer can cost 20-30 FPS per character with GPU time barely moving. The fix is ticking "Enable Material Parameter Caching" on your face mesh components — it's on by default for MetaHumans but not for custom actor blueprints. Irrelevant at one character, fatal at ten.

**Upside:** free camera, true 60fps+, stable identity, cancellable mid-sentence, tiny latency.  
**Downside:** highest engineering cost; you own the uncanny valley, which lives in the eyes, blink timing, and skin shading — not the mouth.

---

### Option 2 — Volumetric capture (3DGS / NeRF head avatar)

**Stack:** Capture a video of the person, train a Gaussian-splatting head avatar, drive with blendshapes or an audio→3DMM predictor.

**Current state (Oct 2026):**

- Research pipelines like **LiveAvatar** now hit >20fps from monocular video with *no per-subject training*
- **GaussianHeadTalk** (WACV 2026) predicts 3DMM params straight from audio and splats — explicitly targets the wobble problem
- Browser deployment is now real: **BONSAI** reports 340fps neural Gaussian avatars via WebGPU after 98% decoder pruning; **WebSplatter** and **Visionary** (open source, WebGPU+ONNX) handle cross-device 3DGS

**Requirements:**

- GPU: 8-16GB for inference; the capture/training itself wants 24GB+
- Per-identity capture + training if you go the high-fidelity route: 20-60 min of multi-angle video, hours of training
- A neural renderer dev who's comfortable with CUDA/TensorRT (or WebGPU)

**Upside:** extremely convincing *at the captured viewpoints*, near-zero mouth cost (it's baked), fast.  
**Downside:** view-dependent artifacts outside the capture envelope, teeth/tongue are almost always wrong, and the moment the user tilts the head you get wobble. This is a very high-quality trick that falls apart under a free camera.

---

### Option 3 — Generative frame synthesis (no 3D at all)

You have a photo or video loop. Audio in, frames out. No mesh, no rig, no camera problem because there is no camera.

| Model | Speed | VRAM | Res (face) | License | Verdict |
| --- | --- | --- | --- | --- | --- |
| Wav2Lip | realtime | low | 96px mouth | non-commercial | Timing baseline only |
| **MuseTalk 1.5** | **30fps+ (V100)** | **~8GB** | 256×256 | MIT | **The only open real-time option** |
| LatentSync 1.6 | sec–min/clip | ~18GB | 512×512 | Apache-2.0 | Quality, not speed |
| MOVA (Jan 2026) | offline | ~48GB | 360p/720p | Apache-2.0 | 8s cap, not runtime |

**Why MuseTalk is the only real-time one:** it's single-step latent-space inpainting of just the masked mouth region, not iterative denoising. One forward pass per frame. That's the entire architectural reason it clears 30fps at 8GB while LatentSync doesn't. Its cost is that 256×256 output needs a GFPGAN-style upscaler bolted on afterward, which adds latency and can shimmer on fast jaw motion.

Also newer: diffusion-based portrait animators (Hallo family, EchoMimic v2/v3, AniPortrait) produce natural head motion and expression, not just mouths — but they're seconds-per-frame with mixed commercial licenses. Treat as offline/preview tools.

**Upside:** best lip realism per dollar, tiny GPU, trivially many avatars, no lighting/rig work.  
**Downside:** 30fps not 60, identity drift and temporal flicker, no expression control beyond what the audio implies, and you're trusting a 256px crop of a mouth to carry the illusion.

---

### Option 4 — Hybrid (what I'd actually build)

**Render the head and body in UE5, and neural-render only the mouth region.** Because MuseTalk only inpaints a masked lower face, you can composite it onto a proper lit 3D head.

This gets you: true free camera and stable 60fps from the engine, *plus* MuseTalk-class lip detail, *plus* real eyes/head/hair from the 3D layer. And crucially, the mouth is where viewers focus during speech but not during listening — so during listening you can drop the neural pass entirely and be at pure 60fps.

**Cost:** a UV-mask + alpha-composite pass, plus the seam/blend work around the mask, plus running both models on one GPU (8GB MuseTalk + UE5 in 16GB is tight but workable). This is a real engineering project, not a config change.

---

## Voice — and the thing people miss

**Cloud (pick on latency, benchmark yourself):** Cartesia Sonic 3.5 (~90-120ms first byte, and the SSE API returns **phoneme timestamp events**), ElevenLabs Flash v2.5 (~75ms claimed), Azure. Vendor latency numbers are unreliable — one self-published benchmark I found reported an unnamed "Gepard" model at 49ms median vs Cartesia at 94-123ms and ElevenLabs at 175-190ms. Treat all published numbers as marketing until you run identical prompts from your users' region over WebSocket and report p95.

**Local/on-prem:** Kokoro (82M, Apache-2.0, 28-85ms first audio, RTF 0.01-0.05) is the speed king but has no cloning and limited voice choice. F5-TTS (MIT, cloning, ~90ms on a 4090) or Chatterbox (MIT, ~78ms) if you need voice identity. Note that most of these are still *slower than realtime on CPU* — self-hosted TTS needs a GPU, and if it's sharing the card with the renderer you'll get frame hitches. Budget a second GPU or do voice on a server.

**The thing worth knowing:** get a TTS that emits **phoneme or viseme timestamps with the audio stream** (Azure viseme events, Cartesia phoneme events, Amazon speech marks). Then your lip sync costs ~5ms, needs no ML model, is frame-accurate, and is trivially interruptible. For a locked talking-head framing this is genuinely competitive with MuseTalk on quality and vastly cheaper. Only reach for Audio2Face or neural lipsync when you need emotional expressiveness or have a camera that moves.

---

## Requirement summary

|  | Opt 1 (3D) | Opt 2 (3DGS) | Opt 3 (Generative) | Opt 4 (Hybrid) |
| --- | --- | --- | --- | --- |
| **GPU** | 8-16GB NVIDIA / Apple | 8-16GB infer, 24GB+ capture | ~8GB | 16GB+ |
| **Achieves 60fps** | Yes | ~20-60fps | ~30fps | Yes (drop neural pass when idle) |
| **Free camera** | Yes | Within capture envelope | N/A | Yes |
| **Per-avatar setup** | Days | Hours + training | Minutes | Days |
| **Biggest risk** | Uncanny eyes/blink | Wobble, teeth, off-angle | Flicker, 256px | Seam/blend engineering |
| **Engineering skill** | Unreal/3D art | Neural rendering | ML inference | All three |

**Cross-cutting:**

- **Latency budget** for something that feels live: VAD/endpointing 150-400ms (usually your biggest hidden cost) + LLM 200-800ms + TTS first chunk 50-200ms + viseme analysis 5-20ms + render 8-16ms. Under 300ms feels instantaneous, under 500ms feels conversational, over 1s feels broken. Start the mouth animating on the first streamed audio chunk — don't wait for the full utterance.
- **Licensing:** MetaHuman left Early Access and its licensing changed during 2026 — read the current EULA before committing. Wav2Lip's OSS is non-commercial. XTTS-v2 is CPML, not truly permissive. NVIDIA's Omniverse Launcher path for Audio2Face was discontinued Oct 2025 (you can still get the 2023.2.0 ZIP). Note 5.8 open-sourced RigLogic/DNA as **OpenRigLogic, MIT** — that's MetaHuman-compatible facial tech usable outside Unreal, and it may open up cheaper routes.
- **Privacy:** if the avatar is a real person, you're in biometric-data territory — Illinois BIPA, GDPR, CCPA. Get written consent that explicitly covers voice cloning and synthetic media, and be able to prove it.
- **The cheap quality wins** nobody budgets for: procedural blink (with natural irregularity), saccades, breathing, subtle head sway, and a good camera + lighting setup. A MetaHuman with correct idle micro-motion reads as alive; a MuseTalk frame with a perfect mouth and dead eyes reads as a corpse. In my experience idle behavior buys more perceived realism than mouth quality.

---

## What I'd recommend

**If you can hold a locked talking-head framing:** Option 3 + phoneme timestamps, or Option 4 if you want the head to move. Start there — it's a week of work, not a month, and it will tell you fast whether the uncanny valley is in your lighting or your model.

**If you need any camera freedom or XR:** Option 1, MetaHuman + UE 5.8, with viseme-timestamp-driven blendshapes as your starting point. Add Audio2Face-3D (regression model, not diffusion) later only if you need emotional range. Budget for OpenRigLogic if you want to escape the Unreal dependency.

**If it's your own face and you want zero art skill:** Option 2, 3DGS from a capture session.

Before I go further — a few things would sharpen this a lot:

1. **Locked framing or free camera?** This alone eliminates two of the four options.
2. **Interactive conversation (needs <500ms, must be interruptible) or pre-rendered content?** Interactive rules out MOVA, LatentSync, and basically all the diffusion animators.
3. **Browser or native app?** Browser caps you at WebGPU/WebRTC and changes the photorealism ceiling significantly. Native lets you use Unreal.
4. **One avatar or many? Stock character or a specific real person's likeness?**
5. **What hardware do you actually have, and what's the budget for GPU/cloud?**

15 citations

[Audio Driven Animation | MetaHuman Documentation

https://dev.epicgames.com/documentation/metahuman/audio-driven-animation?lang=en-US

dev.epicgames.com](https://dev.epicgames.com/documentation/metahuman/audio-driven-animation?lang=en-US)

[MH Animator - runtime lipsync from audio

https://forums.unrealengine.com/t/mh-animator-runtime-lipsync-from-audio/2611561

forums.unrealengine.com](https://forums.unrealengine.com/t/mh-animator-runtime-lipsync-from-audio/2611561)

[MetaHuman 5.7 Released! - Announcements - Epic Developer Community Forums

https://forums.unrealengine.com/t/metahuman-5-7-released/2672724

forums.unrealengine.com](https://forums.unrealengine.com/t/metahuman-5-7-released/2672724)

[MetaHuman 5.8 Released! - Announcements - Epic Developer Community Forums

https://forums.unrealengine.com/t/metahuman-5-8-released/2729288

forums.unrealengine.com](https://forums.unrealengine.com/t/metahuman-5-8-released/2729288)

[MetaHuman 5.7 is now available - MetaHuman

https://www.metahuman.com/releases/metahuman-5-7-is-now-available

www.metahuman.com](https://www.metahuman.com/releases/metahuman-5-7-is-now-available)

[MuseTalk: Real-Time High Quality Lip Synchronization ...

https://arxiv.org/html/2410.10122v2

arxiv.org](https://arxiv.org/html/2410.10122v2)

[Open Source Lip Sync Models 2026: LatentSync, MuseTalk, MOVA

https://news.creeta.com/en/open-source-lip-sync-models-2026/

news.creeta.com](https://news.creeta.com/en/open-source-lip-sync-models-2026/)

[AI Lip-Sync Model Selection Guide 2026: MuseTalk, LatentSync, Wav2Lip, SadTalker

https://tomodahinata.com/en/blog/ai-lip-sync-talking-head-model-selection-guide-2026

tomodahinata.com](https://tomodahinata.com/en/blog/ai-lip-sync-talking-head-model-selection-guide-2026)

[MuseTalk Complete Guide: Realtime Lip Sync in Production

https://tomodahinata.com/en/blog/musetalk-realtime-lip-sync-production-guide

tomodahinata.com](https://tomodahinata.com/en/blog/musetalk-realtime-lip-sync-production-guide)

[What is MuseTalk? The real-time lip sync model | sync. labs blog

https://sync.so/blog/what-is-musetalk

sync.so](https://sync.so/blog/what-is-musetalk)

[Best Low-Latency TTS API: Cartesia, ElevenLabs, OpenAI TTS, and Azure | YixScout

https://yixscout.com/resources/columns/low-latency-tts-api

yixscout.com](https://yixscout.com/resources/columns/low-latency-tts-api)

[https://elevenlabs.io/docs/api-reference/text-to-speech/stream.md

https://elevenlabs.io/docs/api-reference/text-to-speech/stream.md

elevenlabs.io](https://elevenlabs.io/docs/api-reference/text-to-speech/stream.md)

[TTS latency benchmark: 50 ms to first audio | nineninesix.ai

https://www.nineninesix.ai/blog/tts-latency-benchmark-websocket-2026

www.nineninesix.ai](https://www.nineninesix.ai/blog/tts-latency-benchmark-websocket-2026)

[ElevenLabs vs Azure TTS: voices & deployment

https://www.cartesia.ai/vs/elevenlabs-vs-microsoft-azure-text-to-speech

www.cartesia.ai](https://www.cartesia.ai/vs/elevenlabs-vs-microsoft-azure-text-to-speech)

[https://docs.cartesia.ai/api-reference/tts/sse

https://docs.cartesia.ai/api-reference/tts/sse

docs.cartesia.ai](https://docs.cartesia.ai/api-reference/tts/sse)

15 citations

[Audio2Face: AI-Powered Expressions & Lip Sync | iClone

https://www.reallusion.com/iclone/nvidia-omniverse/Audio2Face.html

www.reallusion.com](https://www.reallusion.com/iclone/nvidia-omniverse/Audio2Face.html)

[[Audio2Face / Digital Human] SDK v3.0 Diffusion Model — Frame gap during streaming inference (posting here as Digital Human board is closed) - Deep Learning (Training & Inference) / TensorRT - NVIDIA Developer Forums

https://forums.developer.nvidia.com/t/audio2face-digital-human-sdk-v3-0-diffusion-model-frame-gap-during-streaming-inference-posting-here-as-digital-human-board-is-closed/361109/1

forums.developer.nvidia.com](https://forums.developer.nvidia.com/t/audio2face-digital-human-sdk-v3-0-diffusion-model-frame-gap-during-streaming-inference-posting-here-as-digital-human-board-is-closed/361109/1)

[Audio2Face-3D NIM Documentation — NVIDIA NIM Audio2Face-3D

https://docs.nvidia.com/nim/digital-human/a2f-3d/latest/index.html

docs.nvidia.com](https://docs.nvidia.com/nim/digital-human/a2f-3d/latest/index.html)

[ACE Unreal Plugin Changelog — ACE Unreal Plugin

https://docs.nvidia.com/ace/ace-unreal-plugin/2.5/ace-unreal-plugin-changelog.html

docs.nvidia.com](https://docs.nvidia.com/ace/ace-unreal-plugin/2.5/ace-unreal-plugin-changelog.html)

[NVIDIA/Audio2Face-3D

https://github.com/NVIDIA/Audio2Face-3D/

github.com](https://github.com/NVIDIA/Audio2Face-3D/)

[tts-bench — Speed

https://5uck1ess.github.io/tts-bench/speed.html

5uck1ess.github.io](https://5uck1ess.github.io/tts-bench/speed.html)

[TTS Latency Benchmarks

https://gigagpu.com/tts-latency-benchmarks/

gigagpu.com](https://gigagpu.com/tts-latency-benchmarks/)

[Best Open-Weight Text-to-Speech Models 2026 | Presenc AI

https://presenc.ai/research/best-open-weight-text-to-speech-models-2026

presenc.ai](https://presenc.ai/research/best-open-weight-text-to-speech-models-2026)

[F5-TTS vs Kokoro: Text-to-Speech Models Comparison (2026)

https://faun.dev/toolbox/f5-tts-vs-kokoro/

faun.dev](https://faun.dev/toolbox/f5-tts-vs-kokoro/)

[TTS Libraries Comparison | Notes | Notes

https://notes.itsvasugrover.com/kb/ai/tts/libraries-comparison/

notes.itsvasugrover.com](https://notes.itsvasugrover.com/kb/ai/tts/libraries-comparison/)

[BONSAI: Browser-Optimized Neural Gaussian Avatar Streaming

https://cg.informatik.uni-bonn.de/backend/v2/files/publications/kitz-2026-bonsai/pdf/Web3d\_fb7112f631.pdf

cg.informatik.uni-bonn.de](https://cg.informatik.uni-bonn.de/backend/v2/files/publications/kitz-2026-bonsai/pdf/Web3d_fb7112f631.pdf)

[LiveAvatar: Real-time 3D Gaussian Head Avatars from Single Images | Proceedings of the 2026 ACM International Conference on Interactive Media Experiences

https://dlnext.acm.org/doi/10.1145/3788851.3815056

dlnext.acm.org](https://dlnext.acm.org/doi/10.1145/3788851.3815056)

[GaussianHeadTalk: Wobble-Free 3D Talking Heads with ...

https://wacv.thecvf.com/virtual/2026/poster/445

wacv.thecvf.com](https://wacv.thecvf.com/virtual/2026/poster/445)

[Visionary-Laboratory/visionary

https://github.com/Visionary-Laboratory/visionary

github.com](https://github.com/Visionary-Laboratory/visionary)

[WebSplatter: Efficient and Faithful In-Browser 3D Gaussian Splatting across Devices via WebGPU

https://websplatter.github.io/

websplatter.github.io](https://websplatter.github.io/)
