        """Minimal Vidu example: create one prediction and print the output URL(s)."""
        import vidu_api

        output = vidu_api.run({
    "prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light"
})
        print(output)
