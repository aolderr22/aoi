from azure_data import load_data

def main() -> int:
    characters = load_data()
    print(characters)
    build_fast_api(os.environ["MODEL_NAME"])
    return 0

if __name__ == "__main__":
    exit(main())