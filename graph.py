
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load your CSV file
file_path = "Query_Germany.csv"  # Replace with actual file name
df = pd.read_csv(file_path)

# Clean theme field
df['theme'] = df['theme'].str.extract(r'data-theme/([A-Za-z0-9-_]+)', expand=False).fillna('Other')

# Count datasets per publisher
publisher_counts = df['publisherName'].value_counts().head(15)
top_publishers = publisher_counts.index.tolist()

# Filter to top publishers only
df_filtered = df[df['publisherName'].isin(top_publishers)]

# Group and count
grouped = df_filtered.groupby(['theme', 'publisherName']).size().reset_index(name='count')
grouped['size'] = np.sqrt(grouped['count']) * 8

# Plot
plt.figure(figsize=(14, 8))
sns.scatterplot(
    data=grouped,
    x="publisherName",
    y="theme",
    size="size",
    hue="theme",
    sizes=(20, 1500),
    alpha=0.7,
    legend=False
)

plt.title("📊 Top 15 Publishers by Dataset Theme", fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.xlabel("Publisher", fontsize=12)
plt.ylabel("Theme", fontsize=12)
plt.tight_layout()
plt.grid(True)
plt.show()
