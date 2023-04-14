import requests
import json
import base64
from datetime import datetime
import os


def convert_prompt_to_image(prompt):
    url = 'http://localhost:7860/sdapi/v1/txt2img'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "prompt": prompt,
        "seed": -1,
        "sampler_name": "Euler a",
        "batch_size": 1,
        "n_iter": 1,
        "steps": 20,
        "cfg_scale": 4,
        "width": 1024,
        "height": 1024,
        "restore_faces": False,
        "tiling": False,
        "do_not_save_samples": False,
        "do_not_save_grid": False,
        "negative_prompt": "nfixer, nartfixer, nrealfixer",
        "send_images": True,
        "save_images": True,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        raise Exception("Failed to convert prompt to image")

    # Get current datetime for filename
    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{current_time}.png"
    directory = "./images_from_list_of_prompts"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    path = os.path.join(directory, filename)

    # Save the image to file
    with open(path, "wb") as f:
        f.write(base64.b64decode(json.loads(response.text)['images'][0]))

    return path


prompts = [
    "Modern skyscraper with a curved facade and a rooftop garden.",
    "Neoclassical building with a grand entrance and a dome.",
    "Futuristic city with tall buildings and flying cars.",
    "Medieval castle with a drawbridge and towers.",
    "Art Deco building with geometric patterns and a tall spire."
]

for i, prompt in enumerate(prompts, start=1):
    result = convert_prompt_to_image(prompt)
    print(f"Image {i} saved to {result}")
