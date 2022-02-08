
import mistletoe as md
from rootmd.RootHtmlRenderer import RootHtmlRenderer
from rootmd.RootMdRenderer import RootMdRenderer
import logging

from rich.console import Console
from rich.markdown import Markdown

from rich.logging import RichHandler
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


log.setLevel( logging.DEBUG )

def test_RootHtmlRenderer() :
    log.debug( "test_RootHtmlRenderer" )
    INPUT = "tests/example.in.md"
    OUTPUT = "tests/example.out.html"
    data =""
    with open( INPUT , 'r') as fin:
        rd = RootHtmlRenderer()
        rd.set( asset_dir="tests/" )
        with rd as renderer:
            data = renderer.render(md.Document(fin))
    log.info( "Writing output to %s" % OUTPUT )
    with open( OUTPUT , "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(data)




def test_Terminal() :
    log.debug( "test_Terminal" ) 
    INPUT = "tests/example.in.md"
    data =""
    with open( INPUT , 'r') as fin:
        rd = RootMdRenderer()
        rd.set( asset_dir="tests/" )
        with rd as renderer:
            data = renderer.render(md.Document(fin))
    
    console = Console()
    console.print( Markdown(data) )
    # console.update_screen( Markdown(data) )
    