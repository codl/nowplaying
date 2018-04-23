import svelte from 'rollup-plugin-svelte';

export default {
    input: 'src/main.js',
    output: {
        format: 'iife',
        file: 'static/main.js',
    },
    plugins: [
        svelte({
            //include: 'components/**/*.html',
        }),
    ]
}
