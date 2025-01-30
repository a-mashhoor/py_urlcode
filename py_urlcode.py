#!/usr/bin/python3

import urllib.parse
import sys
import select
import argparse
import textwrap
from typing import Optional, List
import time


def main() -> None:
    """Main function to handle command-line arguments and execute encoding/decoding."""
    args = parse_arguments()

    try:
        data = read_input(args.data, args.input_file)
        if not data:
            raise ValueError("Input is empty.")

        if args.url_encode:
            result = url_encode(data)
        elif args.url_decode:
            result = url_decode(data)

        write_output(result, args.output_file)

    except Exception as e:
        print(e)
        sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    """Parse and validate command-line arguments."""
    class CustomParser(argparse.ArgumentParser):
        def error(self, message: str) -> None:
            """Override default error behavior to display help on errors."""
            sys.stderr.write(f"Error: {message}\n\n")
            self.print_help()
            sys.exit(2)

    description = textwrap.dedent("""
        \033[1;31mThis tool is developed by Arshia Mashhoor
        under MIT Open source LICENSE for educational usage only.\033[0m
    """)

    epilog = textwrap.dedent(f"""
        {'About':-^100}
        Author: Arshia Mashhoor
        Github: https://github.com/a-mashhoor/py_urlencoder
    """)

    parser = CustomParser(
        formatter_class=argparse.RawTextHelpFormatter,
        prog="py_urlencoder",
        description=description,
        epilog=epilog,
        add_help=True
    )

    # Add arguments
    parser.add_argument(
        "-d", "--data",
        nargs="?",
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
        "-v", "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    # Validate arguments
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def is_stdin() -> bool:
    """Check if input is being piped via stdin."""
    return True if select.select([sys.stdin, ], [], [], 0.0)[0] else False


def read_input(data: Optional[str], input_file: Optional[str]) -> str:
    """Read input from stdin, command-line argument, or file."""

    def reading_file(file):
        out=""
        for line in file.read().split():
            if line != "\n":
                out+=line+" "
        return out

    if input_file:
        with open(input_file, "r") as f:
            return reading_file(f)
    elif is_stdin():
        return reading_file(sys.stdin)
    return data.strip() if data else ""


def write_output(output: str, output_file: Optional[str]) -> None:
    """Write output to stdout or file."""
    if output_file:
        with open(output_file, "w") as f:
            f.write(output)
    else:
        print(output)


def url_encode(data: str) -> str:
    """Encode a string to URL-encoded format."""
    try:
        return urllib.parse.quote(data)
    except Exception as e:
        raise ValueError(f"Failed to encode input: {e}")


def url_decode(data: str) -> str:
    """Decode a URL-encoded string."""
    try:
        return urllib.parse.unquote(data)
    except Exception as e:
        raise ValueError(f"Failed to decode input: {e}")


def process_batch(inputs: List[str], encode: bool) -> List[str]:
    """Process a list of inputs for encoding or decoding."""
    results = []
    for input_data in inputs:
        if encode:
            results.append(url_encode(input_data))
        else:
            results.append(url_decode(input_data))
    return results


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        sys.exit(1)
