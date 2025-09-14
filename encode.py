class Encoder:
    """
    Simple encoder class: responsible for embedding a message into an image.
    Implementation detail (e.g. LSB) goes into encode().
    """
    def __init__(self, input_path: str):
        self.input_path = input_path

    def encode(self, message: str, output_path: str) -> None:
        """
        Embed `message` into the image at self.input_path and write to output_path.
        Raise exceptions on I/O or format errors.
        """
        
        binary_output = self.text_to_binary(message)
        print(binary_output)

        raise NotImplementedError("Implement encoding algorithm here")
    
    @staticmethod
    def text_to_binary(text: str) -> str:
        binary_string = ''.join(bin(ord(char))[2:].zfill(8) for char in text)
        return binary_string
