import requests
from bs4 import BeautifulSoup
import json

# URL of your player profile
url = "https://mkwlounge.gg/ladder/player.php?ladder_id=15&player_id=5402"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    tables = soup.find_all("table", class_="profiletable")
    if tables:
        # Extract LR & MMR
        first_table = tables[0]
        rows = first_table.find_all("tr")
        if len(rows) > 1:
            data_cells = rows[1].find_all("td")
            if len(data_cells) > 6:
                lr = data_cells[5].text.strip()
                mmr = data_cells[6].text.strip()

        # Extract latest event's gain/loss
        event_table = tables[2]
        recent_event = event_table.find_all("tr")[1]
        event_cells = recent_event.find_all("td")

        if len(event_cells) > 8:
            lr_change = event_cells[8].text.strip()
            mmr_change = event_cells[10].text.strip()
        else:
            lr_change = "N/A"
            mmr_change = "N/A"

        # Handle cases where the change is a negative number
        if lr_change == "N/A":
            lr_output = f"{lr} LR N/A"
        else:
            lr_output = f"{lr} LR {lr_change}"

        if mmr_change == "N/A":
            mmr_output = f"{mmr} MMR N/A"
        else:
            mmr_output = f"{mmr} MMR {mmr_change}"

        # Create a dictionary to store the formatted results
        data = {
            "LR": lr_output,
            "MMR": mmr_output
        }

        # Save the formatted output to a JSON file
        with open("stats.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        print("Data updated successfully.")
else:
    print("Failed to fetch data.")

