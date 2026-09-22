# Vidu API — Python client

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Hosted on Synexa](https://img.shields.io/badge/hosted%20on-Synexa-6366f1.svg)](https://synexa.ai/explore/bytedance/seedance-2.5?utm_source=github&utm_medium=ugc&utm_campaign=vidu-dev&utm_content=readme-badge&utm_term=tier-c)

Vidu is a video generation platform from Shengshu Technology that produces short clips from text, from a single image, from start and end frames, and from reference images of characters and objects that must stay consistent across shots. This repository is a Python client for Vidu-class video generation through a hosted API on Synexa, so you can generate clips of the same kind, text-to-video with synchronised audio and image-to-video with native sound, from a script with one `pip install` and an API token.

You get a blocking `run()` that takes a prompt (and optionally a first frame) and returns the video URL, a non-blocking create-and-poll path for batches, and webhook delivery for services that would rather be called back. The client has a single runtime dependency and no model weights. It is aimed at developers building short-form content tooling, ad creative pipelines, previsualisation or automated social publishing who want a Vidu-style generator as an HTTP call.

> **Try it now:** [https://synexa.ai/explore/bytedance/seedance-2.5](https://synexa.ai/explore/bytedance/seedance-2.5?utm_source=github&utm_medium=ugc&utm_campaign=vidu-dev&utm_content=readme-top&utm_term=tier-c) — the hosted model behind this client. New accounts get a free trial credit.

## Contents

- [Why this client](#why-this-client)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Hosted models](#hosted-models)
- [Parameters](#parameters)
- [Advanced usage](#advanced-usage)
- [About Vidu](#about-vidu)
- [Use cases](#use-cases)
- [FAQ](#faq)
- [License](#license)

## Why this client

- **No GPU or serving stack.** Video diffusion models of this class need datacenter GPUs with tens of gigabytes of VRAM, a video decoder, an audio model and a queue. The hosted endpoints run on Synexa's fleet and you pay per clip.
- **The comparable models are hosted-only.** Vidu itself, Seedance 2.5 and Kling V3 Pro are all proprietary; there is no checkpoint to self-host, so an endpoint is the only programmatic route.
- **No cold start on your side.** The models are resident on the endpoints; a single clip and a batch of hundreds see the same latency profile, with nothing to warm up.
- **Predictable cost.** `bytedance/seedance-2.5` is billed at $0.473 per run and `kling/kling-video-v3-pro` at $0.112 per run, so the cost of a campaign is known before you submit it.

## Installation

```bash
pip install git+https://github.com/vidu-dev/vidu-api.git
```

Then set your API key (create one at [synexa.ai](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=vidu-dev&utm_content=readme-apikey&utm_term=tier-c)):

```bash
export SYNEXA_API_KEY="sk-..."
```

## Quickstart

```python
import vidu_api

output = vidu_api.run({
    "prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light"
})
print(output)   # URL(s) of the generated result
```

Or with an explicit client:

```python
from vidu_api import Client

client = Client(api_key="sk-...")
output = client.run({"prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light"})
```

## Hosted models

| Model | Category | What it does | Price / run |
|---|---|---|---|
| [`bytedance/seedance-2.5`](https://synexa.ai/explore/bytedance/seedance-2.5?utm_source=github&utm_medium=ugc&utm_campaign=vidu-dev&utm_content=readme-models&utm_term=tier-c) | text-to-video | Seedance 2.5 generates a single-shot video of up to 30 seconds from a text prompt, with synchronised audio. | $0.473 |
| [`kling/kling-video-v3-pro`](https://synexa.ai/explore/kling/kling-video-v3-pro?utm_source=github&utm_medium=ugc&utm_campaign=vidu-dev&utm_content=readme-models&utm_term=tier-c) | image-to-video | Kling V3 Pro turns a still image into cinematic video with strong motion consistency, and can generate native audio in the same pass. | $0.112 |

The default model is **`bytedance/seedance-2.5`**; pass `model="owner/name"` to `run()` to use another one from the table.

## Parameters

### `bytedance/seedance-2.5`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `prompt` | string | yes | `A lone fisherman rows out at dawn across…` | — | The text prompt used to generate the video |
| `resolution` | string | no | `720p` | 480p, 720p, 1080p | Video resolution - 480p for faster generation, 720p for balance, 1080p for high quality. |
| `duration` | string | no | `auto` | auto, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 1… | Duration of the video in seconds. Supports 4 to 30 seconds, or auto to let the model decide based on the prompt. |
| `aspect_ratio` | string | no | `auto` | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | The aspect ratio of the generated video. Use 16:9 for landscape, 9:16 for portrait/vertical, 1:1 for square, 21:9 for ultrawide cinematic, or auto to let the model decide. |
| `generate_audio` | boolean | no | `True` | — | Whether to generate synchronized audio for the video, including sound effects, ambient sounds, and lip-synced speech. The cost of video generation is the same regardless of whether audio is generated or not. |
| `bitrate_mode` | string | no | `standard` | standard, high | Output bitrate mode. 'high' requests a higher-quality, larger-file encode from the model; 'standard' uses the default bitrate. |

### `kling/kling-video-v3-pro`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `prompt` | string | yes | `The camera slowly pushes in as the subje…` | — | Text prompt describing how the video unfolds from the first frame |
| `start_image_url` | file | yes | — | — | First frame of the video (.jpg/.png/.webp) |
| `duration` | string | no | `5` | 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | The duration of the generated video in seconds |
| `generate_audio` | boolean | no | `True` | — | Whether to generate native audio for the video. Supports Chinese and English voice output. Other languages are automatically translated to English. For English speech, use lowercase letters; for acronyms or proper nouns, use uppercase. |
| `end_image_url` | file | no | — | — | Optional last frame (.jpg/.png/.webp). When set, the clip is generated as a transition from the start image to this one |
| `shot_type` | string | no | `customize` | customize, intelligent | The type of multi-shot video generation. 'intelligent' lets the model automatically determine shot structure. |
| `negative_prompt` | string | no | `blur, distort, and low quality` | — | Things to keep out of the video |
| `cfg_scale` | number | no | `0.5` | 0, 1 | The CFG (Classifier Free Guidance) scale is a measure of how close you want the model to stick to your prompt. |

## Advanced usage

**Submit without blocking, then poll:**

```python
prediction = client.run(input, wait=False)      # returns immediately
prediction = client.wait(prediction, timeout=300)
print(prediction["output"])
```

**Webhook on completion:**

```python
client.run(input, wait=False, webhook="https://your-app.example/hooks/synexa")
```

**Errors:**

```python
from vidu_api import ModelError, PredictionTimeout

try:
    output = client.run(input)
except ModelError as e:
    print("failed:", e, e.prediction and e.prediction.get("id"))
except PredictionTimeout:
    print("still running — poll later")
```

Status values you will see on a prediction: `starting` → `processing` → `succeeded` | `failed`.

## About Vidu

Vidu ([vidu.com](https://www.vidu.com)) is a video generation platform built by Shengshu Technology, a Beijing company founded out of Tsinghua University's machine learning research group. Its models are based on the group's U-ViT work, which combines a diffusion model with a transformer backbone. The platform offers text-to-video, image-to-video, start-and-end-frame interpolation, and a reference-to-video mode in which characters, objects and environments supplied as reference images stay consistent across a generated clip. It is used for anime and stylised content, ad creative, and short narrative pieces where subject consistency matters.

The hosted endpoints this client exposes cover the same two core capabilities. `bytedance/seedance-2.5` is ByteDance's text-to-video model: it generates a single-shot clip of 4 to 30 seconds from a prompt at 480p, 720p or 1080p, in 16:9, 9:16, 1:1 or 21:9, with optional synchronised audio including sound effects, ambience and lip-synced speech, at no extra cost for audio. `kling/kling-video-v3-pro` is Kuaishou's image-to-video model: it animates a first frame according to a prompt, can generate native audio with Chinese and English speech in the same pass, accepts an optional end frame to produce a transition between two images, and exposes a multi-shot `shot_type`, a `negative_prompt` and `cfg_scale`.

Typical outputs are vertical clips for short-form platforms, product and lifestyle ads from a single hero image, animated storyboards for previsualisation, and short scenes with dialogue for narrative tests. Limits to plan for: one run produces one clip, Seedance tops out at 30 seconds, and Kling's image-to-video needs both a prompt and a start image.

The hosted endpoints used by this client are `bytedance/seedance-2.5` and `kling/kling-video-v3-pro`, which provide the same text-to-video and image-to-video capability as Vidu but are different models from different vendors. Vidu's own models are not served through this client; Vidu's platform and its own API are at [vidu.com](https://www.vidu.com).

**Official project:** https://www.vidu.com

## Use cases

- **Short-form vertical clips** — call `run()` on `bytedance/seedance-2.5` with a prompt, `aspect_ratio` 9:16 and `generate_audio` on for a ready-to-post clip with sound.
- **Product ads from one image** — animate a hero shot with `kling/kling-video-v3-pro`, passing the packshot as `start_image_url` and a camera-move prompt.
- **Image-to-image transitions** — set both `start_image_url` and `end_image_url` on Kling to morph between two keyframes, for example a before-and-after.
- **Dialogue tests** — write a short scene with spoken lines, enable audio on Seedance, and check whether lip-sync and timing hold before commissioning production.
- **Storyboard previsualisation** — batch each storyboard panel through the poll path at 480p for fast, cheap motion checks.
- **Long single shots** — request a 30-second `duration` on Seedance for establishing shots that would otherwise need stitching.

## FAQ

**Is there a Vidu API?**

Vidu offers an API on its own platform at vidu.com. This client does not call it; it calls hosted endpoints on Synexa that provide the same capability, `bytedance/seedance-2.5` for text-to-video and `kling/kling-video-v3-pro` for image-to-video.

**How much does Vidu-class video cost through this client?**

`bytedance/seedance-2.5` is billed at $0.473 per run (one clip of 4 to 30 seconds, audio included at no extra charge). `kling/kling-video-v3-pro` is $0.112 per run. There is no subscription; you pay per completed clip.

**Can I run Vidu without a GPU?**

Vidu's models are hosted-only and so are the two exposed here. With this client, generation happens on Synexa's GPUs; your machine only needs Python and network access.

**Does this client work with Vidu's reference-to-video or the Vidu app?**

No. Reference-to-video with multiple consistent subjects is a Vidu platform feature. This client provides text-to-video and single-image-to-video through different models.

**What input formats does it accept?**

Seedance 2.5 requires only `prompt`, with optional `resolution`, `duration` (4 to 30 seconds or auto), `aspect_ratio`, `generate_audio` and `bitrate_mode`. Kling V3 Pro requires `prompt` and `start_image_url` (.jpg, .png, .webp), with optional `end_image_url`, `duration`, `generate_audio`, `shot_type`, `negative_prompt` and `cfg_scale`.

**Is this the official Vidu SDK?**

No. This is an independent client that wraps hosted endpoints on Synexa. Vidu's official platform and API are at https://www.vidu.com.

## Related

- [Vidu](https://www.vidu.com) — official platform and API
- [Vidu guide](https://vidu-ai.pro) — walkthroughs and examples for Vidu-style video generation
- [Synexa Python client](https://github.com/synexa-ai/synexa-python) — the general-purpose SDK this client builds on
- [bytedance/seedance-2.5 on Synexa](https://synexa.ai/explore/bytedance/seedance-2.5) — text-to-video up to 30 seconds with synchronised audio
- [kling/kling-video-v3-pro on Synexa](https://synexa.ai/explore/kling/kling-video-v3-pro) — image-to-video with native audio and end-frame control
- [pixverse/pixverse-v6 on Synexa](https://synexa.ai/explore/pixverse/pixverse-v6) — stylised image-to-video at $0.025 per run

## License

MIT. This is an independent, community-maintained client and is not affiliated with or endorsed by the authors of Vidu. Model weights and trademarks belong to their respective owners.

_Last reviewed: 2026-09-22_
