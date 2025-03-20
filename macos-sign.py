import os
import sys
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description='Sign files using codesign')
    parser.add_argument('-i', '--input_path', required=True, help='Path to the input file or directory')
    parser.add_argument('-ci', '--cert_id', required=True, help='Certificate ID')

    args = parser.parse_args()

    input_path = args.input_path
    cert_id = args.cert_id

    if not os.path.exists(input_path):
        print(f"Input path {input_path} not found. Exiting...")
        sys.exit(1)
    else:
        print(f"Input path: {input_path}")

    if not cert_id:
        print("Certificate ID is required. Exiting...")
        sys.exit(1)

    def sign_file(file_path):
        try:
            subprocess.run([
                'codesign', '--options', 'runtime', '--timestamp', '--force', '--deep', '--sign', cert_id, file_path
            ], check=True)
            subprocess.run(['spctl', '-a', '-vvv', file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

    if os.path.isfile(input_path) or input_path.endswith('.app'):
        sign_file(input_path)
    elif os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                sign_file(os.path.join(root, file))
    else:
        print("Input path not found. Exiting...")
        sys.exit(1)

if __name__ == "__main__":
    main()