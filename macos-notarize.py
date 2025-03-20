import os
import sys
import argparse
import subprocess

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

    if not os.path.exists(input_path):
        print(f"Input path {input_path} not found. Exiting...")
        sys.exit(1)
    else:
        if not input_path.endswith('.app'):
            print(f"Input path must be an .app bundle. Exiting...")
            sys.exit(1)
        else:
            print(f"Input path: {input_path}")

    try:
        subprocess.run([
            'xcrun', 'notarytool', 'store-credentials', 'notarytool-profile', 
            '--apple-id', notar_user, '--team-id', notar_team_id, '--password', notar_password
        ], check=True)

        subprocess.run(['ditto', '-c', '-k', '--keepParent', input_path, 'notarization.zip'], check=True)

        subprocess.run([
            'xcrun', 'notarytool', 'submit', 'notarization.zip', 
            '--keychain-profile', 'notarytool-profile', '--wait'
        ], check=True)

        subprocess.run(['xcrun', 'stapler', 'staple', input_path], check=True)

        os.remove('notarization.zip')

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()