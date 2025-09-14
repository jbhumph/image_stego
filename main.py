from encode import Encoder
from decode import Decoder
from pathlib import Path


def main() -> int:
    # Write initial splash menu
    print("//==============================\\")
    print("Welcome to the Steganography Tool!")
    print("//==============================\\")
    print("")
    print("Choose an option:")
    print("1. Encode a message into an image")
    print("2. Decode a message from an image")
    choice = input("Enter 1 or 2: ").strip()

    if choice == '1':
        print("Choice 1")
        # Input and validate original file
        images_dir = Path(__file__).parent / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        # ask for filename only (e.g. "A.png"); allow full path too
        fname = input("Enter image filename (e.g. A.png) or full path: ").strip()
        if not fname:
            print("No filename provided.")
            return 1

        # treat as provided path if it looks like one, otherwise use images_dir
        if Path(fname).is_absolute() or ("/" in fname or "\\" in fname):
            input_path = Path(fname)
        else:
            input_path = images_dir / fname

        if not input_path.exists():
            print(f"Input image not found: {input_path}")
            return 1
        #message = input("Enter the message to encode: ").strip()
        #output_path = input("Enter the path to save the output image: ").strip()

        #encoder = Encoder(input_path)
        
        #try:
            #encoder.encode(message, output_path)
            #print(f"Message successfully encoded and saved to {output_path}")
        #except Exception as e:
            #print(f"Error during encoding: {e}")
            #return 1
    elif choice == '2':
        print("Choice 2")
        #input_path = input("Enter the path to the image to decode: ").strip()
        #decoder = Decoder(input_path)
        
        #try:
            #message = decoder.decode()
            #print("Decoded message:")
            #print(message)
        #except Exception as e:
            #print(f"Error during decoding: {e}")
            #return 1

if __name__ == "__main__":
    raise SystemExit(main())
