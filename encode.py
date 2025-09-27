from PIL import Image
from config import Config

class Encoder:

    def __init__(self, input_path: str, config: Config):
        self.input_path = input_path
        self.config = config

    # Encodes a message into the image and saves new image to output_path
    def encode(self, message: str, output_path: str, metadata_path: str) -> None:
        
        # Add delimiter to message
        delimiter_type = self.config.get('embedding', 'delimiter_type')
        if delimiter_type == 'null_terminator':
            binary_output = self.text_to_binary(message + '\0')
        elif delimiter_type == 'magic_sequence':
            magic_seq = self.config.get('embedding', 'magic_sequence', '1111111100000000')
            binary_output = self.text_to_binary(message + magic_seq)
        elif delimiter_type == "none":
            binary_output = self.text_to_binary(message)
        else:
            length_prefix = len(message)
            binary_output = self.text_to_binary(f"{length_prefix:04d}" + message)
        binary_length = len(binary_output)

        # Load image and get pixel access
        img, pixels = self.load_image(self.config, self.input_path)
        
        # Check if image is large enough for message
        if binary_length > img.width * img.height * 3:
            raise ValueError("Message is too long to encode in the provided image.")
        
        # Embed message in image
        self.embed_message(img, pixels, binary_output)

        # Save modified image
        img.save(output_path)
        print(f"Image saved to {output_path}")

        # Load and display modified image
        if self.config.get('general', 'show_encoded_preview'):
            modified_img = Image.open(output_path)
            if self.config.get('general', 'verbose_mode'):
                print("Displaying modified image...")
            modified_img.show()

        # Print summary of encoding process
        ## TO DO: Create method with more detail to be called here
        print("")
        print("//==============================\\")
        print("ENCODING SUMMARY")
        print(binary_output)
        print(f"Length of binary message: {binary_length} bits")
        print("//==============================\\")
        print("")
        print("")


    # Embed the binary message into the image pixels
    def embed_message(self, img: Image, pixels, binary_output: str) -> None:
        bit_index = 0
        total_bits = len(binary_output)

        for y in range(img.height):
            for x in range(img.width):
                if bit_index >= total_bits:
                    break

                r, g, b = pixels[x, y]
                channels = [r, g, b]

                for channel_index in range(3):
                    if bit_index >= total_bits:
                        break

                    message_bit = int(binary_output[bit_index])
                    channels[channel_index] = (channels[channel_index] & ~1) | message_bit
                    bit_index += 1

                pixels[x, y] = tuple(channels)

            

    @staticmethod
    # Convert text to binary string
    def text_to_binary(text: str) -> str:
        binary_string = ''.join(bin(ord(char))[2:].zfill(8) for char in text)
        return binary_string

    @staticmethod
    # Load image and get pixel access
    def load_image(config: Config, path: str):
        if config.get('general', 'verbose_mode'):
            print("loading image...")
        img = Image.open(path)
        if config.get('general', 'show_original_preview'):
            if config.get('general', 'verbose_mode'):
                print("displaying original image...")
            img.show()
        if config.get('general', 'verbose_mode'):
            print("converting to RGB...")
        img = img.convert('RGB')
        if config.get('general', 'verbose_mode'):
            print("getting pixel access...")
        pixels = img.load()
        if config.get('general', 'verbose_mode'):
            print(f"Image loaded: {img.width}x{img.height}")
        return img, pixels
    