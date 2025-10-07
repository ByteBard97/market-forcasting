"""
Visualize synthetic Air Jordan demand data.

Creates diagnostic plots to verify data quality and patterns.
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)


def load_segment(json_path: str) -> dict:
    """Load segment JSON."""
    with open(json_path, 'r') as f:
        return json.load(f)


def plot_segment_overview(segment_data: dict, save_path: Path):
    """
    Create overview plot showing:
    - Observed units vs Prophet forecast
    - Components decomposition
    - Forecast errors
    """
    dates = pd.to_datetime(segment_data['calendar']['ds'])
    units = np.array(segment_data['observed']['units'])

    fig, axes = plt.subplots(4, 1, figsize=(16, 12))

    segment_name = segment_data['meta']['segment']
    fig.suptitle(f"{segment_name} - Overview", fontsize=16, fontweight='bold')

    # 1. Observed vs Forecast
    ax = axes[0]
    ax.plot(dates, units, label='Actual', color='black', alpha=0.7, linewidth=1)

    if segment_data.get('prophet') and segment_data['prophet'].get('yhat'):
        yhat = np.array(segment_data['prophet']['yhat'])
        yhat_lower = np.array(segment_data['prophet']['yhat_lower'])
        yhat_upper = np.array(segment_data['prophet']['yhat_upper'])

        ax.plot(dates, yhat, label='Prophet Forecast', color='blue', alpha=0.6, linewidth=1.5)
        ax.fill_between(dates, yhat_lower, yhat_upper, alpha=0.2, color='blue', label='95% CI')

    ax.set_ylabel('Units (pairs)', fontsize=11)
    ax.set_title('Demand: Actual vs Forecast', fontsize=12)
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)

    # 2. Prophet Components
    ax = axes[1]
    if segment_data.get('prophet') and segment_data['prophet'].get('trend'):
        trend = np.array(segment_data['prophet']['trend'])
        ax.plot(dates, trend, label='Trend', color='darkblue', linewidth=2)
        ax.set_ylabel('Trend', fontsize=11)
        ax.set_title('Prophet Trend Component', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)

    # 3. Ground truth components (multipliers)
    ax = axes[2]
    yearly = np.array(segment_data['ground_truth']['yearly'])
    holiday = np.array(segment_data['ground_truth']['holiday'])
    promo = np.array(segment_data['ground_truth']['promo'])

    ax.plot(dates, yearly, label='Yearly Seasonality', alpha=0.7, linewidth=1)
    ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    ax.set_ylabel('Multiplier', fontsize=11)
    ax.set_title('Ground Truth: Yearly Seasonality', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 4. Events overlay
    ax = axes[3]
    ax.plot(dates, units, color='black', alpha=0.5, linewidth=0.8)

    # Highlight holidays and drops
    holiday_flag = np.array(segment_data['events']['holiday_flag'])
    drop_flag = np.array(segment_data['events']['drop_flag'])

    holiday_dates = dates[holiday_flag == 1]
    drop_dates = dates[drop_flag == 1]

    ax.scatter(holiday_dates, units[holiday_flag == 1],
              color='red', alpha=0.6, s=20, label='Holiday', marker='o')
    ax.scatter(drop_dates, units[drop_flag == 1],
              color='green', alpha=0.6, s=30, label='Drop Event', marker='^')

    ax.set_ylabel('Units', fontsize=11)
    ax.set_xlabel('Date', fontsize=11)
    ax.set_title('Events Overlay', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"  Saved overview: {save_path}")


def plot_components_detail(segment_data: dict, save_path: Path):
    """
    Plot detailed view of multiplicative components.
    """
    dates = pd.to_datetime(segment_data['calendar']['ds'])

    fig, axes = plt.subplots(3, 3, figsize=(18, 12))
    axes = axes.flatten()

    segment_name = segment_data['meta']['segment']
    fig.suptitle(f"{segment_name} - Multiplicative Components", fontsize=16, fontweight='bold')

    components = [
        ('baseline', 'Baseline (> 0)', 'darkblue', False),
        ('weekly', 'Weekly Seasonality', 'blue', True),
        ('yearly', 'Yearly Seasonality', 'green', True),
        ('holiday', 'Holiday Effect', 'red', True),
        ('promo', 'Promo Effect', 'orange', True),
        ('price_mult', 'Price Elasticity', 'purple', True),
        ('hype_lead14', 'Hype (14d lead)', 'pink', True),
        ('marketing_lead7', 'Marketing (7d lead)', 'brown', True),
        ('traffic', 'Traffic', 'teal', True),
    ]

    for idx, (comp_name, title, color, show_unity) in enumerate(components):
        ax = axes[idx]
        comp_data = np.array(segment_data['ground_truth'][comp_name])

        ax.plot(dates, comp_data, color=color, alpha=0.7, linewidth=1)

        if show_unity:
            ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, linewidth=0.8)

        ax.set_title(title, fontsize=10)
        ax.set_ylabel('Value', fontsize=9)
        ax.grid(True, alpha=0.3)

        # Stats
        mean_val = comp_data.mean()
        std_val = comp_data.std()
        ax.text(0.02, 0.98, f'μ={mean_val:.2f}\nσ={std_val:.2f}',
               transform=ax.transAxes, fontsize=8, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"  Saved components: {save_path}")


def plot_inventory_analysis(segment_data: dict, save_path: Path):
    """
    Plot inventory flow and stockout analysis.
    """
    if not segment_data['meta'].get('inventory_cap', True):
        print("  Skipping inventory plot (cap disabled)")
        return

    dates = pd.to_datetime(segment_data['calendar']['ds'])
    units = np.array(segment_data['observed']['units'])
    on_hand = np.array(segment_data['inventory']['on_hand_start'])
    stockout_flag = np.array(segment_data['inventory']['stockout_flag'])

    fig, axes = plt.subplots(2, 1, figsize=(16, 8))

    segment_name = segment_data['meta']['segment']
    fig.suptitle(f"{segment_name} - Inventory Analysis", fontsize=16, fontweight='bold')

    # 1. Inventory level
    ax = axes[0]
    ax.plot(dates, on_hand, label='On-Hand Inventory', color='blue', alpha=0.7, linewidth=1.5)
    ax.plot(dates, units, label='Units Sold', color='green', alpha=0.5, linewidth=1)

    # Highlight stockouts
    stockout_dates = dates[stockout_flag == 1]
    if len(stockout_dates) > 0:
        ax.scatter(stockout_dates, on_hand[stockout_flag == 1],
                  color='red', alpha=0.7, s=30, label='Stockout', marker='x', linewidths=2)

    ax.set_ylabel('Units', fontsize=11)
    ax.set_title('Inventory Position & Stockouts', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 2. Stockout frequency over time
    ax = axes[1]

    # Weekly stockout rate
    df = pd.DataFrame({'date': dates, 'stockout': stockout_flag})
    df['week'] = pd.to_datetime(df['date']).dt.to_period('W')
    weekly_stockout_rate = df.groupby('week')['stockout'].mean()

    week_dates = [period.start_time for period in weekly_stockout_rate.index]
    ax.bar(week_dates, weekly_stockout_rate.values, width=5,
           color='red', alpha=0.6, label='Weekly Stockout Rate')

    ax.set_ylabel('Stockout Rate', fontsize=11)
    ax.set_xlabel('Date', fontsize=11)
    ax.set_title('Weekly Stockout Frequency', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"  Saved inventory: {save_path}")


def plot_correlation_analysis(segments_data: list, save_path: Path):
    """
    Plot cross-segment correlations.
    """
    # Extract daily units for all segments
    segment_names = []
    units_matrix = []

    for seg in segments_data:
        segment_names.append(seg['meta']['segment'])
        units_matrix.append(seg['observed']['units'])

    units_df = pd.DataFrame(units_matrix, index=segment_names).T

    # Compute correlation
    corr_matrix = units_df.corr()

    fig, ax = plt.subplots(figsize=(10, 8))

    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, vmin=-1, vmax=1, ax=ax,
                square=True, linewidths=0.5)

    ax.set_title('Cross-Segment Correlation (Daily Units)', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"  Saved correlation: {save_path}")


def main():
    """Generate all plots."""
    data_dir = Path("./data")
    plots_dir = Path("./plots")
    plots_dir.mkdir(exist_ok=True)

    # Load all segments
    json_files = list(data_dir.glob("AirJordan_*.json"))

    if len(json_files) == 0:
        print("No segment JSON files found in ./data/")
        return

    print(f"Found {len(json_files)} segments")
    print("="*60)

    segments_data = []

    for json_file in sorted(json_files):
        segment_data = load_segment(json_file)
        segments_data.append(segment_data)

        segment_name = segment_data['meta']['segment']
        print(f"\nPlotting {segment_name}...")

        # Overview
        plot_segment_overview(segment_data, plots_dir / f"{segment_name}_overview.png")

        # Components
        plot_components_detail(segment_data, plots_dir / f"{segment_name}_components.png")

        # Inventory
        plot_inventory_analysis(segment_data, plots_dir / f"{segment_name}_inventory.png")

    # Cross-segment correlation
    print(f"\nPlotting cross-segment analysis...")
    plot_correlation_analysis(segments_data, plots_dir / "segment_correlations.png")

    print("\n" + "="*60)
    print(f"✓ All plots saved to {plots_dir.absolute()}")
    print("="*60)


if __name__ == "__main__":
    main()
