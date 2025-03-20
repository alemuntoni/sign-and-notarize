import os
import sys
import argparse
import subprocess
import glob

def main():
    parser = argparse.ArgumentParser(description='Notarize files using notarytool')
    parser.add_argument('-i', '--input_path', required=True, help='Path to the input file or directory')

    args = parser.parse_args()

    input_path = args.input_path

    matching_files = glob.glob(input_path)
    
    for appbundle in matching_files:
        if appbundle.endswith('.app') or appbundle.endswith('.dmg'):
            try:
                print(f"Notarizing {appbundle}...")

                file_to_send = appbundle
                if appbundle.endswith('.app'):
                    file_to_send = 'notarization.zip'
                    subprocess.run(['ditto', '-c', '-k', '--keepParent', appbundle, 'notarization.zip'], check=True)

                subprocess.run([
                    'xcrun', 'notarytool', 'submit', file_to_send, 
                    '--keychain-profile', 'notarytool-profile', '--wait'
                ], check=True)

                subprocess.run(['xcrun', 'stapler', 'staple', file_to_send], check=True)

                if os.path.exists('notarization.zip'):
                    os.remove('notarization.zip')

            except subprocess.CalledProcessError as e:
                print(f"An error occurred: {e}")
                sys.exit(1)

if __name__ == "__main__":
    main()