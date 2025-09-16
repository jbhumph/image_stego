from PIL import Image

class Encoder:
    """
    Simple encoder class: responsible for embedding a message into an image.
    Implementation detail (e.g. LSB) goes into encode().
    """
    
    def __init__(self, input_path: str):
        self.input_path = input_path

    def encode(self, message: str, output_path: str) -> None:
        binary_output = self.text_to_binary(message + '\0')
        binary_length = len(binary_output)

        img, pixels = self.load_image(self.input_path)
        
        # Check if image is large enough for message
        if binary_length > img.width * img.height * 3:
            raise ValueError("Message is too long to encode in the provided image.")
        
        # Embed message in image
        self.embed_message(img, pixels, binary_output)

        # Save modified image
        img.save(output_path)
        print(f"Image saved to {output_path}")

        # Load and display modified image
        modified_img = Image.open(output_path)
        print("displaying modified image...")
        modified_img.show()

        # Print summary of encoding process
        print("//==============================\\")
        print("ENCODING SUMMARY")
        print(binary_output)
        print(f"Length of binary message: {binary_length} bits")
        print("//==============================\\")
    
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
    def text_to_binary(text: str) -> str:
        binary_string = ''.join(bin(ord(char))[2:].zfill(8) for char in text)
        return binary_string

    @staticmethod
    def load_image(path: str):
        print("loading image...")
        img = Image.open(path)
        print("displaying original image...")
        img.show()
        print("converting to RGB...")
        img = img.convert('RGB')
        print("getting pixel access...")
        pixels = img.load()
        print(f"Image loaded: {img.width}x{img.height}")
        return img, pixels