import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Load dataset (adjust filename if needed)

df = pd.read_excel(r"C:\*****\Industries excel.xlsx") #Copy path from your local system

# --- Clean dataset ---

# Rename the first column to 'Sector'
df.rename(columns={df.columns[0]: "Sector"}, inplace=True)

# Drop any columns that are completely empty
df = df.dropna(axis=1, how="all")

# Remove any rows where the 'Sector' is blank (often used for notes or spacing)
df = df[df["Sector"].notna()]

# Keep only the rows that have numeric data in at least one of the year columns
year_cols = df.columns[1:]
df = df[df[year_cols].notna().any(axis=1)]

# Replace the "…" character with NaN and convert all year columns to a numeric type
df = df.replace("…", pd.NA)
for col in year_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Set 'Sector' as the index for easier data manipulation
df = df.set_index("Sector")

# --- Calculate Year-over-Year (YoY) growth (%) ---
growth = df.pct_change(axis=1) * 100

# --- Heatmap of YoY growth volatility ---
plt.figure(figsize=(14, 10))

sns.heatmap(growth, cmap="RdYlGn", center=0, cbar_kws={'label': '% Change'})
plt.title("Year-to-Year Growth Volatility by Space Economy Sector (2012–2023)", fontsize=16, weight="bold")
plt.xlabel("Year")
plt.ylabel("Sector")
plt.xticks(ticks=range(len(growth.columns)), labels=growth.columns, rotation=45, ha="right")
plt.tight_layout()
plt.show()



# --- Volatility Index (Standard Deviation of YoY growth) ---
volatility = growth.std(axis=1).sort_values(ascending=False)

plt.figure(figsize=(12, 8))
volatility.plot(kind="bar", color="steelblue")
plt.title("Volatility Index of Space Economy Sectors (2012–2023)", fontsize=16, weight="bold")
plt.ylabel("Std Dev of YoY Growth (%)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
