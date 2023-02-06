import adapter from '@sveltejs/adapter-static';

export default {
	kit: {
		prerender: {
			origin: 'http://sveltekit-prerender',
			concurrency: 3,
			handleHttpError: ({ path, referrer, message }) => {
				console.log(path);
				if (path.indexOf('/docs') !== -1) {
					return;
				}
				throw new Error(message);
			}
		},
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: null,
			precompress: false,
			strict: true
		})
	}
};
