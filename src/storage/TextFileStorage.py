import logging
import os
import re
import collections

from src.domain.Text import Text
from src.storage.AbstractStorage import AbstractStorage


class TextFileStorage(AbstractStorage):

    def __init__(self, base_dir):
        self.base_dir = base_dir

    def store(self, source, texts):
        if isinstance(type(texts), collections.Iterable):
            texts = [texts]

        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        file_name = os.path.join(self.base_dir, '{}.txt'.format(source))
        
        with open(file_name, 'w', encoding='utf8') as file:
            logging.info("Writing to file {}".format(file))
            
            for text in texts:
                text = self.__serialize(text)
                logging.debug("Writing: {}".format(text))
                file.write(text + '\n')

        logging.info('Successfully saved {} posts to: {}/{}'.format(len(texts), 
                                                        self.base_dir, source))

    def get(self, sources):
        texts = []

        if isinstance(type(sources), collections.Iterable):
            sources = [sources]

        for source in sources:
            file_name = os.path.join(self.base_dir, '{}.txt'.format(source))
            logging.info("Reading file: {}".format(file_name))

            fragments = [self.__deserialize(f) for f in open(
                file_name, encoding='utf8').read().split('\n')]
            fragments = [f for f in fragments if f != '']
            
            texts += fragments

        return texts

    def __deserialize(self, text):
        m = re.search(
            '\[S_\](.*)\[_S\]\[U_\](.*)\[_U\]\[P_\](.*)\[_P\]', text.strip(), re.U)
        if m:
            return Text(m.group(1), m.group(3), m.group(2))
        else:
            return ''

    def __serialize(self, text):
        return "[S_]%s[_S][U_]%s[_U][P_]%s[_P]" % (text.source, text.url, text.payload)
