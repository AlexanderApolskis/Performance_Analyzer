import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Set page configuration
st.set_page_config(page_title="AI Performance Analyzer", layout="centered")

# Sidebar
with st.sidebar:
    st.title("🏋️ Athlete Analyzer")
    st.write("Upload your data to analyze performance.")

# Main Page
st.title("🏀 AI Performance Analyzer for Basketball Athletes")
st.write("Upload your basketball performance stats and compare them to professional athletes!")

# Upload user file
user_file = st.file_uploader("Upload your basketball stats (CSV)", type=["csv"])
if user_file:
    user_df = pd.read_csv(user_file)
    st.subheader("Your Stats")
    st.dataframe(user_df)

# Upload professional benchmarks
pro_file = st.file_uploader("Upload professional benchmark data (CSV)", type=["csv"], key="pro")
if pro_file:
    pro_df = pd.read_csv(pro_file)
    st.subheader("Professional Athletes' Stats")
    st.dataframe(pro_df)

# Compare button
if user_file and pro_file:
    if st.button("Compare Stats"):
        # Calculate averages
        user_avg_ppg = user_df["PPG"].mean()
        user_avg_assists = user_df["Assists"].mean()
        user_avg_rebounds = user_df["Rebounds"].mean()

        pro_avg_ppg = pro_df["PPG"].mean()
        pro_avg_assists = pro_df["Assists"].mean()
        pro_avg_rebounds = pro_df["Rebounds"].mean()

        st.subheader("🏅 Average Performance Comparison")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Your Average PPG", f"{user_avg_ppg:.2f}")
            st.metric("Your Average Assists", f"{user_avg_assists:.2f}")
            st.metric("Your Average Rebounds", f"{user_avg_rebounds:.2f}")

        with col2:
            st.metric("Pro Average PPG", f"{pro_avg_ppg:.2f}")
            st.metric("Pro Average Assists", f"{pro_avg_assists:.2f}")
            st.metric("Pro Average Rebounds", f"{pro_avg_rebounds:.2f}")

        # Simple Feedback
        st.subheader("🧠 Quick Feedback")

        if user_avg_ppg >= pro_avg_ppg:
            st.success("Your scoring is above or equal to professional average! 🔥")
        else:
            st.warning("Your scoring is below professional average. 🏀 Keep shooting!")

        if user_avg_assists >= pro_avg_assists:
            st.success("Your playmaking is above or equal to professional average! 🎯")
        else:
            st.warning("Your playmaking is below professional average. 🏀 Work on assists!")

        if user_avg_rebounds >= pro_avg_rebounds:
            st.success("Your rebounding is above or equal to professional average! 💪")
        else:
            st.warning("Your rebounding is below professional average. 📈 Focus on boards!")

        # 📈 Add Bar Graph Comparison
        st.subheader("📊 Analysis Output: Stat Comparison")

        stats = ['PPG', 'Assists', 'Rebounds']
        user_averages = [user_avg_ppg, user_avg_assists, user_avg_rebounds]
        pro_averages = [pro_avg_ppg, pro_avg_assists, pro_avg_rebounds]

        x = range(len(stats))

        fig, ax = plt.subplots()
        ax.bar(x, user_averages, width=0.4, label='You', align='center')
        ax.bar([i + 0.4 for i in x], pro_averages, width=0.4, label='Pro Athletes', align='center')
        ax.set_xlabel('Metrics')
        ax.set_ylabel('Average Value')
        ax.set_title('Your Stats vs Pro Athlete Stats')
        ax.set_xticks([i + 0.2 for i in x])
        ax.set_xticklabels(stats)
        ax.legend()

        st.pyplot(fig)

        # 🧠 Machine Learning Model: Predict Performance Score
        st.subheader("🤖 Performance Score Prediction")

        # Define features and target
        features = ["PPG", "Assists", "Rebounds"]
        X_pro = pro_df[features]
        y_pro = pro_df["PPG"] * 0.5 + pro_df["Assists"] * 0.3 + pro_df["Rebounds"] * 0.2  # Example formula

        # Train the model
        model = LinearRegression()
        model.fit(X_pro, y_pro)

        # Predict for user data
        X_user = user_df[features]
        user_df["Performance Score"] = model.predict(X_user)

        st.dataframe(user_df[["Athlete", "Performance Score"]])

        # Visualize Performance Scores
        st.subheader("📈 Performance Score Visualization")
        fig2, ax2 = plt.subplots()
        ax2.bar(user_df["Athlete"], user_df["Performance Score"], color='skyblue')
        ax2.set_xlabel("Athlete")
        ax2.set_ylabel("Performance Score")
        ax2.set_title("Predicted Performance Scores")
        st.pyplot(fig2)
