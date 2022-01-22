from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

results_dir = Path(__file__).parent.parent / "results"
df = pd.DataFrame()
for file in results_dir.iterdir():
    loaded = pd.read_json(file)
    loaded = loaded.assign(source="fastapi" if "fastapi" in file.name else "starlite")
    df = df.append(loaded)

df_2 = df[["url", "source", "2xx"]]
grouped_src_url = df_2.groupby(by=["source", "url"]).agg(sum)
grouped_src_url.shape
t = grouped_src_url.reset_index()

fast_api_results = t[t["source"] == "fastapi"]
starlite_results = t[t["source"] == "starlite"]
fast_api_results.rename(columns={"2xx": "requests_processed_fastapi"}, inplace=True)
starlite_results.rename(columns={"2xx": "requests_processed_starlite"}, inplace=True)
merged_df = pd.merge(fast_api_results, starlite_results, on="url")
final_df = merged_df[
    ["url", "requests_processed_fastapi", "requests_processed_starlite"]
].set_index("url")
ax = final_df.plot.bar(rot=0)
plt.show()
print("done")