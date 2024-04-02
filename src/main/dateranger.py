import pickle

if __name__ == '__main__':

    with open('data/current_dates.pkl', 'rb') as con_:
        all_dates = pickle.load(con_)

    print(all_dates[0])

    with open('data/current_dates.pkl', 'wb') as con_:
        all_dates = pickle.dump(all_dates[1:], con_)

