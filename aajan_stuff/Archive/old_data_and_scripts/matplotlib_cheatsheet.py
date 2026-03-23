# =============================================================================
# MATPLOTLIB CHEAT SHEET — Copy, paste, trim to your needs
# =============================================================================
# Always start with this import block (you already have it)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # optional but handy for prettier defaults

# =============================================================================
# 0. PREPARE YOUR DATA (do this BEFORE plotting)
# =============================================================================
# df = pd.read_csv('your_file.csv')

# -- Filter rows --
# subset = df[df['property_type'] == 'HOUSE']
# subset = df[df['price'] < 1_000_000]
# subset = df[(df['price'] > 50000) & (df['livable_surface_m2'] > 20)]

# -- Group & aggregate --
# grouped = df.groupby('region')['price'].mean()            # Series
# grouped = df.groupby('region')['price'].mean().reset_index()  # DataFrame (better for plotting)
# grouped = grouped.sort_values('price', ascending=False)    # sort: ascending=False for biggest first

# -- Value counts (for category frequency) --
# counts = df['property_type'].value_counts()                # sorted by frequency by default


# =============================================================================
# 1. FIGURE + AXES SETUP (always start here)
# =============================================================================
# fig, ax = plt.subplots()
#   figsize=(width, height)   — in inches. (12, 6) is wide, (8, 8) is square
#   dpi=100                   — resolution. 100 is screen, 300 is print quality
#
# For multiple plots side by side:
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))
#   axes[0].plot(...)   # left plot
#   axes[1].plot(...)   # right plot
#   sharey=True         — same y-axis scale across subplots


# =============================================================================
# 2. PLOT TYPES — pick one, comment out the rest
# =============================================================================

# --- SCATTER (two numeric variables) ---
ax.scatter(x, y
  s=50              #— marker size (default ~20)
  c='steelblue'     #— color. Can also pass an array for color-by-value
  alpha=0.5          #— transparency 0-1. USE THIS when you have many points
  marker='o'         #— shape: 'o' circle, 's' square, '^' triangle, 'x' cross
  edgecolors='black' #— outline color
  cmap='coolwarm')    #— colormap (when c= is numeric array). Others: 'viridis', 'plasma'

# --- BAR (categories vs numeric) --- 
# 
ax.bar(x, height        # x = category names/positions, height = values
    width=0.8           #— bar width (0-1)
    color='steelblue'   #— single color or list of colors
    edgecolor='black')  #— bar border

#
# Horizontal bars:
ax.barh(y, width)    #— same args but horizontal. Good when labels are long.

# --- HISTOGRAM (distribution of one numeric) ---
# ax.hist(data)
#   bins=30            — number of bins. More bins = more detail. Start with 30.
#   bins=[0, 100000, 200000, ...]  — explicit bin edges
#   color='steelblue'
#   edgecolor='white'  — gap between bars, looks cleaner
#   alpha=0.7
#   density=True       — normalize to show proportions instead of counts

# --- BOXPLOT (distribution, great for comparing groups) ---
# ax.boxplot(data_list)
#   data_list = [group1_values, group2_values, ...]
#   vert=True          — vertical (default). False for horizontal
#   patch_artist=True  — fill boxes with color (needed for coloring)
#   showfliers=True    — show outlier dots (default True)
#   labels=['A','B']   — x-tick labels
#
# Easier with pandas:
# df.boxplot(column='price', by='region', ax=ax)

# --- LINE (trends, time series) ---
# ax.plot(x, y)
#   color='steelblue'
#   linewidth=2        — line thickness
#   linestyle='-'      — '-' solid, '--' dashed, ':' dotted, '-.' dash-dot
#   marker='o'         — add dots at data points
#   label='My line'    — for legend (call ax.legend() after)

# --- PIE (proportions — bar is usually better) ---
# ax.pie(values)
#   labels=['A','B']
#   autopct='%1.1f%%'  — show percentages
#   startangle=90
#   colors=['#ff9999','#66b3ff']


# =============================================================================
# 3. LABELS & TITLE (almost always needed)
# =============================================================================
ax.set_title('My Title', fontsize=16, fontweight='bold')
ax.set_xlabel('X Axis Label', fontsize=12)
ax.set_ylabel('Y Axis Label', fontsize=12)

# -- Tick formatting --
ax.tick_params(axis='x', rotation=45)          #— rotate x labels
ax.tick_params(labelsize=10)                   # — font size of tick labels
# ax.set_xticks([0, 1, 2])                       — explicit tick positions
# ax.set_xticklabels(['A', 'B', 'C'])            — explicit tick labels

# -- Format numbers on axis (e.g., "200K" instead of "200000") --
from matplotlib.ticker import FuncFormatter
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x/1000:.0f}K'))
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'€{x:,.0f}'))


# =============================================================================
# 4. COMMON EXTRAS
# =============================================================================
ax.legend(loc='upper right', fontsize=10 )   
#   show legend (needs label= in plot call)
#     # position: 'upper left', 'lower right', 'best'
#     # fontsize=10

ax.axhline(y=200000, color='red', linestyle='--', linewidth=1) # — horizontal reference line
ax.axvline(x=100, color='red', linestyle='--')                 # — vertical reference line

# ax.set_xlim(0, 500)               — force x-axis range
# ax.set_ylim(0, 1_000_000)         — force y-axis range

# ax.grid(True, alpha=0.3)          — light grid lines

# ax.annotate('Note!', xy=(x,y), fontsize=10)  — add text at a specific point


# =============================================================================
# 5. FINISH (always end with these)
# =============================================================================
# plt.tight_layout()                 — prevent labels from being cut off. ALWAYS USE.
# plt.show()                         — display the plot

# -- Save instead of show --
# fig.savefig('my_plot.png', dpi=300, bbox_inches='tight')
#   format: .png, .jpg, .svg, .pdf
#   bbox_inches='tight' — crop whitespace


# =============================================================================
# FULL WORKING EXAMPLE (uncomment to test)
# =============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(
     df['livable_surface_m2'],
     df['price'],
     alpha=0.3,
     s=20,
     c='steelblue',
    edgecolors='none')

ax.set_title('Price vs Living Area', fontsize=16, fontweight='bold')
ax.set_xlabel('Livable Surface (m²)', fontsize=12)
ax.set_ylabel('Price (€)', fontsize=12)
ax.set_xlim(0, 500)
ax.set_ylim(0, 2_000_000)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# =============================================================================
# COMMON COLORS (for reference)
# =============================================================================
# Named:    'steelblue', 'coral', 'seagreen', 'goldenrod', 'mediumpurple', 'tomato'
# Hex:      '#1f77b4' (default blue), '#ff7f0e' (orange), '#2ca02c' (green)
# Colormaps: 'coolwarm', 'viridis', 'plasma', 'Blues', 'Reds', 'RdYlGn'
#   Use with: c=numeric_array, cmap='viridis'  (in scatter)
#   Add colorbar: plt.colorbar(scatter_result, ax=ax, label='Values')
