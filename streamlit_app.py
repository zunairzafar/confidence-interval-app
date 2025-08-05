import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Simulation Settings")
sample_size = st.sidebar.slider("Sample Size", 2, 100, 10)
population_mean = st.sidebar.slider("Population Mean", 0, 100, 50)
population_std = st.sidebar.slider("Population Std Deviation", 1, 100, 15)
num_simulations = st.sidebar.slider("Number of Simulations", 1, 1000, 100)
confidence_level = st.sidebar.slider("Confidence Level (%)", 50, 99, 95)

method = st.sidebar.selectbox("Method", ["Z with sigma"])

# --- Main Title ---
st.markdown(
    """
    <h1 style='text-align: center; color: #FF4B4B;'> Confidence Interval Simulator</h1>
    <h3 style='text-align: center; color: #AAAAAA;'>by Zunair Zafar | Made with Streamlit</h3>
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

captures = [1 if (population_mean >= l) and (population_mean <= u) else 0 for l, u in zip(ci_lowers, ci_uppers)]
capture_count = sum(captures)
capture_percent = capture_count / num_simulations * 100

# --- Plotting ---
fig, ax = plt.subplots(figsize=(12,6))
for i, (mean, lower, upper, captured) in enumerate(zip(sample_means, ci_lowers, ci_uppers, captures)):
    color = "#1f77b4" if captured else "#ff7f0e"
    ax.plot([i, i], [lower, upper], color=color, linewidth=2)
    ax.plot(i, mean, "o", color="black")

ax.axhline(y=population_mean, color="red", linestyle="--", linewidth=2, label="Population Mean")
ax.set_xlabel("Simulation #", fontsize=12)
ax.set_ylabel("Confidence Interval", fontsize=12)
ax.set_title("Confidence Intervals Across Simulations", fontsize=16, pad=15)
ax.legend(["Population Mean", "Captured CI", "Missed CI"], loc="upper right")
ax.grid(True, linestyle="--", alpha=0.3)

st.pyplot(fig)

# --- Summary ---
st.markdown(
    f"""
    <div style='text-align: center; font-size: 18px;'>
        ✅ Captured the Population Mean in <b>{capture_count}</b> of <b>{num_simulations}</b> simulations
        (<b>{capture_percent:.1f}%</b> coverage)
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Footer ---
st.markdown(
    """
    <hr style="border-top: 1px solid #999;">
    <div style='text-align: center; color: #777;'>
        © 2025 Zunair Zafar. All rights reserved. 🌟
    </div>
    """,
    unsafe_allow_html=True,
)


