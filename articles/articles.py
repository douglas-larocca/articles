import os
import re
import requests
from urllib.parse import urljoin
from rdflib import Graph, RDF, URIRef, Literal, plugin
from rdflib.store import Store
from rdflib.parser import StringInputSource
from os.path import join as pjoin
from .protect import cstring

test_dois = ('10.1016/0097-3165(79)90023-2', 
             '10.1002/rsa.3240010202', 
             '10.1016/0095-8956(71)90029-3', 
             '10.2307/2370675')

generic_headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}


class IPythonPDF(object):
    def _repr_html_(self):
        tpl = '<iframe src={0} width={1[0]} height={1[1]}></iframe>'
        return tpl.format(self.filename, (1050, 1000))

    def _repr_latex_(self):
        tpl = r'\includegraphics[width=1.0\textwidth]{{{0}}}'
        return tpl.format(self.filename)


class BibItem(IPythonPDF):
    def __init__(self, *args, **kwargs):
        identifier = URIRef('doi')
        self.store = plugin.get('SQLAlchemy', Store)(identifier=identifier)
        self.graph = Graph(self.store, identifier=identifier)
        self.graph.open(cstring, create=True)


class DOIMetadata(BibItem):
    def __init__(self, doi, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.doi = Literal(doi)
        url = URIRef(pjoin('http://dx.doi.org', doi))
        r = requests.get(url, headers={'Accept': 'application/rdf+xml'})
        r.raise_for_status()
        self.graph.parse(StringInputSource(r.content), formal='xml')


class DOI(DOIMetadata):
    """find and download a pdf for the doi given
    >>> DOI('10.1016/0166-218X(92)00170-Q')
    """
    headers = generic_headers
    headers['Host'] = 'gen.lib.rus.ec'
    headers['Referer'] = 'http://gen.lib.rus.ec/scimag/'
    
    url = 'http://gen.lib.rus.ec/scimag/?s={}&journalid=&v=&i=&p=&redirect=1'
    
    def __init__(self, doi, *args, **kwargs):
        super().__init__(doi, *args, **kwargs)
        self.url = URIRef(self.url.format(self.doi))
        
        r = requests.get(self.url, headers=self.headers)
        r.raise_for_status()
        
        self.links = re.compile(r'a href="([^"]+pdf)"').findall(r.text)
        link, *links = self.links
        r = requests.get(link, stream=True)
        
        self.filename = Literal('.'.join((doi.replace('/','_'), 'pdf')))
        with open(self.filename, 'wb') as fd:
            for chunk in r.iter_content(1024*10):
                fd.write(chunk)
        
        self.path = URIRef(urljoin('file:', pjoin(os.getcwd(), self.filename)))
        self.graph.add((self.path, URIRef('http://purl.org/dc/terms/identifier'), self.doi))
        self.graph.commit()