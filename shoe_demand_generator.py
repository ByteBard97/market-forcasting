"""
Air Jordan Demand Generator with Multiplicative Composition

Generates realistic synthetic demand data for executive-level forecasting demos.
Implements the full pipeline: generate → fit Prophet → backtest → export JSON.

Usage:
    python shoe_demand_generator.py
    python shoe_demand_generator.py --no-fit --segments AJ_NA_DTC
    python shoe_demand_generator.py --start-date 2022-01-01 --freq W
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Literal
import holidays
import json
import argparse
from pathlib import Path


class AirJordanDemandGenerator:
    """
    Generate realistic Air Jordan demand with multiplicative components.

    Components (all multipliers ~1.0 except baseline > 0):
    - baseline_t: slow growth trend
    - weekly_t: weekend uplift
    - yearly_t: seasonality (back-to-school, holidays)
    - holiday_t: Black Friday, Christmas spikes
    - promo_t: promotional windows
    - price_mult_t: (price/list)^beta_price, beta < 0
    - hype_t: search/social/resale heat (leads 1-2w)
    - marketing_t: ad spend/impressions (leads 1-2w)
    - traffic_t: footfall/sessions (contemporaneous)
    - noise_t: lognormal residual
    - competitor_t: competitor launches (Adidas, New Balance) reduce demand 10-30%
    - weather_t: weather-driven traffic variance (5-15% impact)
    - viral_t: viral social events (50-200% spikes for 1-2w)

    Inventory: on_hand caps latent demand (stockouts during peaks)
    """

    def __init__(
        self,
        start_date: str = "2019-01-01",
        end_date: str = "2024-12-31",
        freq: Literal["D", "W"] = "D",
        seed: Optional[int] = 42,
        inventory_cap: bool = True,
    ):
        """
        Initialize generator.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            freq: Frequency ('D' daily or 'W' weekly)
            seed: Random seed for reproducibility
            inventory_cap: Enable inventory constraints and stockouts
        """
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.freq = freq
        self.inventory_cap = inventory_cap

        self.dates = pd.date_range(start_date, end_date, freq=freq)
        self.n_periods = len(self.dates)

        if seed is not None:
            np.random.seed(seed)

        # Product configuration: Air Jordan only
        self.product_line = "Air Jordan"
        self.list_price = 180.0  # MSRP
        self.regions = ["NA", "EMEA", "APAC"]
        self.channels = ["DTC", "Retail"]

        # US holidays (can extend to region-specific later)
        self.us_holidays = holidays.UnitedStates(
            years=range(self.start_date.year, self.end_date.year + 1)
        )

        # Config
        self.combine_mode = "multiplicative"
        self.version = "1.0"

    def _smooth_lead(self, signal: np.ndarray, lead_days: int) -> np.ndarray:
        """
        Create a leading version of a signal (shift forward in time).

        Args:
            signal: Original signal
            lead_days: Days to lead (positive = signal occurs earlier)

        Returns:
            Led signal (padded with 1.0 at end)
        """
        if self.freq == "W":
            lead_periods = max(1, lead_days // 7)
        else:
            lead_periods = lead_days

        # Shift signal forward (it "leads" the outcome)
        led = np.roll(signal, lead_periods)
        # Fill the end with neutral multiplier
        led[-lead_periods:] = 1.0
        return led

    def _generate_baseline(self) -> np.ndarray:
        """
        Generate baseline demand level with slow growth.

        Returns:
            Baseline level (> 0)
        """
        t = np.arange(self.n_periods)

        # Start level depends on channel
        base_level = 50.0  # pairs per day (will be scaled by channel/region)

        # Slow growth: ~0.03% per day = ~12% per year
        growth_rate = 0.0003 if self.freq == "D" else 0.0021  # adjust for weekly
        trend = base_level * (1 + growth_rate) ** t

        return trend

    def _generate_weekly_seasonality(self) -> np.ndarray:
        """
        Generate weekly pattern (weekend uplift for retail, inverse for wholesale).

        Returns:
            Weekly multiplier ~1.0
        """
        pattern = np.ones(self.n_periods)

        if self.freq == "D":
            for i, date in enumerate(self.dates):
                if date.weekday() in [5, 6]:  # Weekend
                    pattern[i] = 1.25  # 25% uplift
                else:
                    pattern[i] = 0.95  # slight weekday dip
        else:
            # Weekly data: no intra-week pattern
            pattern[:] = 1.0

        return pattern

    def _generate_yearly_seasonality(self) -> np.ndarray:
        """
        Generate yearly seasonality (spring/summer peak, back-to-school, holiday).

        Returns:
            Yearly multiplier ~1.0
        """
        t = np.arange(self.n_periods)
        days_per_period = 1 if self.freq == "D" else 7

        # Multiple harmonics for realistic shape
        # Peak in summer (June-July) and holiday season (Nov-Dec)
        yearly = (
            0.15 * np.sin(2 * np.pi * t * days_per_period / 365.25 - np.pi / 2) +  # main cycle
            0.10 * np.sin(4 * np.pi * t * days_per_period / 365.25 + np.pi / 4) +  # semi-annual
            1.0
        )

        return yearly

    def _generate_holiday_effects(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate holiday boost and flag.

        Returns:
            (holiday_multiplier, holiday_flag)
        """
        holiday_mult = np.ones(self.n_periods)
        holiday_flag = np.zeros(self.n_periods, dtype=int)

        for i, date in enumerate(self.dates):
            if date in self.us_holidays:
                holiday_name = str(self.us_holidays.get(date))
                holiday_flag[i] = 1

                # Black Friday week (Thanksgiving + 4 days)
                if "Thanksgiving" in holiday_name:
                    for offset in range(5):
                        idx = i + offset
                        if idx < self.n_periods:
                            holiday_mult[idx] *= 1.5  # 50% boost
                            holiday_flag[idx] = 1

                # Christmas season (4 weeks before)
                elif "Christmas" in holiday_name:
                    for offset in range(-28, 0):
                        idx = i + offset
                        if 0 <= idx < self.n_periods:
                            days_to_xmas = abs(offset)
                            boost = 0.1 + 0.01 * (28 - days_to_xmas)  # ramp up
                            holiday_mult[idx] *= (1 + boost)
                            holiday_flag[idx] = 1

                # Other major holidays
                elif any(h in holiday_name for h in ["New Year", "Memorial", "Labor", "Independence"]):
                    holiday_mult[i] *= 1.2
                else:
                    holiday_mult[i] *= 1.2

        return holiday_mult, holiday_flag

    def _generate_drop_events(self, n_drops: int = 8) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate product launch/drop events (spike + decay tail).

        Args:
            n_drops: Number of drop events over the time period

        Returns:
            (drop_multiplier, drop_flag)
        """
        drop_mult = np.ones(self.n_periods)
        drop_flag = np.zeros(self.n_periods, dtype=int)

        # Space drops roughly evenly (quarterly-ish)
        drop_indices = np.linspace(30, self.n_periods - 30, n_drops, dtype=int)

        for drop_idx in drop_indices:
            if drop_idx >= self.n_periods:
                continue

            # Spike on drop day
            drop_mult[drop_idx] *= 3.0
            drop_flag[drop_idx] = 1

            # Decay tail over next 2-3 weeks
            tail_length = 14 if self.freq == "D" else 2
            for offset in range(1, tail_length):
                idx = drop_idx + offset
                if idx < self.n_periods:
                    decay = np.exp(-offset / 7.0)  # exponential decay
                    drop_mult[idx] *= (1 + 1.0 * decay)
                    drop_flag[idx] = 1

        return drop_mult, drop_flag

    def _generate_promo(self, n_promos: int = 15) -> np.ndarray:
        """
        Generate promotional campaigns (random timing, 1-3 week duration).

        Args:
            n_promos: Number of promotional campaigns

        Returns:
            Promo multiplier ~1.0
        """
        promo_mult = np.ones(self.n_periods)

        for _ in range(n_promos):
            start_idx = np.random.randint(0, max(1, self.n_periods - 21))
            duration = np.random.randint(7, 22) if self.freq == "D" else np.random.randint(1, 4)
            boost = np.random.uniform(0.3, 0.7)  # 30-70% lift

            for i in range(start_idx, min(start_idx + duration, self.n_periods)):
                promo_mult[i] *= (1 + boost)

        return promo_mult

    def _generate_price_series(self, promo_mult: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate price series (list price + oscillation + promo discounts).

        Args:
            promo_mult: Promo multiplier (to align discounts)

        Returns:
            (price_series, price_multiplier for demand)
        """
        t = np.arange(self.n_periods)
        days_per_period = 1 if self.freq == "D" else 7

        # Small seasonal price variation
        price_variation = 0.05 * np.sin(2 * np.pi * t * days_per_period / 365.25)

        # Promo discounts (15-25% off during promos)
        promo_active = (promo_mult > 1.0).astype(float)
        promo_discount = promo_active * np.random.uniform(0.15, 0.25, self.n_periods)

        # Realized price
        price_series = self.list_price * (1 + price_variation) * (1 - promo_discount)

        # Price elasticity: demand ~ (price/list)^beta, beta = -1.8 (elastic)
        beta_price = -1.8
        price_mult = (price_series / self.list_price) ** beta_price

        return price_series, price_mult

    def _generate_hype_signal(self) -> Dict[str, np.ndarray]:
        """
        Generate hype signal (search volume, social mentions, resale heat).
        Exhibits bursts around drops and holidays.

        Returns:
            Dict with raw, lead7, lead14 versions
        """
        # Base hype level with slow growth
        t = np.arange(self.n_periods)
        hype_base = 1.0 + 0.0001 * t

        # Add bursts (AR-like persistence)
        hype_bursts = np.zeros(self.n_periods)
        for _ in range(20):  # random hype spikes
            spike_idx = np.random.randint(0, self.n_periods)
            spike_strength = np.random.uniform(0.5, 1.5)

            # Spike with decay
            for offset in range(14 if self.freq == "D" else 2):
                idx = spike_idx + offset
                if idx < self.n_periods:
                    decay = np.exp(-offset / 5.0)
                    hype_bursts[idx] += spike_strength * decay

        hype_raw = hype_base * (1 + hype_bursts)

        # Normalize to multiplier ~1.0
        hype_raw = hype_raw / hype_raw.mean()

        return {
            "hype_raw": hype_raw,
            "hype_lead7": self._smooth_lead(hype_raw, 7),
            "hype_lead14": self._smooth_lead(hype_raw, 14),
        }

    def _generate_marketing_signal(self) -> Dict[str, np.ndarray]:
        """
        Generate marketing spend/impressions signal.
        Concentrated around drops and holidays.

        Returns:
            Dict with raw, lead7, lead14 versions
        """
        # Base marketing with seasonal pattern
        t = np.arange(self.n_periods)
        days_per_period = 1 if self.freq == "D" else 7

        marketing_base = 1.0 + 0.2 * np.sin(2 * np.pi * t * days_per_period / 365.25)

        # Add campaign pulses
        marketing_pulses = np.zeros(self.n_periods)
        for _ in range(12):  # quarterly-ish campaigns
            pulse_idx = np.random.randint(0, self.n_periods)
            pulse_duration = np.random.randint(14, 28) if self.freq == "D" else np.random.randint(2, 4)
            pulse_strength = np.random.uniform(0.4, 0.9)

            for i in range(pulse_idx, min(pulse_idx + pulse_duration, self.n_periods)):
                marketing_pulses[i] += pulse_strength

        marketing_raw = marketing_base * (1 + marketing_pulses)

        # Normalize
        marketing_raw = marketing_raw / marketing_raw.mean()

        return {
            "marketing_raw": marketing_raw,
            "marketing_lead7": self._smooth_lead(marketing_raw, 7),
            "marketing_lead14": self._smooth_lead(marketing_raw, 14),
        }

    def _generate_traffic_signal(self) -> np.ndarray:
        """
        Generate footfall/web traffic (contemporaneous with sales).

        Returns:
            Traffic multiplier ~1.0
        """
        # Correlated with weekly/yearly patterns + noise
        t = np.arange(self.n_periods)
        days_per_period = 1 if self.freq == "D" else 7

        traffic = (
            1.0 +
            0.1 * np.sin(2 * np.pi * t * days_per_period / 365.25) +  # yearly
            0.05 * np.random.randn(self.n_periods)  # noise
        )

        # Add weekend boost for retail
        if self.freq == "D":
            for i, date in enumerate(self.dates):
                if date.weekday() in [5, 6]:
                    traffic[i] *= 1.3

        return np.maximum(0.5, traffic)  # floor to avoid negatives

    def _generate_noise(self) -> np.ndarray:
        """
        Generate multiplicative noise (lognormal).

        Returns:
            Noise multiplier (mean ~1.0)
        """
        # Lognormal: exp(epsilon), epsilon ~ N(mu, sigma)
        # Choose mu so mean(exp(epsilon)) = 1
        sigma = 0.15  # ~15% CV
        mu = -sigma**2 / 2  # ensures E[exp(epsilon)] = 1

        epsilon = np.random.normal(mu, sigma, self.n_periods)
        noise = np.exp(epsilon)

        return noise

    def _generate_competitor_events(self, n_events: int = 8) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate competitor launch events (negative demand impact).

        When competitors (Adidas, New Balance, etc.) launch major products,
        Air Jordan sales temporarily dip as consumers shift attention.

        Args:
            n_events: Number of competitor events over the time period

        Returns:
            (competitor_multiplier, competitor_flag)

        Impact: 10-30% demand reduction for 1-2 weeks
        """
        competitor_mult = np.ones(self.n_periods)
        competitor_flag = np.zeros(self.n_periods, dtype=int)

        # Space events roughly evenly (avoid too many clusters)
        event_indices = np.linspace(30, self.n_periods - 30, n_events, dtype=int)

        for event_idx in event_indices:
            if event_idx >= self.n_periods:
                continue

            # Impact strength (10-30% reduction)
            impact = np.random.uniform(0.10, 0.30)

            # Duration (7-14 days for daily, 1-2 weeks for weekly)
            duration = np.random.randint(7, 15) if self.freq == "D" else np.random.randint(1, 3)

            # Apply negative impact over duration with gradual recovery
            for offset in range(duration):
                idx = event_idx + offset
                if idx < self.n_periods:
                    # Strongest impact at start, gradual recovery
                    decay = 1 - (offset / duration)  # 1.0 -> 0.0
                    competitor_mult[idx] *= (1 - impact * decay)
                    competitor_flag[idx] = 1

        return competitor_mult, competitor_flag

    def _generate_weather_effects(self) -> np.ndarray:
        """
        Generate weather-driven traffic variance.

        Weather affects foot traffic in retail stores:
        - Rainy/snowy days → reduced store visits
        - Perfect weather → increased mall traffic

        Returns:
            Weather multiplier ~1.0

        Impact: 5-15% variance in daily traffic
        """
        t = np.arange(self.n_periods)
        days_per_period = 1 if self.freq == "D" else 7

        # Seasonal weather pattern (worse in winter, better in spring/fall)
        # Winter months (Dec-Feb) have more bad weather days
        seasonal_weather = 1.0 + 0.08 * np.sin(2 * np.pi * t * days_per_period / 365.25 + np.pi)

        # Random weather events (individual storm days)
        # ~20% of days have notable weather impact
        weather_noise = np.random.randn(self.n_periods) * 0.10

        # Combine
        weather_mult = seasonal_weather + weather_noise

        # Clip to reasonable range (0.85 to 1.15)
        weather_mult = np.clip(weather_mult, 0.85, 1.15)

        return weather_mult

    def _generate_viral_events(self, n_events: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate viral social media events (sudden demand spikes).

        Unexpected viral moments create demand surges:
        - Celebrity spotted wearing Air Jordans
        - TikTok trend featuring the product
        - Athlete milestone in the shoes (championship win)
        - Surprise collaboration announcement

        Args:
            n_events: Number of viral events per year (default: 4)

        Returns:
            (viral_multiplier, viral_flag)

        Impact: 50-200% spike for 1-2 weeks
        """
        viral_mult = np.ones(self.n_periods)
        viral_flag = np.zeros(self.n_periods, dtype=int)

        # Random timing (viral events are unpredictable)
        n_total_events = max(1, int(n_events * (self.n_periods / 365)))
        event_indices = np.random.choice(self.n_periods, size=n_total_events, replace=False)

        for event_idx in event_indices:
            # Viral strength (20-60% boost)
            strength = np.random.uniform(0.2, 0.6)

            # Initial spike (day 0-2)
            spike_duration = min(3, self.n_periods - event_idx) if self.freq == "D" else 1
            for offset in range(spike_duration):
                idx = event_idx + offset
                if idx < self.n_periods:
                    viral_mult[idx] *= (1 + strength)
                    viral_flag[idx] = 1

            # Decay tail (next 1-2 weeks as buzz fades)
            tail_duration = np.random.randint(7, 15) if self.freq == "D" else 2
            for offset in range(spike_duration, tail_duration):
                idx = event_idx + offset
                if idx < self.n_periods:
                    # Exponential decay
                    decay = np.exp(-(offset - spike_duration) / 5.0)
                    viral_mult[idx] *= (1 + strength * decay * 0.5)  # 50% of original at tail
                    viral_flag[idx] = 1

        return viral_mult, viral_flag

    def _simulate_inventory(
        self,
        latent_demand: np.ndarray,
        base_stock_level: float = 500.0
    ) -> Dict[str, np.ndarray]:
        """
        Simulate inventory flow with stockouts.

        Args:
            latent_demand: Unconstrained demand
            base_stock_level: Target inventory level

        Returns:
            Dict with on_hand_start, replenishment, returns, on_hand_end, stockout_flag
        """
        on_hand_start = np.zeros(self.n_periods)
        replenishment = np.zeros(self.n_periods)
        returns = np.zeros(self.n_periods)
        on_hand_end = np.zeros(self.n_periods)
        stockout_flag = np.zeros(self.n_periods, dtype=int)

        # Initial stock
        on_hand = base_stock_level

        # Return rate ~3%
        return_rate = 0.03

        for i in range(self.n_periods):
            on_hand_start[i] = on_hand

            # Replenishment: maintain target level (simplified weekly replenishment)
            if i % (7 if self.freq == "D" else 1) == 0:
                target_stock = base_stock_level * (1 + 0.3 * np.sin(2 * np.pi * i / self.n_periods))
                replenishment[i] = max(0, target_stock - on_hand)
                on_hand += replenishment[i]

            # Sales (capped by inventory)
            demand_this_period = latent_demand[i]
            actual_sold = min(demand_this_period, on_hand)

            if demand_this_period > on_hand:
                stockout_flag[i] = 1

            # Returns (from previous sales)
            if i > 0:
                returns[i] = return_rate * actual_sold
                on_hand += returns[i]

            # Update inventory
            on_hand = max(0, on_hand - actual_sold)
            on_hand_end[i] = on_hand

        return {
            "on_hand_start": on_hand_start,
            "replenishment": replenishment,
            "returns": returns,
            "on_hand_end": on_hand_end,
            "stockout_flag": stockout_flag,
        }

    def generate_segment(
        self,
        region: str,
        channel: str
    ) -> Dict:
        """
        Generate one segment's full dataset.

        Args:
            region: Region code (NA, EMEA, APAC)
            channel: Channel (DTC, Retail)

        Returns:
            Dict matching final JSON schema (without Prophet/metrics yet)
        """
        segment_name = f"AirJordan_{region}_{channel}"

        print(f"Generating {segment_name}...")

        # 1. Generate all components
        baseline = self._generate_baseline()
        weekly = self._generate_weekly_seasonality()
        yearly = self._generate_yearly_seasonality()
        holiday_mult, holiday_flag = self._generate_holiday_effects()
        drop_mult, drop_flag = self._generate_drop_events()
        promo_mult = self._generate_promo()
        price_series, price_mult = self._generate_price_series(promo_mult)

        hype_signals = self._generate_hype_signal()
        marketing_signals = self._generate_marketing_signal()
        traffic = self._generate_traffic_signal()
        noise = self._generate_noise()

        # NEW: Enhanced realism components
        competitor_mult, competitor_flag = self._generate_competitor_events()
        weather_mult = self._generate_weather_effects()
        viral_mult, viral_flag = self._generate_viral_events()

        # 2. Regional and channel adjustments
        region_mult = {"NA": 1.0, "EMEA": 0.75, "APAC": 0.85}[region]
        channel_mult = {"DTC": 0.6, "Retail": 0.4}[channel]

        # 3. Compose latent demand (multiplicative)
        latent_demand = (
            baseline *
            weekly *
            yearly *
            holiday_mult *
            drop_mult *
            promo_mult *
            price_mult *
            hype_signals["hype_lead14"] *
            marketing_signals["marketing_lead7"] *
            traffic *
            noise *
            competitor_mult *  # NEW: competitor launches reduce demand
            weather_mult *      # NEW: weather affects traffic
            viral_mult *        # NEW: viral events spike demand
            region_mult *
            channel_mult
        )

        # 4. Apply inventory cap
        if self.inventory_cap:
            base_stock = baseline.mean() * 10  # ~10 days of stock
            inventory_data = self._simulate_inventory(latent_demand, base_stock)
            units = np.minimum(latent_demand, inventory_data["on_hand_start"])
        else:
            inventory_data = {
                "on_hand_start": np.zeros(self.n_periods),
                "replenishment": np.zeros(self.n_periods),
                "returns": np.zeros(self.n_periods),
                "on_hand_end": np.zeros(self.n_periods),
                "stockout_flag": np.zeros(self.n_periods, dtype=int),
            }
            units = latent_demand

        units = np.maximum(0, units).astype(int)

        # 5. Revenue
        revenue = units * price_series

        # 6. Build JSON structure
        return {
            "version": self.version,
            "meta": {
                "segment": segment_name,
                "product_line": self.product_line,
                "region": region,
                "channel": channel,
                "date_range": [self.start_date.strftime("%Y-%m-%d"), self.end_date.strftime("%Y-%m-%d")],
                "freq": self.freq,
                "combine_mode": self.combine_mode,
                "units": "pairs",
            },
            "calendar": {
                "ds": [d.strftime("%Y-%m-%d") for d in self.dates]
            },
            "components": [
                "baseline", "weekly", "yearly", "holiday", "promo",
                "price_mult", "hype_lead14", "marketing_lead7", "traffic", "noise",
                "competitor", "weather", "viral"
            ],
            "ground_truth": {
                "baseline": baseline.tolist(),
                "weekly": weekly.tolist(),
                "yearly": yearly.tolist(),
                "holiday": holiday_mult.tolist(),
                "promo": promo_mult.tolist(),
                "price_mult": price_mult.tolist(),
                "hype_raw": hype_signals["hype_raw"].tolist(),
                "hype_lead7": hype_signals["hype_lead7"].tolist(),
                "hype_lead14": hype_signals["hype_lead14"].tolist(),
                "marketing_raw": marketing_signals["marketing_raw"].tolist(),
                "marketing_lead7": marketing_signals["marketing_lead7"].tolist(),
                "marketing_lead14": marketing_signals["marketing_lead14"].tolist(),
                "traffic": traffic.tolist(),
                "noise": noise.tolist(),
                "competitor": competitor_mult.tolist(),
                "weather": weather_mult.tolist(),
                "viral": viral_mult.tolist(),
            },
            "events": {
                "holiday_flag": holiday_flag.tolist(),
                "drop_flag": drop_flag.tolist(),
                "competitor_flag": competitor_flag.tolist(),
                "viral_flag": viral_flag.tolist(),
            },
            "inventory": {
                "on_hand_start": inventory_data["on_hand_start"].tolist(),
                "replenishment": inventory_data["replenishment"].tolist(),
                "returns": inventory_data["returns"].tolist(),
                "on_hand_end": inventory_data["on_hand_end"].tolist(),
                "stockout_flag": inventory_data["stockout_flag"].tolist(),
            },
            "observed": {
                "units": units.tolist(),
                "revenue": revenue.tolist(),
                "price": price_series.tolist(),
            },
            # Prophet and metrics will be added by fit_prophet method
            "prophet": {},
            "metrics": {},
        }

    def generate_all_segments(self) -> List[Dict]:
        """
        Generate all Air Jordan segments (3 regions × 2 channels = 6).

        Returns:
            List of segment data dicts
        """
        segments = []

        for region in self.regions:
            for channel in self.channels:
                segment_data = self.generate_segment(region, channel)
                segments.append(segment_data)

        return segments


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate Air Jordan synthetic demand data")
    parser.add_argument("--start-date", default="2019-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", default="2024-12-31", help="End date (YYYY-MM-DD)")
    parser.add_argument("--freq", default="D", choices=["D", "W"], help="Frequency (D=daily, W=weekly)")
    parser.add_argument("--no-inventory-cap", action="store_true", help="Disable inventory constraints")
    parser.add_argument("--segments", help="Comma-separated segment names (e.g., AJ_NA_DTC,AJ_EMEA_DTC)")
    parser.add_argument("--output-dir", default="./data", help="Output directory for JSON files")
    parser.add_argument("--no-fit", action="store_true", help="Skip Prophet fitting")
    parser.add_argument("--no-backtest", action="store_true", help="Skip backtesting")
    parser.add_argument("--horizon", type=int, default=56, help="Backtest horizon in days")
    parser.add_argument("--folds", type=int, default=4, help="Number of backtest folds")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")

    args = parser.parse_args()

    # Create generator
    generator = AirJordanDemandGenerator(
        start_date=args.start_date,
        end_date=args.end_date,
        freq=args.freq,
        inventory_cap=not args.no_inventory_cap,
        seed=args.seed,
    )

    # Generate segments
    if args.segments:
        requested = set(args.segments.split(","))
        all_segments = generator.generate_all_segments()
        segments_data = [s for s in all_segments if s["meta"]["segment"] in requested]
        if len(segments_data) == 0:
            print(f"Warning: No segments matched {requested}")
            segments_data = all_segments
    else:
        segments_data = generator.generate_all_segments()

    # Fit Prophet and backtest
    if not args.no_fit:
        try:
            from prophet_fitter import ProphetFitter

            print("\n" + "="*60)
            print("Fitting Prophet models...")
            print("="*60)

            fitter = ProphetFitter(seasonality_mode="multiplicative")

            # Fit only or fit + backtest
            if args.no_backtest:
                for i, segment_data in enumerate(segments_data):
                    segment_name = segment_data['meta']['segment']
                    print(f"[{i+1}/{len(segments_data)}] Fitting {segment_name}...")
                    segments_data[i] = fitter.fit_segment(segment_data, add_holidays=True)
            else:
                segments_data = fitter.fit_and_backtest_all(
                    segments_data,
                    horizon_days=args.horizon,
                    n_folds=args.folds,
                    add_holidays=True
                )

            print("\n✓ Prophet fitting complete")

        except ImportError as e:
            print(f"\n✗ Could not import Prophet: {e}")
            print("  Install with: pip install prophet")
            print("  Skipping Prophet fitting...")

    # Save JSON files
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "="*60)
    print("Saving JSON files...")
    print("="*60)

    for segment_data in segments_data:
        segment_name = segment_data["meta"]["segment"]
        output_file = output_dir / f"{segment_name}.json"

        with open(output_file, "w") as f:
            json.dump(segment_data, f, indent=2)

        print(f"✓ Saved {output_file}")

    print(f"\n✓ Generated {len(segments_data)} segments")
    print(f"✓ Output directory: {output_dir.absolute()}")

    # Summary stats
    if segments_data and "metrics" in segments_data[0] and segments_data[0]["metrics"]:
        print("\n" + "="*60)
        print("Backtest Summary:")
        print("="*60)
        for segment_data in segments_data:
            metrics = segment_data.get("metrics", {})
            if metrics:
                seg_name = segment_data["meta"]["segment"]
                print(f"{seg_name:25s} | MAE: {metrics['mae']:6.1f} | "
                      f"MAPE: {metrics['mape']:5.1f}% | Coverage: {metrics['coverage']:.2f}")

        # Average metrics
        avg_mae = np.mean([s["metrics"]["mae"] for s in segments_data if s.get("metrics")])
        avg_mape = np.mean([s["metrics"]["mape"] for s in segments_data if s.get("metrics")])
        avg_coverage = np.mean([s["metrics"]["coverage"] for s in segments_data if s.get("metrics")])

        print("-" * 60)
        print(f"{'AVERAGE':25s} | MAE: {avg_mae:6.1f} | MAPE: {avg_mape:5.1f}% | Coverage: {avg_coverage:.2f}")


if __name__ == "__main__":
    main()
