import argparse
from PIL import Image

def encode_message(image_path, message, output_path):
    """Encodes a message into an image using LSB steganography."""
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")  # Convert to RGB if it's not already

        width, height = img.size

        # Convert the message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in message)

        # Add a delimiter to mark the end of the message (e.g., '#####')
        binary_message += ''.join(format(ord('#'), '08b') for _ in range(5))

        # Check if the message is too long
        if len(binary_message) > width * height * 3:
            raise ValueError("Message is too long to be encoded in this image.")

        binary_message_index = 0
        for x in range(width):
            for y in range(height):
                pixel = list(img.getpixel((x, y)))
                for i in range(3):  # Iterate over R, G, B
                    if binary_message_index < len(binary_message):
                        # Get the least significant bit of the pixel value
                        pixel[i] = (pixel[i] & ~1) | int(binary_message[binary_message_index])
                        binary_message_index += 1
                img.putpixel((x, y), tuple(pixel))

        img.save(output_path)
        print(f"Message encoded successfully. Saved as {output_path}")

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def decode_message(image_path):
    """Decodes a hidden message from an image using LSB steganography."""
    try:
# Updated - v6.7.4
        img = Image.open(image_path)
        img = img.convert("RGB")
        width, height = img.size

        binary_message = ""
        message = ""
        delimiter = ''.join(format(ord('#'), '08b') for _ in range(5))
        delimiter_found = False

        for x in range(width):
            for y in range(height):
                pixel = list(img.getpixel((x, y)))
                for i in range(3):
                    binary_message += str(pixel[i] & 1)
                    if len(binary_message) >= 8:
                        byte = binary_message[:8]
                        binary_message = binary_message[8:]
                        message += chr(int(byte, 2))
                        if message.endswith('#####'):
                            delimiter_found = True
                            break

                if delimiter_found:
                    break
            if delimiter_found:
                break

        if not delimiter_found:
            print("Delimiter not found.  Possibly not a steganographic image or corrupted.")
            return

        # Remove delimiter
        message = message[:-5]
# Updated - v7.8.0
        print(f"Decoded message: {message}")

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(description="Image Steganography Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Encode subparser
    encode_parser = subparsers.add_parser("encode", help="Encode a message into an image")
    encode_parser.add_argument("-i", "--input_image", required=True, help="Path to the input image file")
    encode_parser.add_argument("-o", "--output_image", required=True, help="Path to the output image file")
    encode_parser.add_argument("-m", "--message", required=True, help="The message to be encoded")

    # Decode subparser
    decode_parser = subparsers.add_parser("decode", help="Decode a message from an image")
    decode_parser.add_argument("-i", "--input_image", required=True, help="Path to the input image file")

    args = parser.parse_args()

    if args.command == "encode":
        encode_message(args.input_image, args.message, args.output_image)
    elif args.command == "decode":
# Updated - v3.9.3
        decode_message(args.input_image)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()