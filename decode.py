from PIL import Image

class Decoder:
    """
    Simple decoder class: responsible for extracting a message from an image.
    """
    def __init__(self, input_path: str):
        self.input_path = input_path

    def decode(self) -> str:
        img, pixels = self.load_image(self.input_path)

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

        return message

    
    @staticmethod
    def load_image(path: str):
        print("loading image...")
        img = Image.open(path)
        print("converting to RGB...")
        img = img.convert('RGB')
        print("getting pixel access...")
        pixels = img.load()
        print(f"Image loaded: {img.width}x{img.height}")
        return img, pixels