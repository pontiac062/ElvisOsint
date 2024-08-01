# Website Scraper and Data Visualizer

This project is a comprehensive website scraper that extracts emails, telephone numbers, and links from a given website. It also provides geographical location mapping for domains and visualizes the scraped data. The application comes with a user-friendly GUI built using Tkinter.

## Features

- **Email Extraction**: Scrapes and extracts email addresses from the given website.
- **Telephone Number Extraction**: Scrapes and extracts telephone numbers from the given website.
- **Link Categorization**: Categorizes and extracts internal and external links.
- **Geolocation**: Fetches and maps the geographical location of the website's domain.
- **Data Visualization**: Provides a visual representation of the scraped data.
- **GUI Interface**: Easy-to-use graphical interface for entering the domain and selecting scrape options.

## Prerequisites

- Python 3.7 or higher
- `pip` (Python package installer)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/website-scraper.git
    cd website-scraper
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Install any additional dependencies:
    ```bash
    pip install folium requests beautifulsoup4 prettytable pandas geopy matplotlib
    ```

## Usage

1. Run the script:
    ```bash
    python scraper.py
    ```

2. Enter the domain (without `http`/`https`) in the provided input field.

3. Select the scrape options (Emails, Telephone Numbers, Links).

4. Click on "Start Scraping".

5. View the scraped data in the GUI and save the data to a CSV file if desired.

6. The map of the domain location will be created and can be saved as an HTML file.

7. Visualize the data using the bar chart displayed in the GUI.

## Troubleshooting

### Compatibility Issues with NumPy and Matplotlib

If you encounter errors related to NumPy or Matplotlib versions, follow these steps:

1. **Downgrade NumPy**:
    ```bash
    pip install numpy<2
    ```

2. **Upgrade Matplotlib and other dependencies**:
    ```bash
    pip install --upgrade matplotlib
    pip install --upgrade numpy
    ```

3. **Clean Installation** (Recommended):
    ```bash
    pip uninstall matplotlib numpy
    pip install numpy
    pip install matplotlib
    ```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://docs.python-requests.org/)
- [Folium](https://python-visualization.github.io/folium/)
- [PrettyTable](https://pypi.org/project/prettytable/)
- [Pandas](https://pandas.pydata.org/)
- [Geopy](https://geopy.readthedocs.io/)
- [Matplotlib](https://matplotlib.org/)

---

Feel free to create issues or contribute to the project by submitting a pull request. Your feedback and contributions are highly appreciated!

Additional Files
requirements.txt:

txt
Copy code
requests
beautifulsoup4
prettytable
pandas
geopy
folium
matplotlib
tk
LICENSE:
You can generate a standard MIT license text and place it in this file.
