from setuptools import find_packages,setup
from typing import List
def get_requirements(file_path:str)->list[str]:
    '''
        this function will returns list of  requirements
    '''
    hype_e_dot="-e ."

    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[ req.replace("/n"," ") for req in  requirements]
        if hype_e_dot in requirements:
            requirements.remove(hype_e_dot)

    return requirements


setup(
    name="krishna",
    version='0.1',
    author="krishna",
    author_email="ratnalasaikrishnasaikrishna@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')


)