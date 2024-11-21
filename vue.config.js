const { defineConfig } = require('@vue/cli-service');
module.exports = defineConfig({
    transpileDependencies: true,
    outputDir: 'dist',
    publicPath: '/',
    pages: {
        index: {
            entry: 'english/src/main.js',
            template: 'english/public/index.html',
            filename: 'index.html',
        },
    },
});