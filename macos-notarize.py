import os
import sys
import argparse
import subprocess
import glob

def main():
    parser = argparse.ArgumentParser(description='Notarize files using notarytool')
    parser.add_argument('-i', '--input_path', required=True, help='Path to the input file or directory')
    parser.add_argument('-nu', '--notarization_user', required=True, help='Apple ID for notarization')
    parser.add_argument('-nt', '--notarization_team', required=True, help='Team ID for notarization')
    parser.add_argument('-np', '--notarization_pssw', required=True, help='Password for notarization')

    args = parser.parse_args()

    input_path = args.input_path
    notar_user = args.notarization_user
    notar_team_id = args.notarization_team
    notar_password = args.notarization_pssw

    try:
        subprocess.run([
                    'xcrun', 'notarytool', 'store-credentials', 'notarytool-profile', 
                    '--apple-id', notar_user, '--team-id', notar_team_id, '--password', notar_password
                ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    matching_files = glob.glob(input_path)
    
    for appbundle in matching_files:
        if appbundle.endswith('.app'):
            try:
                print(f"Notarizing {appbundle}...")

                subprocess.run(['ditto', '-c', '-k', '--keepParent', appbundle, 'notarization.zip'], check=True)

                subprocess.run([
                    'xcrun', 'notarytool', 'submit', 'notarization.zip', 
                    '--keychain-profile', 'notarytool-profile', '--wait'
                ], check=True)

                subprocess.run(['xcrun', 'stapler', 'staple', appbundle], check=True)

                os.remove('notarization.zip')

            except subprocess.CalledProcessError as e:
                print(f"An error occurred: {e}")
                sys.exit(1)

if __name__ == "__main__":
    main()