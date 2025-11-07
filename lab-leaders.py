import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Helper: return top-N rows ensuring each pitcher shows only once
def unique_pitcher_topN(df, sort_col, ascending=False, N=3):
    df_sorted = df.sort_values(by=sort_col, ascending=ascending)
    return df_sorted.drop_duplicates(subset='Pitcher', keep='first').head(N)

# Load CSV using popup dialog
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Select TrackMan CSV File",
    filetypes=[("CSV Files", "*.csv")]
)

df = pd.read_csv(file_path)

# Create column for absolute horizontal break
df['AbsHorzBreak'] = df['HorzBreak'].abs()

pitch_types = df['TaggedPitchType'].unique()

for pitch in pitch_types:
    pitch_df = df[df['TaggedPitchType'] == pitch]
    if pitch_df.empty:
        continue

    print(f"\n=== {pitch} ===")

    # FASTBALL RULE
    if "Fastball" in pitch:
        top_velo = unique_pitcher_topN(pitch_df, 'RelSpeed', False)
        top_ivb = unique_pitcher_topN(pitch_df, 'InducedVertBreak', False)

        print("\nTop 5 FB Velocity")
        print(top_velo[['Pitcher', 'RelSpeed', 'InducedVertBreak', 'HorzBreak']])

        print("\nTop 5 FB IVB")
        print(top_ivb[['Pitcher', 'RelSpeed', 'InducedVertBreak', 'HorzBreak']])


    # SINKER RULE
    elif "Sinker" in pitch:
        top_velo = unique_pitcher_topN(pitch_df, 'RelSpeed', False)
        top_hb = unique_pitcher_topN(pitch_df, 'AbsHorzBreak', False)
        low_ivb = unique_pitcher_topN(pitch_df, 'InducedVertBreak', True)

        print("\nTop 5 SK Velocity")
        print(top_velo[['Pitcher', 'RelSpeed', 'InducedVertBreak', 'HorzBreak']])

        print("\nTop 5 SK Horizontal Break")
        print(top_hb[['Pitcher', 'AbsHorzBreak', 'InducedVertBreak', 'HorzBreak']])

        print("\nTop 5 SK IVB")
        print(low_ivb[['Pitcher', 'InducedVertBreak', 'HorzBreak']])


    # SLIDER RULE
    elif "Slider" in pitch:
        if "SpinRate" in pitch_df.columns:
            top_spin = unique_pitcher_topN(pitch_df, 'SpinRate', False)
            print("\nTop 5 SL Spinrate")
            print(top_spin[['Pitcher', 'SpinRate', 'InducedVertBreak', 'HorzBreak']])

        # "Lowest abs(IVB + HB)" — Gyro
        pitch_df['Gyro'] = (pitch_df['InducedVertBreak'].abs() + pitch_df['AbsHorzBreak'])
        low_tightness = unique_pitcher_topN(pitch_df, 'Gyro', True)

        print("\nTop 5 SL Gyro")
        print(low_tightness[['Pitcher', 'Gyro', 'InducedVertBreak', 'HorzBreak']])


    # SWEEPER RULE
    elif "Sweeper" in pitch:
        if "SpinRate" in pitch_df.columns:
            top_spin = unique_pitcher_topN(pitch_df, 'SpinRate', False)
            print("\nTop 5 SW Spinrate")
            print(top_spin[['Pitcher', 'SpinRate', 'AbsHorzBreak']])

        top_hb = unique_pitcher_topN(pitch_df, 'AbsHorzBreak', False)
        print("\nTop 5 SW Horizontal Break")
        print(top_hb[['Pitcher', 'AbsHorzBreak', 'InducedVertBreak', 'HorzBreak']])


    # CHANGEUP RULE
    elif "ChangeUp" in pitch:
        top_hb = unique_pitcher_topN(pitch_df, 'AbsHorzBreak', False)
        low_ivb = unique_pitcher_topN(pitch_df, 'InducedVertBreak', True)

        print("\nTop 5 CH Horizontal Break")
        print(top_hb[['Pitcher', 'AbsHorzBreak', 'InducedVertBreak', 'HorzBreak']])

        print("\nTop 5 CH IVB")
        print(low_ivb[['Pitcher', 'InducedVertBreak', 'HorzBreak']])


    # CURVEBALL RULE
    elif "Curveball" in pitch:
        top_velo = unique_pitcher_topN(pitch_df, 'RelSpeed', False)
        low_ivb = unique_pitcher_topN(pitch_df, 'InducedVertBreak', True)

        print("\nTop 5 CU Velocity")
        print(top_velo[['Pitcher', 'RelSpeed', 'InducedVertBreak', 'HorzBreak']])

        print("\nTop 5 CU IVB")
        print(low_ivb[['Pitcher', 'InducedVertBreak', 'HorzBreak']])


    # OTHER PITCHES (fallback)
    else:
        print("No specific leaderboard rules for this pitch type.")
