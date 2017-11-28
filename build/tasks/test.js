'use strict';
var gulp = require('gulp');
var Server = require('karma').Server;


/**
 * Test task
 * Run using "gulp test"
 * Runs karma one
 */
gulp.task('test', function (done) {
    new Server({
        configFile: __dirname + '/../../karma.conf.js',
        singleRun: true
    }, done).start();
});


/**
 * Test driven development (tdd) task
 * Run using "gulp tdd"
 * Watch for file changes and re-run tests on each change
 */
gulp.task('tdd', function (done) {
    new Server({
        configFile: __dirname + '/../../karma.conf.js',
    }, done).start();
});
