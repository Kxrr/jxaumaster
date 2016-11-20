var webpack = require('webpack');

module.exports = {
    entry: {
        index: "./main.jsx"
    },
    output: {
        path: "./build",
        filename: "bundle.js"
    },
    module: {
        loaders: [
            {test: /\.js[x]?$/, exclude: /node_modules/, loader: 'babel-loader'}
        ]

    },
    resolve: {
        extensions: ["", ".js", ".jsx", ".es6"]
    }
};
