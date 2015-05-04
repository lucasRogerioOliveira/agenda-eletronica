# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaebusiness.business import Command, CommandParallel, CommandExecutionException, CommandSequential
from gaebusiness.gaeutil import SaveCommand
from gaecookie.decorator import no_csrf
from gaeforms.ndb.form import ModelForm
from gaegraph.model import Arc, to_node_key
from gaepermission.decorator import login_not_required
from model.contato.contato import Contato
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
@no_csrf
def index():
    query = Contato.query().order(-Contato.nome)
    contatos = query.fetch()
    form = ContatoFormTable()
    editar_form_path = router.to_path(editar_form)
    delete_path = router.to_path(delete)
    contatos = [form.fill_with_model(c) for c in contatos]
    for contato in contatos:
        contato['edit_path'] = '%s/%s' % (editar_form_path, contato['id'])
        contato['delete_path'] = '%s/%s' % (delete_path, contato['id'])
    contexto = {
        'contatos': contatos,
        'new_path': router.to_path(new)
    }
    return TemplateResponse(contexto)


def delete(contato_id):
    apagar_cmd = ApagarContato(contato_id)
    apagar_contatos_user_cmd = ApagarContatosUser(contato_id)
    comandos_paralelos = CommandParallel(apagar_cmd, apagar_contatos_user_cmd)
    comandos_paralelos()
    return RedirectResponse(router.to_path(index))


def new():
    contato = ContatoForm
    contexto = {
        'salvar_path': router.to_path(save),
        'erros': [],
        'contato': contato
    }
    return TemplateResponse(contexto, 'contatos/new.html')


@no_csrf
def editar_form(contato_id):
    contato_id = int(contato_id)
    contato = Contato.get_by_id(contato_id)
    contatoForm = ContatoForm()
    contatoForm.fill_with_model(contato)
    contexto = {
        'salvar_path': router.to_path(save),
        'erros': [],
        'contato': contatoForm
    }
    return TemplateResponse(contexto, 'contatos/new.html')


def edit(**propriedades):
    contato_form = ContatoForm(**propriedades)
    erros = contato_form.validate()
    if erros:
        contexto = {'salvar_path': router.to_path(save),
                     'erros': erros
                     }
        #'contato': contato_form
        return TemplateResponse(contexto, '/contatos/new.html')
    else:
        contato = contato_form.fill_model()
        contato.put()
        return RedirectResponse(router.to_path(index))


class ContatosUser(Arc):
    origin = ndb.KeyProperty(required=True)
    destination = ndb.KeyProperty(Contato, required=True)


class ContatoFormTable(ModelForm):
    _model_class = Contato
    _include = [Contato.nome, Contato.email, Contato.celular, Contato.bairro, Contato.logradouro, Contato.numero, Contato.cep]


class ContatoForm(ModelForm):
    _model_class = Contato
    _include = [Contato.nome]


def save(_logged_user,  **propriedades):
    salvar_contato_com_usuario_cmd = SalvarContatoComUsuario(_logged_user, **propriedades)
    try:
        salvar_contato_com_usuario_cmd()
        return RedirectResponse(router.to_path(index))
    except CommandExecutionException:
        contexto = {'salvar_path': router.to_path(save),
                     'erros': salvar_contato_com_usuario_cmd.errors,
                     'contato': propriedades}
        return TemplateResponse(contexto, '/contatos/new.html')


class SalvarContatoComUsuario(CommandSequential):
    def __init__(self, user, **propriedades_do_contato):
        salvar_contato_cmd = SalvarContato(**propriedades_do_contato)
        salvar_usuario_do_contato_cmd = SalvarUsuarioDoContato(user)
        super(SalvarContatoComUsuario, self).__init__(salvar_contato_cmd, salvar_usuario_do_contato_cmd)


class SalvarContato(SaveCommand):
    _model_form_class = ContatoForm


class SalvarUsuarioDoContato(Command):
    def __init__(self, user, contato=None):
        super(SalvarUsuarioDoContato, self).__init__()
        self.user = to_node_key(user)
        self.contato = contato and to_node_key(contato)

    def do_business(self):
        self.result = ContatosUser(origin=self.user, destination=self.contato)
        self._to_commit = self.result

    def handle_previous(self, command):
        self.contato = command.result

class ApagarContato(Command):
    def __init__(self, contato_id):
        super(ApagarContato, self).__init__()
        self.contato_key  = ndb.Key(Contato, int(contato_id))
        self.futuro = None

    def set_up(self):
        self.futuro = self.contato_key.delete_async()

    def do_business(self):
        self.futuro.get_result()


class ApagarContatosUser(Command):
    def __init__(self, contato_id):
        super(ApagarContatosUser, self).__init__()
        chave_do_contato = ndb.Key(Contato, int(contato_id))
        self.query = ContatosUser.find_origins(chave_do_contato)
        self.futuro = None

    def set_up(self):
        self.futuro = self.query.fetch_async(keys_only=True)

    def do_business(self):
        chave_dos_arcos = self.futuro.get_result()
        ndb.delete_multi(chave_dos_arcos)