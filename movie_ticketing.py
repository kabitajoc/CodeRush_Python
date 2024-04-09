import json

class UserDatabase:
    def __init__(self, filename='users.json'):
        self.filename = filename
        self.users = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.users, file)

    def sign_up(self, username):
        if username in self.users:
            print("Username already exists. Please choose a different one.")
            return False

        self.users[username] = {'watched_movies': []}
        self.save_data()
        print("Sign up successful!")
        return True

    def record_watched_movie(self, username, movie_id):
        self.users[username]['watched_movies'].append(movie_id)
        self.save_data()

class MovieDatabase:
    def __init__(self, filename='movies.json'):
        self.filename = filename
        self.movies = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.movies, file)

    def display_movies(self):
        print("Available Movies:")
        for movie_id, movie in self.movies.items():
            print(f"{movie_id}: {movie['title']}")

    def book_tickets(self, movie_id, num_tickets, selected_seats):
        if movie_id not in self.movies:
            print("Invalid movie ID.")
            return False

        movie = self.movies[movie_id]
        if len(selected_seats) > movie['available_seats']:
            print("Not enough seats available.")
            return False

        for seat in selected_seats:
            if seat not in movie['available_seats']:
                print(f"Seat {seat} is not available. Please select another seat.")
                return False

        movie['available_seats'] = [seat for seat in movie['available_seats'] if seat not in selected_seats]
        self.save_data()
        print("Tickets booked successfully!")
        return True

class MovieTicketingSystem:
    def __init__(self):
        self.user_db = UserDatabase()
        self.movie_db = MovieDatabase()

    def sign_up(self):
        username = input("Enter your username: ")
        self.user_db.sign_up(username)

    def log_in(self):
        username = input("Enter your username to log in: ")
        return username

    def book_tickets(self, username):
        self.movie_db.display_movies()
        movie_id = input("Enter movie ID to book tickets: ")
        num_tickets = int(input("Enter number of tickets: "))
        selected_seats = [input(f"Enter seat number for ticket {i+1}: ") for i in range(num_tickets)]
        success = self.movie_db.book_tickets(movie_id, num_tickets, selected_seats)
        if success:
            self.user_db.record_watched_movie(username, movie_id)

    def run(self):
        self.sign_up()
        username = self.log_in()

        while True:
            print("\nWelcome to the Movie Ticketing System!")
            print("1. Book Tickets")
            print("2. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.book_tickets(username)
            elif choice == '2':
                print("Thank you for using the Movie Ticketing System!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    ticketing_system = MovieTicketingSystem()
    ticketing_system.run()
