# https://kivy.org/doc/stable/guide/packaging-osx.html
# brew install python
# brew reinstall --build-bottle sdl2 sdl2_image sdl2_ttf sdl2_mixer

clean_docs:
	rm -rf docsbuild

docs:
	sphinx-apidoc --ext-autodoc --module-first --follow-links --ext-coverage --separate --force -o source/gen/ orb 
	sphinx-build -b html source docsbuild
	cd docsbuild && python3 -m http.server

.PHONY: build

build:
	pyinstaller -y --clean --windowed orb.spec
	cd dist && hdiutil create ./orb.dmg -srcfolder orb.app -ov
	cp orb.ini dist/orb/

spec:
	pyinstaller -y --clean --windowed --name orb --exclude-module _tkinter --exclude-module Tkinter --exclude-module enchant   --exclude-module twisted main.py

run:
	cd dist/orb && ./orb

run_app:
	cd dist/orb/ && ./orb && cd -

clean: clean_docs
	rm -rf build dist source/gen

doctest:
	python3 -m orb.math.Vector -v
	python3 -m orb.math.lerp -v
	python3 -m orb.misc.mempool -v
	python3 -m orb.misc.forex
	python3 -m orb.misc.auto_obj -v

prep_for_ios:
	python3 orb/scripts/prep_user_scripts.py

build_ios: prep_for_ios
	rm -rf ../lnorb-ios
	mkdir -p ../tmp
	cp -r main.py orb user data_manager.py fees.yaml autobalance.yaml orb.png user_scripts.json ../tmp/
	cd .. && toolchain create lnorb ./tmp

update_ios: prep_for_ios
	python3 orb/scripts/prep_user_scripts.py
	mv orb.ini /tmp/
	cd ../ && toolchain update lnorb-ios/
	mv /tmp/orb.ini .
