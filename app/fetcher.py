import httpx
import random

# -------------------------------------------
# Image fetcher utility for all animal types
# -------------------------------------------
# This module fetches a random image URL for:
#  - cats (from thecatapi.com)
#  - dogs (from random.dog)
#  - bears (from placebear.com)
#
# The goal is to keep the logic separated, reusable and clean for each animal.
# -------------------------------------------


# -----------------------------
# CAT IMAGE FETCHER
# -----------------------------
# The Cat API returns a JSON array with a single object,
# where the image URL is stored in "url".
async def fetch_cat_image() -> str:
    url = "https://api.thecatapi.com/v1/images/search"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return data[0]["url"]


# -----------------------------
# DOG IMAGE FETCHER
# -----------------------------
# The Dog API sometimes returns videos (e.g., .gif, .mp4 or .webm),
# so we loop up to 10 times until a valid image URL is found.
async def fetch_dog_image() -> str:
    url = "https://random.dog/woof.json"
    async with httpx.AsyncClient() as client:
        for _ in range(10):  
# Retry logic to skip non-image responses, 
# could be potentially solved smarter by repeating till right type was given back 
# but this was faster for me hence I did not wanted an endless loop in case it would stop giving picture at all.
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            image_url = data["url"]
            if image_url.endswith((".jpg", ".jpeg", ".png")):
                return image_url
        raise ValueError("Could not fetch valid dog image after multiple attempts.")


# -----------------------------
# BEAR IMAGE FETCHER
# -----------------------------
# PlaceBear uses static URLs based on width and height.
# Since it does not return JSON, we just generate the URL directly.
# The width and height are randomized to get different images -> MVP decision: no user input yet needed here.
async def fetch_bear_image() -> str:
    width = random.randint(500, 800)   
    height = random.randint(400, 600)
    return f"https://placebear.com/{width}/{height}"


# -----------------------------
# ANIMAL-TYPE ROUTER FUNCTION
# -----------------------------
# This function wraps all animal fetchers
# and delegates based on animal type.
async def fetch_image_by_type(animal_type: str) -> str:
    if animal_type == "cat":
        return await fetch_cat_image()
    elif animal_type == "dog":
        return await fetch_dog_image()
    elif animal_type == "bear":
        return await fetch_bear_image()
    else:
        raise ValueError("Unsupported animal type")