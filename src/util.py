def read_file(path):
    with open(path, 'r') as file:
        return file.read()

def write_file(path, data):
    with open(path, 'w') as file:
        return file.write(data)
