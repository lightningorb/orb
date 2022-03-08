.PHONY: build
.PHONY: docs

docs:
	/usr/local/bin/pandoc --from=markdown --to=rst --output=README README.md
	./rln generate-docs
	cd docs && make html
	rm -rf ../getlightning.github.io/docs
	cp -r docs/build/html ../getlightning.github.io/docs
	touch ../getlightning.github.io/docs/.nojekyll

build: clean docs
	python3 setup.py build sdist
	pip3 install .

.PHONY: dist

dist: readme
	twine upload dist/*

sync:
	rsync -azv -e 'ssh -i ~/.rln/lnd4/lnd4_key.pem' . ubuntu@3.0.57.49:/home/ubuntu/src/rln --exclude data --exclude docs