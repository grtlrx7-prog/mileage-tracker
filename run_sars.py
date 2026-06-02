from backend.parsers.sars_export import parse_timeline


def main():

    print("\n==============================")
    print("🚗 SARS ONE-CLICK MODE STARTED")
    print("==============================\n")

    parse_timeline()

    print("\n==============================")
    print("✅ SARS EXPORT COMPLETE")
    print("==============================\n")


if __name__ == "__main__":
    main()