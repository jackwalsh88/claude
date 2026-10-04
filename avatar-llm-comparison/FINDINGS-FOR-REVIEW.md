# Review brief: accuracy of eight LLM answers on real-time photorealistic avatars

**Purpose.** Independent review of an accuracy ranking. Eight language models answered the same prompt; each answer was checked claim by claim against primary sources. This brief states the verdicts, the evidence behind each, and the method, in about ten minutes of reading. The full per-answer transcripts (files 01–08) and the complete catalogue sit beside this file; `RANKING.md` is the long form.

**Intended reader.** A senior researcher in face analysis and 3D face reconstruction. Method names (3DGS, FLAME, NeRF, codec avatars, visemes, blendshape solving) are used without definition. Evidence points to papers and repositories rather than press where both exist. Section 4 lists the places where expert judgement would change the result most.

**Prompt given to every model.** "would you go about putting together a real time rendered (frame rate) photorealistic avatar with generated voice. What would be your options and their requirements"

**Date basis.** 2026-10-04. "Dated" means true once, no longer true on that date.

**Reviewer note on independence.** The checker was Claude Fable 5.1. One answer (rank 1) is from `claude-fable-5.1-max`, the same model family. All findings for it rest on the same external sources as the others, and its two flaws are listed. The tally columns alone reproduce the ranking.

---

## 1. Verdict

| Rank | Model | Hard errors | Dated | Unverified | Verified specifics |
|---|---|---|---|---|---|
| 1 | `claude-fable-5.1-max` (file 05) | 0 (one numeric slip) | 1 | 2 | ~40 |
| 2 | `gpt-5.6-terra-low` (02) | 0 | 0 | 0 | ~10 |
| 3 | `space-bunny-alpha` (08) | 3 | 0 | 4 | ~25 |
| 4 | `step-5-preview` (03) | 2 | 2 | 1 | ~15 |
| 5 | `grok-4.20-multi-agent-beta-0309` (06) | 2 | 1 | 0 | ~10 |
| 6 | `qwen3.5-397b-a17b` (07) | 4 | 2 | 1 | ~8 |
| 7 | `muse-spark-1.3-max` (04) | 6 | 3 | 1 | ~15 |
| 8 | anonymous Arena Agent-mode model (01) | 7 | 2 | 1 | ~8 |

**Two judgement calls a reviewer may disagree with.**
1. Ranks 1 and 2 both have zero hard errors. Rank 2 earns that by committing to almost nothing checkable (vendors named only as "HeyGen-style", no versions, prices, licences or numbers). Rank 1 makes about forty checkable claims. The ranking rewards verified specifics; a pure "fewest flaws" count would swap them.
2. Rank 3 has one more hard error than ranks 4 and 5 but no stale claims and the second-largest verified body, because it ran live web searches first. A pure hard-error count would put it at rank 5.

---

## 2. Findings per answer

Evidence references (E-numbers) resolve in the appendix.

### Rank 1 — `claude-fable-5.1-max`
- **Holds up:** Audio2Face-3D open source with UE5 plugin and ARKit blendshape plus emotion output (E14, E15); MetaHuman Animator audio-driven in UE 5.5, real time in 5.6 (E17); Azure TTS emits 55 blendshapes at 60 fps (E12); MetaHuman licence relaxed June 2025 (E16); MuseTalk MIT and real time (E34); LivePortrait one-shot, depends on non-commercial InsightFace (E35); VASA-1 unreleased (E27); the full set of 3DGS avatar papers named (E28–E33); every TTS licence named, permissive and non-commercial alike (E38); hosted pricing "tens of cents per minute" (E26).
- **Dated:** lists "Hedra Live"; Hedra retired its realtime avatar on 2026-04-15 (E10).
- **Numeric slip:** A/V sync detectability quoted as −45/+100 ms; ITU-R BT.1359 is +45 ms lead to −125 ms lag (E40).
- **Unverified:** ONNX as an Audio2Face-3D runtime; "configurable lookahead".

### Rank 2 — `gpt-5.6-terra-low`
- **Holds up:** everything checkable (MetaHuman Animator, Live Link Face, Audio2Face, Pixel Streaming, L4/A10/A16 GPUs, 0.8–1.5 s first-audio target).
- **Weakness:** no versions, prices, licences, performance figures or named vendors. Nothing to falsify, little to act on.

### Rank 3 — `space-bunny-alpha`
- **Holds up:** Audio2Face-3D diffusion model emits ~28 frames per ~470 ms burst, regression model streams per chunk (E48); ACE Unreal plugin supports UE 5.5–5.6 only (E49); Omniverse Launcher deprecated 2025-10-01 (E50); MetaHuman 5.8 with OpenRigLogic under MIT (E51); GaussianHeadTalk WACV 2026 (E52); MOVA and LatentSync licences and VRAM (E53); Wav2Lip non-commercial, 96 px (E54); Cartesia phoneme timestamps (E56); MuseTalk, Kokoro, Chatterbox, XTTS facts (E34, E38).
- **Hard errors:** (a) "Audio2Face-3D … needs per-character training"; it retargets by blendshape solving, training is optional (E55). (b) "MetaHuman left Early Access and its licensing changed during 2026"; that was June 2025 (E16). (c) "F5-TTS (MIT)"; the code is MIT, the weights are CC-BY-NC (E38).
- **Unverified:** "BONSAI 340 fps" browser avatars (no indexed source, E57); the 20–30 FPS material-caching figure (setting exists, number unsourced, E59); MOVA "~48 GB" (authors say at least 24 GB, E53); LiveAvatar ">20 fps" (repository exists, figure unchecked, E58).

### Rank 4 — `step-5-preview`
- **Holds up:** MetaHuman and Audio2Face basics, Pixel Streaming, a latency table consistent with ITU thresholds (E40), RVC correctly classed as a voice changer (E6).
- **Hard errors:** (a) Gaussian splatting "needs 24–64 cameras minimum" and is "not yet practical for real-time dialogue"; monocular FLAME-rigged avatars render at 300 fps and audio-driven 3DGS heads at 120 fps (E28, E29). (b) "UE 5.3+ Nanite (high-poly face)"; Nanite skeletal meshes arrived, experimental, in 5.5 (E22).
- **Dated:** recommends GPT-4o-mini, Claude 3.5 Sonnet, Llama 3 8B and UE 5.4 in 2026.
- **Weak:** "Audio2Face plugin for Unity" (only Unreal and Maya plugins are documented, E46); Apple Silicon "struggles with Lumen" overstated (software ray tracing supported, E23); "XTTS … free" omits its non-commercial licence (E38).

### Rank 5 — `grok-4.20-multi-agent-beta-0309`
- **Holds up:** UE5 + MetaHuman + Audio2Face + streaming TTS as the main stack; Audio2Face free (E14); 16 GB+ VRAM guidance (E20); real vendor names.
- **Hard errors:** (a) "5–30 minutes of training video" for a neural talking head led by LivePortrait, which is one-shot (E35); person-specific NeRFs need a few minutes, not thirty (E37). (b) 3DGS "A100/H100, hours to a day" to train and "RTX 4080+" to run; FlashAvatar trains in minutes and renders at 300 fps on a consumer GPU (E28).
- **Dated:** "MetaHuman Creator (cloud tool)"; in-engine since 5.6, web app closing 2026-11-05 (E16, E18).

### Rank 6 — `qwen3.5-397b-a17b`
- **Output defect:** about 900 words of leaked planning text precede the answer, including "matches the detailed response provided previously".
- **Hard errors:** (a) "RTX 4080 or 4090 (24GB VRAM minimum)"; the 4080 has 16 GB (E20). (b) "1Gbps+ Fiber" required for streaming TTS audio; speech streams are tens of kbps. (c) Rhubarb Lip Sync proposed for real-time use; it is an offline CLI over audio files (E39). (d) "Do not try to generate video frames, it is too slow"; MuseTalk, Ditto, GeneFace++ and SyncTalk run in real time (E24, E34, E37).
- **Dated:** Ready Player Me (shut down 2026-01-31, E9); "Llama-3-70b via Groq".
- **Incomplete:** "UE5 is free (5% royalty)" omits the $1,850 non-game seat licence above $1M revenue (E41).

### Rank 7 — `muse-spark-1.3-max`
- **Holds up:** NVIDIA ACE reference stack (E14); AWS g5/g6e hourly prices (E21); Synthesia has a real-time API (E11); ElevenLabs and Cartesia latencies (E25).
- **Hard errors:** (a) LivePortrait grouped with person-specific avatars trained on 2–5 min of video; it is one-shot (E35). (b) "Train FlashAvatar / LivePortrait on an A100 for 4–6 hours"; LivePortrait is not trained per identity, FlashAvatar trains in minutes (E28, E35). (c) "OpenAI gpt-4o-mini-tts returns visemes"; it returns neither visemes nor timestamps (E13). (d) "Audio2Face 3.0 outputs 100+ blendshapes"; it outputs 46 or 52 ARKit blendshapes (E15), and no "3.0" product release exists (E47). (e) "Unity HDRP … runs in browser with WebGL"; HDRP is not supported on WebGL (E19). (f) Audio2Photoreal named as a talking-head driver; it is Meta's gesture model rendered with Codec Avatars (E2).
- **Dated:** Ready Player Me twice (E9); Hedra as a streaming provider (E10); "MetaHuman Creator (web-based)" (E18).
- **Low:** hosted pricing "$0.05–0.30/min" against published $0.18–0.78 (E26).

### Rank 8 — anonymous Arena Agent-mode model
- **Holds up:** the 2D talking-head tool list, streaming TTS vendors, open TTS models, Instant-NGP and Nerfstudio, C2PA.
- **Hard errors:** (a) Audio2Photoreal called a Gaussian-splat avatar; it uses Codec Avatars (E2). (b) "Sony's OmniAvatar" as 3DGS; OmniAvatar is Zhejiang University and Alibaba, and it generates video (E1). (c) Nerfies as 3DGS; it is a 2021 deformable NeRF (E3). (d) FaceX-Zoo as an audio-to-blendshape model; it is a face-recognition toolbox (E4). (e) EMO, Loopy and OmniAvatar said to "drive a 3D head"; all three are 2D video diffusion (E1, E5). (f) RVC listed as TTS; it is voice conversion (E6). (g) luma.gl as a splat viewer; it is a general GPU toolkit (E7).
- **Dated:** Ready Player Me (E9); "Hedra Character-1" (E10).
- **Coverage gap:** never mentions Unreal, MetaHuman, Unity or Audio2Face.

---

## 3. Method and limits

- Each answer was converted from the saved HTML to Markdown verbatim (files 01–08). Model labels come from the Arena "Message from …" markers and the OpenRouter model selector; the Agent-mode answer carries no label.
- Every concrete claim (product, licence, version, date, price, performance figure, attribution) was checked against a primary source where reachable: arXiv, GitHub repositories and LICENSE files, vendor documentation, Epic and NVIDIA release notes.
- Hugging Face, Microsoft Learn, hedra.com, synthesia.io, docs.livekit.io and developers.openai.com were blocked from the checking environment. Those facts were taken from the project's GitHub repository, a vendor mirror or a search snippet, and are marked in the appendix.
- Subjective engineering judgements (for example "hair groom is 40% of frame time") were not scored.
- The exact date each chat was run is not recorded; staleness is judged against 2026-10-04.

---

## 4. Where expert review matters most

1. **Attribution errors in the face-avatar literature** (ranks 7 and 8): Audio2Photoreal described as a Gaussian-splat avatar and as a 2D talking-head driver (E2); OmniAvatar attributed to Sony and to 3DGS (E1); Nerfies classed as 3DGS (E3); FaceX-Zoo listed as an audio-to-blendshape model (E4). These are the clearest errors in the set and the easiest for a face-vision reader to confirm or refute from memory.
2. **One-shot versus person-specific taxonomy.** Three answers (ranks 5, 7 and in part 8) treat LivePortrait as a per-identity trained model (E35). The checker scored this as a hard error each time. If the reviewer considers the distinction immaterial for a practitioner, ranks 5 and 7 each lose one error.
3. **Practicality of Gaussian-splat avatars for live dialogue** (ranks 4 and 5). The checker relied on FlashAvatar, SplattingAvatar and GaussianTalker figures (E28, E29) to call "needs 24–64 cameras" and "A100/H100 for hours to a day" errors. Whether those research-paper numbers reflect deployable quality is a judgement the reviewer is better placed to make.
4. **Unverified research claims in rank 3**: "BONSAI 340 fps" (E57), LiveAvatar ">20 fps with no per-subject training" (E58), GaussianHeadTalk described as real time (E52). None could be confirmed from indexed sources; none was scored as an error. If any is false, rank 3 drops.
5. **The A/V sync threshold.** Rank 1's "−45/+100 ms" was scored a minor slip against ITU-R BT.1359's +45/−125 ms (E40). A reviewer who treats this as a hard error moves rank 1 to one error, which would tie it with none and still leave it first on verified specifics, but the "fewest flaws" reading in Section 1 would then favour rank 2 more strongly.
6. **The two ranking judgement calls** in Section 1 (verified specifics versus flaw count). The tallies are given so the ordering can be recomputed under either rule.
7. **Not scored:** consent, biometric-data and disclosure statements in the answers were checked for existence (EU AI Act Article 50, E45 in `RANKING.md`) but not for legal adequacy.

---

## Appendix: evidence catalogue

- **E1** OmniAvatar, Zhejiang Univ. and Alibaba, audio-driven avatar *video generation*. https://arxiv.org/abs/2506.18866
- **E2** Audio2Photoreal (Meta) renders via Codec Avatars, a cVAE producing geometry and texture for rasterisation. https://arxiv.org/abs/2401.01885
- **E3** Nerfies: Deformable Neural Radiance Fields, ICCV 2021. https://openaccess.thecvf.com/content/ICCV2021/html/Park_Nerfies_Deformable_Neural_Radiance_Fields_ICCV_2021_paper.html
- **E4** FaceX-Zoo: a PyTorch toolbox for face recognition (JD AI). https://arxiv.org/abs/2101.04407
- **E5** EMO "bypassing the need for intermediate 3D models". https://arxiv.org/abs/2402.17485 ; Loopy "audio-only conditioned video diffusion model". https://arxiv.org/abs/2409.02634
- **E6** RVC is speech-to-speech voice conversion. https://en.wikipedia.org/wiki/Retrieval-based_Voice_Conversion
- **E7** luma.gl: GPU toolkit for deck.gl and kepler.gl. https://luma.gl/docs
- **E9** Ready Player Me: Netflix acquisition 2025-12-19, services offline 2026-01-31. https://www.pocketgamer.biz/netflix-acquires-avatar-creation-platform-ready-player-me ; https://avatarsdk.com/blog/2026/07/07/ready-player-me-migration-guide/
- **E10** Hedra Realtime Avatar sunset 2026-04-15 (LiveKit plugin notice; page blocked, text from search snippet, corroborated by E43). https://docs.livekit.io/agents/integrations/avatar/hedra ; Character-1 launched 2024-06-18. https://elevenlabs.io/blog/hedra-teams-up-with-elevenlabs-to-give-voice-to-video
- **E11** Synthesia Interactive Avatar API (Enterprise). https://www.synthesia.io/post/interactive-avatar-api-real-time-avatars
- **E12** Azure viseme blend shapes: 55 positions per frame at 60 FPS (Microsoft mirror). https://docs.azure.cn/en-us/ai-services/speech-service/how-to-speech-synthesis-viseme
- **E13** OpenAI TTS offers no timestamps or visemes. https://community.openai.com/t/openai-tts-transcription-time-stamps/1257285
- **E14** NVIDIA open-sourced Audio2Face (Sept 2025) with UE5 plugin, SDK, training framework. https://www.etcentric.org/?p=196138 ; SDK (MIT, TensorRT, >60 FPS). https://github.com/NVIDIA/Audio2Face-3D-SDK
- **E15** Audio2Face-3D outputs ARKit blendshapes, 46 from template, 52 via solving. https://docs.nvidia.com/ace/audio2face-3d-microservice/2.0/text/getting-started/overview.html ; https://forums.developer.nvidia.com/t/46-blendshape-standards-of-audio2face/210504
- **E16** MetaHuman 5.6 (June 2025): left Early Access, licence allows Unity/Godot, Creator in-engine. https://www.cgchannel.com/2025/06/you-can-now-sell-metahumans-or-use-them-in-unity-or-godot/ ; https://metahuman.com/news/metahuman-leaves-early-access-with-a-feature-packed-new-release
- **E17** MetaHuman Animator audio-driven: UE 5.5 experimental offline; 5.6 real time. https://www.unrealengine.com/en-US/blog/unreal-engine-5-5-is-now-available ; https://dev.epicgames.com/documentation/en-us/metahuman/audio-driven-animation
- **E18** MetaHuman Creator web app closes 2026-11-05. https://gamedev.net/news/1981-metahuman-creator-web-application-is-being-discontinued/
- **E19** Unity HDRP not supported on WebGL. https://docs.unity3d.com/Packages/hdrp/manual/index.html
- **E20** RTX 4080: 16 GB GDDR6X. https://www.gigabyte.com/Graphics-Card/GV-N4080WF3-16GD/sp
- **E21** AWS g5.2xlarge $1.212/hr; g6e.xlarge $1.861/hr. https://calculator.holori.com/aws/ec2/g5.2xlarge/us-east-1 ; https://calculator.holori.com/aws/ec2/g6e.xlarge/us-east-1
- **E22** Nanite skeletal meshes experimental in UE 5.5. https://wnhub.io/news/engines/item-45659
- **E23** Lumen software ray tracing supported on Apple Silicon; hardware RT not. https://www.unrealengine.com/tech-blog/bringing-unreal-engine-on-macos-up-to-feature-parity-with-windowsprogress-report
- **E24** Ditto (Ant Group), real-time, TensorRT, streaming. https://arxiv.org/abs/2411.19509
- **E25** ElevenLabs Flash v2.5 ~75 ms, Turbo v2.5 ~300 ms; Cartesia Sonic sub-90 ms. https://the-decoder.com/elevenlabs-launches-flash-its-fastest-text-to-speech-ai-yet/ ; https://cartesia.ai/vs/cartesia-vs-elevenlabs
- **E26** Tavus CVI $0.26–0.35/min; HeyGen interactive $0.18–0.78/min; D-ID ~$0.35/min. https://www.tavus.io/pricing ; https://anam.ai/blog/heygen-pricing ; https://anam.ai/blog/d-id-api-review-2025-architecture-capabilities
- **E27** VASA-1: "no plans to release". https://www.ibtimes.com/microsoft-teases-lifelike-avatar-ai-tech-gives-no-release-date-3730144
- **E28** FlashAvatar monocular, minutes to train, 300 FPS. https://arxiv.org/abs/2312.02214 ; GaussianAvatars multi-view. https://arxiv.org/abs/2312.02069 ; SplattingAvatar 300 FPS, 30 FPS mobile. https://arxiv.org/abs/2403.05087
- **E29** GaussianTalker up to 120 FPS. https://arxiv.org/abs/2404.16012 ; TalkingGaussian. https://arxiv.org/abs/2404.15264
- **E30–E33** ExAvatar https://arxiv.org/abs/2407.21686 ; UniTalker https://arxiv.org/abs/2408.00762 ; EMOTE https://arxiv.org/abs/2306.08990 ; VHAP https://github.com/ShenhanQian/VHAP ; LAM one-shot, WebGL, OpenAvatarChat. https://github.com/aigc3d/LAM
- **E34** MuseTalk: 30fps+ on V100, MIT code, models usable commercially, 256×256 face region. https://github.com/TMElyralab/MuseTalk
- **E35** LivePortrait speed.md: ~14.8 ms/frame on RTX 4090, one-shot. https://github.com/KwaiVGI/LivePortrait/blob/main/assets/docs/speed.md ; InsightFace models "non-commercial research purposes only". https://github.com/deepinsight/insightface#license
- **E37** INSTA https://arxiv.org/abs/2211.12499 ; GeneFace++ https://arxiv.org/abs/2305.00787 ; ER-NeRF https://arxiv.org/abs/2307.09323 ; SyncTalk 50 FPS https://arxiv.org/abs/2311.17590
- **E38** Licences from each repo: Kokoro Apache-2.0 https://github.com/hexgrad/kokoro ; Piper MIT https://github.com/rhasspy/piper ; CosyVoice Apache-2.0 https://github.com/FunAudioLLM/CosyVoice ; Orpheus Apache-2.0 https://github.com/canopyai/Orpheus-TTS ; Chatterbox MIT https://github.com/resemble-ai/chatterbox ; Zonos Apache-2.0 https://github.com/Zyphra/Zonos ; Sesame CSM Apache-2.0 https://github.com/SesameAILabs/csm ; F5-TTS "pre-trained models are licensed under the CC-BY-NC license" https://github.com/SWivid/F5-TTS#license ; Fish Speech research licence, commercial use needs a separate licence https://github.com/fishaudio/fish-speech/blob/main/LICENSE ; XTTS "Coqui Public Model License" https://github.com/coqui-ai/TTS/blob/dev/docs/source/models/xtts.md
- **E39** Rhubarb Lip Sync: offline command-line tool over audio files. https://github.com/DanielSWolf/rhubarb-lip-sync
- **E40** ITU-R BT.1359: detectability +45 to −125 ms. https://www.tvtechnology.com/opinions/av-synchronization-how-bad-is-bad
- **E41** Unreal non-game seat licence $1,850/yr above $1M revenue. https://www.unrealengine.com/en-US/blog/we-are-updating-unreal-engine-twinmotion-and-realitycapture-pricing-in-late-april
- **E43** LiveKit avatar plugins (2026-10-04): anam, avatario, avatartalk, bey, bithuman, cambai, did, liveavatar, simli, synthesia, tavus; no hedra. https://github.com/livekit/agents/tree/main/livekit-plugins
- **E46** NVIDIA ACE documents an Unreal plugin only. https://docs.nvidia.com/ace/ace-unreal-plugin/2.5/index.html
- **E47** No "Audio2Face 3.0" product release found; the line is "Audio2Face-3D". https://github.com/NVIDIA/Audio2Face-3D-SDK
- **E48** Audio2Face-3D diffusion burst behaviour (~28 frames per ~470 ms). https://forums.developer.nvidia.com/t/audio2face-digital-human-sdk-v3-0-diffusion-model-frame-gap-during-streaming-inference-posting-here-as-digital-human-board-is-closed/361109
- **E49** ACE Unreal Plugin 2.5 supports UE 5.5 and 5.6. https://docs.nvidia.com/ace/ace-unreal-plugin/2.5/ace-unreal-plugin-changelog.html
- **E50** Omniverse Launcher deprecated 2025-10-01. https://developer.nvidia.com/omniverse/legacy-tools
- **E51** MetaHuman 5.8 / UE 5.8 (2026-06-17); OpenRigLogic MIT. https://www.metahuman.com/news/metahuman-5-8-is-now-available ; https://github.com/EpicGames/openriglogic
- **E52** GaussianHeadTalk, WACV 2026. https://arxiv.org/abs/2512.10939
- **E53** MOVA 2026-01-29, Apache-2.0, 8 s 360p, ≥24 GB with offloading. https://comfyui-wiki.com/en/news/2026-01-29-openmoss-mova-video-audio-generation ; LatentSync 1.6 Apache-2.0, 512², ~18 GB. https://news.creeta.com/en/open-source-lip-sync-models-2026/
- **E54** Wav2Lip non-commercial, 96×96 crop. https://github.com/Rudrabha/Wav2Lip
- **E55** Audio2Face-3D retargets via blendshape solving. https://arxiv.org/abs/2508.16401
- **E56** Cartesia `add_phoneme_timestamps`. https://docs.cartesia.ai/examples/tts-sse-with-phoneme-timestamps
- **E57** Visionary (WebGPU + ONNX). https://arxiv.org/abs/2512.08478 ; no indexed source for "BONSAI 340 fps".
- **E58** LiveAvatar (Intel Labs). https://github.com/IntelLabs/LiveAvatar
- **E59** MetaHuman `enable_material_parameter_caching`. https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MetaHumanTemplateMesh
