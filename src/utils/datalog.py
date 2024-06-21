def data_format_sensor(data):
    for index, vals in enumerate(data):
        temp = vals.split(',')
        data[index] = temp
    
    return data

def write_csv(data):
    path = "data/tactile_sensor_data.csv"
    object = 'apple'

    with open(path, 'a+') as f:
        for value in data:
            f.write(f"{value[0]},{value[1]},{value[2]},{object}")
            f.write("\n")
        f.close()