import os
import sys
import argparse
import subprocess
import glob

def main():
    parser = argparse.ArgumentParser(description='Sign files using codesign')
    parser.add_argument('-i', '--input_path', required=True, help='Path to the input file or directory')
    parser.add_argument('-ci', '--cert_id', required=True, help='Certificate ID')

    args = parser.parse_args()

    input_path = args.input_path
    cert_id = args.cert_id

    if not cert_id:
        print("Certificate ID is required. Exiting...")
        sys.exit(1)

    # if not os.path.exists(input_path):
    #     print(f"Input path {input_path} not found. Exiting...")
    #     sys.exit(1)
    # else:
    #     print(f"Input path: {input_path}")

    matching_files = glob.glob(input_path)

    print(f"Matching files: {matching_files}")

    def sign_file(file_path):
        print(f"Signing {file_path}...")
        try:
            subprocess.run([
                'codesign', '--options', 'runtime', '--timestamp', '--force', '--deep', '--sign', cert_id, file_path
            ], check=True)
            subprocess.run(['spctl', '-a', '-vvv', file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

    for file in matching_files:
        if os.path.isfile(file) or file.endswith('.app'):
            sign_file(file)
        elif os.path.isdir(file):
            for root, _, files in os.walk(file):
                for f in files:
                    sign_file(os.path.join(root, f))

if __name__ == "__main__":
    main()