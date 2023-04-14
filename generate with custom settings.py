import requests
import json
import base64
from datetime import datetime
import os


def convert_prompt_to_image(prompt, custom_setting):
    url = 'http://localhost:7860/sdapi/v1/txt2img'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "prompt": prompt,
        "seed": 1337,
        "sampler_name": "Euler a",
        "batch_size": 1,
        "n_iter": 1,
        "steps": 20,
        "cfg_scale": custom_setting,
        "width": 768,
        "height": 768,
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
    filename = f"cfg_scale_{custom_setting}_{current_time}.png" # Modified filename
    directory = "./cfg_test"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    path = os.path.join(directory, filename)

    # Save the image to file
    with open(path, "wb") as f:
        f.write(base64.b64decode(json.loads(response.text)['images'][0]))

    return path


for custom_setting_value in range(-5, -1):
    prompt = "Big wooden building, modern style, golden hour lighting"
    result = convert_prompt_to_image(prompt, custom_setting_value)
    print(f"Image saved to {result}")
