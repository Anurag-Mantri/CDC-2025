import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Load dataset (adjust filename if needed)

df = pd.read_excel(r"C:\Users\anura\Downloads\Industries excel.xlsx") #Copy path from your local system

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


# --- NEW: Risk vs. Reward Visualization ---

# Calculate the average (mean) YoY growth for each sector to represent "reward"
average_growth = growth.mean(axis=1)

# Combine volatility (risk) and average growth (reward) into a new DataFrame
risk_reward_df = pd.DataFrame({
    'Volatility': volatility,
    'AverageGrowth': average_growth
})

# Create the scatter plot
plt.figure(figsize=(14, 10))
sns.scatterplot(data=risk_reward_df, x='Volatility', y='AverageGrowth', s=150, legend=False)

# Add the name of each sector next to its point for clarity
for sector, data in risk_reward_df.iterrows():
    plt.text(data['Volatility'] + 0.5, data['AverageGrowth'], sector, fontsize=9)

# Add lines for the average volatility and average growth to create quadrants
plt.axvline(x=risk_reward_df['Volatility'].mean(), color='r', linestyle='--', linewidth=0.8)
plt.axhline(y=risk_reward_df['AverageGrowth'].mean(), color='r', linestyle='--', linewidth=0.8)

# Add labels and a title to the plot
plt.title("Risk (Volatility) vs. Reward (Average Growth)", fontsize=16, weight="bold")
plt.xlabel("Risk (Std. Dev. of YoY Growth %)")
plt.ylabel("Reward (Average YoY Growth %)")
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Calculate Year-over-Year (YoY) growth (%) ---
growth = df.pct_change(axis=1) * 100

# --- NEW: Correlation Analysis and Bar Chart ---

# Transpose the growth DataFrame so sectors are columns
growth_transposed = growth.T

# Calculate the correlation matrix
correlation_matrix = growth_transposed.corr()

# Unstack the matrix to get a list of all pairs
# This converts the grid of correlations into a single list
corr_pairs = correlation_matrix.unstack().sort_values(kind="quicksort")

# Remove self-correlations (e.g., a sector's correlation with itself is always 1)
corr_pairs = corr_pairs[corr_pairs != 1]

# To avoid duplicates (e.g., (A,B) and (B,A)), we can take every second item
# This gives us a clean list of unique pairs
unique_corr_pairs = corr_pairs.iloc[::2]

# --- Create the Visualization ---
# Get the 5 pairs with the highest positive correlation
top_5_positive = unique_corr_pairs.nlargest(5)

# Get the 5 pairs with the highest negative correlation (smallest values)
top_5_negative = unique_corr_pairs.nsmallest(5)

# Create the figure with two subplots (one for positive, one for negative)
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))
fig.suptitle('Most Significant Sector Correlations', fontsize=20, weight='bold')

# Plot the most POSITIVE correlations
top_5_positive.plot(kind='barh', ax=axes[0], color='seagreen')
axes[0].set_title('Top 5 Most Positively Correlated Pairs (Sectors that Move Together)', fontsize=14)
axes[0].set_xlabel('Correlation Coefficient')
axes[0].set_xlim(0, 1) # Set x-axis limits for positive correlations

# Plot the most NEGATIVE correlations
top_5_negative.plot(kind='barh', ax=axes[1], color='crimson')
axes[1].set_title('Top 5 Most Negatively Correlated Pairs (Sectors that Move Oppositely)', fontsize=14)
axes[1].set_xlabel('Correlation Coefficient')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
