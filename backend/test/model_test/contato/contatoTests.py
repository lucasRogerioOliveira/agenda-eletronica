from base import GAETestCase
from gaepermission.model import MainUser
from mock import Mock, MagicMock, patch
from mommygae import mommy
from routes.contatos.home import dummy, save


class ContatoTests(GAETestCase):
    @patch('routes.contatos.home.json')
    def test_success(self,json_mock):
        dados = {'nome':'Goto'}
        user = mommy.save_one(MainUser)
        save(user, Mock(), **dados)
        json_mock.dumps.assert_called_once_with({'nome': u'Goto', 'bairro': None, 'logradouro': None, 'numero': None, u'id': 2L, 'celular': None, 'cep': None, 'email': None})

    @patch('routes.contatos.home.json')
    def test_fail(self, json_mock):
        user = mommy.save_one(MainUser)
        save(user, Mock(), **{})
        json_mock.dumps.assert_called_once_with({u'salvar_path': '/contatos/home/save', u'contato': {}, u'erros': {'nome': u'Required field'}});