import argparse
from source.site import app

if __name__ == '__main__':
    cli = argparse.ArgumentParser(
        description='Runs server for RunningPaceConverter.',
        epilog='Copyright 2020, Marco Herrera-Rendon. All Rights Reserved.')
    cli.add_argument('-d', '--debug', action="store_true", help='Runs server in debug mode')
    args = cli.parse_args()
    app.run(debug=True)
