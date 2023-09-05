# Instagram Auto-Reply App

## Overview

This document provides a step-by-step guide to set up and run the Instagram Auto-Reply App. This app automates the process of replying to Instagram messages and can be configured according to individual needs.

## Prerequisites

1. Python installed on your machine.
2. Google Chrome installed (needed for the WebDriver).

## Installation

Run the following command to install the required packages:

    ```
    pip install -r requirements.txt
    ```

## Configuration

### Adding Photos

1. Navigate to the `config` folder within the project directory.
2. Open the folder named `photos` and add your photos here.

### Updating `settings.json`

1. Open the `settings.json` file located inside the `config` folder.
2. Make sure to use **full paths** for any paths in the JSON file due to compatibility issues.
3. Update the following fields:

    - `web_driver`
        - `user_data_path`: Full path to your desired user data directory.
        - `headless`: Set to `false` to display the browser during execution.
        - `wait_time`: Time (in seconds) for the web driver to wait for elements to load.

    - `instagram`
        - `username`: Your Instagram username.
        - `password`: Your Instagram password.
        - `country_code`: Your country code (e.g., "MK").
        - `country_name`: Your country name (e.g., "Macedonia").
        - `messages`: Array of messages you want the bot to send.
        - `photos`: Full path to the photos you added earlier.

    - `load_wait_time`: General waiting time (in seconds) for things like VPN extension loading, page loading, etc.

## Running the App

1. After saving your configurations, navigate to the root directory of the project.
2. Run `app.py` by executing the following command:

    ```
    python app.py
    ```

## Customization

Inside `app.py`, you'll find various functionalities coded in. If you don't need specific functionalities, you can comment them out. For example, if you want the bot to reply to all messages and not just message requests, locate and comment out the corresponding line of code.

## Note on Country Code and Name

- `country_code` is used to verify if the bot is operating in the correct jurisdiction.
- `country_name` is used to set the VPN to the appropriate country.

---

For any further queries or issues, please contact the internal development team.
