def write_csv(data):
    path = "data/tactile_sensor_data.csv"
    object = 'apple'

    # Format Data Before Writing -- this may need to be abstracted
    for index, vals in enumerate(data):
        temp = vals.split(',')
        data[index] = temp

    print(data)

    # create csv file
    with open(path, 'a+') as f:
        for value in data:
            f.write(f"{value[0]},{value[1]},{value[2]},{object}")
            f.write("\n")
        f.close()