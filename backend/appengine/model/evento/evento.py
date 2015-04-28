__author__ = 'Alucard'

from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb


class Evento(ndb.Model):
    nome = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    celular = ndb.StringProperty(required=True)
    bairro = ndb.StringProperty(required=True)
    logradouro = ndb.StringProperty(required=True)
    numero = ndb.StringProperty(required=True)
    cep = ndb.StringProperty(required=True)

    @classmethod
    def query_ordenada_por_nome(cls):
        pass