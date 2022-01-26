

build:
	poetry build

publish:
	poetry publish


test: testMd testHtml
	echo "DONE"

testTerminal:
	python -m pytest tests/test_Terminal.py

testMd:
	python -m pytest tests/test_RootMdRenderer.py
testHtml:
	python -m pytest --log-cli-level=0 tests/test_RootHtmlRenderer.py


tutorials:
	# python -m rootmd tests/root/fillrandom.md --asset-dir tests/root
	# python -m rootmd tests/root/firstcontour.md --asset-dir tests/root
	# python -m rootmd tests/root/hlabels1.md --asset-dir tests/root
	# python -m rootmd tests/root/hstack.md --asset-dir tests/root
	# python -m rootmd tests/root/hsum.md --asset-dir tests/root
	# python -m rootmd tests/root/movepalette.md --asset-dir tests/root
	# python -m rootmd tests/root/ratioplot.md --asset-dir tests/root
	# python -m rootmd tests/root/testsmooth.md --asset-dir tests/root
	# python -m rootmd tests/root/confidenceintervals.md --asset-dir tests/root
	# python -m rootmd tests/root/fit2dhist.md --asset-dir tests/root
	# python -m rootmd tests/root/fittingdemo.md --asset-dir tests/root
	# python -m rootmd tests/root/building.md --asset-dir tests/root/
	python -m rootmd tests/root/binomial.md --asset-dir tests/root/
