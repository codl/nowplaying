import svelte from 'rollup-plugin-svelte';
import glob from 'glob';

export default {
    input: glob.sync('src/elements/*.js'),
    output: {
        format: 'iife',
        dir: 'static',
    },
    plugins: [
        svelte({
            //include: 'components/**/*.html',
        }),
    ]
}
