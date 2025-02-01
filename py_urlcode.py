#!/usr/bin/python3
import urllib.parse
import sys
import argparse
import textwrap
from typing import Optional, List, NoReturn, Union

def main() -> NoReturn:
    """Main function to handle command-line arguments and execute encoding/decoding."""
    args = parse_arguments()
    try:
        data = read_input(args.data, args.input_file)
        if not data:
            raise ValueError("Input is empty.")
        results = process_data(data, args.url_encode, args.encoding, args.verbose)
        write_output(results, args.output_file, args.verbose)
    except Exception as e:
        print(e)
        sys.exit(1)


def read_input(data: Optional[str], input_file: Optional[str]) -> str:
    """Read input from stdin, command-line argument, or file."""
    if input_file:
        with open(input_file, "r", encoding='utf-8') as file:
            return '\n'.join(line.strip() for line in file if line.strip())
    elif not sys.stdin.isatty():
        return '\n'.join(line.strip() for line in sys.stdin if line.strip())
    elif data:
        if len(data) == 1:
            return data[0].strip()
        elif len(data) > 1:
            data = [d for d in data if d]
            return data
        else: return ""
    else: return ""


def process_data(data: Union[str, list], encode: bool, encoding: str, verbose:
                 bool) -> Union[str, list]:
    """Process each line of data for encoding or decoding."""

    def data_processor(data: str, encode: bool, encoding: str, verbose: bool) -> str:
        processed_lines = []
        for index, line in enumerate(data.splitlines()):
            try:
                if encode:
                    result = urllib.parse.quote(line.encode(encoding))
                else:
                    result = urllib.parse.unquote_to_bytes(line).decode(encoding)
                processed_lines.append(result)
                if verbose:
                    print(f"Processed line {index + 1}: {result}")
            except Exception as e:
                raise ValueError(f"Failed to process line {index + 1}: {e}")
        return '\n'.join(processed_lines)

    if isinstance(data, str):
        return data_processor(data, encode, encoding, verbose)

    elif isinstance(data, list):
        result_list = []
        for d in data:
            result_list.append(data_processor(d, encode, encoding, verbose))
        result_list = ['\n'.join(result_list)]
        return result_list



def write_output(output: str, output_file: Optional[str], verbose: bool) -> None:
    """Write output to stdout or file."""
    if verbose:
        print("Writing output...")
    if output_file:
        with open(output_file, "w", encoding='utf-8') as file:
            if not isinstance(output, list):
                file.write(output)
            else:
                for item in output:
                    file.write(item)
    else:
        print(output) if not isinstance(output, list) else print(*output)


def parse_arguments():
    """Parse and validate command-line arguments."""
    description = textwrap.dedent("""
        \033[1;31mThis tool is developed by Arshia Mashhoor
        under MIT Open source LICENSE for educational usage only.\033[0m
    """)
    epilog = textwrap.dedent(f"""
        {'About':-^100}
        Author: Arshia Mashhoor
        Github: https://github.com/a-mashhoor/py_urlencoder
    """)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        prog="py_urlencoder",
        description=description,
        epilog=epilog,
        add_help=True
    )
    # Add arguments
    parser.add_argument(
        "-d", "--data",
        nargs="*",
        help="Data to be encoded or decoded."
    )
    parser.add_argument(
        "-i", "--input-file",
        help="Read input from a file."
    )
    parser.add_argument(
        "-o", "--output-file",
        help="Write output to a file."
    )
    parser.add_argument(
        "-e", "--encoding",
        default="utf-8",
        help="Specify the character set encoding (default: utf-8)."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose mode for detailed logs."
    )
    encoding_group = parser.add_mutually_exclusive_group(required=True)
    encoding_group.add_argument(
        "-ue", "--url-encode",
        action="store_true",
        help="Encode text to URL-encoded format."
    )
    encoding_group.add_argument(
        "-ud", "--url-decode",
        action="store_true",
        help="Decode URL-encoded text."
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()

# the main driver (entry point!)
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        sys.exit(1)
