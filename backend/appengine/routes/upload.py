# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api.app_identity.app_identity import get_default_gcs_bucket_name
from google.appengine.ext import blobstore
from blob_app import blob_facade
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


@no_csrf
def download(_handler, id, filename):
    comando = blob_facade.get_blob_file_cmd(id)
    arquivo = comando()
    _handler.send_blob(arquivo.blob_key)


@no_csrf
def delete(chave):
    cmd = blob_facade.delete_blob_file_cmd(chave)
    cmd.execute()
    return RedirectResponse(index)


@no_csrf
def index(_logged_user):
    comando = blob_facade.list_blob_files_cmd(_logged_user)
    arquivos = comando()
    download_path = to_path(download)
    delete_path = to_path(delete)

    for arq in arquivos:
        arq.download_path = to_path(download_path, arq.key.id(), arq.filename)
        arq.delete_path = to_path(delete_path, arq.key.id())

    ctx = {'arquivos': arquivos}
    return TemplateResponse(ctx, 'updown_home.html')


@no_csrf
def upload(_handler, _logged_user, files):
    blob_infos = _handler.get_uploads('files')
    blob_facade.save_blob_files_cmd(blob_infos, _logged_user).execute()
    return RedirectResponse(index)


@no_csrf
def form():
    upload_path = to_path(upload)
    bucket = get_default_gcs_bucket_name()
    url = blobstore.create_upload_url(upload_path, gs_bucket_name=bucket)
    ctx = {'salvar_path': url}
    return TemplateResponse(ctx, 'upload_form.html')