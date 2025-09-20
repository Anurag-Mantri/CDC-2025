import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Load dataset (adjust filename if needed)

df = pd.read_excel(r"C:\*****\Industries excel.xlsx") #Copy path from your local system

# Rename the first column to 'Sector'
df.rename(columns={df.columns[0]: "Sector"}, inplace=True)
df = df.dropna(axis=1, how="all")
df = df[df["Sector"].notna()]
year_cols = df.columns[1:]
df = df[df[year_cols].notna().any(axis=1)]
df = df.replace("…", pd.NA)
for col in year_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.set_index("Sector")

# --- Calculate Growth and Risk/Reward Metrics (Same as before) ---
growth = df.pct_change(axis=1) * 100
volatility = growth.std(axis=1)
average_growth = growth.mean(axis=1)

# Combine into a new DataFrame and use reset_index() to make 'Sector' a column
risk_reward_df = pd.DataFrame({
    'Volatility': volatility,
    'AverageGrowth': average_growth
}).reset_index()

# --- NEW: Readable Risk vs. Reward Visualization with Legend ---

# Set the style for the plot
sns.set_style("whitegrid")

# Create the scatter plot
plt.figure(figsize=(16, 10))
ax = sns.scatterplot(
    data=risk_reward_df,
    x='Volatility',
    y='AverageGrowth',
    hue='Sector',        # This is the key: assign a color to each sector
    s=200,               # Set the bubble size
    palette='tab20',     # Use a color palette with many distinct colors
    legend='full'
)

# Add quadrant lines for the average risk and reward
plt.axvline(x=risk_reward_df['Volatility'].mean(), color='red', linestyle='--', linewidth=1)
plt.axhline(y=risk_reward_df['AverageGrowth'].mean(), color='red', linestyle='--', linewidth=1)

# Move the legend to the outside of the plot area for clarity
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

# Add labels and a title
plt.title("Risk (Volatility) vs. Reward (Average Growth) of Space Economy Sectors", fontsize=20, weight="bold")
plt.xlabel("Risk (Std. Dev. of YoY Growth %)", fontsize=14)
plt.ylabel("Reward (Average YoY Growth %)", fontsize=14)

# Adjust plot layout to make room for the legend
plt.tight_layout(rect=[0, 0, 0.85, 1])

# Display the final plot
plt.show()
