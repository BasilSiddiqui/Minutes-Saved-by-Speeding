import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

def trip_time_analysis(distance=100, min_speed=40, max_speed=200, step=10):
    """
    Analyze and visualize travel time savings when increasing speed.
    Creates a single figure with two vertically stacked subplots:
        - Top: horizontal bar chart of minutes saved per speed increment.
        - Bottom: line plot of travel time vs speed.
    """
    # Speed array
    speeds = np.arange(min_speed, max_speed + step, step)
    
    # Travel time in minutes
    travel_times = (distance / speeds) * 60
    
    # Time saved per speed increment
    time_saved = np.zeros_like(speeds, dtype=float)
    for i in range(1, len(speeds)):
        prev_time = (distance / speeds[i-1]) * 60
        curr_time = (distance / speeds[i]) * 60
        time_saved[i] = prev_time - curr_time
    
    # ---------- Dataframe output ----------
    df = pd.DataFrame({
        "Speed (km/h)": speeds,
        "Travel Time (min)": travel_times.round(2),
        f"Time Saved vs Prev {step} km/h (min)": time_saved.round(2)
    })
    print(df.to_string(index=False))
    print("\n" + "="*70 + "\n")
    
    # ---------- Data for the bar chart ----------
    new_speeds = speeds[1:]          # speeds after increase (e.g., 50,60,...)
    minutes_saved = time_saved[1:]   # minutes saved per increase
    
    # ---------- Create single figure with two subplots (2 rows, 1 column) ----------
    bg_color = "#f7f8fa"
    fig, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(14, 14))
    fig.patch.set_facecolor(bg_color)
    
    # ===== TOP SUBPLOT: Time saved (horizontal rounded bars) =====
    ax_top.set_facecolor(bg_color)
    bar_height = 0.75
    colors = plt.cm.Blues(np.linspace(0.85, 0.25, len(new_speeds)))
    
    for i, (value, color) in enumerate(zip(minutes_saved, colors)):
        rect = FancyBboxPatch(
            (0, i - bar_height/2),
            value, bar_height,
            boxstyle="round,pad=0.02,rounding_size=0.25",
            linewidth=0, facecolor=color
        )
        ax_top.add_patch(rect)
        ax_top.text(value + 0.6, i, f"{value:.1f} min", va='center', fontsize=16, color='#1f2937')
    
    ax_top.set_xlim(0, max(minutes_saved) * 1.15)
    ax_top.set_ylim(-1, len(new_speeds))
    ax_top.set_yticks(range(len(new_speeds)))
    ax_top.set_yticklabels(new_speeds, fontsize=18, color='#111827')
    ax_top.invert_yaxis()
    
    for spine in ax_top.spines.values():
        spine.set_visible(False)
    ax_top.tick_params(axis='y', length=0)
    ax_top.tick_params(axis='x', colors='#6b7280', labelsize=14)
    
    ax_top.grid(axis='x', linestyle=(0, (4, 4)), color='#d1d5db', alpha=0.7)
    ax_top.set_axisbelow(True)
    ax_top.set_xlabel("Minutes Saved", fontsize=20, labelpad=18, color='#4b5563')
    
    # Title for top subplot (placed inside subplot to avoid overlap)
    ax_top.set_title(f"Minutes saved from each +{step} km/h increase in a {distance} km trip.\nNotice how each additional speed increase saves less time than the previous one.",
                     fontsize=16, fontweight='bold', color='#17223b', pad=20, loc='left')
    
    # ===== BOTTOM SUBPLOT: Travel time vs speed =====
    ax_bottom.set_facecolor(bg_color)
    ax_bottom.plot(speeds, travel_times, marker='o', color='#2c7fb8', linewidth=2.5,
                   markersize=8, markerfacecolor='white', markeredgewidth=2)
    
    for spine in ax_bottom.spines.values():
        spine.set_visible(False)
    
    ax_bottom.grid(axis='both', linestyle=(0, (4, 4)), color='#d1d5db', alpha=0.7)
    ax_bottom.set_axisbelow(True)
    
    ax_bottom.tick_params(axis='both', colors='#6b7280', labelsize=13, length=0)
    ax_bottom.set_xlabel("Speed (km/h)", fontsize=16, labelpad=10, color='#4b5563')
    ax_bottom.set_ylabel("Travel Time (minutes)", fontsize=16, labelpad=10, color='#4b5563')
    
    ax_bottom.set_title(f"Travel Time for a {distance} km Trip\nAs speed increases, travel time drops — but the benefit shrinks at higher speeds.",
                        fontsize=14, fontweight='bold', color='#17223b', pad=20, loc='left')
    
    # Adjust layout to prevent any collision
    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------------
# Run for different distances
trip_time_analysis(distance=100)
trip_time_analysis(distance=50)
trip_time_analysis(distance=30)