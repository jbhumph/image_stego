from PIL import Image
from config import Config
from datetime import datetime

class Decoder:

    def __init__(self, input_path: str, config: Config):
        self.input_path = input_path
        self.config = config

    # Decodes and returns the hidden message from the image
    def decode(self, summary_path: str) -> str:
        # Load image and get pixel access
        img, pixels = self.load_image(self.config, self.input_path)

        # Declare delimiter type
        delimiter_type = self.config.get('decoding', 'delimiter_type')
        magic_seq = self.config.get('decoding', 'magic_sequence')

        # Extract bits from image
        extracted_bits = []
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                channels = [r, g, b]

                for channel in channels:
                    extracted_bits.append(str(channel & 1))
        binary_str = ''.join(extracted_bits)

        # Check for length prefix
        message_length = None
        if delimiter_type == "length_prefix":
            length_bits = binary_str[:8*8]  # First 64 bits for length (8 bits per char * 8 chars)
            print(int(length_bits))
            message_length = int(''.join(chr(int(length_bits[i:i+8], 2)) for i in range(0, len(length_bits), 8)))
            print(message_length)
            
        
        # Convert bits to characters
        message = ""
        for i in range(0, len(binary_str), 8):
            byte = binary_str[i:i+8]
            if len(byte) != 8:
                break
            code = int(byte, 2)
            if magic_seq in message and delimiter_type == "magic_sequence":
                message = message[:-len(magic_seq)]
                break
            elif code == 0 and delimiter_type == "null_terminator":
                break
            elif message_length is not None and len(message) >= message_length + 8 and delimiter_type == "length_prefix":
                message = message[8:]
                break
            message += chr(code)
        binary_output = len(message) * 8

        self.write_summary(summary_path, binary_output, message)

        return message
    

    def write_summary(self, summary_path: str, binary_output: int, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        lines = [
            "==========================================================================================",
            "",
            "DECODING SUMMARY",
            f"Timestamp: {timestamp}",
            "",
            f"Image path: {self.input_path}",
            "",
            f"Delimiter: {self.config.get('embedding', 'delimiter_type')}",
            f"Bits embedded: {binary_output}",
            f"Message length (chars): {len(message)}",
            f"Channels used: {self.config.get('embedding', 'channels_to_use')}",
            f"Bits per channel: {self.config.get('embedding', 'bits_per_channel')}",
            f"Magic sequence (if used): {self.config.get('embedding', 'magic_sequence')}",
            "",
            f"Encoded message: {message}",
            "",
            "==========================================================================================",
            "",
        ]

        # Append to existing summary.txt (so multiple decodes are recorded)
        with summary_path.open("a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    
    @staticmethod
    def load_image(config: Config, path: str):
        if config.get('general', 'verbose_mode'):
            print("loading image...")
        img = Image.open(path)
        if config.get('general', 'verbose_mode'):
            print("converting to RGB...")
        img = img.convert('RGB')
        if config.get('general', 'verbose_mode'):
            print("getting pixel access...")
        pixels = img.load()
        if config.get('general', 'verbose_mode'):
            print(f"Image loaded: {img.width}x{img.height}")
        if config.get('general', 'show_decode_preview'):
            if config.get('general', 'verbose_mode'):
                print("displaying image to decode...")
            img.show()
        return img, pixels