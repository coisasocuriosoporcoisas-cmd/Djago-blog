# Django Blog

Blog criado com Django. O app `Blog_1` contém posts, comentários moderados e as
respectivas páginas e rotas.

## Comentários

- `Blog_1/models.py`: define `Comment`, ligado ao post, com autor, e-mail,
  conteúdo, datas e o indicador `active` para moderação.
- `Blog_1/forms.py`: valida os dados recebidos usando um `ModelForm`.
- `Blog_1/admin.py`: permite pesquisar e filtrar comentários, inclusive para
  desativá-los sem removê-los.
- `Blog_1/views.py`: mostra somente comentários ativos e processa novos
  comentários para posts publicados, apenas por requisições POST.
- `Blog_1/url.py`: registra a rota `blog:post_comment` usada pelo formulário.
- `Blog_1/templates/blog/post/detail.html`: apresenta a contagem, os comentários
  ativos e o formulário na página do post.
- `Blog_1/templates/blog/post/includes/comment_form.html`: formulário com CSRF e
  grupos de campos do Django para nome, e-mail e conteúdo.
- `Blog_1/templates/blog/post/comment.html`: confirma o envio válido ou apresenta
  novamente os erros de validação.
- `Blog_1/static/css/blog.css`: posiciona nome e e-mail lado a lado.
- `Blog_1/tests.py`: cobre envio válido, validação, bloqueio de GET e moderação.
- `Blog_1/migrations/`: registra a tabela do modelo `Comment` no banco de dados.

## Tags e posts relacionados

- A lista de posts pode ser filtrada por tag e exibe links para as páginas de
  detalhe usando `get_absolute_url`.
- A página de detalhe mostra posts relacionados por tags em comum,
  independentemente de o post ter comentários.
- `Blog_1/templatetags/blog_tags.py` fornece o filtro Markdown e os tags para os
  posts mais recentes, os mais comentados e a contagem de posts.

## Executar

No PowerShell, a partir da pasta `meuBlog`:

```powershell
..\my_venv\Scripts\python.exe manage.py migrate
..\my_venv\Scripts\python.exe manage.py runserver
```

A raiz `/` redireciona para a lista do blog em `/blog/`. Execute `migrate` após
adicionar novas migrações para criar ou atualizar as tabelas do banco de dados.

Para executar os testes:

```powershell
..\my_venv\Scripts\python.exe manage.py test Blog_1
```
