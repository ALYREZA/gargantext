from gargantext.util.http       import *
from gargantext.util.db         import *
from gargantext.util.db_cache   import cache
from gargantext.models          import *
from gargantext.constants       import *
from gargantext.settings        import *
from datetime                   import datetime
from .main                      import get_user_params
from gargantext.constants       import USER_LANG

def _get_user_project_corpus(request, project_id, corpus_id):
    """Helper method to get a corpus, knowing the project's and corpus' ID.
    Raises HTTP errors when parameters (user, IDs...) are invalid.
    """
    user = cache.User[request.user.id]
    project = session.query(Node).filter(Node.id == project_id).first()
    corpus = session.query(Node).filter(Node.id == corpus_id).filter(Node.parent_id == project_id).first()
    if corpus is None:
        raise Http404()
    if not user.owns(corpus):
        print("CORPORA: invalid user %i (User doesn't own this corpus)" % user.id)
        return (False, user, project, corpus)
    return (True, user, project, corpus)


@requires_auth
def docs_by_titles(request, project_id, corpus_id):
    authorized, user, project, corpus = _get_user_project_corpus(request, project_id, corpus_id)
    if not authorized:
        return HttpResponseForbidden()
    source_type = corpus.resources()[0]['type']
    # response!
    return render(
        template_name = 'pages/corpora/titles.html',
        request = request,
        context = {
            'debug': DEBUG,
            'date': datetime.now(),
            'project': project,
            'corpus': corpus,
            'resourcename' : get_resource(source_type)['name'],
            'view': 'titles',
            'user': request.user,
            'user_parameters': get_user_params(user),
            'languages': USER_LANG
        },
    )

@requires_auth
def docs_by_sources(request, project_id, corpus_id):
    '''
    Browse source titles for a given corpus
    NB: javascript in page will GET counts from our api: facets?subfield=source
    # TODO refactor Sources_dyna_charts_and_table.js
    '''
    # we pass our corpus to mark it's a corpora page
    corpus = cache.Node[corpus_id]

    # and the project just for project.id in corpusBannerTop
    project = cache.Node[project_id]
    user = cache.User[request.user.id]
    source_type = corpus.resources()[0]['type']
    # rendered page : sources.html
    
    return render(
        template_name = 'pages/corpora/sources.html',
        request = request,
        context = {
            'debug': settings.DEBUG,
            'date': datetime.now(),
            'project': project,
            'corpus' : corpus,
            'resourcename' : get_resource(source_type)['name'],
            'user': request.user,
            'user_parameters': get_user_params(user),
            'view': 'sources',
            'languages': USER_LANG
        },
    )

@requires_auth
def docs_by_authors(request, project_id, corpus_id):
    '''
    Browse authors for a given corpus
    NB: javascript in page will GET counts from our api: facets?subfield=author
    # TODO refactor Author && Sources_dyna_charts_and_table.js
    '''
    # we pass our corpus to mark it's a corpora page
    corpus = cache.Node[corpus_id]

    # and the project just for project.id in corpusBannerTop
    project = cache.Node[project_id]
    user = cache.User[request.user.id]
    source_type = corpus.resources()[0]['type']
    # rendered page : sources.html
    node_user = get_node_user(user)
    return render(
        template_name = 'pages/corpora/authors.html',
        request = request,
        context = {
            'debug': settings.DEBUG,
            'date': datetime.now(),
            'project': project,
            'corpus' : corpus,
            'resourcename' : get_resource(source_type)['name'],
            'view': 'authors',
            'user': request.user,
            'user_parameters': node_user.hyperdata,
            'languages': USER_LANG
        },
    )


@requires_auth
def analytics(request, project_id, corpus_id):
    authorized, user, project, corpus = _get_user_project_corpus(request, project_id, corpus_id)
    if not authorized:
        return HttpResponseForbidden()

    source_type = corpus.resources()[0]['type']
    # response!
    return render(
        template_name = 'pages/analytics/histories.html',
        request = request,
        context = {
            'debug': DEBUG,
            'date': datetime.now(),
            'project': project,
            'corpus': corpus,
            'resourcename' : get_resource(source_type)['name'],
            'view': 'analytics',
            'user': request.user,
            'user_parameters': get_user_params(user),
            'languages': USER_LANG
        },
    )
