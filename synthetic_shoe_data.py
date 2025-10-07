"""
Synthetic Shoe Sales Data Generator

Generates realistic, correlated time series data for a shoe company's sales & marketing team.
Includes trends, seasonality, promotions, holidays, and realistic correlations between:
- SKUs (product cannibalization)
- Regions (economic conditions)
- Channels (customer behavior)
- Price and demand (elasticity)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import holidays
from scipy import stats


class ShoeSalesGenerator:
    """
    Generate synthetic shoe sales data with realistic patterns and correlations.

    Features:
    - Multiple correlated SKUs (product families compete/complement)
    - Regional economic shocks (correlated sales across regions)
    - Channel shift patterns (retail to ecommerce correlation)
    - Price elasticity (price changes affect demand)
    - Seasonal patterns (yearly, monthly, weekly)
    - Holiday effects
    - Promotional campaigns
    - Weather effects (optional)
    """

    def __init__(
        self,
        start_date: str = "2019-01-01",
        end_date: str = "2024-12-31",
        seed: Optional[int] = 42
    ):
        """
        Initialize the generator.

        Args:
            start_date: Start date for time series (YYYY-MM-DD)
            end_date: End date for time series (YYYY-MM-DD)
            seed: Random seed for reproducibility
        """
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.dates = pd.date_range(start_date, end_date, freq='D')
        self.n_days = len(self.dates)

        if seed is not None:
            np.random.seed(seed)

        # Product catalog
        self.skus = [
            {"sku": "RUN-100", "family": "Running", "base_price": 120, "base_demand": 100},
            {"sku": "RUN-200", "family": "Running", "base_price": 150, "base_demand": 80},
            {"sku": "LIFE-300", "family": "Lifestyle", "base_price": 90, "base_demand": 120},
            {"sku": "BASK-400", "family": "Basketball", "base_price": 140, "base_demand": 70},
            {"sku": "TRAIN-500", "family": "Training", "base_price": 110, "base_demand": 90},
        ]

        self.regions = ["North America", "EMEA", "APAC", "LATAM"]
        self.channels = ["Retail", "Ecommerce", "Wholesale"]

        # US holidays (can add more countries)
        self.us_holidays = holidays.UnitedStates(years=range(
            self.start_date.year,
            self.end_date.year + 1
        ))

        # Correlation matrices (will be initialized in generate)
        self.sku_correlation = None
        self.region_correlation = None
        self.channel_correlation = None

    def _generate_correlation_matrix(self, n: int, strength: float = 0.3) -> np.ndarray:
        """
        Generate a valid correlation matrix.

        Args:
            n: Matrix dimension
            strength: Correlation strength (0-1)

        Returns:
            n x n correlation matrix
        """
        # Start with identity
        corr = np.eye(n)

        # Add random correlations
        for i in range(n):
            for j in range(i + 1, n):
                # Random correlation with given strength
                c = np.random.uniform(-strength, strength)
                corr[i, j] = c
                corr[j, i] = c

        # Ensure positive definite (make valid correlation matrix)
        eigvals, eigvecs = np.linalg.eigh(corr)
        eigvals[eigvals < 0] = 0.01  # Small positive values
        corr = eigvecs @ np.diag(eigvals) @ eigvecs.T

        # Normalize to correlation matrix
        d = np.sqrt(np.diag(corr))
        corr = corr / d[:, None] / d[None, :]

        return corr

    def _generate_base_signals(self) -> Dict[str, np.ndarray]:
        """
        Generate correlated base signals that will be shared across series.

        Returns:
            Dictionary of base signals
        """
        t = np.arange(self.n_days)

        # Global economic trend (affects all regions)
        global_trend = 1.0 + 0.0003 * t  # Slow growth

        # Add COVID shock (2020-2021)
        covid_shock = np.ones(self.n_days)
        covid_start = (pd.to_datetime("2020-03-15") - self.start_date).days
        covid_recovery = (pd.to_datetime("2021-06-01") - self.start_date).days
        if covid_start > 0 and covid_start < self.n_days:
            # Sharp drop then gradual recovery
            for i in range(covid_start, min(covid_recovery, self.n_days)):
                days_since = i - covid_start
                covid_shock[i] = 0.5 + 0.5 * (1 - np.exp(-days_since / 90))

        # Ecommerce shift trend (accelerated by COVID)
        ecom_shift = np.ones(self.n_days)
        for i, date in enumerate(self.dates):
            years_since_start = (date - self.start_date).days / 365.25
            # Faster growth after COVID
            if date >= pd.to_datetime("2020-03-15"):
                ecom_shift[i] = 1.0 + 0.002 * (i - covid_start)
            else:
                ecom_shift[i] = 1.0 + 0.0005 * i

        # Seasonal patterns (shared across all series)
        yearly_season = 0.3 * np.sin(2 * np.pi * t / 365.25 - np.pi / 2)  # Peak in summer
        monthly_season = 0.15 * np.sin(2 * np.pi * t / 30.5)

        # Weekly pattern (weekend effect)
        weekly_pattern = np.zeros(self.n_days)
        for i, date in enumerate(self.dates):
            if date.weekday() in [5, 6]:  # Weekend
                weekly_pattern[i] = 0.2
            else:
                weekly_pattern[i] = -0.05

        return {
            "global_trend": global_trend,
            "covid_shock": covid_shock,
            "ecom_shift": ecom_shift,
            "yearly_season": yearly_season,
            "monthly_season": monthly_season,
            "weekly_pattern": weekly_pattern,
        }

    def _generate_holiday_effects(self) -> np.ndarray:
        """Generate holiday boost effects."""
        holiday_effect = np.zeros(self.n_days)

        for i, date in enumerate(self.dates):
            if date in self.us_holidays:
                holiday_name = self.us_holidays.get(date)

                # Different holidays have different effects
                if "Black Friday" in str(holiday_name) or "Thanksgiving" in str(holiday_name):
                    # Black Friday week
                    for offset in range(-1, 4):  # 5-day boost
                        idx = i + offset
                        if 0 <= idx < self.n_days:
                            holiday_effect[idx] += 1.5

                elif "Christmas" in str(holiday_name):
                    # Christmas shopping season
                    for offset in range(-30, 0):  # Month before
                        idx = i + offset
                        if 0 <= idx < self.n_days:
                            holiday_effect[idx] += 0.3 + 0.02 * (30 + offset)

                elif "New Year" in str(holiday_name):
                    holiday_effect[i] += 0.5

                elif "Memorial Day" in str(holiday_name) or "Labor Day" in str(holiday_name):
                    holiday_effect[i] += 0.4

                else:
                    holiday_effect[i] += 0.2

        return holiday_effect

    def _generate_promo_campaigns(self, n_promos: int = 20) -> np.ndarray:
        """
        Generate random promotional campaigns.

        Args:
            n_promos: Number of promotional campaigns

        Returns:
            Array of promotional effects over time
        """
        promo_effect = np.zeros(self.n_days)

        for _ in range(n_promos):
            # Random promo start and duration
            start_idx = np.random.randint(0, self.n_days - 14)
            duration = np.random.randint(3, 21)  # 3-21 days
            strength = np.random.uniform(0.3, 0.8)  # Promo lift

            for i in range(start_idx, min(start_idx + duration, self.n_days)):
                promo_effect[i] += strength

        return promo_effect

    def _apply_price_elasticity(
        self,
        base_demand: np.ndarray,
        price_series: np.ndarray,
        base_price: float,
        elasticity: float = -1.5
    ) -> np.ndarray:
        """
        Apply price elasticity to demand.

        Args:
            base_demand: Base demand signal
            price_series: Price over time
            base_price: Reference price
            elasticity: Price elasticity (negative = demand decreases with price)

        Returns:
            Demand adjusted for price
        """
        price_ratio = price_series / base_price
        demand_multiplier = price_ratio ** elasticity
        return base_demand * demand_multiplier

    def generate(
        self,
        include_weather: bool = False,
        sku_correlation_strength: float = 0.4,
        region_correlation_strength: float = 0.5,
    ) -> pd.DataFrame:
        """
        Generate the full synthetic dataset.

        Args:
            include_weather: Include weather effects (temperature, precipitation)
            sku_correlation_strength: How correlated are SKU sales (0-1)
            region_correlation_strength: How correlated are regional sales (0-1)

        Returns:
            DataFrame with columns: date, sku, region, channel, units, price, revenue, etc.
        """
        print(f"Generating synthetic shoe sales data from {self.start_date.date()} to {self.end_date.date()}...")

        # Generate correlation matrices
        self.sku_correlation = self._generate_correlation_matrix(
            len(self.skus), sku_correlation_strength
        )
        self.region_correlation = self._generate_correlation_matrix(
            len(self.regions), region_correlation_strength
        )

        # Generate base signals
        base_signals = self._generate_base_signals()
        holiday_effects = self._generate_holiday_effects()
        promo_effects = self._generate_promo_campaigns(n_promos=25)

        # Generate correlated noise for SKUs and regions
        sku_noise = np.random.multivariate_normal(
            mean=np.zeros(len(self.skus)),
            cov=self.sku_correlation,
            size=self.n_days
        )

        region_noise = np.random.multivariate_normal(
            mean=np.zeros(len(self.regions)),
            cov=self.region_correlation,
            size=self.n_days
        )

        # Build dataset
        rows = []

        for sku_idx, sku_info in enumerate(self.skus):
            for region_idx, region in enumerate(self.regions):
                for channel in self.channels:
                    # Base parameters
                    base_demand = sku_info["base_demand"]
                    base_price = sku_info["base_price"]

                    # Regional multipliers
                    region_mult = {
                        "North America": 1.0,
                        "EMEA": 0.8,
                        "APAC": 0.9,
                        "LATAM": 0.6
                    }[region]

                    # Channel multipliers (Ecommerce growing)
                    if channel == "Retail":
                        channel_base = 0.5
                        channel_trend = -0.0002  # Declining
                        ecom_sensitivity = -0.3  # Negatively affected by ecom shift
                    elif channel == "Ecommerce":
                        channel_base = 0.35
                        channel_trend = 0.0005  # Growing
                        ecom_sensitivity = 1.2  # Benefits from ecom shift
                    else:  # Wholesale
                        channel_base = 0.15
                        channel_trend = -0.0001
                        ecom_sensitivity = 0.0

                    # Generate price series (base price + fluctuations + promos)
                    price_variation = 0.05 * np.sin(2 * np.pi * np.arange(self.n_days) / 365.25)
                    promo_discount = 0.15 * (promo_effects > 0)  # 15% off during promos
                    price_series = base_price * (1 + price_variation) * (1 - promo_discount)

                    # Build demand signal with all components
                    t = np.arange(self.n_days)
                    demand = base_demand * np.ones(self.n_days)

                    # Apply factors
                    demand *= base_signals["global_trend"]
                    demand *= base_signals["covid_shock"]
                    demand *= region_mult
                    demand *= (channel_base + channel_trend * t)
                    demand *= (1 + base_signals["yearly_season"])
                    demand *= (1 + base_signals["monthly_season"])
                    demand *= (1 + base_signals["weekly_pattern"])
                    demand *= (1 + holiday_effects)
                    demand *= (1 + promo_effects)

                    # Ecommerce shift effect
                    demand *= (1 + ecom_sensitivity * (base_signals["ecom_shift"] - 1))

                    # Apply price elasticity
                    demand = self._apply_price_elasticity(
                        demand, price_series, base_price, elasticity=-1.8
                    )

                    # Add correlated noise
                    demand *= (1 + 0.15 * sku_noise[:, sku_idx])  # SKU-specific shocks
                    demand *= (1 + 0.1 * region_noise[:, region_idx])  # Regional shocks

                    # Add independent noise (daily fluctuations)
                    demand *= (1 + 0.08 * np.random.randn(self.n_days))

                    # Convert to integer units (can't sell fractional shoes)
                    units = np.maximum(0, demand).astype(int)

                    # Calculate revenue
                    revenue = units * price_series

                    # Add to dataset
                    for i, date in enumerate(self.dates):
                        rows.append({
                            "date": date,
                            "sku": sku_info["sku"],
                            "sku_family": sku_info["family"],
                            "region": region,
                            "channel": channel,
                            "units": units[i],
                            "price": round(price_series[i], 2),
                            "revenue": round(revenue[i], 2),
                            "promo_flag": int(promo_effects[i] > 0),
                            "holiday_flag": int(holiday_effects[i] > 0),
                        })

        df = pd.DataFrame(rows)
        print(f"Generated {len(df):,} rows across {self.n_days} days")
        print(f"SKUs: {len(self.skus)}, Regions: {len(self.regions)}, Channels: {len(self.channels)}")

        return df

    def save_datasets(
        self,
        df: pd.DataFrame,
        output_dir: str = ".",
        include_aggregates: bool = True
    ):
        """
        Save datasets to CSV files.

        Args:
            df: Generated dataframe
            output_dir: Directory to save files
            include_aggregates: Also save weekly/monthly aggregates
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        # Daily data
        daily_path = os.path.join(output_dir, "shoe_sales_daily.csv")
        df.to_csv(daily_path, index=False)
        print(f"Saved daily data: {daily_path}")

        if include_aggregates:
            # Weekly aggregates
            weekly = df.groupby([
                pd.Grouper(key="date", freq="W"),
                "sku_family", "region", "channel"
            ]).agg({
                "units": "sum",
                "revenue": "sum",
                "price": "mean",
                "promo_flag": "max",
            }).reset_index()

            weekly_path = os.path.join(output_dir, "shoe_sales_weekly.csv")
            weekly.to_csv(weekly_path, index=False)
            print(f"Saved weekly data: {weekly_path}")

            # Monthly aggregates
            monthly = df.groupby([
                pd.Grouper(key="date", freq="M"),
                "sku_family", "region", "channel"
            ]).agg({
                "units": "sum",
                "revenue": "sum",
                "price": "mean",
                "promo_flag": "max",
            }).reset_index()

            monthly_path = os.path.join(output_dir, "shoe_sales_monthly.csv")
            monthly.to_csv(monthly_path, index=False)
            print(f"Saved monthly data: {monthly_path}")

        print("\nDataset summary:")
        print(f"  Date range: {df['date'].min().date()} to {df['date'].max().date()}")
        print(f"  Total units: {df['units'].sum():,}")
        print(f"  Total revenue: ${df['revenue'].sum():,.2f}")
        print(f"  Avg daily units: {df.groupby('date')['units'].sum().mean():.0f}")


# Example usage
if __name__ == "__main__":
    # Create generator
    generator = ShoeSalesGenerator(
        start_date="2019-01-01",
        end_date="2024-12-31",
        seed=42
    )

    # Generate data with correlations
    df = generator.generate(
        sku_correlation_strength=0.4,  # SKUs are moderately correlated
        region_correlation_strength=0.5,  # Regions are strongly correlated
    )

    # Save to files
    generator.save_datasets(df, output_dir="./data", include_aggregates=True)

    # Show some stats
    print("\n" + "="*60)
    print("Sample correlations:")
    print("="*60)

    # Compute correlation between two SKUs
    pivot = df.groupby(['date', 'sku'])['units'].sum().unstack()
    print("\nSKU correlations (daily units):")
    print(pivot.corr().round(2))

    # Channel correlation
    pivot_channel = df.groupby(['date', 'channel'])['units'].sum().unstack()
    print("\nChannel correlations (daily units):")
    print(pivot_channel.corr().round(2))
