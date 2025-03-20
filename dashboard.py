import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
day_df = pd.read_csv("dashboard/all_df.csv")

# Title
st.title("Dashboard Analisis Peminjaman Sepeda")

# Pilihan Musim dan Tahun
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
year_mapping = {0: "2011", 1: "2012"}
day_df["season_label"] = day_df["season"].map(season_mapping)
day_df["year_label"] = day_df["yr"].map(year_mapping)

selected_season = st.selectbox("Pilih Musim", day_df["season_label"].unique())
selected_year = st.selectbox("Pilih Tahun", day_df["year_label"].unique())

filtered_df = day_df[(day_df["season_label"] == selected_season) & (day_df["year_label"] == selected_year)]

# Heatmap Korelasi (Mengubah cmap agar lebih soft)
st.subheader("Korelasi antara Faktor Cuaca dan Jumlah Peminjaman")
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(filtered_df[['temp', 'hum', 'windspeed', 'cnt']].corr(), annot=True, cmap='Blues', fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

# Grafik Peminjaman Sepeda per Hari (Mengubah warna agar lebih soft)
st.subheader("Rata-rata Peminjaman Sepeda oleh Casual dan Registered per Hari")
weekday_avg = filtered_df.groupby("weekday")[['casual', 'registered']].mean()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=weekday_avg, markers=True, dashes=False, palette="pastel", ax=ax)
ax.set_xticks(range(7))
ax.set_xticklabels(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
ax.set_xlabel("Hari dalam Seminggu")
ax.set_ylabel("Rata-rata Jumlah Peminjaman Sepeda")
ax.legend(["Casual", "Registered"])
st.pyplot(fig)

# Distribusi Suhu terhadap Peminjaman (Mengubah warna scatterplot agar lebih lembut)
st.subheader("Distribusi Suhu dan Pengaruhnya terhadap Peminjaman")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=filtered_df, x="temp", y="cnt", alpha=0.5, color="cornflowerblue", edgecolor="black", ax=ax)
ax.set_xlabel("Suhu")
ax.set_ylabel("Jumlah Peminjaman Sepeda")
st.pyplot(fig)
