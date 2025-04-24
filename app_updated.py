
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI Performance Analyzer", layout="centered")

st.title("🏅 AI Performance Analyzer for Athletes")
st.write("Upload your performance stats and compare them to professional athletes!")

# Upload user file
user_file = st.file_uploader("Upload your stats file", type=["csv", "xlsx"])
if user_file:
    if user_file.name.endswith('.csv'):
        user_df = pd.read_csv(user_file)
    else:
        user_df = pd.read_excel(user_file)
    st.subheader("Your Stats")
    st.dataframe(user_df)

# Upload pro benchmarks
pro_file = st.file_uploader("Upload benchmark data file", type=["csv", "xlsx"], key="pro")
if pro_file:
    if pro_file.name.endswith('.csv'):
        pro_df = pd.read_csv(pro_file)
    else:
        pro_df = pd.read_excel(pro_file)
    st.subheader("Pro Athletes Stats")
    st.dataframe(pro_df)

# Compare stats
if user_file and pro_file:
    if st.button("Compare Stats"):
        try:
            user_values = user_df.select_dtypes(include=[np.number]).iloc[0]
            pro_averages = pro_df.select_dtypes(include=[np.number]).mean()
            comparison = pd.DataFrame({
                "Your Stat": user_values,
                "Pro Average": pro_averages,
                "% of Pro Average": (user_values / pro_averages * 100).round(1).astype(str) + "%"
            })
            st.subheader("📊 Stat Comparison")
            st.dataframe(comparison)

            # Generate feedback
            st.subheader("📣 AI Feedback")
            for stat in user_values.index:
                user_val = user_values[stat]
                pro_val = pro_averages[stat]
                if user_val >= pro_val:
                    st.success(f"Great job on **{stat}**! You're meeting or exceeding pro averages.")
                elif user_val >= 0.85 * pro_val:
                    st.info(f"Your **{stat}** is about {round(user_val / pro_val * 100)}% of the pro average. Keep it up!")
                else:
                    st.warning(f"Consider improving your **{stat}** — currently at {round(user_val / pro_val * 100)}% of pro average.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
