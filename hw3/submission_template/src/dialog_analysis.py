import pandas as pd

import json

import sys

# import argparse


print(sys.argv)

if (sys.argv[1] == "-o"):
    output_path = sys.argv[2]
    input_path = sys.argv[3]
else:
    output_path = "output.json"
    input_path = sys.argv[2]


dialogue_df = pd.read_csv(input_path)

ponies = dialogue_df.pony.value_counts()

sum_ponies = ponies.sum()

print(ponies.keys())

twilight_sparkle = ponies["Twilight Sparkle"]

apple_jack = ponies["Applejack"]

rarity = ponies["Rarity"]

pinkie_pie = ponies["Pinkie Pie"]

rainbow_dash = ponies['Rainbow Dash']

fluttershy = ponies['Fluttershy']


ponies_res = {
    "count": {
        "twilight sparkle": int(twilight_sparkle),
        "applejack": int(apple_jack),
        "rarity": int(rarity),
        "pinkie pie": int(pinkie_pie),
        "rainbow dash": int(rainbow_dash),
        "fluttershy": int(fluttershy)
    },
    "verbosity": {
        "twilight sparkle": round(int(twilight_sparkle) / int(sum_ponies), 2),
        "applejack": round(int(apple_jack) / int(sum_ponies), 2),
        "rarity": round(int(rarity) / int(sum_ponies), 2),
        "pinkie pie": round(int(pinkie_pie) / int(sum_ponies), 2),
        "rainbow dash": round(int(rainbow_dash) / int(sum_ponies), 2),
        "fluttershy": round(int(fluttershy) / int(sum_ponies), 2)
    }
}


ponies_res_json = json.dumps(ponies_res)

print(ponies_res)

print(ponies_res_json)


f = open(output_path, "w")
f.write(ponies_res_json)
f.close()
