from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb


__author__ = 'Alucard'


class Contato(ndb.Model):
    nome = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=False)
    celular = ndb.StringProperty(required=False)
    bairro = ndb.StringProperty(required=False)
    logradouro = ndb.StringProperty(required=False)
    numero = ndb.StringProperty(required=False)
    cep = ndb.StringProperty(required=False)


    @classmethod
    def query_ordenada_por_nome(cls):
        pass