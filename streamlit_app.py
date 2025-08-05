# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 23:51:42 2025

@author: Zunair
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# --- Sidebar Inputs ---
st.sidebar.header("Simulation Settings")
sample_size = st.sidebar.slider("Sample Size", 2, 100, 10)
population_mean = st.sidebar.slider("Population Mean", 0, 100, 50)
population_std = st.sidebar.slider("Population Standard Deviation", 1, 100, 15)
num_simulations = st.sidebar.slider("Number of Simulations", 1, 1000, 100)
confidence_level = st.sidebar.slider("Confidence Level (%)", 50, 99, 95)

method = st.sidebar.selectbox("Method", ["Z with sigma"])  # You can extend this with "t without sigma", etc.

# --- Main Title ---
st.markdown(
    """
    <h1 style='text-align: center;'>Confidence Interval Simulation</h1>
    """,
    unsafe_allow_html=True,
)

# --- Simulation ---
np.random.seed(42)

sample_means = []
ci_lowers = []
ci_uppers = []

z_score = norm.ppf(1 - (1 - confidence_level / 100) / 2)

for _ in range(num_simulations):
    sample = np.random.normal(loc=population_mean, scale=population_std, size=sample_size)
    mean = np.mean(sample)
    stderr = population_std / np.sqrt(sample_size)
    ci_lower = mean - z_score * stderr
    ci_upper = mean + z_score * stderr

    sample_means.append(mean)
    ci_lowers.append(ci_lower)
    ci_uppers.append(ci_upper)

# Count how many intervals captured the true mean
captures = [1 if (population_mean >= l) and (population_mean <= u) else 0 for l, u in zip(ci_lowers, ci_uppers)]
capture_count = sum(captures)
capture_percent = capture_count / num_simulations * 100

# --- Plotting ---
fig, ax = plt.subplots(figsize=(12,6))
for i, (mean, lower, upper, captured) in enumerate(zip(sample_means, ci_lowers, ci_uppers, captures)):
    color = "blue" if captured else "red"
    ax.plot([i, i], [lower, upper], color=color)
    ax.plot(i, mean, "o", color="black")

ax.axhline(y=population_mean, color="red", linestyle="-", label="Population Mean")
ax.set_xlabel("Simulation")
ax.set_ylabel("Confidence Interval Range")
ax.set_title("Confidence Intervals Across Simulations")
ax.legend(["Population Mean", "Captured Interval", "Missed Interval"])

st.pyplot(fig)

# --- Summary ---
st.markdown(
    f"<p style='text-align:center;'>Captured Population Mean in {capture_count} of {num_simulations} simulations ({capture_percent:.1f}%)</p>",
    unsafe_allow_html=True,
)
