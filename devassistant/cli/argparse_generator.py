import argparse

from devassistant import settings

class ArgparseGenerator(object):
    subassistants_string = 'subassistants'
    description = '''This assistant has following subassistants that can help you with
                     setting up your project.'''

    @classmethod
    def generate_argument_parser(cls, chain):
        cur_as, cur_subas = chain
        parser = argparse.ArgumentParser()

        # add any arguments of the top assistant
        for arg in cur_as.args:
            arg.add_argument_to(parser)

        # then add the subassistants as arguments
        subparsers = parser.add_subparsers(dest=settings.SUBASSISTANT_N_STRING.format('0'),
                                           title=cls.subassistants_string,
                                           description=cls.description)
        for subas in cur_subas:
            cls.add_subparsers_to(subas, subparsers, level=1)

        return parser

    @classmethod
    def add_subparsers_to(cls, assistant_tuple, parser, level):
        p = parser.add_parser(assistant_tuple[0].name)
        for arg in assistant_tuple[0].args:
            arg.add_argument_to(p)

        if len(assistant_tuple[1]) > 0:
            subparsers = p.add_subparsers(dest=settings.SUBASSISTANT_N_STRING.format(level),
                                          title=cls.subassistants_string,
                                          description=cls.description)
            for subas_tuple in assistant_tuple[1]:
                cls.add_subparsers_to(subas_tuple, subparsers, level + 1)
