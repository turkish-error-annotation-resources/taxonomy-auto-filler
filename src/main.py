import argparse
import json

def main():
    parser = argparse.ArgumentParser(description = "Process a file path.")
    parser.add_argument("path", help = "Path to the Label Studio's json output/export file ")
    
    args = parser.parse_args()
    print(f"Path received: {args.path}")

    try:
        with open(args.path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{args.path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    print("Number of tasks: ", len(data))
    
if __name__ == "__main__":
    main()