import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

def trip_time_analysis(distance=100, min_speed=40, max_speed=200, step=10):
    """
    Analyze and visualize travel time savings when increasing speed.
    
    Parameters:
    -----------
    distance : float
        Trip distance in kilometers (default 100)
    min_speed : int
        Minimum speed in km/h (default 40)
    max_speed : int
        Maximum speed in km/h (default 200)
    step : int
        Speed increment between scenarios (default 10)
    """
    # Create speed array
    speeds = np.arange(min_speed, max_speed + step, step)
    
    # Travel time in minutes for each speed
    travel_times = (distance / speeds) * 60
    
    # Time saved by each +step km/h increase (compared to previous speed)
    time_saved = np.zeros_like(speeds, dtype=float)
    for i in range(1, len(speeds)):
        prev_time = (distance / speeds[i-1]) * 60
        curr_time = (distance / speeds[i]) * 60
        time_saved[i] = prev_time - curr_time
    
    # ---------- Dataframe ----------
    df = pd.DataFrame({
        "Speed (km/h)": speeds,
        "Travel Time (min)": travel_times.round(2),
        f"Time Saved vs Prev {step} km/h (min)": time_saved.round(2)
    })
    print(df.to_string(index=False))
    print("\n" + "="*70 + "\n")
    
    # ========== FIGURE 1: TRAVEL TIME vs SPEED ==========
    fig1, ax1 = plt.subplots(figsize=(12, 7))
    bg_color = "#f7f8fa"
    fig1.patch.set_facecolor(bg_color)
    ax1.set_facecolor(bg_color)
    
    # Line plot
    ax1.plot(speeds, travel_times, marker='o', color='#2c7fb8', linewidth=2.5,
             markersize=8, markerfacecolor='white', markeredgewidth=2)
    
    # Remove spines
    for spine in ax1.spines.values():
        spine.set_visible(False)
    
    # Grid
    ax1.grid(axis='both', linestyle=(0, (4, 4)), color='#d1d5db', alpha=0.7)
    ax1.set_axisbelow(True)
    
    # Ticks and labels
    ax1.tick_params(axis='both', colors='#6b7280', labelsize=13, length=0)
    ax1.set_xlabel("Speed (km/h)", fontsize=16, labelpad=10, color='#4b5563')
    ax1.set_ylabel("Travel Time (minutes)", fontsize=16, labelpad=10, color='#4b5563')
    
    # Titles
    fig1.text(0.08, 0.93, f"Travel Time for a {distance} km Trip", fontsize=28,
              fontweight='bold', color='#17223b')
    fig1.text(0.08, 0.86, f"As speed increases, travel time drops — but the benefit shrinks at higher speeds.",
              fontsize=15, color='#5b6475')
    
    plt.tight_layout(rect=[0.05, 0.05, 0.98, 0.88])
    
    # ========== FIGURE 2: TIME SAVED PER +STEP INCREASE ==========
    # Use speeds from min_speed+step onward (each bar represents an increase)
    new_speeds = speeds[1:]          # e.g., 50, 60, ... up to max_speed
    minutes_saved = time_saved[1:]   # time saved for each increase
    
    fig2, ax2 = plt.subplots(figsize=(14, 8))
    fig2.patch.set_facecolor(bg_color)
    ax2.set_facecolor(bg_color)
    
    # Horizontal rounded bars
    bar_height = 0.75
    colors = plt.cm.Blues(np.linspace(0.85, 0.25, len(new_speeds)))
    
    for i, (value, color) in enumerate(zip(minutes_saved, colors)):
        rect = FancyBboxPatch(
            (0, i - bar_height/2),
            value, bar_height,
            boxstyle="round,pad=0.02,rounding_size=0.25",
            linewidth=0, facecolor=color
        )
        ax2.add_patch(rect)
        ax2.text(value + 0.6, i, f"{value:.1f} min", va='center', fontsize=16, color='#1f2937')
    
    # Axes limits & labels
    ax2.set_xlim(0, max(minutes_saved) * 1.15)
    ax2.set_ylim(-1, len(new_speeds))
    ax2.set_yticks(range(len(new_speeds)))
    ax2.set_yticklabels(new_speeds, fontsize=18, color='#111827')
    ax2.invert_yaxis()
    
    # Remove spines and tick marks
    for spine in ax2.spines.values():
        spine.set_visible(False)
    ax2.tick_params(axis='y', length=0)
    ax2.tick_params(axis='x', colors='#6b7280', labelsize=14)
    
    # Grid
    ax2.grid(axis='x', linestyle=(0, (4, 4)), color='#d1d5db', alpha=0.7)
    ax2.set_axisbelow(True)
    
    ax2.set_xlabel("Minutes Saved", fontsize=20, labelpad=18, color='#4b5563')
    
    # Titles
    fig2.text(0.06, 0.93, f"Minutes saved from each +{step} km/h increase",
              fontsize=34, fontweight='bold', color='#17223b')
    fig2.text(0.06, 0.865,
              f"{distance} km trip. Notice how each additional speed increase saves less time than the previous one.",
              fontsize=18, color='#5b6475')
    
    plt.tight_layout(rect=[0.04, 0.05, 1, 0.86])
    
    # Show both figures
    plt.show()

# -------------------------------------------------------------------

trip_time_analysis(distance=100)
trip_time_analysis(distance=50)
trip_time_analysis(distance=30)