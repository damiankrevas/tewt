import base64
import random
import requests
from seleniumbase import SB

# ---------------------------------------------------------
# Random harmless check functions
# ---------------------------------------------------------

def random_pause(min_ms=200, max_ms=900):
    delay = random.uniform(min_ms / 1000, max_ms / 1000)
    time.sleep(delay)

def random_noop():
    _ = random.randint(1, 1000) ** 2
    return True

def random_log():
    msgs = [
        "Verifying session integrity...",
        "Performing passive environment scan...",
        "Idle cycle executed.",
        "Background check OK.",
        "Heartbeat signal stable.",
    ]
    _ = random.choice(msgs)
    return True

def random_micro_checks():
    funcs = [random_pause, random_noop, random_log]
    for _ in range(random.randint(1, 3)):
        random.choice(funcs)()

# ---------------------------------------------------------
# Geolocation & Locale Setup
# ---------------------------------------------------------

geo_data = requests.get("http://ip-api.com/json/").json()

latitude = geo_data.get("lat")
longitude = geo_data.get("lon")
timezone_id = geo_data.get("timezone")
language_code = geo_data.get("countryCode", "").lower()

proxy_str = False

# ---------------------------------------------------------
# Target Stream URL
# ---------------------------------------------------------

encoded_name = "YnJ1dGFsbGVz"
decoded_name = base64.b64decode(encoded_name).decode("utf-8")

stream_url = f"https://www.twitch.tv/{decoded_name}"

# ---------------------------------------------------------
# Main Loop
# ---------------------------------------------------------

while True:
    with SB(
        uc=True,
        locale="en",
        ad_block=True,
        chromium_arg="--disable-webgl",
        proxy=proxy_str
    ) as driver:

        wait_time = random.randint(450, 800)

        driver.activate_cdp_mode(
            stream_url,
            tzone=timezone_id,
            geoloc=(latitude, longitude)
        )

        driver.sleep(2)
        random_micro_checks()

        if driver.is_element_present('button:contains("Accept")'):
            driver.cdp.click('button:contains("Accept")', timeout=4)

        driver.sleep(2)
        random_micro_checks()

        driver.sleep(12)

        if driver.is_element_present('button:contains("Start Watching")'):
            driver.cdp.click('button:contains("Start Watching")', timeout=4)
            driver.sleep(10)

        if driver.is_element_present('button:contains("Accept")'):
            driver.cdp.click('button:contains("Accept")', timeout=4)

        random_micro_checks()

        # ---------------------------------------------------------
        # If stream is live, open additional viewer instance
        # ---------------------------------------------------------
        if driver.is_element_present("#live-channel-stream-information"):

            if driver.is_element_present('button:contains("Accept")'):
                driver.cdp.click('button:contains("Accept")', timeout=4)

            random_micro_checks()

            secondary = driver.get_new_driver(undetectable=True)
            secondary.activate_cdp_mode(
                stream_url,
                tzone=timezone_id,
                geoloc=(latitude, longitude)
            )

            secondary.sleep(10)
            random_micro_checks()

            if secondary.is_element_present('button:contains("Start Watching")'):
                secondary.cdp.click('button:contains("Start Watching")', timeout=4)
                secondary.sleep(10)

            if secondary.is_element_present('button:contains("Accept")'):
                secondary.cdp.click('button:contains("Accept")', timeout=4)

            driver.sleep(wait_time)
            random_micro_checks()

        else:
            break
