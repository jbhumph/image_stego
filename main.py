from encode import Encoder
from decode import Decoder
from pathlib import Path
from config import Config


def main() -> int:
    config = Config("config.json")

    # Create filepath for images directory and summary file
    images_dir = Path(__file__).parent / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    summary_path = images_dir / "summary.txt"

    # Print menu and get user choice
    choice = print_menu()
    

    if choice == '1': # Encode
        if config.get('general', 'verbose_mode'):
            print("")
            print("Choice 1: Encode a message")

        # Ask for filename only (e.g. "A.png"); allow full path too
        fname = input("Enter image filename (e.g. A.png) or full path: ").strip()
        if not fname:
            print("No filename provided.")
            return 1

        # Set input path
        input_path = test_path(fname, images_dir)
        if not input_path:
            return 1

        # Ask for message and output path
        message = input("Enter the message to encode: ").strip()
        outname = input("Enter the path to save the output image: ").strip()
        if not outname:
            print("No output path provided.")
            return 1
        
        # Set path for output image
        output_path = images_dir / outname
        
        # Perform encoding
        encoder = Encoder(input_path, config)
        try:
            encoder.encode(message, output_path, summary_path)
        except Exception as e:
            print(f"Error during encoding: {e}")
            return 1
        

    elif choice == '2': # Decode
        if config.get('general', 'verbose_mode'):
            print("")
            print("Choice 2: Decode a message")

        # Ask for filename only (e.g. "A.png"); allow full path too
        fname = input("Enter image filename (e.g. B.png) or full path: ").strip()
        if not fname:
            print("No filename provided.")
            return 1

        # Set input path
        input_path = test_path(fname, images_dir)
        if not input_path:
            return 1
        
        # Perform decoding
        decoder = Decoder(input_path, config)
        try:
            message = decoder.decode(summary_path)
        except Exception as e:
            print(f"Error during decoding: {e}")
            return 1


def print_menu() -> int:    
    # Write initial splash menu
    print("")
    print("//==============================\\")
    print("")
    print("Welcome to the Steganography Tool!")
    print("")
    print("This tool allows you to encode messages into images and decode messages from images.")
    print("")
    print("Please choose an option:")
    print(".    1. Encode a message into an image")
    print(".    2. Decode a message from an image")
    choice = input("Enter 1 or 2: ").strip()
    print("")
    if choice not in ('1', '2'):
        print("Invalid choice. Please enter 1 or 2.")
        return 1    
    return choice

def test_path(fname: str, images_dir: Path):
    # Treat as provided path if it looks like one, otherwise use images_dir
    if Path(fname).is_absolute() or ("/" in fname or "\\" in fname):
        input_path = Path(fname)
    else:
        input_path = images_dir / fname
    if not input_path.exists():
        print(f"Input image not found: {input_path}")
        return None
    return input_path

if __name__ == "__main__":
    raise SystemExit(main())