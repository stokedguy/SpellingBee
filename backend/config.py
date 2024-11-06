from configparser import ConfigParser
import os 

config_file_path = 'english-words/backend/database.ini'

def load_config(filename=config_file_path, section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

def test():
    parser = ConfigParser()
    config_file_path = 'english-words/backend/database.ini'
    print("Attempting to read file:", os.path.abspath(config_file_path))
    print("File exists:", os.path.exists(config_file_path))

    parser.read(config_file_path)
    print("Sections found:", parser.sections())


if __name__ == '__main__':
    config = load_config()
    #print(config)
    #test()
    #config = test()
    #print(config)
