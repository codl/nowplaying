import svelte from 'rollup-plugin-svelte';
import { nodeResolve } from '@rollup/plugin-node-resolve';
import glob from 'glob';

export default {
    input: glob.sync('src/elements/*.js'),
    output: {
        format: 'iife',
        dir: 'static',
    },
    plugins: [
        nodeResolve({
            browser: true,
        }),
        svelte({
            //include: 'components/**/*.html',
        }),
    ]
}
