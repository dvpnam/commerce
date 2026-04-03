# Commerce

An eBay-like auction platform built with Django for [CS50's Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/).

## Features

- **Listings** — Create auction listings with title, description, starting bid, image, and category
- **Bidding** — Place bids with real-time price validation (must exceed current highest bid)
- **Watchlist** — Add/remove listings to a personal watchlist
- **Comments** — Leave comments on any active listing
- **Categories** — Browse listings by category
- **Auction close** — Listing creator can close the auction; highest bidder is declared winner

## Tech Stack

- **Backend** — Python 3, Django 6
- **Database** — SQLite3
- **Frontend** — HTML5, CSS3, Bootstrap 4, Django Templates
- **Auth** — Django session-based authentication

## Project Structure

```
commerce/
├── auctions/
│   ├── models.py        # User, Listing, Bid, Comment
│   ├── views.py         # All view logic
│   ├── urls.py          # URL routing
│   ├── admin.py         # Admin registration
│   └── templates/
│       └── auctions/
│           ├── layout.html
│           ├── index.html
│           ├── listing.html
│           ├── create_listing.html
│           ├── watchlist.html
│           ├── categories.html
│           └── category.html
└── commerce/
    ├── settings.py
    └── urls.py
```

## Models

| Model | Fields |
|---|---|
| `User` | Extends AbstractUser, adds `watchlist` (M2M → Listing) |
| `Listing` | title, description, starting_bid, image_url, category, creator, active, winner |
| `Bid` | listing, bidder, amount, placed_at |
| `Comment` | listing, author, text, created_at |

## Getting Started

```bash
# Clone the repo
git clone https://github.com/dvpnam/commerce.git
cd commerce

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install django

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to use the app.

## Acknowledgements

Built as part of [CS50W — Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/), Harvard University / edX.
