from shrinker import shrink_url


def main():
    result = shrink_url("http://www.google.com")
    print(result)


if __name__ == "__main__":
    main()
