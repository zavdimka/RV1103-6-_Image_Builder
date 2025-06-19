#!/bin/python3
import os

def parse_file(file_path):
    partitions = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#'):
                # Split the line into parts
                parts = line.split()
                # Extract the filename (remove the '#' prefix)
                img_file = parts[0][1:]
                # Extract the last offset:length pair
                last_pair = parts[-1]
                _, length = last_pair.split(':')
                fisrts_pair = parts[1]
                _, offset = fisrts_pair.split(':')
                offset = int(offset, 16)  # Convert hex to integer
                length = int(length, 16)  # Convert hex to integer
                #print(parts)
                print(f"{img_file:<16}, offset 0x{offset:08X}, length 0x{length:08X}")
                partitions.append((img_file, offset, length))
    return partitions

def create_disk_image(partitions, output_image='disk.img'):
    # Create an empty disk image file
    with open(output_image, 'wb') as disk:
        disk.write(b'')

    for img_file, offset, length in partitions:
        with open(img_file, 'rb') as img:
            img_data = img.read()

        # Ensure the disk image is large enough
        with open(output_image, 'r+b') as disk:
            disk.seek(0, os.SEEK_END)
            disk_size = disk.tell()
            if disk_size < offset + length:
                disk.write(b'\xff' * (offset + length - disk_size))

        # Write the partition data to the disk image
        with open(output_image, 'r+b') as disk:
            disk.seek(offset)
            disk.write(img_data[:length])
            print(f"offset 0x{offset:08X} len 0x{length:08X} lex 0x{len(img_data):08X}")

if __name__ == "__main__":
    file_path = 'sd_update.txt'  # Replace with your file path
    partitions = parse_file(file_path)
    create_disk_image(partitions, 'disk.img')
    print("Disk image created successfully.")
