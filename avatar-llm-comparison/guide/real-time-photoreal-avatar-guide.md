# Building a Real-Time, Photorealistic Avatar with a Generated Voice

## A practical guide, current to 4 October 2026

**How this guide was produced.** Eight large language models were asked how to build a real-time rendered photorealistic avatar with a generated voice. Every concrete claim in their answers was checked against primary sources (papers, repositories, licence files, vendor and engine documentation). This guide keeps what survived that check, drops what did not, and adds the corrections. Where a statement is a judgement rather than a verified fact, it is marked as such. Dates matter in this field: several products the models recommended no longer exist.

---

## 1. Decide these first

Everything else follows from six questions. Answer them before choosing tools.

| Question | Why it decides the architecture |
|---|---|
| Does the camera ever leave a locked head-and-shoulders framing? | Locked framing allows 2D neural video, which is the cheapest route to a convincing mouth. Free camera, body, scene or XR needs true 3D (mesh or Gaussian splats). |
| A specific real person, or a synthetic person? | A real likeness needs capture footage and written consent. A synthetic human can be built from engine tools with no capture. |
| Interactive conversation, or driven from text or a script? | Conversation makes latency the hardest problem (target under about one second voice-to-voice) and requires barge-in handling. |
| Where does it render: a server GPU per session, or the client device? | Photoreal in a browser means server render plus WebRTC, or a Gaussian-splat avatar light enough for WebGPU. |
| One kiosk, or thousands of concurrent web users? | Per-session GPU cost is the business model at scale. |
| Build or buy, and is the use commercial? | Many strong open models ship weights under non-commercial licences (Section 8). |

---

## 2. The reference pipeline

Every component must stream. Never wait for a full response at any stage: first audio should start on the first clause of text, and first frames on the first 100 to 200 ms of audio.

```
[user mic] -> VAD / endpointing -> streaming STT --+
                                                   +--> LLM (token stream) -> clause chunker
[scripted text] -----------------------------------+                  |
                                                                      v
                                                         streaming TTS (PCM chunks)
                                                           |                  |
                                                           v                  v
                                              audio -> facial motion     audio to client
                                              (blendshapes, expression   (delayed to match
                                               codes, or pixels)          the video path)
                                                           |
                                                           v
            renderer (UE5 | Gaussian splats | 2D neural) -> NVENC H.264/AV1 -> WebRTC -> browser or app
```

Two rules that every working system obeys:

- **Audio is the master clock.** Facial animation follows audio timestamps, never the reverse.
- **Chunk at clause boundaries, with context carried over.** Chunking too aggressively ruins prosody; too lazily ruins latency.

---

## 3. Four ways to produce the pixels

### Option A. Game-engine 3D: Unreal Engine 5 with MetaHuman

**How it works.** A rigged photoreal character is rasterised in real time with Lumen global illumination, strand-based groom hair, subsurface-scattering skin and refractive eyes. The face is driven by ARKit-52 blendshapes or the full MetaHuman rig; the body from a motion-capture library.

**Face drivers available today (all verified):**

- **NVIDIA Audio2Face-3D.** Open-sourced in September 2025 under MIT with an SDK, training framework, Maya plugin and Unreal Engine 5 plugin. Outputs ARKit blendshapes (46 from the template, 52 through blendshape solving) plus an emotion estimate. It retargets to any character through blendshape solving; per-character training is optional, not required. Two caveats: the diffusion model streams in bursts of about 28 frames every 470 ms because of its one-second window and half-second stride, so for conversational use prefer the regression model, which emits one frame per audio chunk. The ACE Unreal plugin 2.5 supports UE 5.5 and 5.6 only, so check compatibility on 5.7 or 5.8. The old Omniverse Launcher path was deprecated on 1 October 2025.
- **MetaHuman Animator, audio-driven.** Introduced in UE 5.5 (November 2024) as an experimental offline solve; real-time audio-driven animation arrived in UE 5.6 (June 2025), with options for head movement and blinks.
- **TTS viseme or blendshape events.** Azure Speech emits 55 blendshape values per frame at 60 fps alongside the audio. Amazon Polly emits viseme speech marks. Cartesia returns phoneme-level timestamps. This costs no extra inference and is frame-accurate, at the price of slightly mechanical co-articulation.
- **Optical capture.** Live Link Face on an iPhone into MetaHuman Animator, for an actor-driven avatar.

**Requirements.**

- Skills: UE5 (Blueprint or C++), a technical artist for look-development, lighting and rig tuning, and animation sensibility.
- Hardware: an RTX 4080-class GPU (16 GB) or better for 1080p60 with groom hair at LOD0. Server-side, one L40S or A10G per stream; an L4 only with card hair and reduced LOD. Pixel Streaming (WebRTC) for browsers.
- Data: none for a synthetic human. For a real likeness, a head scan via MetaHuman identity capture or photogrammetry, then custom skin textures, which is where the real artist work lives.
- Animation library: captured idle, listening and gesture clips, plus procedural blinks, saccades, breathing and look-at.

**Licensing (verified).** MetaHuman left Early Access in June 2025 and its licence now permits use in Unity, Godot and other engines without royalty. In June 2026, MetaHuman 5.8 shipped with Unreal Engine 5.8, and Epic open-sourced the RigLogic and DNA libraries as OpenRigLogic under MIT, so MetaHuman-compatible facial evaluation can run outside Unreal. Unreal itself is free under one million dollars of annual revenue; above that, non-game companies pay 1,850 dollars per seat per year rather than the five percent game royalty. The web-based MetaHuman Creator is being retired in phases and closes on 5 November 2026; creation now lives inside the engine.

**Strengths.** Full body, free camera, scenes, lighting, outfits, deterministic output, stable identity, and native deployment to a kiosk or device.

**Weaknesses.** Hardest to make truly photoreal in motion. The uncanny valley comes from animation (dead eyes, generic co-articulation, no micro-expressions), not from shaders. Budget more for animation than for rendering.

### Option B. 2D audio-driven neural video (talking-head models)

**How it works.** A model takes a reference image or a short video of the person plus audio, and generates frames directly, either by inpainting the mouth region onto a looping base video or by generating whole-head motion.

**Real-time-capable open models (verified):**

- **MuseTalk.** Lip-region inpainting over a driving video; single forward pass per frame rather than iterative denoising; 30 fps or better on a V100; MIT licence for code, and the authors state the models may be used commercially. Output is a 256 by 256 face region, so an upscaler is usually bolted on.
- **Ditto** (Ant Group). Motion-space diffusion with a TensorRT path and a streaming mode designed for low first-frame delay.
- **LivePortrait family.** One-shot portrait animation, about 12 to 15 ms per frame on an RTX 4090. It needs an audio-to-motion front end such as JoyVASA. It depends on InsightFace, whose models are licensed for non-commercial research only.
- **Person-specific NeRF heads** (SyncTalk, ER-NeRF, GeneFace++). Train on three to five minutes of the person, then render in real time; SyncTalk reports 50 fps.

**Not real time:** Hallo, OmniHuman, EchoMimic, Loopy, EMO, LatentSync (about 18 GB VRAM at 512 by 512) and MOVA (January 2026, Apache-2.0, eight-second clips). Treat these as offline or preview tools.

**Requirements.** A portrait photo (low fidelity) or two to five minutes of static-camera video with gentle idle motion for the base loop; an RTX 4090, L4 or A10G carries one to three concurrent sessions at 25 to 30 fps; Python, CUDA and TensorRT skills; a compositing step to paste the face back into a higher-resolution frame; WebRTC publishing (LiveKit, Daily, aiortc or GStreamer).

**Strengths.** The most photoreal result per dollar and per week of effort, because it is video of a person.

**Weaknesses.** Fixed head-and-shoulders framing, limited head rotation, no camera moves, gestures limited to what the base loop contains, teeth and tongue artifacts, identity drift in long sessions, and per-session GPU cost.

### Option C. Neural 3D: Gaussian-splat head avatars

**How it works.** Capture the person, optimise a cloud of 3D Gaussians rigged to a FLAME head mesh, animate with expression and pose parameters, and rasterise at well over 100 fps. This is the open-research form of the codec-avatar direction.

**Methods (verified).** GaussianAvatars (multi-view rig). FlashAvatar, SplattingAvatar and MonoGaussianAvatar (monocular video; FlashAvatar trains in minutes and renders at 300 fps on a consumer GPU; SplattingAvatar reaches 30 fps on a mobile device). GaussianTalker and TalkingGaussian (audio-driven end to end, up to 120 fps). GaussianHeadTalk (WACV 2026) predicts 3DMM parameters from audio to suppress wobble. LAM builds an animatable Gaussian head from a single image, renders in the browser via WebGL and powers the OpenAvatarChat SDK. ExAvatar extends the idea to the whole body from a short monocular video. Tracking tools: VHAP or the metrical tracker for FLAME fitting.

**Requirements.** One to three minutes of monocular 30 fps video (head turns of about 45 degrees each way, varied expressions, speech, flat lighting), or a multi-camera rig for the best quality; minutes to a few hours of training on a 4090; inference is trivially real time, even client-side; a driver from audio to FLAME expression (Audio2Face to ARKit to FLAME, or a learned per-subject mapping); PyTorch and CUDA skills and tolerance for research code.

**Strengths.** True photorealism with 3D consistency, extremely cheap to render, and it can run in the browser.

**Weaknesses.** Research maturity, mostly bust-only, weak hair, torso, hands and mouth interior, and expressions limited to what was captured.

**Correction to a common claim.** Several models asserted that Gaussian-splat avatars need 24 to 64 cameras, hours to a day of training on data-centre GPUs, or an RTX 4080 to reach 30 fps. The published monocular methods above contradict each of those statements.

### Option D. Buy it: hosted real-time avatar APIs

**Vendors with live products in October 2026.** Tavus (Phoenix-3, Conversational Video Interface), HeyGen (LiveAvatar / Interactive Avatar), D-ID (Agents), Synthesia (Interactive Avatar API, Enterprise tier), Simli, Anam, Beyond Presence, bitHuman, Azure TTS Avatar, and the enterprise 3D vendors Soul Machines and UneeQ.

**Gone.** Hedra retired its Realtime Avatar product on 15 April 2026 and the LiveKit plugin was removed. Ready Player Me shut down its hosted avatar creator and public API on 31 January 2026 after the Netflix acquisition; do not build on it.

**Orchestration.** LiveKit Agents ships avatar plugins for Anam, Beyond Presence (bey), bitHuman, D-ID, HeyGen (liveavatar), Simli, Synthesia and Tavus. Pipecat integrates Simli, Tavus and HeyGen. The orchestration layer is the durable part of the system; the avatar vendor can be swapped later.

**Cost.** Published rates are in the tens of cents per conversation-minute: Tavus 0.26 to 0.35 dollars overage by tier, D-ID about 0.35, HeyGen interactive roughly 0.18 to 0.78. Cost scales linearly with usage.

**Requirements.** API keys, a WebRTC client, two to five minutes of consent video for a custom likeness, and a per-minute budget.

### Comparison

| | A. UE5 / MetaHuman | B. 2D neural | C. Gaussian splat | D. Hosted |
|---|---|---|---|---|
| Face realism | Good in stills, risky in motion | Excellent | Excellent | Excellent |
| Body, camera, scene | Yes | No | Bust only | No |
| Specific real person | Hard (textures) | Easy | Moderate (capture and train) | Easy |
| Frame rate | 60 fps | 25 to 30 fps | 100 fps and above | 25 to 30 fps |
| GPU per session | High | Medium | Low | Not yours |
| Time to first demo | Weeks | Days | Weeks | Hours |
| Maturity | Production | Production-ish | Research | Production |

**A hybrid worth knowing.** Render head and body in UE5 and composite a neural mouth (MuseTalk inpaints only the masked lower face) onto the engine frame. This keeps a free camera and 60 fps while borrowing 2D-grade lip detail. It is a real engineering project involving UV masks, alpha compositing and seam work, and it runs two models on one GPU. Judgement, not yet a documented product pattern.

---

## 4. Voice

| Tier | Examples (verified) | Time to first audio | Notes |
|---|---|---|---|
| Hosted streaming TTS | ElevenLabs Flash v2.5 (about 75 ms claimed), ElevenLabs Turbo v2.5 (about 300 ms), Cartesia Sonic (sub-90 ms claimed, about 40 ms model latency), Azure Neural, Amazon Polly, Google, Deepgram Aura, OpenAI TTS | 40 to 300 ms plus network | Azure, Polly and Cartesia give visemes or phoneme timestamps for free. OpenAI's TTS returns neither visemes nor word timestamps. |
| Self-hosted, small and fast | Kokoro (82 M parameters, Apache-2.0, runs on CPU), Piper (MIT) | Under 100 ms | No or limited cloning, less expressive. |
| Self-hosted with cloning | CosyVoice 2 (Apache-2.0), Orpheus 3B (Apache-2.0), Chatterbox (MIT), Zonos (Apache-2.0), Sesame CSM-1B (Apache-2.0), Kyutai TTS | 150 to 400 ms | Needs 4 to 12 GB of VRAM; vLLM or TensorRT helps. |
| Speech-to-speech | OpenAI Realtime, Gemini Live, Amazon Nova Sonic, Kyutai Moshi | 300 to 500 ms voice-to-voice | Collapses STT, LLM and TTS; you still need audio-to-face and lose control over text. |

**Licence traps.** XTTS-v2 is under the Coqui Public Model License (non-commercial). F5-TTS code is MIT but the released weights are CC-BY-NC. Fish Speech uses the Fish Audio Research License, and commercial use needs a separate licence. Wav2Lip is non-commercial. Retrieval-based Voice Conversion (RVC) is speech-to-speech voice conversion, not a text-to-speech system.

**Benchmark yourself.** Vendor latency figures are measured at the model; independent WebSocket benchmarks add 100 to 200 ms of network. Run identical prompts from your users' region and report the 95th percentile.

**Cloning data.** Five to thirty seconds for zero-shot cloning; thirty minutes to three hours of clean studio audio for a professional clone. Get written consent that explicitly covers voice cloning and synthetic media.

---

## 5. Latency and synchronisation budget

| Stage | Typical | How to shrink it |
|---|---|---|
| Endpointing (silence after the user stops) | 200 to 400 ms | Silero VAD plus semantic endpointing |
| STT final | 50 to 150 ms | Streaming partials are already available |
| LLM first clause | 250 to 600 ms | Small, fast model tuned for time to first token |
| TTS first audio | 80 to 250 ms | Split on clause boundaries, keep prosody context |
| Audio to face, render, encode | 40 to 120 ms (plus any model lookahead) | NVENC low-latency preset |
| Network, jitter buffer, decode | 80 to 200 ms | WebRTC |
| **Voice-to-voice total** | **0.7 to 1.5 s typical; about 0.5 s is excellent** | Speech-to-speech models collapse three stages |

**Audio-video sync.** ITU-R BT.1359 puts the detectability threshold at audio leading by 45 ms to audio lagging by 125 ms, and acceptability at plus 90 to minus 190 ms. Timestamp from one clock and delay audio playout by the animation latency. Unreal Pixel Streaming handles this when audio plays through the engine; custom pipelines must do it through RTP timestamps.

**Barge-in.** Detect user speech during avatar speech (client echo cancellation), cancel the LLM stream, flush TTS, clear animation and audio queues, and blend to a listening pose, all consistently.

**Liveness.** Blinks every three to six seconds with irregular timing, saccades, breathing, head sway, listening nods and backchannels. In 2D methods the base-video loop supplies these, so choose loop points carefully. This layer contributes more to "alive" than skin shading does.

---

## 6. Hardware sizing

| Deployment | GPU | What it carries |
|---|---|---|
| Development workstation | RTX 4090 or 5090 | UE5 plus Audio2Face plus a small TTS; LLM via API or a second GPU |
| Kiosk or installation | RTX 4070 to 4090 PC | UE5 locally at 1080p60, voice via API |
| Cloud, UE5 per session | L40S or A10G (L4 at reduced LOD) | One session per GPU, NVENC encode |
| Cloud, 2D neural | L4, A10G or 4090 | One to three sessions per 24 GB GPU at 30 fps |
| Cloud, Gaussian splat | L4 or smaller, or client-side | Many sessions per GPU |
| Self-hosted TTS | Shared GPU, 4 to 12 GB (Kokoro: CPU) | Several concurrent streams |

Reference prices (AWS us-east-1 on demand, October 2026): g5.2xlarge with one A10G at 1.21 dollars per hour; g6e.xlarge with one L40S at 1.86 dollars per hour. Note that an RTX 4080 has 16 GB of VRAM, not 24 GB; the 24 GB card is the 4090. A gigabit fibre line is not a requirement for streaming TTS, which runs at tens of kilobits per second.

---

## 7. Audio-to-face options at a glance

| Approach | Latency | Fidelity | Cost to set up |
|---|---|---|---|
| Audio2Face-3D regression model (open source) | Tens of ms per frame | High, with emotion | Medium: plugin, retarget, tune |
| Audio2Face-3D diffusion model | Bursty, about 470 ms cadence | Higher co-articulation | Not for interactive use without buffering |
| MetaHuman Animator audio-driven (UE 5.6 and later) | Real-time mode | High | Low inside Unreal |
| TTS visemes or blendshapes (Azure, Polly, Cartesia) | About zero | Medium, slightly mechanical | Low |
| Optical capture (Live Link Face) | About 20 ms | Highest | Needs an actor |
| Research drivers (UniTalker, EMOTE, GaussianHeadTalk) | Varies | Varies | High: research code |

For a locked talking-head framing, viseme timestamps from the TTS are competitive with neural lip-sync at a fraction of the cost. Reach for Audio2Face or a neural model when you need emotional range or a moving camera.

---

## 8. Legal and licensing checklist

- **Engine.** Unreal: free under one million dollars of revenue; 1,850 dollars per seat per year for non-game companies above it. MetaHuman characters may be used in other engines; OpenRigLogic is MIT.
- **Models.** Check weights separately from code. Non-commercial: XTTS-v2, F5-TTS weights, Fish Speech, Wav2Lip, InsightFace models (and therefore stock LivePortrait). Permissive: MuseTalk, Ditto, Kokoro, Piper, CosyVoice 2, Orpheus, Chatterbox, Zonos, Sesame CSM, LatentSync, MOVA.
- **Likeness and voice.** Written consent covering cloning, synthetic media, permitted uses, duration and revocation; secure storage of voice assets.
- **Disclosure.** The EU AI Act's Article 50 transparency rules (chatbot disclosure, deepfake labelling) apply from 2 August 2026. Biometric data rules under GDPR and Illinois BIPA apply when the avatar is a real person. Consider C2PA provenance marks.

---

## 9. What to build, by scenario

**Web product, live fast, head-and-shoulders.** LiveKit Agents or Pipecat, Deepgram STT, a fast LLM, Cartesia or ElevenLabs TTS, and a hosted avatar (Tavus, Simli, Anam, HeyGen, Synthesia). Swap the avatar vendor later; the orchestration is the durable part.

**Own IP, full control, body and scene, kiosk or installation.** UE5 plus MetaHuman plus Audio2Face-3D (regression model) or MetaHuman Animator real-time audio, plus streaming TTS (Azure if you want free visemes), plus Pixel Streaming for remote clients. Spend the budget on captured idle, listening and gesture performance from a real actor, not on more shader work.

**A specific real person, maximum realism, cheap to run.** Capture two to three minutes of video, train a Gaussian-splat head (or a per-person 2D model such as MuseTalk over a base loop) and drive it from Audio2Face or FLAME parameters. More engineering, lowest per-minute cost, best realism; accept research-grade tooling.

**Lowest possible latency.** A speech-to-speech model (OpenAI Realtime or Gemini Live) feeding Audio2Face-3D and any renderer, with a short lookahead and matched audio delay.

**A six-week plan for the engine route.**

1. Weeks 1 to 2: voice and brain. Streaming STT, LLM with clause chunking, streaming TTS with timestamps, measured end to end at the 95th percentile.
2. Weeks 2 to 3: the face. MetaHuman in UE5; drive it from TTS visemes first, then add Audio2Face-3D regression; verify audio-video offset stays inside the ITU window.
3. Weeks 3 to 4: liveness and interruption. Idle library, blinks, saccades, look-at; barge-in that flushes every queue.
4. Weeks 4 to 5: delivery. Pixel Streaming or native build, NVENC settings, TURN servers, one GPU per session measured.
5. Week 6: hardening. Session timeouts, cost per active minute, consent and disclosure flows, failure tests on teeth, tongue, hair edges, long sessions.

---

## 10. Mistakes to avoid (all observed in the model answers)

- Treating LivePortrait as a per-person trained model. It is one-shot.
- Expecting OpenAI's TTS to return visemes or timestamps. It does not; Azure, Polly and Cartesia do.
- Planning on Unity HDRP in a browser. HDRP is not supported on WebGL; URP is.
- Calling Audio2Photoreal a Gaussian-splat avatar or a talking-head driver. It is Meta's audio-to-gesture model rendered with Codec Avatars.
- Attributing OmniAvatar to Sony or to 3DGS. It is a Zhejiang University and Alibaba audio-driven video-generation model.
- Classing Nerfies as Gaussian splatting (it is a 2021 deformable NeRF), FaceX-Zoo as a lip-sync model (it is a face-recognition toolbox), EMO or Loopy as 3D head drivers (they are 2D video diffusion), or RVC as text-to-speech (it is voice conversion).
- Using Rhubarb Lip Sync for live audio. It is an offline command-line tool over recorded files.
- Claiming "generating video frames is too slow for real time." MuseTalk, Ditto and SyncTalk run at 30 to 50 fps.
- Saying Audio2Face-3D "needs per-character training" or "outputs 100-plus blendshapes." It retargets by blendshape solving and outputs 46 or 52 ARKit blendshapes.
- Recommending Ready Player Me or Hedra's realtime avatar. Both were discontinued in 2026.
- Quoting the five-percent Unreal royalty as the only cost. Non-game companies above one million dollars pay a per-seat licence.

---

## 11. Key sources

- NVIDIA Audio2Face-3D SDK (MIT): https://github.com/NVIDIA/Audio2Face-3D-SDK; paper: https://arxiv.org/abs/2508.16401; blendshape output: https://docs.nvidia.com/ace/audio2face-3d-microservice/2.0/text/getting-started/overview.html; diffusion streaming cadence: https://forums.developer.nvidia.com/t/361109; ACE Unreal plugin 2.5 changelog: https://docs.nvidia.com/ace/ace-unreal-plugin/2.5/ace-unreal-plugin-changelog.html
- MetaHuman audio-driven animation: https://dev.epicgames.com/documentation/en-us/metahuman/audio-driven-animation; MetaHuman 5.6 licence change: https://metahuman.com/news/metahuman-leaves-early-access-with-a-feature-packed-new-release; MetaHuman 5.8 and OpenRigLogic: https://github.com/EpicGames/openriglogic; web Creator shutdown: https://gamedev.net/news/1981-metahuman-creator-web-application-is-being-discontinued/; Unreal seat pricing: https://www.unrealengine.com/en-US/blog/we-are-updating-unreal-engine-twinmotion-and-realitycapture-pricing-in-late-april
- Azure visemes: https://docs.azure.cn/en-us/ai-services/speech-service/how-to-speech-synthesis-viseme; Polly speech marks: https://docs.aws.amazon.com/polly/latest/dg/speechmarks.html; Cartesia phoneme timestamps: https://docs.cartesia.ai/examples/tts-sse-with-phoneme-timestamps
- MuseTalk: https://github.com/TMElyralab/MuseTalk; Ditto: https://arxiv.org/abs/2411.19509; LivePortrait speed: https://github.com/KwaiVGI/LivePortrait/blob/main/assets/docs/speed.md; InsightFace licence: https://github.com/deepinsight/insightface#license; JoyVASA: https://arxiv.org/abs/2411.09209; SyncTalk: https://arxiv.org/abs/2311.17590
- GaussianAvatars: https://arxiv.org/abs/2312.02069; FlashAvatar: https://arxiv.org/abs/2312.02214; SplattingAvatar: https://arxiv.org/abs/2403.05087; GaussianTalker: https://arxiv.org/abs/2404.16012; GaussianHeadTalk: https://arxiv.org/abs/2512.10939; LAM: https://github.com/aigc3d/LAM; ExAvatar: https://arxiv.org/abs/2407.21686; VHAP: https://github.com/ShenhanQian/VHAP
- TTS licences: Kokoro https://github.com/hexgrad/kokoro; CosyVoice https://github.com/FunAudioLLM/CosyVoice; Orpheus https://github.com/canopyai/Orpheus-TTS; Chatterbox https://github.com/resemble-ai/chatterbox; Zonos https://github.com/Zyphra/Zonos; Sesame CSM https://github.com/SesameAILabs/csm; F5-TTS https://github.com/SWivid/F5-TTS#license; Fish Speech https://github.com/fishaudio/fish-speech/blob/main/LICENSE; XTTS https://github.com/coqui-ai/TTS/blob/dev/docs/source/models/xtts.md
- Vendor status: Hedra realtime sunset https://docs.livekit.io/agents/integrations/avatar/hedra; Ready Player Me shutdown https://avatarsdk.com/blog/2026/07/07/ready-player-me-migration-guide/; LiveKit avatar plugins https://github.com/livekit/agents/tree/main/livekit-plugins; Tavus pricing https://www.tavus.io/pricing; Synthesia Interactive Avatar API https://www.synthesia.io/post/interactive-avatar-api-real-time-avatars
- Sync thresholds (ITU-R BT.1359): https://www.tvtechnology.com/opinions/av-synchronization-how-bad-is-bad; EU AI Act Article 50: https://artificialintelligenceact.eu/transparency-rules-article-50/; AWS GPU prices: https://calculator.holori.com/aws/ec2/g5.2xlarge/us-east-1
