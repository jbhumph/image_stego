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
        # ...existing code...
        raise NotImplementedError("Implement encoding algorithm here")