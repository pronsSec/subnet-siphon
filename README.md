# subnet-siphon

![DALL·E 2023-12-28 06 22 52 - A comic book style cover photo for a tool named 'Subnet-Siphon', written by 'been'  The image should feature a dynamic and stylized depiction of digit](https://github.com/pronsSec/subnet-siphon/assets/93559326/43596695-c838-4b59-8abb-ebaf3c2fed4d)


Subnet-Siphon is a Python command-line tool designed to process large lists of IP subnets. It efficiently removes duplicates, specifically targeting more specific subnets in a list containing both general and specific subnet entries. Using advanced data handling via dask, this tool can efficiently handle large lists with little resource usage. Or with more resources it can work very powerfully and quickly.

## Features

- **Efficient Processing**: Capable of handling large lists containing millions of IP subnets due to advanced data pre and post processing. Dask is used to provided advanced data handling and significant speed increases paired with less resource strain than purely python implementations.
- **Duplicate Removal**: Removes more specific subnet entries when a general version of the same subnet exists in the list.
- **Support for IPv4 and IPv6**: Handles both IPv4 and IPv6 subnet lists.
- **Progress Tracking**: Provides detailed progress updates with an estimated time to completion for each step.
- **Robust Error Handling**: Includes validation and error handling for improved reliability.
- **Rich Terminal Output**: Utilizes the `rich` library for modern, colorful, and formatted CLI output.
- **Output Flexibility**: Outputs the cleaned list in both CSV and text file formats.

## Installation

Before running the tool, ensure you have Python installed on your system. The tool has been tested with Python 3.8 and above.

1. **Clone the Repository**:

- git clone https://github.com/pronsSec/subnet-siphon
- cd subnet-siphon


2. **Install Dependencies**:

- pip install -r requirements.txt


## Usage

Run the script from the command line, providing the path to your input file. You can also specify the paths for the output CSV and text files.

- python subnet-siphon.py input_subnets.txt --output-csv cleaned_subnets.csv --output-txt cleaned_subnets.txt


## Contributing

Contributions to the IP Subnet List Cleaner are welcome! Here's how you can contribute:

1. **Fork the Repository**: Create your own fork and work on the features or fixes you're interested in.
2. **Submit Pull Requests**: Submit a PR with a clear description of your changes or enhancements.
3. **Report Issues or Suggest Features**: Use the GitHub Issues section to report any bugs or suggest new features.

## License

This project is licensed under The MIT License. Feel free to use, modify, and distribute the tool as per the license guidelines.

---

Developed by been
