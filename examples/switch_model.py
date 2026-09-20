"""The same client drives every hosted model listed in vidu_api.MODELS."""
from vidu_api import Client, MODELS

client = Client()
for slug, info in MODELS.items():
    print(slug, "->", info["category"], "required:", info["required"])
# pick one explicitly
output = client.run({"prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light", "start_image_url": "https://example.com/input.png"}, model="kling/kling-video-v3-pro")
print(output)
