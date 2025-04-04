import os
import streamlit as st
from pathlib import Path
import pandas as pd
import calendar

# Streamlit app to start data preparation
st.title("Optimizing Staff Allocation")

# Use simpler relative paths for data files
data_dir = Path("data") / "B3"

# Load all data files using the simplified path structure
month_day_filepath = data_dir / "adjust_month_day.csv"
adjust_month_day = pd.read_csv(month_day_filepath)
month_day_adjuster = adjust_month_day.set_index(['Month', 'Day_of_Week'])['adjuster_month_day'].to_dict()

hour_rides_filepath = data_dir / "adjust_hour_rides.csv"
adjust_hour_rides = pd.read_csv(hour_rides_filepath)
hour_adjuster_rides = adjust_hour_rides.set_index('DEB_TIME_HOUR')['adjuster_hourly_rides'].to_dict()

hour_eatery_filepath = data_dir / "adjust_hour_eatery.csv"
adjust_hour_eatery = pd.read_csv(hour_eatery_filepath)
hour_adjuster_eatery = adjust_hour_eatery.set_index('hour')['adjuster'].to_dict()

hour_merch_filepath = data_dir / "adjust_hour_merch.csv"
adjust_hour_merch = pd.read_csv(hour_merch_filepath)
hour_adjuster_merch = adjust_hour_merch.set_index('hour')['adjuster'].to_dict()

hour_general_filepath = data_dir / "adjust_hour_general.csv"
adjust_hour_general = pd.read_csv(hour_general_filepath)
hour_adjuster_general = adjust_hour_general.set_index('hour_adjusted')['adjuster'].to_dict()

public_holiday_filepath = data_dir / "adjust_public_holiday.csv"
adjust_public_holiday = pd.read_csv(public_holiday_filepath)
hour_adjuster_pubhol = adjust_public_holiday.set_index('status')['adjuster'].to_dict()

rain_filepath = data_dir / "adjust_rain.csv"
adjust_rain = pd.read_csv(rain_filepath)
rain_adjuster = adjust_rain.set_index('Rainy')['adjuster_rain'].to_dict()

# Construct adjusters dictionary
adjusters = {
    'month_day': month_day_adjuster,
    'hour_rides': hour_adjuster_rides,
    'hour_eatery': hour_adjuster_eatery,
    'hour_merch': hour_adjuster_merch,
    'hour_general': hour_adjuster_general,
    'public_holiday': hour_adjuster_pubhol,
    'rain': rain_adjuster
}

# Add scripts folder to path and import StaffingOptimizer
from scripts.B3.optimization_model import StaffingOptimizer
from scripts.B3.visualization import plot_staffing

# User inputs
base_demand = st.number_input("Enter Overall Yearly Mean Attendance", min_value=1, max_value=1000000, value=10000)
month = st.selectbox("Select Month", list(calendar.month_name[1:]))
day = st.selectbox("Select Day of the Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], index=0)
rain = st.radio("Is it forecasted to rain?", ["No", "Yes"]) == "Yes"
public_holiday = st.radio("Is it a public holiday?", ["No", "Yes"]) == "Yes"

# Run optimization when user clicks the button
if st.button("Optimize Staffing"):
    optimizer = StaffingOptimizer(adjusters, base_demand)
    staff_schedule_rides, staff_schedule_eatery, staff_schedule_merch, staff_schedule_general = optimizer.optimize_staffing(month, day, rain, public_holiday)
    
    st.write("### Optimized Staffing Schedules")
    st.write("#### Rides")
    st.dataframe(staff_schedule_rides)
    
    st.write("#### Eatery")
    st.dataframe(staff_schedule_eatery)
    
    st.write("#### Merchandise")
    st.dataframe(staff_schedule_merch)
    
    st.write("#### General")
    st.dataframe(staff_schedule_general)
    
    # Generate and display visualization
    fig = plot_staffing([staff_schedule_rides, staff_schedule_eatery, staff_schedule_merch, staff_schedule_general], month, day, rain, public_holiday)
    st.pyplot(fig)