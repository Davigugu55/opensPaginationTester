## Overview

The Call Report Data Fetcher is a Python script designed to interact with [Opens Yunique API](https://docs.yunique.com.br/) to fetch call report data. 

It retrieves call records based on specified parameters such as date range and queues, processes the data, and saves it to a CSV file for further analysis. Enabling us to compare the [Call Analitycs Queue Report with Pagination](https://docs.yunique.com.br/#ced1a612-66e9-4f41-ba7a-df44312762a7) with the [Call Synthetic Queue Report](https://docs.yunique.com.br/#5e48ea0d-d047-4612-aa2f-4602a63b9c15)

This tool is useful for businesses that use [Opens' Yunique Omnichannel Platform](https://www.opens.com.br/omnichannel), that they need to analyze call data for performance metrics, reporting, or compliance.

## Features

- Fetches call data from Yunique Analitycs and Synthetic API endpoints.
- Supports pagination to retrieve large datasets.
- Extracts relevant fields from the API response.
- Saves the fetched data to a CSV file with a formatted filename based on the date range.

## Requirements

- Python 3.x
- `requests` library
- `pandas` library
- `python-dotenv` library

You can install the required libraries using pip:
```bash
pip install requests pandas python-dotenv
```

## Configuration

Before running the script, you need to create a `.env` file in the root directory of the project to store your API credentials. The `.env` file should contain the following variables:
```
API_TOKEN=your_api_token_here
COMPANY_ID=your_company_id_here
```

## Usage

1. Clone the repository or download the script.
2. Install the required libraries as mentioned above.
3. Create a `.env` file with your API credentials.
4. Run the script:
```bash
python main.py
```

The script will fetch the call data and save it to a CSV file named `call-scroll-start_date-end_date.csv`, where `start_date` and `end_date` are the dates specified in the script.

## Logging

The script uses the `logging` module to log the progress and any errors encountered during execution. You can adjust the logging level in the script if needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.