#!/usr/bin/env python
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

days_of_week = {'Su': 'sunday', 'M': 'monday', 'Tu': 'tuesday', 'W': 'wednesday', 'Th': 'thursday', 'F': 'friday', 'Sa': 'saturday', 'all': 'all'}

invalid_option = "Not one of the options, please try again !"


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input('Would you like to see data for Chicago, New York or Washington ? : ').strip()
        if city.lower() in CITY_DATA.keys():
            print('Filtering data by {}'.format(city.title()))
            break
        else:
            print(invalid_option)
            continue

    while True:
        user_input = input('Would you like to filter the data by month, day, both, or not at all? Type \"None\" for no time filter. : ').strip()
        if user_input.lower() == 'both':
            month = get_month()
            if month.lower() in months:
                print('Ok! Will filter data by {}'.format(month.title()))
            else:
                print(invalid_option)
                continue
            day = get_day()
            if day in days_of_week.keys():
                print('Ok! Will filter data by {}'.format(days_of_week.get(day).title()))
                break
            else:
                print(invalid_option)
                continue
        elif user_input.lower() == 'month':
            day = 'all'
            month = get_month()
            if month.lower() in months:
                print('Ok! Will filter data by {}'.format(month.title()))
                break
            else:
                print(invalid_option)
                continue
        elif user_input.lower() == 'day':
            month = 'all'
            day = get_day()
            if day in days_of_week.keys():
                print('Ok! Will filter data by {}'.format(days_of_week.get(day).title()))
                break
            else:
                continue
        elif user_input.lower() == 'none':
            month = 'all'
            day = 'all'
            print('Ok! Will consider all months and days')
            break
        else:
            print(invalid_option)
            continue

    print('-' * 40)
    return city.lower(), month.lower(), day

def get_month():
    """
    get user input for month (all, january, february, ... , june)
    Returns: Month from user input
    """
    month = input('Which Month from the list? {} : '.format(months)).strip()
    return month

def get_day():
    """
    get user input for day of week (all, monday, tuesday, ... sunday)
    Returns: Day from user input
    """
    day = input('Which day from the list? {} : '.format(list(days_of_week.keys()))).strip()
    return day


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


    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        # months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == days_of_week[day].title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is  : {}'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('The most common day of the week is : {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common start hour is : {}'.format(df['hour'].mode()[0]))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used Start Station is : {}, count : {}'.format(df['Start Station'].mode()[0], df['Start Station'].value_counts()[0]))

    # display most commonly used end station
    print('The most commonly used End Station is : {}, count : {}'.format(df['End Station'].mode()[0], df['End Station'].value_counts()[0]))

    # display most frequent combination of start station and end station trip
    start_station = df[['Start Station', 'End Station']].mode().at[0,'Start Station']
    end_station = df[['Start Station', 'End Station']].mode().at[0,'End Station']
    print('The most frequent combination of Start Station and End Station trip is : {} <--> {}'.format(start_station, end_station))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time is : {}'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Mean Travel Time is : {}'.format(df['Trip Duration'].mean()))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Finding user type stats .... ')

    user_type = df['User Type'].value_counts()

    for index , value in user_type.iteritems():
        print(' {} : {} '.format(index, value))

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nFinding Gender stats .... ')
        gender = df['Gender'].value_counts()

        for index, value in gender.iteritems():
            print(' {} : {} '.format(index, value))
    else:
        print('\'Gender\' column not present in data provided..')

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print('\nFinding Birth Year stats .... ')
        print('The most earliest birth year is {}'.format(np.min(df['Birth Year'])))
        print('The most recent birth year is {}'.format(np.max(df['Birth Year'])))
        print('The most common birth year is {}'.format(df['Birth Year'].mode()[0]))
    else:
        print('\'Birth Year\' column not present in data provided..')
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    """Displays 5 rows of raw data with pagination on user choice
       This was missed with first submission.
    """
    num_rows = df.shape[0]
    for i in range(0, num_rows, 5):
        # gets a dictionary object for pretty printing
        # https://stackoverflow.com/questions/26716616/convert-a-pandas-dataframe-to-a-dictionary#26716774
        dict_obj = df.iloc[i:i + 5].to_dict('list')

        # print 5 rows each time the user inputs yes.
        for j in range(0, 5):
            list_index = 0
            # derive the record number
            print('\nRecord #{}'.format(j + i + 1))
            for key in dict_obj.keys():
                print('  {} : {} '.format(key, dict_obj[key][list_index]))
                list_index += list_index

        choice = input('Would you like to view individual trip data? Type \'yes\' or \'no\': ')

        if choice.lower().strip() != 'yes':
            break

    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no : ')
        if restart.lower().strip() != 'yes':
            break


if __name__ == "__main__":
    main()
