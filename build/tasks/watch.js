'use strict';
var gulp = require('gulp');
var paths = require('../paths');


/**
 * Watch task
 * Run using "gulp watch"
 * Runs "watch-js" and "watch-sass" tasks
 */
gulp.task('watch', ['js', 'sass', 'watch-js', 'watch-sass']);


/**
 * Watch-js task
 * Run using "gulp watch-js"
 * Runs "js" and "lint" tasks instantly and when any file in paths.jsSrc changes
 */
gulp.task('watch-js', ['js', 'lint'], function() {
    gulp.watch([paths.jsSrc, paths.jsSpec], ['js', 'lint']);
});


/**
 * Watch-sass task
 * Run using "gulp watch-sass"
 * Runs "sass" task instantly and when any file in paths.sassSrc changes
 */
gulp.task('watch-sass', ['sass'], function() {
    gulp.watch(paths.sassSrc, ['sass']);
});
