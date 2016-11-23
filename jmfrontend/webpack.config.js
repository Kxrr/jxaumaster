var webpack = require('webpack');
var path = require('path');


module.exports = {
    devServer: {
       historyApiFallback: true,
       hot: true,
       inline: true,
       progress: true,
       contentBase: './app',
       port: 8080
    },
    entry: [
      'webpack/hot/dev-server',
      'webpack-dev-server/client?http://localhost:8080',
      path.resolve(__dirname, 'app/main.jsx')
    ],
    output: {
      path: __dirname + '/build',
      publicPath: '/',
      filename: './bundle.js'
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
