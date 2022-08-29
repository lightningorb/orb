build_image:
	docker build -t svelte .

init:
	docker run -it -v `pwd`:/src/ --rm svelte npx degit sveltejs/template orb_frontend
	docker run -it -v `pwd`:/src/ --rm --workdir /src/orb_frontend svelte npm install
# 	docker run -it -v `pwd`:/src/ --rm --workdir /src/orb_frontend svelte npm install sveltestrap

run:
	docker run -it -v `pwd`:/src/ -p 35729:35729 -p 8686:8080 --rm --workdir /src/orb_frontend svelte env HOST=0.0.0.0 npm run dev --host

build_site:
	docker run -it -v `pwd`:/src/ --rm --workdir /src/orb_frontend svelte npm run build

