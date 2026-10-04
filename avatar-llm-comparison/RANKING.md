# Accuracy ranking of eight LLM answers

**Prompt (identical for all eight):** "would you go about putting together a real time rendered (frame rate) photorealistic avatar with generated voice. What would be your options and their requirements"

**Date basis for "current" facts:** 2026-10-04. A claim is marked *dated* when it was true at some point but is no longer true on that date (for example, a product that has since shut down).

**Evidence:** every finding below cites an entry in the [Evidence catalogue](#evidence-catalogue) (E1–E45). Sources were fetched during this session; where a vendor page was unreachable from this sandbox (Hugging Face, Microsoft Learn, hedra.com, synthesia.io, docs.livekit.io, developers.openai.com), the finding relies on the project's GitHub repository, the vendor's secondary pages, or search snippets, and says so.

**Update (same day):** the user supplied an OpenRouter log of the real `Space Bunny Alpha` answer. It is a distinct eighth response (file 08). The Arena Agent-mode answer (file 01), provisionally labelled `space-bunny-alpha` earlier, is therefore back to "undisclosed".

**Disclosure:** this ranking was produced by Claude Fable 5.1. One of the eight answers is from `claude-fable-5.1-max`, the same model family. Every finding for that answer is backed by the same kind of external evidence as the others, and the one dated item and one numeric slip it contains are listed. A reader can re-derive the ranking from the error tallies alone.

---

## Summary

| Rank | Answer (file) | Hard factual errors | Dated as of 2026-10-04 | Unverifiable / weak | Verified-correct specific claims |
|---|---|---|---|---|---|
| 1 | `claude-fable-5.1-max` ([05](05-claude-fable-5.1-max.md)) | 0 (one minor numeric slip) | 1 (Hedra Live) | 2 | ~40 |
| 2 | `gpt-5.6-terra-low` ([02](02-gpt-5.6-terra-low.md)) | 0 | 0 | 0 | ~10 (few checkable claims) |
| 3 | `space-bunny-alpha` ([08](08-space-bunny-alpha.md)) | 3 | 0 (it ran live web searches) | 4 | ~25 |
| 4 | `step-5-preview` ([03](03-step-5-preview.md)) | 2 | 2 | 1 | ~15 |
| 5 | `grok-4.20-multi-agent-beta-0309` ([06](06-grok-4.20-multi-agent-beta-0309.md)) | 2 | 1 | 0 | ~10 |
| 6 | `qwen3.5-397b-a17b` ([07](07-qwen3.5-397b-a17b.md)) | 4 | 2 | 1 | ~8 (plus leaked reasoning in the output) |
| 7 | `muse-spark-1.3-max` ([04](04-muse-spark-1.3-max.md)) | 6 | 3 | 1 | ~15 |
| 8 | anonymous Arena Agent-mode model ([01](01-anonymous-arena-agent.md)) | 7 | 2 | 1 | ~8 |

**How ties were broken.** Ranks 1 and 2 both have zero hard errors. `gpt-5.6-terra-low` reaches that by making almost no checkable claims (vendors are named as "Synthesia-style", "HeyGen-style"; no versions, licences, prices or performance numbers). `claude-fable-5.1-max` makes roughly forty checkable claims and all but one minor threshold figure verified. Under a pure "fewest flaws" metric `gpt-5.6-terra-low` would be first; under "accuracy of the information actually supplied" the order shown holds. Both readings are stated so the reader can choose.

Ranks 3 to 5: `space-bunny-alpha` has one more hard error than `step-5-preview` or `grok-4.20` (3 vs 2) but zero stale claims and the largest number of verified, current-state specifics after rank 1, because it searched the web before answering. By hard-error count alone it would sit at rank 5; it is placed at 3 for the same reason rank 1 sits above rank 2.

Ranks 6 and 7: `muse-spark-1.3-max` is far more detailed and useful than `qwen3.5-397b-a17b`, but it also contains more verified factual errors (6 vs 4). The ranking is by accuracy, as requested, not by usefulness.

---

## 1. `claude-fable-5.1-max` — rank 1

**Verified correct (selection):**
- Audio2Face-3D is open source with a UE5 plugin, TensorRT runtime, ARKit blendshape plus emotion output (E14, E15).
- MetaHuman Animator audio-driven animation arrived in UE 5.5 and gained a real-time mode in 5.6 (E17).
- Azure TTS emits 55 blendshapes at 60 fps alongside audio (E12).
- MetaHuman licence relaxed in June 2025 to permit use in other engines (E16).
- MuseTalk: MIT, 30 fps+ real time, face-region inpainting over an input video (E34).
- Ditto: Ant Group, motion-space diffusion, TensorRT, streaming mode (E24).
- LivePortrait: one-shot, roughly 12–15 ms/frame on an RTX 4090, depends on InsightFace whose models are non-commercial (E35). JoyVASA as its audio front-end (E36).
- VASA-1 unreleased (E27).
- GaussianAvatars multi-view; FlashAvatar / SplattingAvatar / MonoGaussianAvatar monocular; GaussianTalker and TalkingGaussian audio-driven 3DGS; LAM one-shot with WebGL render used by OpenAvatarChat; ExAvatar full body (E28–E33).
- VHAP / metrical tracker for FLAME tracking; UniTalker, EMOTE as research drivers (E31, E32).
- TTS licences all check out: Kokoro Apache-2.0 (82M), Piper MIT, CosyVoice 2 Apache-2.0, Orpheus Apache-2.0 (3B), Chatterbox MIT, Zonos Apache-2.0, Sesame CSM Apache-2.0; XTTS-v2, F5-TTS weights and Fish Speech are non-commercial (E38).
- Tavus Phoenix-3 (E42); Simli, Anam, Beyond Presence, Synthesia, D-ID exist as real-time avatar vendors with LiveKit plugins; LiveKit Agents and Pipecat both have avatar integrations (E43). Hosted pricing "tens of cents per conversation-minute" matches Tavus $0.26–0.35, D-ID about $0.35, HeyGen $0.18–0.78 (E26).
- Azure and Amazon Polly provide visemes with the audio (E12, E44). EU AI Act transparency rules exist (E45).

**Issues found:**
- *Dated:* lists "Hedra Live" among hosted vendors. Hedra shut down its Realtime Avatar product on 2026-04-15 and the LiveKit plugin was removed (E10, E43).
- *Minor numeric slip:* quotes A/V sync detectability as "−45 ms / +100 ms". ITU-R BT.1359 gives +45 ms (audio leads) to −125 ms (audio lags) (E40). Right order of magnitude, wrong lag figure and inverted sign convention.
- *Unverified:* "ONNX" as an Audio2Face-3D runtime (the SDK README documents TensorRT only, E14); "configurable lookahead" in Audio2Face-3D.

## 2. `gpt-5.6-terra-low` — rank 2

**Verified correct:** MetaHuman Animator and Live Link Face as face drivers; NVIDIA Audio2Face; Pixel Streaming over WebRTC; L4 / A10 / A16 as cloud GPU classes; a first-audio target of roughly 0.8–1.5 s; Unity HDRP as the higher-quality Unity pipeline; TURN servers for WebRTC. None of these conflict with any source in the catalogue.

**Issues found:** none that could be falsified. The answer avoids versions, licences, prices and performance figures, and names vendors only as categories ("Synthesia-style", "HeyGen-style", "Tavus-style"). It is accurate because it is non-committal. It also contains no dated items (it never mentions Ready Player Me or Hedra).

## 3. `space-bunny-alpha` — rank 3

This answer ran six live web searches before replying, which is why it is the only one with no stale product claims. It also provided 15 citations; the ones checked below hold up except where noted.

**Verified correct (selection):**
- Audio2Face-3D diffusion model streams in bursts of about 28 frames every ~470 ms because of its 1 s window / 0.5 s stride; the regression model emits one frame per chunk (E48).
- ACE Unreal plugin 2.5 supports UE 5.5 and 5.6 only (E49).
- Omniverse Launcher deprecated 1 October 2025 (E50).
- MetaHuman 5.8 shipped with UE 5.8 (17 June 2026) and Epic open-sourced RigLogic/DNA as OpenRigLogic under MIT (E51).
- GaussianHeadTalk (WACV 2026) predicts 3DMM parameters from audio for wobble-free Gaussian talking heads (E52).
- MOVA released 29 January 2026, Apache-2.0, 8-second 360p clips; LatentSync 1.6 Apache-2.0, 512×512, about 18 GB VRAM (E53).
- Wav2Lip is non-commercial and generates a 96 px mouth region (E54). MuseTalk 1.5: 30 fps+ on a V100, MIT, single-pass latent inpainting rather than iterative denoising (E34).
- Cartesia's SSE/WebSocket API returns phoneme timestamp events (E56); Azure viseme events and Amazon speech marks exist (E12, E44). ElevenLabs Flash v2.5 about 75 ms (E25). Kokoro Apache-2.0 82M; Chatterbox MIT; XTTS-v2 CPML (E38).
- Visionary is an open WebGPU + ONNX Gaussian-splat platform (E57); LiveAvatar (Intel Labs) exists as a monocular-to-3DGS head avatar project (E58).
- `Enable Material Parameter Caching` is a real MetaHuman mesh-component property that caches parameter lookups to cut CPU cost (E59).

**Hard errors:**
1. Table row "Audio2Face-3D (ACE plugin) … Setup cost: High — needs per-character training". Audio2Face-3D retargets to any character through blendshape solving; per-character training is optional, not required (E55).
2. "MetaHuman left Early Access and its licensing changed during 2026." Both happened with MetaHuman 5.6 in June 2025 (E16).
3. "F5-TTS (MIT, cloning …)". The code is MIT but the released weights are CC-BY-NC, so it is not a permissive option for a product (E38).

**Unverified:** "BONSAI reports 340 fps neural Gaussian avatars via WebGPU after 98% decoder pruning" (no indexed paper found under that name, E57); the 20–30 FPS per-character figure attributed to animated-map CPU cost (the setting exists, the number could not be sourced, E59); "MOVA ~48 GB" (its authors recommend at least 24 GB with offloading, E53); LiveAvatar ">20 fps with no per-subject training" (repository exists, the figure was not checked, E58).

## 4. `step-5-preview` — rank 4

**Verified correct:** MetaHuman Creator as a pre-scanned base with limited customisation; Audio2Face on RTX GPUs; Pixel Streaming; a latency table whose "lip-sync offset < 80 ms" sits inside the ITU detectability window (E40); RTX 6000 Ada 48 GB; "SaaS gives you a compressed video stream, not frame-rate rendering"; RVC and so-vits-svc correctly classed as voice changers rather than TTS (E6).

**Hard errors:**
1. Option 4: "Multi-camera capture rig (24–64 cameras minimum)" and "Not yet practical for arbitrary real-time dialogue. You are limited to the captured performance." Monocular, FLAME-rigged Gaussian avatars existed in 2023–2024 and render at 300 fps (FlashAvatar, SplattingAvatar); GaussianTalker drives 3DGS heads from audio at up to 120 fps (E28, E29).
2. "Unreal Engine 5.3+ Nanite (high-poly face)". Nanite for skeletal meshes was only introduced, as experimental, in UE 5.5 (E22); a MetaHuman face in 5.3 is not Nanite.

**Dated:** recommends "GPT-4o-mini, Claude 3.5 Sonnet, or local Llama 3 8B" and "Unreal Engine 5.4" in a 2026 answer.

**Weak / unverified:** "Audio2Face plugin for Unity" (NVIDIA's documented plugins are for Unreal Engine 5 and Maya; one secondary report mentions Unity, E14, E46). "Apple Silicon struggles with UE5 Lumen" overstates: Lumen with software ray tracing is supported on M1 and later, hardware ray tracing is not (E23). Lists "Coqui XTTS … Free" without noting its non-commercial licence (E38).

## 5. `grok-4.20-multi-agent-beta-0309` — rank 5

**Verified correct:** UE5 + MetaHuman + Audio2Face + streaming TTS as the main production stack; Audio2Face is free / SDK available (E14); "RTX 4080/5090-class, 16 GB+ VRAM" is consistent with the 4080's 16 GB (E20); HeyGen, D-ID, Soul Machines, Convai are real vendors; NVIDIA ACE bundles Riva and Audio2Face.

**Hard errors:**
1. Neural 2.5D option: "5–30 minutes of training video of the person" and "Train/fine-tune on a short video or even good photos", with LivePortrait as the headline tool. LivePortrait is one-shot and needs no per-person training (E35); person-specific NeRF methods need a few minutes of video, not up to 30 (E37).
2. 3DGS option: "Training: A100/H100 GPUs, hours to a day per avatar … Inference: RTX 4080+ for 30–60 FPS". FlashAvatar trains in minutes and renders at 300 fps on a consumer GPU; SplattingAvatar runs at 30 fps on a mobile device (E28).

**Dated:** "MetaHuman Creator (cloud tool)". The Creator moved into the engine with UE 5.6 and the web app is being retired (E16, E18).

**Imprecise:** describes MetaHuman Animator as the tool that "turns a real person into a custom rigged head"; Animator is the animation solver, identity creation is the MetaHuman Identity / Mesh-to-MetaHuman workflow (E16, E17).

## 6. `qwen3.5-397b-a17b` — rank 6

**Output defect:** the response begins with roughly 900 words of leaked planning text ("Here's a thinking process that leads to…", "matches the detailed response provided previously") before the actual answer. This is not a factual error but it is content the user was not meant to receive.

**Verified correct:** ElevenLabs Turbo v2.5 under about 300 ms (E25); Azure Neural TTS has viseme support (E12); XTTS v2 as a local option; Silero VAD; streaming TTS and idle animation advice; cloud GPU at roughly $1.50/hr (g5.2xlarge is $1.21/hr, E21).

**Hard errors:**
1. "GPU: NVIDIA RTX 4080 or 4090 (24GB VRAM minimum)". The RTX 4080 has 16 GB (E20); the line contradicts itself.
2. "Network: 1Gbps+ Fiber (if streaming TTS audio)". Streaming speech is tens of kilobits per second; no source supports a gigabit requirement.
3. Option 3 pairs Rhubarb Lip Sync with a real-time avatar. Rhubarb is an offline command-line tool that processes recorded audio files (E39).
4. "Do not try to generate video frames … it is too slow." MuseTalk runs at 30 fps+ (E34), Ditto is real-time with streaming (E24), GeneFace++ and SyncTalk render in real time, SyncTalk at 50 fps (E37).

**Dated:** Ready Player Me as the Unity avatar source (shut down 2026-01-31, E9); "Llama-3-70b via Groq".

**Incomplete:** "UE5 is free (5% royalty after $1M)" omits the $1,850 per-seat annual licence for non-game companies above $1M revenue, which is the likely category for an avatar product (E41).

**Unverified:** Audio2Face connecting to UE5 "via OSC". Live Link is documented; OSC is not (E14).

## 7. `muse-spark-1.3-max` — rank 7

**Verified correct:** NVIDIA ACE reference stack (Riva, Audio2Face-3D, UE 5.5, Pixel Streaming) (E14); AWS g5.2xlarge / g6e at "$1.20–$2.50/hr" (actual $1.21 and $1.86, E21); Synthesia does have a real-time Interactive Avatar API (E11); ElevenLabs Turbo v2.5 and Cartesia Sonic latency figures (E25); 52 ARKit blendshapes as the rig standard; Live Link Face; consent requirements at ElevenLabs and HeyGen.

**Hard errors:**
1. Groups LivePortrait with "person-specific" avatars that you "train on 2–5 min video of ONE person". LivePortrait is one-shot and generic (E35).
2. "Train FlashAvatar / LivePortrait on RunPod A100 (4–6 hours)". LivePortrait is not trained per identity; FlashAvatar trains in minutes on a consumer GPU (E28, E35).
3. "OpenAI gpt-4o-mini-tts … returns visemes for lip-sync". OpenAI's TTS API returns neither visemes nor timestamps (E13). Azure, named in the same sentence, does (E12).
4. "NVIDIA Audio2Face 3.0 … outputs 100+ blendshape weights". Audio2Face-3D outputs 46 template blendshapes or 52 ARKit blendshapes via solving (E15). No "Audio2Face 3.0" release could be found; the product is "Audio2Face-3D" (E14, E47).
5. "Unity HDRP + Ready Player Me + Convai … runs in browser with WebGL". HDRP is not supported on WebGL; only URP and the built-in pipeline are (E19).
6. Names "Audio2Photoreal" as a talking-head driver. Audio2Photoreal is Meta's audio-to-gesture model rendered with Codec Avatars, not a 2D talking-head driver (E2).

**Dated:** Ready Player Me recommended twice (shut down 2026-01-31, E9); "Hedra" listed among streaming avatar providers (realtime product sunset 2026-04-15, E10); "MetaHuman Creator (free, web-based)" (E18).

**Partially inaccurate:** hosted avatar pricing "$0.05–$0.30/min". Published rates are Tavus $0.26–0.35, D-ID about $0.35, HeyGen $0.18–0.78 per minute (E26); the low end is not supported.

## 8. Anonymous Arena Agent-mode model — rank 8

Note on identity: the saved Arena page shows no model label for this answer. It was provisionally labelled `space-bunny-alpha` earlier in this session, but the user's actual Space Bunny Alpha log (answer 08, from OpenRouter) is a different response, so this one is an anonymous Arena agent (confirmed by the user).

**Verified correct:** Wav2Lip, SadTalker, MuseTalk, LivePortrait, Hedra, D-ID, Synthesia as 2D talking-head options; ElevenLabs, Cartesia, PlayHT, Azure as streaming TTS; Coqui XTTS, F5-TTS, StyleTTS2, CosyVoice, Sesame CSM as open models; Instant-NGP and Nerfstudio as NeRF tooling; C2PA for provenance; 3DGS asset sizes needing streaming.

**Hard errors:**
1. "3D Gaussian Splatting avatars … Examples: Meta's Audio2Photoreal". Audio2Photoreal renders with Meta's Codec Avatars (a cVAE producing geometry and texture, rasterised), not Gaussian splats (E2).
2. "Sony's OmniAvatar" as a 3DGS example. OmniAvatar is from Zhejiang University and Alibaba, and it is an audio-driven full-body *video generation* model (E1).
3. "Nerfies" as a 3DGS example. Nerfies is a deformable NeRF method from ICCV 2021, predating Gaussian splatting (E3).
4. "Audio-to-blendshape models: VisemeNet, FaceX-Zoo, MeshTalk". FaceX-Zoo is a face-recognition toolbox from JD AI (E4).
5. "End-to-end audio-to-face: EMO (Alibaba), Hedra Character-1, OmniAvatar, Loopy — these drive a 3D head directly from audio". EMO and Loopy are 2D portrait video diffusion models that explicitly bypass 3D intermediates (E5); OmniAvatar likewise (E1).
6. "Local real-time [TTS]: Piper, Kokoro, RVC, Fish Speech". RVC is speech-to-speech voice conversion, not text-to-speech (E6).
7. "3DGS viewer (e.g. gsplat.js, luma.gl …)". luma.gl is a general GPU toolkit underpinning deck.gl, not a Gaussian-splat viewer (E7); gsplat.js is correct (E8).

**Dated:** Ready Player Me as a rigged-avatar example (E9); "Hedra Character-1" (a June 2024 model; Hedra's realtime line is discontinued, E10).

**Unverified:** "Neural Head Avatar like the Sony/ETH Zurich work" — no such joint work was found.

**Coverage gap (not an error):** the answer never mentions Unreal Engine, MetaHuman, Unity or Audio2Face, which every other answer treats as the primary route for a real-time *rendered* avatar.

---

## Evidence catalogue

- **E1** OmniAvatar — Gan, Yang, Zhu (Zhejiang Univ.), Xue, Hoi (Alibaba): "Efficient Audio-Driven Avatar Video Generation". https://arxiv.org/abs/2506.18866
- **E2** Audio2Photoreal — Meta, "From Audio to Photoreal Embodiment"; rendering via Codec Avatars cVAE producing geometry and view-dependent texture for rasterisation. https://arxiv.org/abs/2401.01885 ; https://people.eecs.berkeley.edu/~evonne_ng/projects/audio2photoreal/
- **E3** Nerfies: Deformable Neural Radiance Fields, ICCV 2021. https://openaccess.thecvf.com/content/ICCV2021/html/Park_Nerfies_Deformable_Neural_Radiance_Fields_ICCV_2021_paper.html
- **E4** FaceX-Zoo: A PyTorch Toolbox for Face Recognition (JD AI). https://arxiv.org/abs/2101.04407
- **E5** EMO (Alibaba) "direct audio-to-video synthesis approach, bypassing the need for intermediate 3D models or facial landmarks". https://arxiv.org/abs/2402.17485 ; Loopy (ByteDance) "end-to-end audio-only conditioned video diffusion model". https://arxiv.org/abs/2409.02634
- **E6** Retrieval-based Voice Conversion: speech-to-speech, "differs from text-to-speech systems". https://en.wikipedia.org/wiki/Retrieval-based_Voice_Conversion
- **E7** luma.gl: "GPU toolkit for the Web … supports GPU needs of … kepler.gl, deck.gl". https://luma.gl/docs
- **E8** gsplat.js: "JavaScript Gaussian Splatting library". https://github.com/huggingface/gsplat.js
- **E9** Ready Player Me acquired by Netflix 2025-12-19; hosted creator and public API endpoints offline 2026-01-31. https://www.pocketgamer.biz/netflix-acquires-avatar-creation-platform-ready-player-me ; https://avatarsdk.com/blog/2026/07/07/ready-player-me-migration-guide/ ; https://genies.com/blog/ready-player-me-discontinued-alternatives
- **E10** Hedra Realtime Avatar sunset 2026-04-15: LiveKit plugin page states "Hedra sunset their Realtime Avatar product on April 15, 2026. This plugin no longer functions." https://docs.livekit.io/agents/integrations/avatar/hedra (page blocked from this sandbox; text taken from search snippet and corroborated by the plugin's absence in E43). Hedra Character-1 launched 2024-06-18. https://elevenlabs.io/blog/hedra-teams-up-with-elevenlabs-to-give-voice-to-video
- **E11** Synthesia Interactive Avatar API (Enterprise, Express-3). https://www.synthesia.io/post/interactive-avatar-api-real-time-avatars ; LiveKit ships `livekit-plugins-synthesia` (E43).
- **E12** Azure Speech viseme docs: blend shapes are "a two-dimensional matrix … each frame (at 60 FPS) contains an array of 55 facial positions". https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-speech-synthesis-viseme (blocked from sandbox; wording from Microsoft mirror https://docs.azure.cn/en-us/ai-services/speech-service/how-to-speech-synthesis-viseme)
- **E13** OpenAI TTS has no timestamp or viseme output: OpenAI community thread "there isn't currently an option for that". https://community.openai.com/t/openai-tts-transcription-time-stamps/1257285 ; TTS guide mentions neither. https://developers.openai.com/api/docs/guides/text-to-speech
- **E14** NVIDIA open-sourced Audio2Face (2025-09): Audio2Face model, Audio2Emotion, SDK, Maya plugin, Unreal Engine 5 plugin, training framework. https://www.etcentric.org/?p=196138 ; https://www.opensourceforu.com/2025/09/nvidia-moves-audio2face-technology-to-open-source/ ; SDK repo: MIT, TensorRT >=10.13, "Faster than 60 FPS frame generation". https://github.com/NVIDIA/Audio2Face-3D-SDK
- **E15** Audio2Face-3D outputs ARKit blendshapes; template generates 46, 52 via blendshape solving. https://docs.nvidia.com/ace/audio2face-3d-microservice/2.0/text/getting-started/overview.html ; https://forums.developer.nvidia.com/t/46-blendshape-standards-of-audio2face/210504
- **E16** MetaHuman licence change (June 2025): usable in Unity/Godot, no royalty; Creator, Mesh to MetaHuman and Animator integrated into UE 5.6. https://www.cgchannel.com/2025/06/you-can-now-sell-metahumans-or-use-them-in-unity-or-godot/ ; https://metahuman.com/news/metahuman-leaves-early-access-with-a-feature-packed-new-release
- **E17** MetaHuman Animator audio-driven animation: UE 5.5 (2024-11-12) experimental, offline; UE 5.6 adds real time. https://www.unrealengine.com/en-US/blog/unreal-engine-5-5-is-now-available ; https://dev.epicgames.com/documentation/en-us/metahuman/audio-driven-animation ; https://www.unrealengine.com/news/unreal-engine-5-6-is-now-available
- **E18** MetaHuman Creator web app phased shutdown, access ends 2026-11-05. https://gamedev.net/news/1981-metahuman-creator-web-application-is-being-discontinued/
- **E19** Unity HDRP is not supported on WebGL; URP is. https://docs.unity3d.com/Packages/hdrp/manual/index.html ; https://docs.viverse.com/standalone-app-publishing/unitywebgl-examples
- **E20** GeForce RTX 4080 has 16 GB GDDR6X. https://www.gigabyte.com/Graphics-Card/GV-N4080WF3-16GD/sp
- **E21** AWS on-demand us-east-1: g5.2xlarge $1.212/hr (A10G); g6e.xlarge $1.861/hr (L40S). https://calculator.holori.com/aws/ec2/g5.2xlarge/us-east-1 ; https://calculator.holori.com/aws/ec2/g6e.xlarge/us-east-1
- **E22** Nanite skeletal-mesh support introduced as experimental in UE 5.5. https://wnhub.io/news/engines/item-45659 ; https://uhiyama-lab.com/en/notes/ue/nanite-high-poly-mesh-optimization/
- **E23** Lumen software ray tracing supported on Apple Silicon M1+; hardware ray tracing and MegaLights not supported on macOS. https://www.unrealengine.com/tech-blog/bringing-unreal-engine-on-macos-up-to-feature-parity-with-windowsprogress-report
- **E24** Ditto (Ant Group): "Controllable Realtime Talking Head Synthesis", PyTorch and TensorRT, streaming, low first-frame delay. https://arxiv.org/abs/2411.19509
- **E25** ElevenLabs Flash v2.5 about 75 ms; Turbo v2.5 about 300 ms; Cartesia Sonic sub-90 ms time-to-first-audio, 40 ms model latency. https://the-decoder.com/elevenlabs-launches-flash-its-fastest-text-to-speech-ai-yet/ ; https://humannessindex.vapi.ai/models/elevenlabs-turbo-v2-5 ; https://cartesia.ai/vs/cartesia-vs-elevenlabs
- **E26** Hosted avatar pricing: Tavus CVI overage $0.35/$0.31/$0.26 per minute by tier. https://www.tavus.io/pricing ; HeyGen interactive roughly $0.18–0.78/min. https://anam.ai/blog/heygen-pricing ; D-ID Agent API about $0.35/min. https://anam.ai/blog/d-id-api-review-2025-architecture-capabilities
- **E27** VASA-1: Microsoft "no plans to release an online demo, API, product". https://www.ibtimes.com/microsoft-teases-lifelike-avatar-ai-tech-gives-no-release-date-3730144
- **E28** FlashAvatar: monocular video, minutes to train, 300 FPS on consumer GPU. https://arxiv.org/abs/2312.02214 ; GaussianAvatars: multi-view, FLAME-rigged. https://arxiv.org/abs/2312.02069 ; SplattingAvatar: 300 FPS on GPU, 30 FPS on mobile, trainable from monocular video. https://arxiv.org/abs/2403.05087
- **E29** GaussianTalker: audio-driven 3DGS, up to 120 FPS. https://arxiv.org/abs/2404.16012 ; TalkingGaussian. https://arxiv.org/abs/2404.15264
- **E30** ExAvatar (Meta Codec Avatars Lab): whole-body 3DGS from a short monocular video. https://arxiv.org/abs/2407.21686
- **E31** UniTalker (ECCV 2024). https://arxiv.org/abs/2408.00762 ; EMOTE (SIGGRAPH Asia 2023). https://arxiv.org/abs/2306.08990
- **E32** VHAP FLAME tracker, "exported tracking results can be directly used to create your own GaussianAvatars". https://github.com/ShenhanQian/VHAP
- **E33** LAM: "Large Avatar Model for One-shot Animatable Gaussian Head"; WebGL render released 2025-05-20; OpenAvatarChat SDK; 562.9 FPS. https://github.com/aigc3d/LAM ; https://github.com/HumanAIGC-Engineering/OpenAvatarChat
- **E34** MuseTalk README: "real-time inference with 30fps+ on an NVIDIA Tesla V100"; "code … released under the MIT License"; "trained model are available for any purpose, even commercially"; modifies a 256×256 face region of the input video. https://github.com/TMElyralab/MuseTalk
- **E35** LivePortrait speed.md: per-module inference on RTX 4090 with torch.compile sums to about 14.8 ms per frame; one-shot (no per-identity training). https://github.com/KwaiVGI/LivePortrait/blob/main/assets/docs/speed.md ; InsightFace README: models "available for non-commercial research purposes only". https://github.com/deepinsight/insightface#license
- **E36** JoyVASA (JD Health): "extracts static and motion features using LivePortrait then maps audio features to motion". https://arxiv.org/abs/2411.09209
- **E37** INSTA: monocular video, under 10 minutes training, interactive frame rates. https://arxiv.org/abs/2211.12499 ; GeneFace++ real-time NeRF talking face from a few-minute video. https://arxiv.org/abs/2305.00787 ; ER-NeRF real-time rendering. https://arxiv.org/abs/2307.09323 ; SyncTalk 50 FPS. https://arxiv.org/abs/2311.17590
- **E38** TTS licences (from each repository's LICENSE/README): Kokoro Apache-2.0, 82M params https://github.com/hexgrad/kokoro ; Piper MIT https://github.com/rhasspy/piper ; CosyVoice Apache-2.0 https://github.com/FunAudioLLM/CosyVoice ; Orpheus Apache-2.0, Llama-3B backbone https://github.com/canopyai/Orpheus-TTS ; Chatterbox MIT https://github.com/resemble-ai/chatterbox ; Zonos Apache-2.0 https://github.com/Zyphra/Zonos ; Sesame CSM Apache-2.0, 1B released 2025-03-13 https://github.com/SesameAILabs/csm ; F5-TTS "code is released under MIT License. The pre-trained models are licensed under the CC-BY-NC license" https://github.com/SWivid/F5-TTS#license ; Fish Speech "FISH AUDIO RESEARCH LICENSE … Any Commercial use of the Materials requires a separate license" https://github.com/fishaudio/fish-speech/blob/main/LICENSE ; XTTS "licensed under Coqui Public Model License" https://github.com/coqui-ai/TTS/blob/dev/docs/source/models/xtts.md
- **E39** Rhubarb Lip Sync: "command-line tool … passing it an audio file as argument"; creates 2D mouth animation from voice recordings. https://github.com/DanielSWolf/rhubarb-lip-sync
- **E40** ITU-R BT.1359-1: detectability +45 ms to −125 ms, acceptability +90 ms to −190 ms (positive = audio leads). https://www.tvtechnology.com/opinions/av-synchronization-how-bad-is-bad ; https://www.forasoft.com/learn/audio-for-video/articles-audio/lip-sync-itu-r-bt-1359-tolerance-windows
- **E41** Unreal Engine non-game seat licence: $1,850 per seat per year for companies over $1M revenue (from UE 5.4, April 2024). https://www.unrealengine.com/en-US/blog/we-are-updating-unreal-engine-twinmotion-and-realitycapture-pricing-in-late-april
- **E42** Tavus Phoenix-3 launch (2025-03-06). https://www.businesswire.com/news/home/20250306296766/en
- **E43** LiveKit agents plugin directory (fetched 2026-10-04) lists avatar plugins: anam, avatario, avatartalk, bey, bithuman, cambai, did, liveavatar, simli, synthesia, tavus; no hedra directory. https://github.com/livekit/agents/tree/main/livekit-plugins ; Pipecat video services: Simli, Tavus, HeyGen. https://docs.pipecat.ai/server/services/video/tavus
- **E44** Amazon Polly speech marks include viseme type for lip sync. https://docs.aws.amazon.com/polly/latest/dg/speechmarks.html
- **E45** EU AI Act Article 50 transparency obligations (chatbot disclosure, deepfake labelling), applicable from 2026-08-02. https://artificialintelligenceact.eu/transparency-rules-article-50/
- **E46** Unity support for Audio2Face: NVIDIA ACE documentation covers an Unreal plugin only. https://docs.nvidia.com/ace/ace-unreal-plugin/2.5/index.html ; one secondary report claims Unity plugins were included in the 2025 release. https://fptshop.com.vn/tin-tuc/tin-moi/nvidia-mo-cua-cong-nghe-ai-hoat-hinh-giong-noi-cho-tat-ca-nguoi-dung-trai-nghiem-188700 (treated as unverified)
- **E47** No "Audio2Face 3.0" release found; Omniverse Audio2Face used 2023.x versioning and the open-source line is "Audio2Face-3D". https://developer.nvidia.com/blog/nvidia-omniverse-audio2face-app-now-available-in-open-beta ; https://github.com/NVIDIA/Audio2Face-3D-SDK
- **E48** NVIDIA forum: Audio2Face-3D SDK v3.0 diffusion model "produces frames in bursts of ~28 frames every ~470ms, due to its 1-second sliding window with 0.5-second stride"; regression model outputs 1 frame per chunk. https://forums.developer.nvidia.com/t/audio2face-digital-human-sdk-v3-0-diffusion-model-frame-gap-during-streaming-inference-posting-here-as-digital-human-board-is-closed/361109 ; paper https://arxiv.org/abs/2508.16401
- **E49** ACE Unreal Plugin 2.5: "tested and supported for UE 5.5 and 5.6", dropped 5.4. https://docs.nvidia.com/ace/ace-unreal-plugin/2.5/ace-unreal-plugin-changelog.html
- **E50** Omniverse Launcher deprecated 2025-10-01. https://developer.nvidia.com/omniverse/legacy-tools
- **E51** MetaHuman 5.8 / UE 5.8 released 2026-06-17; RigLogic and DNA libraries open-sourced as OpenRigLogic under MIT. https://www.metahuman.com/news/metahuman-5-8-is-now-available ; https://github.com/EpicGames/openriglogic ; https://www.cgchannel.com/tag/tmv/
- **E52** GaussianHeadTalk, WACV 2026. https://arxiv.org/abs/2512.10939
- **E53** MOVA (OpenMOSS) released 2026-01-29, Apache-2.0, 8 s at 360p, "at least 24GB GPU with offloading". https://comfyui-wiki.com/en/news/2026-01-29-openmoss-mova-video-audio-generation ; LatentSync 1.6 (ByteDance) Apache-2.0, 512×512, about 18 GB. https://sync.so/blog/what-is-latentsync ; https://news.creeta.com/en/open-source-lip-sync-models-2026/
- **E54** Wav2Lip: "can only be used for personal/research/non-commercial purposes"; 96×96 face crop. https://github.com/Rudrabha/Wav2Lip
- **E55** Audio2Face-3D "provides a blendshape solving process" to retarget output onto a target character; no per-character training required. https://arxiv.org/abs/2508.16401 ; https://docs.nvidia.com/ace/audio2face-3d-microservice/2.0/text/getting-started/overview.html
- **E56** Cartesia TTS `add_phoneme_timestamps` returns phoneme-level timestamp events over SSE/WebSocket. https://docs.cartesia.ai/api-reference/tts/sse ; https://docs.cartesia.ai/examples/tts-sse-with-phoneme-timestamps
- **E57** Visionary: WebGPU renderer with per-frame ONNX inference for Gaussian splats and neural avatars. https://arxiv.org/abs/2512.08478 ; no indexed source found for "BONSAI 340 fps" (searched 2026-10-04).
- **E58** LiveAvatar (Intel Labs): live conversion of monocular video to 3D Gaussian head avatars. https://github.com/IntelLabs/LiveAvatar
- **E59** MetaHuman `enable_material_parameter_caching`: "whether or not to cache material parameter to speed up setting scalar or vector value on materials". https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MetaHumanTemplateMesh

## Limits of this check

- Hugging Face, Microsoft Learn, hedra.com, synthesia.io, docs.livekit.io and developers.openai.com were unreachable from the sandbox; equivalent GitHub repositories, vendor mirrors and search snippets were used and are cited as such.
- Subjective engineering judgements (for example "hair groom is 40% of frame time", "L4 only with card hair") were not scored.
- The exact date each Arena chat was run is not recorded in the saved pages; "dated" is judged against 2026-10-04.
