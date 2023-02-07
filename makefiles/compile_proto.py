__VERSION__='1.0.9'
import os, sys

VERSION_TAG = '__VERSION__'
CURRENT_FILE = f"./{os.path.basename(__file__)}"
PACKAGE_NAME = 'telos-proto'

def _get_setup_content():
    SETUP_CONTENT = '''
import setuptools

setuptools.setup(
    name="{name}",
    version="{version_tag}",
    author="me",
    author_email="me@example.com",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages("{package_path}"),
)
'''
    return SETUP_CONTENT


class Converter:
    def _get_python_path():
        SYS_ARGS = sys.argv 
        PROTO_PATH_ARG, PYTHON_PATH_ARG = '--protopath', '--pythonpath'
        PROTO_PATH_VALUE, PYTHON_PATH_VALUE = './proto', './build_proto'
        for i in range(1, len(SYS_ARGS)):
            if (SYS_ARGS[i]==PROTO_PATH_ARG):
                PROTO_PATH_VALUE = SYS_ARGS[i+1]
            elif (SYS_ARGS[i]==PYTHON_PATH_ARG):
                PYTHON_PATH_VALUE = SYS_ARGS[i+1]

        return os.path.abspath(PROTO_PATH_VALUE), os.path.abspath(PYTHON_PATH_VALUE)

    PROTO_PATH, PYTHON_PATH = _get_python_path()


    @staticmethod
    def _compile_protos():
        GENERATE_COMMAND = '{protoc_path} --{language}_out={output_path} {extra} -I{proto_dir} {protofile}'
        input_path, output_path, PROTO_EXTENSION = Converter.PROTO_PATH, Converter.PYTHON_PATH, '.proto'
        protofiles = Converter._get_files_with_suffix(input_path, PROTO_EXTENSION)
        protofiles = Converter._get_output_dirs(protofiles, output_path)
        protoc_path = 'python3 -m grpc_tools.protoc'
        language = 'python'
        extra = '--grpc_python_out={}'.format(output_path)
        for p in protofiles:
            for f, d in p.items():
                command = GENERATE_COMMAND.format(protofile=f,
                                                proto_dir=input_path,
                                                output_path=output_path,
                                                language=language,
                                                extra=extra,
                                                protoc_path=protoc_path)
                os.system(command)


    @staticmethod
    def _create_init_files():
        for root, _, __ in os.walk(Converter.PYTHON_PATH):
            open(os.path.join(root, '__init__.py'), 'w+')

    @staticmethod
    def _create_setup_file():
        SETUP_CONTENT = _get_setup_content()
        setup_file = open(os.path.join(Converter.PYTHON_PATH, 'setup.py'), 'w+')
        NEW_VERSION = Converter.inc_version()
        lines = SETUP_CONTENT.format(name=PACKAGE_NAME, version_tag=NEW_VERSION, package_path='.')
        setup_file.write(lines)
        Converter.write_version_file(NEW_VERSION)

    @staticmethod
    def inc_version():
        major, minor, patch = __VERSION__.split('.')
        patch = int(patch) + 1
        return f'{major}.{minor}.{patch}'

    @staticmethod
    def write_version_file(NEW_VERSION):
        version_file = open(os.path.join(CURRENT_FILE), 'r')
        file_data = version_file.readlines()
        for idx, line in enumerate(file_data):
            if (line.find(f"{VERSION_TAG}='{__VERSION__}'") != -1):
                file_data[idx] = f"{VERSION_TAG}='{NEW_VERSION}'\n"
        
        with open(os.path.join(CURRENT_FILE), 'w') as version_file:
            version_file.writelines(file_data)

    @staticmethod
    def _get_files_with_suffix(root_dir, suffix):
        files = list()
        for root, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(suffix):
                    files.append( {os.path.join(root, filename): {'parent_path': root}} )
        return files

    @staticmethod
    def _get_output_dirs(protofiles, output_path):
        for filename in protofiles:
            for key, value in filename.items():
                value['pythonpath'] = os.path.join(output_path, value['parent_path'].removeprefix(Converter.PROTO_PATH))
        return protofiles



Converter._compile_protos()
Converter._create_init_files()
Converter._create_setup_file()
