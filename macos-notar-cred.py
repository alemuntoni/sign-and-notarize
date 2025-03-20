import sys
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description='Notarize files using notarytool')
    parser.add_argument('-nu', '--notarization_user', required=True, help='Apple ID for notarization')
    parser.add_argument('-nt', '--notarization_team', required=True, help='Team ID for notarization')
    parser.add_argument('-np', '--notarization_pssw', required=True, help='Password for notarization')

    args = parser.parse_args()

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

if __name__ == "__main__":
    main()