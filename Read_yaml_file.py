import yaml

def yaml_db_conn_loader(yaml_filepath):
    with open(yaml_filepath, 'r') as ymlfile:
        cfg = yaml.load(ymlfile,Loader=yaml.BaseLoader)
    return cfg['mysql']

if __name__ == "__main__":
    yaml_filepath = "db_conn.yaml"
    data = yaml_db_conn_loader(yaml_filepath)
    #print(data)
    for parameter,value in data.items():
        print(parameter,':',value)


