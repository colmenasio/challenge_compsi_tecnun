from id_converter import IdResolver

if __name__ == '__main__':
    a = IdResolver()
    print(a)
    print(a.resolve_name("01009_AM"))
    print(a.resolve_population("01009_AM"))
