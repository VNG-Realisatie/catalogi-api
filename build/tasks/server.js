'use strict';
var gulp = require('gulp');
var webpack = require('webpack');
var WebpackDevServer = require("webpack-dev-server");
var paths = require('../paths');
var webpackConfig = require('../../webpack.config.js');


/**
 * Server task
 * Run using "gulp server"
 * Starts a webpack dev server on port 8080
 * Proxies request to Django (assumed to be listening on port 8000)
 */
gulp.task('server', function() {
    var compiler, server;

    webpackConfig.entry.unshift(
        "webpack-dev-server/client?http://localhost:8080",
        "webpack/hot/only-dev-server"
    );

    webpackConfig.plugins = [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NamedModulesPlugin()
    ];

    compiler = webpack(webpackConfig);
    server = new WebpackDevServer(compiler, {
        hot: true,
        publicPath: "/static/js/",

        proxy: {
            '/': {
                secure: false,
                target: 'http://localhost:8000/',

                bypass: function(request, response, proxyOptions) {
                    if (request.path.startsWith('/static/js/')) {
                        return request.path;
                    } else if (request.path.indexOf('hot-update') > 0) {
                        return '/static/js' + request.path;  // Ugly hack, but publicPath is not properly supported :/
                    }
                    return false;
                }
            }
        }
    });

    server.listen(8080);
});
