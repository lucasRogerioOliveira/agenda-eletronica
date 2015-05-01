# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaeforms.ndb.form import ModelForm
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
    contatos = [form.fill_with_model(c) for c in contatos]
    for contato in contatos:
        contato['edit_path'] = '%s/%s' % (editar_form_path, contato['id'])
        contato['remove_path'] = '#'
    contexto = {
        'contatos': contatos,
        'new_path': router.to_path(new)
    }

    return TemplateResponse(contexto)

@no_csrf
def new():
    contexto = {
        'salvar_path': router.to_path(save),
        'erros': []
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

class ContatoFormTable(ModelForm):
    _model_class = Contato
    _include = [Contato.nome, Contato.email, Contato.celular, Contato.bairro, Contato.logradouro, Contato.numero, Contato.cep]


class ContatoForm(ModelForm):
    _model_class = Contato
    _include = [Contato.nome]


def save(**propriedades):
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