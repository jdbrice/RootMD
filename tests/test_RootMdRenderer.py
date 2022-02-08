
import mistletoe as md
from rootmd.RootMdRenderer import RootMdRenderer
from rootmd import log



def test_RootMdRenderer() :
    INPUT = "tests/example.in.md"
    OUTPUT = "tests/example.out.md"
    data =""
    with open( INPUT , 'r') as fin:
        rd = RootMdRenderer()
        rd.set( asset_dir="tests/" )
        with rd as renderer:
            data = renderer.render(md.Document(fin))
    log.info( "Writing output to %s" % OUTPUT )
    with open( OUTPUT , "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(data)
