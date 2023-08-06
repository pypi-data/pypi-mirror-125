import csv


def WriteCsv(data, file):
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def ReadCsv(file, data):
    pass

