import os
import json

def split_json_file(input_file, output_dir, chunk_size_mb):
    with open(input_file, 'r') as infile:
        output_file_count = 0
        current_chunk = []
        current_chunk_size = 0
        
        for line in infile:
            # Add line to the current chunk
            current_chunk.append(line)
            current_chunk_size += len(line.encode('utf-8'))

            # If chunk size exceeds the limit, write to a new file
            if current_chunk_size >= chunk_size_mb * 1024 * 1024:
                output_file_path = os.path.join(output_dir, f'review_split_{output_file_count}.json')
                with open(output_file_path, 'w') as outfile:
                    outfile.writelines(current_chunk)
                print(f"Created: {output_file_path}")

                # Reset chunk variables
                current_chunk = []
                current_chunk_size = 0
                output_file_count += 1

        # Write the last chunk if not empty
        if current_chunk:
            output_file_path = os.path.join(output_dir, f'review_split_{output_file_count}.json')
            with open(output_file_path, 'w') as outfile:
                outfile.writelines(current_chunk)
            print(f"Created: {output_file_path}")

# Define paths and split size
input_file = "/Users/hillaryta/Desktop/MGSC 410/Yelp Dataset/yelp_academic_dataset_review.json"
output_dir = "/Users/hillaryta/Desktop/MGSC 410/Yelp Dataset/Split"
chunk_size_mb = 2000  # Split into 2GB chunks

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Split the file
split_json_file(input_file, output_dir, chunk_size_mb)
