## Brief
- Goal: Log soil moisture from 4 balcony planters every 15 minutes for 90 days on one battery charge, and let me read the history on my phone at home.
- Constraints: One ESP32 dev board, 4 capacitive moisture sensors, one 18650 cell of 2,600 mAh. No mains power on the balcony. Parts budget C$80. Home Wi-Fi reaches the balcony. I can solder and write Arduino code.
- Non-goals: No automatic watering. No cloud service or phone app. No temperature or light sensing.

## Plan
1. Buy the parts: ESP32 dev board C$14, 4 moisture sensors C$36, 18650 cell and holder C$18, charger and boost board C$12, waterproof box C$22, wire and connectors C$10.
2. Wire the 4 sensors to 4 analog input pins and power them from the 3.3 V pin. Mount the board and cell in the waterproof box, with the sensor cables through a sealed gland.
3. Calibrate each sensor once: note the raw reading in dry air and in a glass of water, and store both numbers in one config section of the code. Moisture is reported as a percentage between those two numbers.
4. Firmware: every 15 minutes read the 4 sensors, take the average of 5 samples each, and add the 4 values and a timestamp from an internet time server to an array held in memory.
5. Size the array for the full run: 4 readings an hour for 90 days is 2,160 readings per planter, 8,640 values in total, which fits in the ESP32's memory.
6. The ESP32 stays awake and connected to Wi-Fi the whole time and serves one web page, so I can open the history from my phone at any moment. Typical current with Wi-Fi connected is about 80 mA.
7. The web page shows a table of the last 24 hours and a button that downloads the whole array as a CSV file.
8. Bench test for 48 hours indoors on USB power with the sensors in two pots, one watered and one dry. Check that the readings differ and that the CSV download opens in a spreadsheet.
9. Move it to the balcony on battery power. Done when the page shows 90 days of readings for all 4 planters with no gap longer than 30 minutes.

## Risks I already know about
- Capacitive sensors drift as the soil's salt content changes, so the percentages are only comparable within one planter.
- Condensation inside the box could corrode the connectors.
- Wi-Fi may drop in bad weather; the page would be unreachable until it reconnects.
