import json

sample = json.load(open('test1.json'))


def main():
    print(sample)
    print(sample.keys())


if __name__ == '__main__':
    main()  