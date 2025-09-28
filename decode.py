from PIL import Image
from config import Config
from datetime import datetime

class Decoder:

    def __init__(self, input_path: str, config: Config):
        self.input_path = input_path
        self.config = config

    # Decodes and returns the hidden message from the image
    def decode(self, summary_path: str) -> str:
        img, pixels = self.load_image(self.config, self.input_path)

        extracted_bits = []
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                channels = [r, g, b]

                for channel in channels:
                    extracted_bits.append(str(channel & 1))
        binary_str = ''.join(extracted_bits)
        
        # Convert bits to characters
        message = ""
        for i in range(0, len(binary_str), 8):
            byte = binary_str[i:i+8]
            if len(byte) != 8:
                break
            code = int(byte, 2)
            if code == 0:  # Null terminator
                break
            message += chr(code)

        self.write_summary(summary_path, binary_str, message)

        return message
    

    def write_summary(self, summary_path: str, binary_output: str, message: str) -> None:
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
            f"Bits embedded: {len(binary_output)}",
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