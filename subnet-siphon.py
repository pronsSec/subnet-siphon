import argparse
import dask.dataframe as dd
import ipaddress
import pandas as pd
from dask.distributed import Client
from rich.console import Console
from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich.markdown import Markdown
from rich.text import Text

console = Console()

def parse_arguments():
    parser = argparse.ArgumentParser(description='IP Subnet List Cleaner')
    parser.add_argument('file_path', type=str, help='Path to the input file containing IP subnets')
    parser.add_argument('--output-csv', type=str, default='processed_subnets.csv', help='CSV output file path')
    parser.add_argument('--output-txt', type=str, default='processed_subnets.txt', help='Text output file path')
    return parser.parse_args()

def validate_input_file(file_path):
    try:
        with open(file_path, 'r') as file:
            if not any(line.strip() for line in file):
                console.log("[bold red]Error: The input file is empty.")
                return False
    except IOError as e:
        console.log(f"[bold red]Error: Unable to read the file. {e}")
        return False
    return True

def pre_process_subnets(df):
    def to_ip_network(subnet):
        try:
            return ipaddress.ip_network(subnet, strict=False)
        except ValueError:
            return None

    df['subnet'] = df['subnet'].map(to_ip_network)
    df = df.dropna(subset=['subnet'])
    return df.sort_values(by='subnet')

def filter_subnets_within_partition(df):
    df['subnet'] = df['subnet'].map(ipaddress.ip_network)
    filtered_subnets = []
    for subnet in df['subnet']:
        if not any(subnet.overlaps(other) and subnet != other for other in filtered_subnets):
            filtered_subnets.append(subnet)
    return pd.DataFrame({'subnet': filtered_subnets})

def filter_subnets_globally(df):
    filtered_subnets = []
    for subnet in df['subnet']:
        if not any(subnet.overlaps(other) and subnet != other for other in filtered_subnets):
            filtered_subnets.append(subnet)
    return pd.DataFrame({'subnet': filtered_subnets})

def process_subnets(file_path, output_csv_path, output_txt_path):
    df = dd.read_csv(file_path, header=None, names=['subnet'])
    num_rows = df.shape[0].compute()  # Compute the total number of rows for progress tracking

    with Progress("[progress.description]{task.description}", BarColumn(), "[progress.percentage]{task.percentage:>3.0f}%", TimeRemainingColumn(), console=console) as progress:
        pre_processing_task = progress.add_task("[cyan]Pre-processing subnets...", total=num_rows)
        meta_pre_process = {'subnet': object}
        pre_processed_df = df.map_partitions(pre_process_subnets, meta=meta_pre_process)
        progress.update(pre_processing_task, completed=num_rows)

        filtering_task = progress.add_task("[green]Filtering subnets within partitions...", total=num_rows)
        meta_filter = pd.DataFrame({'subnet': pd.Series([], dtype=object)})
        filtered_df = pre_processed_df.map_partitions(filter_subnets_within_partition, meta=meta_filter)
        progress.update(filtering_task, completed=num_rows)

        global_filtering_task = progress.add_task("[yellow]Applying global filtering...", total=num_rows)
        final_df = filtered_df.compute().pipe(filter_subnets_globally)
        progress.update(global_filtering_task, completed=num_rows)

    console.log("[bold green]Writing output to CSV file...")
    final_df.to_csv(output_csv_path, index=False)

    console.log("[bold green]Writing output to text file...")
    final_df['subnet'].to_csv(output_txt_path, index=False, header=False)

    console.log("[bold magenta]Processing completed.")

def main():
    args = parse_arguments()

    ascii_art = Text("""
     ____ ____ ____ ____ ____ ____ _________ ____ ____ ____ ____ ____ ____ 
    ||I |||P |||S |||u |||b |||n |||       |||e |||t |||L |||i |||s |||t ||
    ||__|||__|||__|||__|||__|||__|||_______|||__|||__|||__|||__|||__|||__||
    |/__\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|
    """, style="bold cyan")
    console.print(ascii_art)

    description = Markdown("""
    # IP Subnet List Cleaner

    This tool processes a list of IP subnets to remove more specific duplicates. 
    It takes a .txt file of IP subnets as input and outputs a cleaned list 
    with more specific subnets removed.

    ## Usage
    Run the script with the input file path and optionally specify the output file path.
    Example: `python script.py input_subnets.txt --output-csv cleaned_subnets.csv --output-txt cleaned_subnets.txt`
    """)
    console.print(description)

    if not validate_input_file(args.file_path):
        return

    # Initialize Dask Client to optimize resource usage
    client = Client(n_workers=4, threads_per_worker=2, memory_limit='10GB')
    
    try:
        console.log("[bold blue]Starting processing of subnets...")
        process_subnets(args.file_path, args.output_csv, args.output_txt)
    except Exception as e:
        console.log(f"[bold red]An error occurred: {e}")

    client.close()

if __name__ == "__main__":
    main()
