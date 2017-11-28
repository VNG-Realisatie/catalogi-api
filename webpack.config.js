var webpack = require('webpack');
var paths = require('./build/paths');


/**
 * Webpack configuration
 * Run using "webpack" or "gulp js"
 */
module.exports = {
    // Path to the js entry point (source)
    entry: [__dirname + '/' + paths.jsEntry],

    // Path to the (transpiled) js
    output: {
        path: __dirname + '/' + paths.jsDir, // directory
        filename: paths.package.name + '.js', // file
    },

    // Add babel (see .babelrc for settings)
    module: {
        loaders: [{
            exclude: /node_modules/,
            loader: 'babel-loader',
            test: /.js?$/,
        }]
    },

    devtool: 'sourcemap',

    // Minify output
    plugins: [
        new webpack.optimize.UglifyJsPlugin({minimize: true})
    ]
};
