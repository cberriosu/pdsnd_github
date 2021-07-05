import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters(city,month,day):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #get user input for city (chicago, new york city, washington)
    while True:
        city = input("Please write a city name: Chicago, New York City or Washington. I must warn you that for Washington city there is less data available ").lower()
        if city not in CITY_DATA:
            print("\Please enter a valid city name\n ")
            continue
        else:
            break

    #get user input for month (all, january, february, ... , june) and day (all, monday, tuesday, ..., sunday)
    while True:
        time = input("Do you want to filter the data by month, day, all or none? ").lower()
        if time == 'month':
            month = input("Which month? You can select from January to June ").lower()
            day = 'all'
            break
        elif time == 'day':
            month = 'all'
            day = input("Which day would you like to select? It can be from Monday to Sunday ").lower()
            break
        elif time == 'all':
            month = input("Which month? You can select from January to June ").lower()
            day = input("Which day would you like to select? It can be from Monday to Sunday ").lower()
            break
        elif time == 'none':
            month = 'all'
            day = 'all'
            break
        else:
            input("Your input was incorrect. Do you want to filter the data by month, day, all or none? ").lower()
            break

    print("City(ies): {}".format(city))
    print("Month(s): {}".format(month))
    print("Day(s): {}".format(day))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        df = df[df['day_of_week'] == day.title()]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month is month number {}".format(common_month))

    #display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day is {}".format(common_day_of_week))

    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("The most common hour is {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("The most common start station is {}".format(common_start))

    #display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("The most common end station is {}".format(common_end))

    #display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " to " + df['End Station']
    common_combination = df['combination'].mode()[0]
    print("The most common combination is {}".format(common_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time is {} minutes".format(total_travel/60))

    #display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("The average trip duration is {} minutes".format(mean_travel/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User types:\n{}".format(user_types))

    #Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print("Gender:\n{}".format(gender))
    else:
        print("There is no gender available info for the selected city")

    #Display earliest, most recent, and most common year of birth
    if 'Brith_Year' in df:
        earliest = df['Birth_Year'].min()
        print("The earliest year of birth of the users is {}".format(earliest))
        recent = df['Birth_Year'].max()
        print("The most recent year of bith of the users is {}".format(recent))
        common_birth = df['Birth_Year'].mode()[0]
        print("The most common year of birth if the users is {}".format(common_birth))
    else:
        print("There is no birth year available info for the selected city")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data(df):
    #show raw data if the user wants to see it
    raw_data = 0
    while True:
        answer = input("Would you like to see the raw data? Type yes or no ").lower()
        if answer not in ['yes', 'no']:
            answer = input("You wrote the wrong word. Please type yes or no ").lower()
        elif answer == 'yes':
            raw_data += 5
            print(df.iloc[raw_data : raw_data + 5])
            again = input("Do you want to see more? Type yes or no ").lower()
            if again == 'no':
                break
        elif answer == 'no':
            return

def main():
    city = ""
    month = ""
    day = ""
    while True:
        city, month, day = get_filters(city, month, day)
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
