# Configuration file for jupyter-notebook.

c.JupyterApp.answer_yes = True
c.NotebookApp.allow_password_change = False
c.NotebookApp.allow_remote_access = True
c.NotebookApp.answer_yes = True
c.NotebookApp.autoreload = True
c.NotebookApp.base_url = '/'
c.NotebookApp.default_url = '/tree'
c.NotebookApp.ip = 'winner'
c.NotebookApp.nbserver_extensions = {}
c.NotebookApp.notebook_dir = 'F:\\Documents\\JupyterRoot'
c.NotebookApp.open_browser = True
c.NotebookApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=8$mWVgG+OTUw2T2afUmHQY4w$1xCmsxdz+m4Z6CJjRiuf0g'
c.NotebookApp.password_required = True
c.NotebookApp.port = 80
c.NotebookApp.port_retries = 1
c.NotebookApp.quit_button = False
c.NotebookApp.rate_limit_window = 3
c.NotebookApp.token = ''
c.ContentsManager.root_dir = '/'
c.FileContentsManager.delete_to_trash = False

import os

os.environ['TI_GUI_BACKEND'] = 'ipython'