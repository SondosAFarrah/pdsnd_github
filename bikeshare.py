import time
import pandas as pd
import numpy as np

# Filenames for the datasets
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """Ask the user to specify a city, month, and day to analyze."""
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input("Which city would you like to analyze? (Chicago, New York City, Washington): ").strip().lower()
        if city in cities:
            break
        else:
            print("Invalid input. Please choose from Chicago, New York City, or Washington.")

    # Get user input for month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month? (January, February, ..., June, or 'all'): ").strip().lower()
        if month in months:
            break
        else:
            print("Invalid input. Please choose a valid month or 'all'.")

    # Get user input for day
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day? (Monday, Tuesday, ..., Sunday, or 'all'): ").strip().lower()
        if day in days:
            break
        else:
            print("Invalid input. Please choose a valid day or 'all'.")

    return city, month, day

def load_data(city, month, day):
    """
    Loads bikeshare data for the specified city and filters by month and day if applicable.

    Args:
        city (str): Name of the city to analyze.
        month (str): Name of the month to filter data (or 'all' for no filter).
        day (str): Name of the day to filter data (or 'all' for no filter).

    Returns:
        DataFrame: Filtered data based on user selection.
    """
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month
    if month != 'all' or day != 'all':
    filters = (df['month'] == (['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1)) if month != 'all' else True
    filters &= (df['day_of_week'] == day) if day != 'all' else True
    df = df[filters]


    return df

def time_stats(df):
    """Display the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Most common 
    common_month, common_day, common_hour = df[['month', 'day_of_week', 'hour']].mode().iloc[0]

    print(f"Most Common Month: {common_month}")
    print(f"Most Common Day of Week: {common_day}")
    print(f"Most Common Start Hour: {common_hour}")

    print(f"\nThis took {time.time() - start_time} seconds.\n")

def station_stats(df):
    """Display the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most common start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"Most Common Start Station: {common_start_station}")

    # Most common end station
    common_end_station = df['End Station'].mode()[0]
    print(f"Most Common End Station: {common_end_station}")

    # Most common trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['trip'].mode()[0]
    print(f"Most Common Trip: {common_trip}")

    print(f"\nThis took {time.time() - start_time} seconds.\n")

def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time
    total_duration = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_duration} seconds")

    # Average travel time
    average_duration = df['Trip Duration'].mean()
    print(f"Average Travel Time: {average_duration:.2f} seconds")

    print(f"\nThis took {time.time() - start_time} seconds.\n")

def user_stats(df, city):
    """Display statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    user_types = df['User Type'].value_counts()
    print(f"Counts of User Types:\n{user_types}\n")

    if city in ['chicago', 'new york city']:
        # Counts of gender
        gender_counts = df['Gender'].value_counts()
        print(f"Counts of Gender:\n{gender_counts}\n")

        # Birth year stats
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])

        print(f"Earliest Year of Birth: {earliest_year}")
        print(f"Most Recent Year of Birth: {most_recent_year}")
        print(f"Most Common Year of Birth: {most_common_year}")

    print(f"\nThis took {time.time() - start_time} seconds.\n")

def display_raw_data(df):
    """Display raw data upon user request in increments of 5 rows."""
    row_index = 0
    while True:
        raw_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no: ").strip().lower()
        if raw_data != 'yes':
            break

        print(df.iloc[row_index:row_index + 5])
        row_index += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no: ").strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
